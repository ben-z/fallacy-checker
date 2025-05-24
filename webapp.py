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

import re # Added for transcript parsing

# Constants
API_KEY = "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"
MODEL_ID = "qwen/qwen3-32b"

from typing import Tuple, List, Dict # For type hinting

def parse_timestamped_transcript(transcript_content: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Parses a timestamped transcript string into a list of segment dictionaries
    and a list of parsing error messages.

    Args:
        transcript_content: The entire content of the transcript file as a string.

    Returns:
        A tuple containing:
            - parsed_segments: A list of dictionaries, where each dictionary
                               represents a transcript segment.
            - parsing_errors: A list of strings, where each string is an
                              error message for a line that couldn't be parsed.
    """
    parsed_segments: List[Dict[str, str]] = []
    parsing_errors: List[str] = []
    # Regex to capture: ID, Start Time, End Time, Speaker, Text
    # Example line: "503 00:43:29,413 --> 00:43:39,295 [SPEAKER_01]: Some text here"
    segment_pattern = re.compile(
        r"^\s*(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\s+\[(SPEAKER_\d+)\]:\s*(.+?)\s*$"
    )

    for i, line in enumerate(transcript_content.splitlines()):
        stripped_line = line.strip()
        if not stripped_line: # Skip empty or whitespace-only lines silently
            continue
        
        match = segment_pattern.match(stripped_line)
        if match:
            segment = {
                "id": match.group(1),
                "start_time": match.group(2),
                "end_time": match.group(3),
                "speaker": match.group(4),
                "text": match.group(5).strip()
            }
            parsed_segments.append(segment)
        else:
            parsing_errors.append(
                f"Skipped line {i+1}: '{stripped_line}' - did not match expected format."
            )
    return parsed_segments, parsing_errors

# Page Configuration and Title
st.set_page_config(page_title="Live Fallacy Checker", layout="wide")
st.title("Live Fallacy Checker")
st.markdown("Enter a sentence below to check for common logical fallacies (Ad Hominem, Straw Man, Slippery Slope, False Dichotomy, Appeal to Emotion).")

# File Uploaders
uploaded_video_file = st.file_uploader(
    "Upload Video File",
    type=['mp4', 'mov', 'avi', 'mkv'],  # Added mkv as another common video type
    key="video_uploader"
)

uploaded_transcript_file = st.file_uploader(
    "Upload Timestamped Transcript File",
    type=['txt', 'vtt'],
    key="transcript_uploader"
)

# Input Area
user_sentence = st.text_area("Sentence to analyze:", height=100, key="user_sentence_input", help="Type or paste the sentence you want to check.")

# Analyze Button
# Suggestion: Rename button if its primary function shifts more towards transcript analysis
analyze_button = st.button("Analyze Input", key="analyze_button", help="Click to analyze the provided transcript or sentence.")

# Results Display Area (Conditional on button press)
if analyze_button:
    # Prioritize transcript analysis if a transcript file is uploaded
    if uploaded_transcript_file is not None:
        if uploaded_video_file is None:
            st.error("Please upload both video and transcript files if you are using the file upload feature.")
        else:
            st.subheader("Transcript Analysis Results")
            st.markdown("---") # Visual separator

            # Display the video if uploaded
            st.video(uploaded_video_file)
            st.markdown("---") # Separator after video

            transcript_content = uploaded_transcript_file.getvalue().decode("utf-8")
            
            if not transcript_content.strip():
                st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")
            else:
                parsed_segments, parsing_errors = parse_timestamped_transcript(transcript_content)

                if parsing_errors:
                    with st.expander("View Transcript Parsing Issues", expanded=True):
                        for error_msg in parsing_errors:
                            st.warning(error_msg)
                
                if not parsed_segments:
                    st.warning("No valid transcript segments could be parsed. Please check the file format and content.")
                    # If there were parsing errors, they are already shown. 
                    # If no errors but also no segments, this message is important.
                else:
                    # Implement Speaker Grouping
                    grouped_segments = []
                if parsed_segments:
                    current_speaker = parsed_segments[0]["speaker"]
                    current_text = parsed_segments[0]["text"]
                    current_start_time = parsed_segments[0]["start_time"]
                    current_end_time = parsed_segments[0]["end_time"]

                    for i in range(1, len(parsed_segments)):
                        segment = parsed_segments[i]
                        if segment["speaker"] == current_speaker:
                            current_text += " " + segment["text"]
                            current_end_time = segment["end_time"] # Update end time
                        else:
                            grouped_segments.append({
                                "speaker": current_speaker,
                                "full_text": current_text,
                                "start_time": current_start_time,
                                "end_time": current_end_time
                            })
                            current_speaker = segment["speaker"]
                            current_text = segment["text"]
                            current_start_time = segment["start_time"]
                            current_end_time = segment["end_time"]
                    
                    # Append the last grouped segment
                    grouped_segments.append({
                        "speaker": current_speaker,
                        "full_text": current_text,
                        "start_time": current_start_time,
                        "end_time": current_end_time
                    })

                if not grouped_segments:
                    st.info("No speaker segments found after grouping.")
                else:
                    analysis_results_list = []
                    total_segments_to_analyze = len(grouped_segments)
                    progress_bar = st.progress(0)
                    
                    with st.spinner(f"Analyzing {total_segments_to_analyze} grouped segment(s)... This may take a while."):
                        for i, group in enumerate(grouped_segments):
                            # Record start time for this segment's analysis
                            segment_start_time_analysis = time.perf_counter()

                            raw_api_response = call_qwen_api(group["full_text"], API_KEY, MODEL_ID)
                            fallacy_type, rationale = parse_fallacy_response(raw_api_response)
                            
                            # Record end time for this segment's analysis
                            segment_end_time_analysis = time.perf_counter()
                            duration_ms_segment = (segment_end_time_analysis - segment_start_time_analysis) * 1000

                            analysis_results_list.append({
                                "speaker": group["speaker"],
                                "start_time": group["start_time"],
                                "end_time": group["end_time"],
                                "original_text": group["full_text"],
                                "fallacy_type": fallacy_type,
                                "rationale": rationale,
                                "raw_api_response": raw_api_response, # For debugging
                                "processing_time_ms": duration_ms_segment
                            })
                            progress_bar.progress((i + 1) / total_segments_to_analyze)
                    
                    st.success(f"Analysis complete for {total_segments_to_analyze} segment(s)!")
                    
                    if analysis_results_list:
                        st.subheader("Fallacy Analysis History")
                        for i, result in enumerate(analysis_results_list): # Added enumerate for unique keys
                            st.markdown(f"**Time:** {result['start_time']} - {result['end_time']}")
                            st.markdown(f"**Speaker:** {result['speaker']}")
                            # Using a unique key for each text_area
                            st.text_area("Analyzed Text:", 
                                         value=result['original_text'].replace('$', '\\$'), 
                                         height=150,  # Slightly increased height for better readability
                                         disabled=True, 
                                         key=f"text_{result['speaker']}_{result['start_time']}_{i}")

                            if result['fallacy_type'] and result['fallacy_type'] != "FORMAT_ERROR" and result['fallacy_type'] != "PARSE_ERROR" and result['fallacy_type'] != "Error:" and result['fallacy_type'] is not None:
                                st.warning(f"**Detected Fallacy:** {result['fallacy_type']}")
                                if result['rationale']: # Ensure rationale exists
                                    st.info(f"**Rationale:** {result['rationale'].replace('$', '\\$')}")
                            elif result['fallacy_type'] == "FORMAT_ERROR" or result['fallacy_type'] == "PARSE_ERROR":
                                 st.error(f"Model Response Error for this segment.")
                                 st.caption(f"Raw output: {result['raw_api_response']}")
                            elif result['raw_api_response'].startswith("Error:"):
                                st.error(f"API Error: {result['raw_api_response']}")
                            else: # No fallacy and no error
                                st.success("No fallacy detected in this segment.")
                            
                            st.caption(f"Segment processing time: {result['processing_time_ms']:.2f} ms")
                            st.markdown("---") # Visual separator for each entry
                    else:
                        st.info("No analysis results to display.")

    # Fallback to single sentence analysis if no transcript file is uploaded
    elif user_sentence.strip():
        st.subheader("Single Sentence Analysis Results")
        st.markdown("---") # Visual separator
        st.write(f"**Input Sentence:** {user_sentence.replace("$", "\\$")}") # Show what was analyzed

        raw_api_response = "" # Initialize
        fallacy_type = None   # Initialize
        rationale_text = ""   # Initialize
        duration_ms = 0       # Initialize

        with st.spinner("Analyzing your sentence... please wait."):
            start_time = time.perf_counter()
            actual_sentence_to_analyze = user_sentence 
            raw_api_response = call_qwen_api(actual_sentence_to_analyze, API_KEY, MODEL_ID)
            if not raw_api_response.startswith("Error:"):
                fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
            else:
                rationale_text = raw_api_response 
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
        
        st.markdown("#### Analysis Result:")
        if raw_api_response.startswith("Error:"):
            st.error(f"{raw_api_response}")
        elif fallacy_type == "FORMAT_ERROR":
            st.error("Model Response Error: Could not properly parse the model's output.")
            st.caption(f"Raw model output received: {rationale_text}")
        elif fallacy_type is None:
            st.success("No fallacy detected.")
        else:
            st.warning(f"Detected Fallacy: {fallacy_type}")

        if not raw_api_response.startswith("Error:") and fallacy_type and fallacy_type != "FORMAT_ERROR" and rationale_text:
            st.markdown("#### Rationale:")
            st.write(rationale_text.replace("$", "\\$"))
        
        st.markdown("#### Processing Time:")
        st.caption(f"{duration_ms:.2f} ms")
            
    else:
        # This case handles when analyze_button is clicked but neither transcript nor sentence is provided
        st.warning("Please upload a transcript or enter a sentence to analyze.")

# Optional: Add a small footer or instruction area
st.markdown("---")
st.caption("Powered by Qwen3 32B on Cerebras via OpenRouter. Hackathon Project.")
