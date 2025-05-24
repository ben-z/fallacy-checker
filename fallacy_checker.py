import requests
import time
import sys # Added for sys.exit

gold_standard_data = [
    {
        "sentence": "Your fashion sense is so bad, it's no wonder you can't make a good argument about economic policy.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Attacking the person's fashion sense instead of their economic arguments."
    },
    {
        "sentence": "My opponent wants to improve our parks, which clearly means he's happy to ignore the homeless crisis!",
        "fallacy_type": "Straw Man",
        "rationale": "Misrepresenting the opponent's position (improving parks) as ignoring homelessness."
    },
    {
        "sentence": "If we legalize marijuana, then everyone will start using harder drugs, and society will collapse.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Asserting a chain reaction of negative consequences without sufficient evidence."
    },
    {
        "sentence": "You must either be a complete genius or a total idiot; there's no in-between.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting only two extreme options when others may exist."
    },
    {
        "sentence": "Just imagine the joy on a child's face if you donate to this cause; how could you refuse?",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Using the image of a joyful child to evoke an emotional response for donation."
    },
    {
        "sentence": "The sun rises in the east and sets in the west.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "What is your favorite color?",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "This report indicates a 10% increase in sales over the last quarter.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "I believe that investing in renewable energy is crucial for the future.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "He's a terrible singer, so his views on climate change must be wrong.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Dismissing views on climate change based on singing ability."
    },
    {
        "sentence": "The new city council member wants to cut funding for the library; clearly, she wants our children to grow up ignorant.",
        "fallacy_type": "Straw Man",
        "rationale": "Misrepresenting cutting library funding as wanting children to be ignorant."
    },
    {
        "sentence": "If we allow students to use tablets in class, they'll soon forget how to write by hand, and then literacy rates will plummet.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Claiming tablet use will inevitably lead to plummeting literacy rates."
    },
    {
        "sentence": "Either you support my plan completely, or you're against our company's success.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting only two options: complete support or being against success."
    },
    {
        "sentence": "Please, think of the suffering animals; we have to pass this new animal welfare bill right now!",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Using the suffering of animals to pressure for immediate bill passage."
    },
    {
        "sentence": "The capital of France is Paris.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "What time does the train to London depart?",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Research suggests that a balanced diet contributes to good health.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Many people enjoy walking in the park during autumn.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "You wouldn't understand the complexities of this issue; you didn't even go to college.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Dismissing someone's understanding based on their college education."
    },
    {
        "sentence": "So you think we should invest more in public transportation? It's clear you want to bankrupt the city with your wild spending ideas.",
        "fallacy_type": "Straw Man",
        "rationale": "Exaggerating investing in public transport as wanting to bankrupt the city."
    },
    {
        "sentence": "If we let them build that new apartment complex, traffic will become unbearable, and our quiet neighborhood will be ruined forever.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Claiming building an apartment complex will inevitably lead to a ruined neighborhood."
    },
    {
        "sentence": "It's simple: either we increase military spending, or we leave ourselves vulnerable to attack.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting only two options regarding military spending and vulnerability."
    },
    {
        "sentence": "Look at these heartbreaking images of disaster victims; you must donate to our relief fund.",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Using heartbreaking images to compel donations."
    },
    {
        "sentence": "The Earth revolves around the Sun.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "How many cups of coffee do you drink per day?",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "The company's stock price increased by 5% yesterday.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Public speaking can be a challenging skill to master.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Only a fool would disagree with my assessment of the political situation.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Implying that anyone who disagrees is a fool."
    },
    {
        "sentence": "The proposal is to reduce taxes for the wealthy, which is clearly an attempt to make the poor even poorer.",
        "fallacy_type": "Straw Man",
        "rationale": "Misrepresenting the intent of tax reduction for the wealthy."
    },
    {
        "sentence": "If we don't ban this video game, our children will all become violent criminals.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Asserting that not banning a video game will inevitably lead to children becoming violent criminals."
    },
    {
        "sentence": "You're either with us or against us in this important matter.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting a binary choice of being with or against, allowing no middle ground."
    },
    {
        "sentence": "This puppy has been abandoned and needs a loving home; how can you turn your back on such a defenseless creature?",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Appealing to pity for an abandoned puppy to persuade someone to adopt it."
    },
    {
        "sentence": "Water boils at 100 degrees Celsius at sea level.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "What are your plans for the weekend?",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "The latest inflation figures are a cause for concern among economists.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Learning a new language can open up many opportunities.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "Given his criminal record, his testimony about the incident is completely unreliable.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Dismissing testimony based on the person's past criminal record rather than the testimony's merits."
    },
    {
        "sentence": "You say we need more environmental regulations? So you want to destroy businesses and jobs, do you?",
        "fallacy_type": "Straw Man",
        "rationale": "Misrepresenting the call for more environmental regulations as a desire to destroy businesses and jobs."
    },
    {
        "sentence": "If we allow a single exception to this rule, the entire system will break down.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Claiming a single exception will inevitably lead to the entire system breaking down."
    },
    {
        "sentence": "We must either adopt this new software immediately or face becoming obsolete in the market.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting only two options: adopting new software or becoming obsolete."
    },
    {
        "sentence": "Don't you feel a surge of pride when you hear our national anthem? That's why our policies are the best.",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Using feelings of pride from the national anthem to argue for the superiority of policies."
    },
    {
        "sentence": "The Pacific Ocean is the largest ocean on Earth.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "What is the best way to learn to play the guitar?",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "The government announced new guidelines for international travel.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "It's important to consider all viewpoints before making a decision.",
        "fallacy_type": "None",
        "rationale": ""
    },
    {
        "sentence": "He's affiliated with that political party, so everything he says is biased and untrustworthy.",
        "fallacy_type": "Ad Hominem",
        "rationale": "Dismissing all statements from someone based on their political affiliation."
    },
    {
        "sentence": "My opponent advocates for stricter gun control. It's obvious he wants to disarm all law-abiding citizens and leave them defenseless.",
        "fallacy_type": "Straw Man",
        "rationale": "Misrepresenting advocating for stricter gun control as wanting to disarm all citizens."
    },
    {
        "sentence": "If you don't get a perfect score on this test, you'll never get into a good university, and your future will be ruined.",
        "fallacy_type": "Slippery Slope",
        "rationale": "Claiming not getting a perfect score will inevitably lead to a ruined future."
    },
    {
        "sentence": "You can either accept the job offer as it is, or you can remain unemployed.",
        "fallacy_type": "False Dichotomy",
        "rationale": "Presenting only two options: accepting the current job offer or unemployment."
    },
    {
        "sentence": "Think of the brave soldiers who fought for our freedom; supporting this war is the only patriotic choice.",
        "fallacy_type": "Appeal to Emotion",
        "rationale": "Using the image of brave soldiers to argue that supporting a specific war is the only patriotic choice."
    }
]

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
        "Identify the single most obvious logical fallacy in the user's sentence. Fallacies to consider: Ad Hominem, Appeal to Authority, Appeal to Emotion, Circular Reasoning, False Dichotomy, Hasty Generalization, Post Hoc Ergo Propter Hoc, Slippery Slope, Straw Man. "
        "Output format: \"FALLACY_TYPE: Rationale (1-2 short sentences).\" If no fallacy is present, output \"None\". Be concise in your rationale."
    )
    data = {
        "model": model_id,
        "provider": {
            "only": ["Cerebras"]
        },
        "temperature": 0.7,
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
                        known_fallacies_upper = ["AD HOMINEM", "APPEAL TO AUTHORITY", "APPEAL TO EMOTION", "CIRCULAR REASONING", "FALSE DICHOTOMY", "HASTY GENERALIZATION", "POST HOC ERGO PROPTER HOC", "SLIPPERY SLOPE", "STRAW MAN"]
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

    # 1. Handle "None" with Rationale (More Leniently):
    # Check for "None" (case-insensitive) possibly followed by a separator and rationale
    # The goal is to capture "None", "None.", "None: explanation", "none. It is a fact" etc. as (None, None)
    temp_upper_stripped = response_text_stripped.upper()
    if temp_upper_stripped.startswith("NONE"):
        if len(temp_upper_stripped) == 4: # Exactly "NONE"
            return (None, None)
        # Check if the character after "NONE" is a common separator or space
        # This allows for "None." or "None: " or "None " followed by more text.
        elif temp_upper_stripped[4] in ['.', ':', ' ']:
            # We can optionally capture the text after "None[./: ]" as the rationale if needed in the future,
            # but for now, if it starts with "None" and a separator, consider it (None, None).
            return (None, None) 

    prefix = "FALLACY_TYPE: "
    known_fallacies_list_for_primary_path = ["Ad Hominem", "Appeal to Authority", "Appeal to Emotion", "Circular Reasoning", "False Dichotomy", "Hasty Generalization", "Post Hoc Ergo Propter Hoc", "Slippery Slope", "Straw Man"]


    if response_text_stripped.startswith(prefix):
        remaining_text = response_text_stripped[len(prefix):].strip()
        
        # Sort known_fallacies by length in descending order to prioritize longer matches
        # (e.g., "Post Hoc Ergo Propter Hoc" before "Post Hoc")
        # This list is defined above for clarity, can be moved inside if preferred.
        sorted_known_fallacies = sorted(known_fallacies_list_for_primary_path, key=len, reverse=True)

        for fallacy_template in sorted_known_fallacies:
            # Perform a case-insensitive check
            if remaining_text.upper().startswith(fallacy_template.upper()):
                # Determine the character immediately following the match in remaining_text
                char_after_match = None
                if len(remaining_text) > len(fallacy_template):
                    char_after_match = remaining_text[len(fallacy_template)]
                
                # Condition for valid match:
                # - char_after_match is None (remaining_text is exactly the fallacy name)
                # - OR char_after_match is not a letter or digit
                if char_after_match is None or not char_after_match.isalnum():
                    actual_fallacy_name = fallacy_template # Use canonical casing
                    
                    rationale_text = remaining_text[len(fallacy_template):].strip()
                    # Clean up the beginning of rationale_text
                    actual_rationale = rationale_text.lstrip(' .:').strip()
                    
                    # Normalize common variations like "Appeal To Emotion" to "Appeal to Emotion"
                    # This specific normalization might be redundant if fallacy_template is already canonical,
                    # but can be kept if there's a chance fallacy_template itself isn't perfectly cased.
                    # For now, assuming fallacy_template from known_fallacies_list_for_primary_path is canonical.
                    # if " To " in actual_fallacy_name:
                    #     actual_fallacy_name = actual_fallacy_name.replace(" To ", " to ")

                    return (actual_fallacy_name, actual_rationale)
        
        # If the loop completes without returning, no known fallacy was identified
        # at the beginning of remaining_text according to the new logic.
        return ("FORMAT_ERROR", response_text_stripped) # Or a more specific error/fallback
    else:
        # Fallback for direct fallacy name if "FALLACY_TYPE:" prefix is missing
        # This known_fallacies list is used for the fallback path
        known_fallacies = ["Ad Hominem", "Appeal to Authority", "Appeal to Emotion", "Circular Reasoning", "False Dichotomy", "Hasty Generalization", "Post Hoc Ergo Propter Hoc", "Slippery Slope", "Straw Man"]
        
        # 2. Improve Fallback Path Logic
        parts = response_text_stripped.split(":", 1) # More lenient with space after colon
        
        potential_fallacy_name_from_llm = parts[0].strip().replace("_", " ")
        # Rationale is everything after the first colon.
        extracted_rationale = parts[1].strip() if len(parts) > 1 else ""

        for known_fallacy in known_fallacies:
            if potential_fallacy_name_from_llm.lower() == known_fallacy.lower():
                return (known_fallacy, extracted_rationale) # Return canonical casing
        
        # If the "None" check at the beginning didn't catch it,
        # and it doesn't match "FALLACY_TYPE:" prefix,
        # and it doesn't match any known fallacy in the fallback, it's a format error.
        return ("FORMAT_ERROR", response_text_stripped)

def evaluate_model(api_key, model_id):
    """
    Evaluates the fallacy detection model against a gold standard dataset.
    """
    correct_predictions = 0
    total_sentences = len(gold_standard_data)

    print("\n--- Detailed Evaluation Results ---")

    for item in gold_standard_data:
        sentence = item["sentence"]
        gold_fallacy_type = item["fallacy_type"]
        gold_rationale = item["rationale"]

        # Ensure gold_fallacy_type is None if it's "None" string for direct comparison
        if gold_fallacy_type == "None":
            gold_fallacy_type = None

        raw_api_response = call_qwen_api(sentence, api_key, model_id)
        llm_fallacy_type, llm_rationale = parse_fallacy_response(raw_api_response)

        print(f"\nSentence: {sentence}")
        # Adjust printing for gold_fallacy_type if it's None
        gold_display_fallacy = "None" if gold_fallacy_type is None else gold_fallacy_type
        print(f"  Gold Standard: {gold_display_fallacy} - Rationale: {gold_rationale if gold_rationale else 'N/A'}")
        
        # Adjust printing for llm_fallacy_type if it's None
        llm_display_fallacy = "None" if llm_fallacy_type is None else llm_fallacy_type
        print(f"  LLM Output: {llm_display_fallacy} - Rationale: {llm_rationale if llm_rationale else 'N/A'}")
        print(f"  Raw API Response: {raw_api_response}")


        if llm_fallacy_type == gold_fallacy_type:
            correct_predictions += 1
            print("  Result: CORRECT")
        else:
            print("  Result: INCORRECT")
        print("-" * 30)

    accuracy = correct_predictions / total_sentences if total_sentences > 0 else 0

    print("\n--- Evaluation Summary ---")
    print(f"Total Sentences: {total_sentences}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2%}")
    print("------------------------")
    
    # For now, returning accuracy, but could expand to return detailed results list
    return accuracy


if __name__ == "__main__":
    api_key = "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"
    model_id = "qwen/qwen3-32b" 

    print(f"Using Qwen model: {model_id} for Fallacy Checker Evaluation.")

    # # Comment out or remove file processing logic (transcript.txt)
    # # transcript_filepath = "transcript.txt"
    # # results_log_filepath = "results.log"
    # # print(f"Processing transcript: {transcript_filepath}")
    # # print(f"Logging results to: {results_log_filepath}")
    # # try:
    # #     with open(transcript_filepath, 'r', encoding='utf-8') as transcript_file, \
    # #          open(results_log_filepath, 'w', encoding='utf-8') as results_file:
            
    # #         results_file.write("Sentence|Fallacy Type|Rationale|Latency (ms)\n")

    # #         for line in transcript_file:
    # #             sentence = line.strip()
    # #             if not sentence:
    # #                 continue

    # #             print(f"\nAnalyzing sentence: \"{sentence}\"")
                
    # #             start_time = time.perf_counter()
    # #             raw_api_response = call_qwen_api(sentence, api_key, model_id)
    # #             fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
    # #             end_time = time.perf_counter()
                
    # #             duration_ms = (end_time - start_time) * 1000
                
    # #             print(f"Raw API Response:\n{raw_api_response}")
                
    # #             if fallacy_type:
    # #                 if fallacy_type == "FORMAT_ERROR":
    # #                     print(f"Format Error: Could not parse response: {rationale_text}")
    # #                 else:
    # #                     print(f"Fallacy Detected: {fallacy_type}")
    # #                     print(f"Rationale: {rationale_text}")
    # #             else:
    # #                 if rationale_text is None: # Explicitly "None" from API
    # #                     print("No fallacy detected.")
    # #                 else: 
    # #                     print(f"Unexpected response state: {raw_api_response}")

    # #             print(f"Processing time: {duration_ms:.2f} ms")
                
    # #             fallacy_to_log = fallacy_type if fallacy_type else "None"
    # #             # Ensure rationale_text is not None before calling replace
    # #             rationale_to_log = rationale_text.replace('\n', ' ') if rationale_text else "" 
    # #             results_file.write(f"{sentence}|{fallacy_to_log}|{rationale_to_log}|{duration_ms:.2f}\n")
                
    # #             print("-" * 50)
            
    # #         print(f"\nProcessing of transcript complete. Detailed results logged to {results_log_filepath}")

    # # except FileNotFoundError:
    # #     print(f"Error: Transcript file not found at {transcript_filepath}")
    # #     sys.exit(1)
    # # except Exception as e:
    # #     print(f"An unexpected error occurred during processing: {e}")
    # #     sys.exit(1)

    # # Comment out or remove the interactive while True loop
    # # while True:
    # #     sentence_input = input("\nEnter a sentence to analyze (or type 'quit' to exit): ")
        
    # #     if sentence_input.strip().lower() == 'quit':
    # #         print("Exiting Live Fallacy Checker.")
    # #         break
        
    # #     if not sentence_input.strip():
    # #         continue
            
    # #     print(f"\nAnalyzing: \"{sentence_input}\"")
        
    # #     start_time = time.perf_counter()
    # #     raw_api_response = call_qwen_api(sentence_input, api_key, model_id)
    # #     fallacy_type, rationale_text = parse_fallacy_response(raw_api_response)
    # #     end_time = time.perf_counter()
        
    # #     duration_ms = (end_time - start_time) * 1000
        
    # #     print(f"Raw API Response:\n{raw_api_response}")
        
    # #     if fallacy_type:
    # #         if fallacy_type == "FORMAT_ERROR":
    # #             print(f"Format Error: Could not parse response: {rationale_text}")
    # #         else:
    # #             print(f"Fallacy Detected: {fallacy_type}")
    # #             print(f"Rationale: {rationale_text}")
    # #     else:
    # #         if rationale_text is None: # Explicitly "None" from API
    # #             print("No fallacy detected.")
    # #         else: 
    # #             # This case should ideally not be hit if FORMAT_ERROR handles other non-None cases
    # #             # and parse_fallacy_response correctly returns (None, None) for "None"
    # #             print(f"Unexpected response state (parsed as no fallacy, but rationale present or API error): {raw_api_response}")

    # #     print(f"Processing time: {duration_ms:.2f} ms")
    # #     print("-" * 50)

    evaluate_model(api_key, model_id)
