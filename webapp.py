import streamlit as st
import time # For timing
# Attempt to import from fallacy_checker, ensure it doesn't break if fallacy_checker has issues on import for now
try:
    from fallacy_checker import call_qwen_api, parse_fallacy_response
except ImportError:
    st.error("Failed to import fallacy_checker.py. Make sure it's in the same directory.")
    # Define dummy functions if import fails, so UI can still be sketched
    def call_qwen_api(sentence, api_key, model_id): return "Error: Backend not loaded"
    def parse_fallacy_response(response_text): return ("PARSE_ERROR", response_text)

# Constants
API_KEY = "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"
MODEL_ID = "qwen/qwen3-32b"

# Page Configuration and Title
st.set_page_config(page_title="Live Fallacy Checker", layout="wide")
st.title("Live Fallacy Checker")
st.markdown("Enter a sentence below to check for common logical fallacies (Ad Hominem, Straw Man, Slippery Slope, False Dichotomy, Appeal to Emotion).")

# Input Area
user_sentence = st.text_area("Sentence to analyze:", height=100, key="user_sentence_input", help="Type or paste the sentence you want to check.")

# Analyze Button
analyze_button = st.button("Analyze Sentence", key="analyze_button", help="Click to submit the sentence for fallacy detection.")

# Results Display Area (Conditional on button press)
if analyze_button:
    if user_sentence.strip():
        st.subheader("Analysis Results")
        st.markdown("---") # Visual separator
        st.write(f"**Input Sentence:** {user_sentence}") # Show what was analyzed

        raw_api_response = "" # Initialize
        fallacy_type = None   # Initialize
        rationale_text = ""   # Initialize
        duration_ms = 0       # Initialize

        with st.spinner("Analyzing your sentence... please wait."):
            # Record start time
            start_time = time.perf_counter()

            # Call backend functions
            actual_sentence_to_analyze = user_sentence 
            raw_api_response = call_qwen_api(actual_sentence_to_analyze, API_KEY, MODEL_ID)
            # Only parse if the API call didn't return a direct error
            if not raw_api_response.startswith("Error:"):
                fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
            else: # API call itself failed, rationale_text might be empty or hold error info
                rationale_text = raw_api_response 

            # Record end time and calculate duration
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
        
        # Display results
        st.markdown("#### Analysis Result:") # General heading for the result type

        if raw_api_response.startswith("Error:"):
            st.error(f"{raw_api_response}") # Display direct API/network errors from call_qwen_api
        elif fallacy_type == "FORMAT_ERROR":
            st.error("Model Response Error: Could not properly parse the model's output.")
            st.caption(f"Raw model output received: {rationale_text}") # rationale_text holds the problematic response
        elif fallacy_type is None: # No fallacy detected
            st.success("No fallacy detected.")
        else: # Fallacy detected
            st.warning(f"Detected Fallacy: {fallacy_type}")

        # Display Rationale only if a valid fallacy was detected and rationale exists
        if not raw_api_response.startswith("Error:") and fallacy_type and fallacy_type != "FORMAT_ERROR" and rationale_text:
            st.markdown("#### Rationale:")
            st.write(rationale_text)
        
        # Display Processing Time (always, if analysis was attempted)
        st.markdown("#### Processing Time:")
        st.caption(f"{duration_ms:.2f} ms")
        
    else:
        st.warning("Please enter a sentence to analyze.")

# Optional: Add a small footer or instruction area
st.markdown("---")
st.caption("Powered by Qwen3 32B on Cerebras via OpenRouter. Hackathon Project.")
