from dotenv import load_dotenv
load_dotenv()
import os
import uuid
import time
import logging
from ldclient.config import Config
import ldclient
from ldobserve import ObservabilityPlugin, ObservabilityConfig, observe
from ldclient import Context
from ldai.client import LDAIClient, AIConfig, ModelConfig, LDMessage

# LAUNCHDARKLY + OBSERVABILITY 
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")
if not sdk_key:
    raise RuntimeError("Missing LAUNCHDARKLY_SDK_KEY")

ldclient.set_config(Config(
    sdk_key=sdk_key,
    plugins=[ObservabilityPlugin(ObservabilityConfig(
        service_name="llm_observability_v1",
        service_version=os.getenv("GIT_SHA", "dev"),
        environment=os.getenv("ENV", "development")
    ))]
))

print("Waiting for LaunchDarkly to fully initialize (max 30s)...")
start_time = time.time()
while not ldclient.get().is_initialized():
    if time.time() - start_time > 30:
        print("Timeout reached — continuing anyway (traces will still work)")
        break
    time.sleep(0.5)

print("LaunchDarkly ready — Observability active")
# INSTRUMENT OPENAI
def ensure_openai_instrumented():
    from opentelemetry.instrumentation.openai import OpenAIInstrumentor
    OpenAIInstrumentor().instrument(force=True)
    print("OpenAI auto-instrumented — LLM spans will appear in LaunchDarkly")

ensure_openai_instrumented()

# Openai CLIENTS 
import openai
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ld_ai_client = LDAIClient(ldclient.get())

# GENERATE FUNCTION 
def generate(**kwargs) -> str:
    print("generate() called with:", kwargs)

    # Top-level manual span — will appear in LaunchDarkly
    with observe.start_span("generate_summary"):
        observe.record_log("Starting summary generation", logging.INFO)

        user_id = str(uuid.uuid4())
        context = (
            Context.builder(user_id)
            .kind("user")
            .set("firstName", "Hafsa")
            .set("lastName", "Akram")
            .build()
        )

        # CRITICAL: Evaluate flag FIRST so traces get tagged with flag metadata
        # This is required for traces to appear in LaunchDarkly dashboard
        flag_enabled = ldclient.get().variation("llm_observability_v1", context, False)
        if not flag_enabled:
            return "LLM testing is turned off."

        try:
            # Span for fetching AI Config
            with observe.start_span("get_ai_config"):
                fallback = AIConfig(
                    enabled=True,
                    model=ModelConfig(name="gpt-4o", parameters={"temperature": 0.8}),
                    messages=[
                        LDMessage(role="system",
                                  content="""
                                        You are an expert Text Summarizer. Summarize concisely:
                                        Text: {{TEXT}}``
                                        Structure:
                                        1. Executive Summary (1-2 sentences)
                                        2. Key Points (bullets)
                                        3. Action Items

                                        Provide ONLY the summary """.strip())])
                config_value, tracker = ld_ai_client.config("llm_observability_v1",context,fallback,kwargs)
            # Build messages from AI Config (or fallback)
            messages = config_value.messages or []
            
            # # CRITICAL: Add user's actual text as a message
            # if not any(m.role == "user" for m in messages):
            #     user_text = kwargs.get("TEXT", "")
            #     if user_text:
            #         messages = list(messages) + [LDMessage(role="user", content=user_text)]
            
            model_name = config_value.model.name if config_value.model else "gpt-4"

            # Span for the actual OpenAI call — this creates the green LLM span!
            with observe.start_span("openai_completion"):
                completion = tracker.track_openai_metrics(
                    lambda: openai_client.chat.completions.create(
                        model=model_name,
                        messages=[msg.to_dict() for msg in messages],
                    )
                )

            response = completion.choices[0].message.content.strip()
            print("Summary generated successfully")
            return response

        except Exception as e:
            observe.record_log(f"Error in generate(): {e}", logging.ERROR)
            print("ERROR in generate():", e)
            import traceback
            traceback.print_exc()
            return f"Error: {e}"

        finally:
            # Ensures traces are sent immediately
            ldclient.get().flush()