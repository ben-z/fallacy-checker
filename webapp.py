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

import re # Added for transcript parsing - re may not be needed anymore by parser but kept for now
import pysrt # Added for SRT parsing
from typing import Tuple, List, Dict # For type hinting

# Constants
API_KEY = "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"
MODEL_ID = "qwen/qwen3-32b"

# Initialize session state for video seek time
if 'video_seek_time' not in st.session_state:
    st.session_state.video_seek_time = 0.0


def parse_srt_transcript(transcript_content: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Parses an SRT transcript string into a list of segment dictionaries
    and a list of parsing error messages using pysrt.

    Args:
        transcript_content: The entire content of the SRT transcript file as a string.

    Returns:
        A tuple containing:
            - parsed_segments: A list of dictionaries, where each dictionary
                               represents a transcript segment.
            - parsing_errors: A list of strings, where each string is an
                              error message if parsing fails.
    """
    parsed_segments: List[Dict[str, str]] = []
    parsing_errors: List[str] = []

    try:
        subs = pysrt.from_string(transcript_content, error_handling=pysrt.ERROR_PASS)
        
        if not subs and transcript_content.strip(): # File has content but pysrt couldn't parse any subs
             parsing_errors.append(
                "The SRT file content could not be parsed by pysrt, or it resulted in no valid subtitle segments. "
                "Please ensure it is a valid SRT format."
            )
             return parsed_segments, parsing_errors


        for sub_item in subs:
            start_time_str = (
                f"{sub_item.start.hours:02}:{sub_item.start.minutes:02}:"
                f"{sub_item.start.seconds:02},{sub_item.start.milliseconds:03}"
            )
            end_time_str = (
                f"{sub_item.end.hours:02}:{sub_item.end.minutes:02}:"
                f"{sub_item.end.seconds:02},{sub_item.end.milliseconds:03}"
            )
            segment = {
                "id": str(sub_item.index),
                "start_time": start_time_str,
                "end_time": end_time_str,
                "speaker": f"SPEAKER_SRT_{sub_item.index}",  # Unique speaker ID for each SRT segment
                "text": sub_item.text_without_tags  # Or sub_item.text
            }
            parsed_segments.append(segment)
            
    except Exception as e: # Catch any exception from pysrt.from_string itself
        parsing_errors.append(f"Failed to parse SRT file due to an unexpected error: {str(e)}")
        # Return empty segments as parsing fundamentally failed
        return [], parsing_errors
        
    return parsed_segments, parsing_errors

def timestamp_to_seconds(ts_str: str) -> float:
    """
    Converts a timestamp string "HH:MM:SS,mmm" to total seconds.
    Returns 0.0 on parsing error and prints an error message.
    """
    try:
        parts = ts_str.split(':')
        if len(parts) != 3:
            raise ValueError("Timestamp format error: Expected 3 parts separated by ':'")
        
        h = int(parts[0])
        m = int(parts[1])
        
        sec_ms_part = parts[2]
        if ',' not in sec_ms_part:
            raise ValueError("Timestamp format error: Expected ',' separating seconds and milliseconds")
            
        sec_ms = sec_ms_part.split(',')
        if len(sec_ms) != 2:
            raise ValueError("Timestamp format error: Expected 2 parts for seconds and milliseconds")
            
        s = int(sec_ms[0])
        ms = int(sec_ms[1])
        
        total_seconds = h * 3600 + m * 60 + s + ms / 1000.0
        return total_seconds
    except ValueError as e:
        print(f"Error converting timestamp '{ts_str}': {e}")
        return 0.0
    except Exception as e: # Catch any other unexpected errors during parsing
        print(f"An unexpected error occurred converting timestamp '{ts_str}': {e}")
        return 0.0

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
    label="Upload SRT Transcript File (.srt)", # Updated label
    type=['srt'],                             # Updated file type
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

            # Display the video if uploaded, using session state for start_time
            st.video(uploaded_video_file, start_time=int(st.session_state.video_seek_time))
            st.markdown("---") # Separator after video

            transcript_content = uploaded_transcript_file.getvalue().decode("utf-8")
            
            if not transcript_content.strip():
                st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")
            else:
                # Updated to call the new SRT parser
                parsed_segments, parsing_errors = parse_srt_transcript(transcript_content)

                if parsing_errors: # Display errors from pysrt parsing attempt
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

                            # Add "Jump to this moment" button
                            seek_time_seconds = timestamp_to_seconds(result['start_time'])
                            button_label = f"Jump to video at {result['start_time']}"
                            button_key = f"jump_button_{i}"
                            
                            if st.button(button_label, key=button_key):
                                st.session_state.video_seek_time = float(seek_time_seconds)
                                # Streamlit will rerun from top. st.video will use the updated session_state.
                                # No explicit st.experimental_rerun() needed here.

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
