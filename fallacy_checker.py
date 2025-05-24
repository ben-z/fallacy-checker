import requests
import time
import sys # Added for sys.exit

def call_qwen_api(sentence: str, api_key: str, model_id: str) -> str:
    """
    Calls the Qwen API to process a sentence for fallacy detection.

    Args:
        sentence: The sentence to process.
        api_key: The API key for authentication.
        model_id: The specific Qwen model ID to use.

    Returns:
        The processed sentence from the API, or an error message.
    """
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    system_message_content = (
        "Identify fallacy in user sentence. Fallacies: Ad Hominem, Straw Man, Slippery Slope, False Dichotomy, Appeal to Emotion. "
        "Output: \"FALLACY_TYPE: Rationale (max 1-2 short sentences).\" OR \"None\". "
        "Be very concise and fast. Pick one most obvious fallacy."
    )
    data = {
        "model": model_id,
        "provider": {
            "only": ["Cerebras"]
        },
        "temperature": 0.1,
        # "max_tokens": 70, # Removed max_tokens
        "messages": [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": sentence}
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("choices") and isinstance(response_json["choices"], list) and len(response_json["choices"]) > 0:
                choice = response_json["choices"][0]
                message = choice.get("message")
                if message:
                    content = message.get("content")
                    if content and content.strip(): # Check if content is not empty
                        return content.strip()
                    
                    reasoning = message.get("reasoning")
                    if reasoning and reasoning.strip():
                        lines = reasoning.strip().splitlines()
                        known_fallacies_upper = ["AD HOMINEM", "STRAW MAN", "SLIPPERY SLOPE", "FALSE DICHOTOMY", "APPEAL TO EMOTION"]
                        for line_idx, line_text in enumerate(reversed(lines)):
                            stripped_line_upper = line_text.strip().upper()
                            if stripped_line_upper == "NONE":
                                return "None" 
                            for fallacy in known_fallacies_upper:
                                if stripped_line_upper.startswith(fallacy + ":"):
                                    # Try to reconstruct from this point, including subsequent lines if part of rationale
                                    relevant_lines = lines[len(lines) - 1 - line_idx:]
                                    return " ".join(l.strip() for l in relevant_lines).strip()
            
            print(f"Debug: Raw response JSON on unexpected structure (after trying reasoning): {response.text}")
            return "Error: Unexpected response structure."
        else:
            return f"Error: API request failed with status code {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: An exception occurred during the API request: {e}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"

def parse_fallacy_response(response_text: str) -> tuple[str | None, str | None]:
    """
    Parses the fallacy detection response from the API.

    Args:
        response_text: The raw string response from the API.

    Returns:
        A tuple containing (fallacy_type, rationale).
        (None, None) if "None" was returned.
        ("FORMAT_ERROR", original_text) if parsing fails.
    """
    response_text_stripped = response_text.strip()
    if response_text_stripped == "None":
        return (None, None)

    prefix = "FALLACY_TYPE: "
    if response_text_stripped.startswith(prefix):
        remaining_text = response_text_stripped[len(prefix):]
        parts = remaining_text.split(". Rationale: ", 1)
        actual_fallacy_name = parts[0].strip()
        actual_rationale = parts[1].strip() if len(parts) > 1 else ""
        return (actual_fallacy_name, actual_rationale)
    else:
        # Fallback for direct fallacy name if "FALLACY_TYPE:" prefix is missing
        # This was observed with the updated heuristic in call_qwen_api
        known_fallacies = ["Ad Hominem", "Straw Man", "Slippery Slope", "False Dichotomy", "Appeal to Emotion"]
        for fallacy_name in known_fallacies:
            if response_text_stripped.upper().startswith(fallacy_name.upper() + ":"):
                parts = response_text_stripped.split(": ", 1)
                extracted_fallacy_name = parts[0].strip() # Keep original casing
                extracted_rationale = parts[1].strip() if len(parts) > 1 else ""
                return (extracted_fallacy_name, extracted_rationale)
        
        return ("FORMAT_ERROR", response_text_stripped)

if __name__ == "__main__":
    api_key = "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"
    model_id = "qwen/qwen3-32b" 

    print(f"Using Qwen model: {model_id} for Live Fallacy Checker.")

    # # Comment out or remove file processing logic
    # transcript_filepath = "transcript.txt"
    # results_log_filepath = "results.log"
    # print(f"Processing transcript: {transcript_filepath}")
    # print(f"Logging results to: {results_log_filepath}")
    # try:
    #     with open(transcript_filepath, 'r', encoding='utf-8') as transcript_file, \
    #          open(results_log_filepath, 'w', encoding='utf-8') as results_file:
            
    #         results_file.write("Sentence|Fallacy Type|Rationale|Latency (ms)\n")

    #         for line in transcript_file:
    #             sentence = line.strip()
    #             if not sentence:
    #                 continue

    #             print(f"\nAnalyzing sentence: \"{sentence}\"")
                
    #             start_time = time.perf_counter()
    #             raw_api_response = call_qwen_api(sentence, api_key, model_id)
    #             fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
    #             end_time = time.perf_counter()
                
    #             duration_ms = (end_time - start_time) * 1000
                
    #             print(f"Raw API Response:\n{raw_api_response}")
                
    #             if fallacy_type:
    #                 if fallacy_type == "FORMAT_ERROR":
    #                     print(f"Format Error: Could not parse response: {rationale_text}")
    #                 else:
    #                     print(f"Fallacy Detected: {fallacy_type}")
    #                     print(f"Rationale: {rationale_text}")
    #             else:
    #                 if rationale_text is None: # Explicitly "None" from API
    #                     print("No fallacy detected.")
    #                 else: 
    #                     print(f"Unexpected response state: {raw_api_response}")

    #             print(f"Processing time: {duration_ms:.2f} ms")
                
    #             fallacy_to_log = fallacy_type if fallacy_type else "None"
    #             # Ensure rationale_text is not None before calling replace
    #             rationale_to_log = rationale_text.replace('\n', ' ') if rationale_text else "" 
    #             results_file.write(f"{sentence}|{fallacy_to_log}|{rationale_to_log}|{duration_ms:.2f}\n")
                
    #             print("-" * 50)
            
    #         print(f"\nProcessing of transcript complete. Detailed results logged to {results_log_filepath}")

    # except FileNotFoundError:
    #     print(f"Error: Transcript file not found at {transcript_filepath}")
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"An unexpected error occurred during processing: {e}")
    #     sys.exit(1)

    while True:
        sentence_input = input("\nEnter a sentence to analyze (or type 'quit' to exit): ")
        
        if sentence_input.strip().lower() == 'quit':
            print("Exiting Live Fallacy Checker.")
            break
        
        if not sentence_input.strip():
            continue
            
        print(f"\nAnalyzing: \"{sentence_input}\"")
        
        start_time = time.perf_counter()
        raw_api_response = call_qwen_api(sentence_input, api_key, model_id)
        fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000
        
        print(f"Raw API Response:\n{raw_api_response}")
        
        if fallacy_type:
            if fallacy_type == "FORMAT_ERROR":
                print(f"Format Error: Could not parse response: {rationale_text}")
            else:
                print(f"Fallacy Detected: {fallacy_type}")
                print(f"Rationale: {rationale_text}")
        else:
            if rationale_text is None: # Explicitly "None" from API
                print("No fallacy detected.")
            else: 
                # This case should ideally not be hit if FORMAT_ERROR handles other non-None cases
                # and parse_fallacy_response correctly returns (None, None) for "None"
                print(f"Unexpected response state (parsed as no fallacy, but rationale present or API error): {raw_api_response}")

        print(f"Processing time: {duration_ms:.2f} ms")
        print("-" * 50)
