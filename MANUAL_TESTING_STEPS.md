# Manual Testing Steps for Video Fallacy Checker

## I. Prerequisites
1.  Ensure Python environment is set up with all dependencies from `requirements.txt` installed (including `pysrt`).
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure the OpenRouter API Key (`API_KEY`) and Model ID (`MODEL_ID`) in `webapp.py` are correctly configured if live API calls are to be tested.
3.  Have a sample video file ready (e.g., `sample.mp4`, `sample.mov`). Any short video will do.
4.  Use the provided `test_transcript.srt` for transcript-related tests.

## II. Running the Application
1.  Open a terminal in the repository root.
2.  Run the Streamlit application using the command:
    ```bash
    streamlit run webapp.py
    ```
3.  The application should open in your default web browser.

## III. Core Functionality Testing: Transcript and Video Analysis

1.  **Successful Upload and Analysis Path with `test_transcript.srt`:**
    *   **Action:** Locate the "Upload Video File" widget. Click "Browse files" and select your sample video file.
    *   **Expected:** The file name should appear.
    *   **Action:** Locate the "Upload SRT Transcript File (.srt)" widget. Click "Browse files" and select `test_transcript.srt`.
    *   **Expected:** The file name `test_transcript.srt` should appear.
    *   **Action:** Click the "Analyze Input" button.
    *   **Expected UI Updates & Checks:**
        1.  A spinner message "Analyzing X grouped segment(s)..." should appear (where X is the number of entries in the SRT, e.g., 9).
        2.  The uploaded video should be displayed and playable under "Transcript Analysis Results".
        3.  **Parsing Errors:** Check for an expander "View Transcript Parsing Issues".
            *   **Expected:** For `test_transcript.srt` (which is now valid SRT), this expander should either not appear or show no errors.
        4.  **Fallacy Analysis History:** A subheader "Fallacy Analysis History" should appear.
        5.  **Segment Verification (Each SRT entry is a segment):**
            *   **Segment 1:**
                *   Time: `00:00:01,000 - 00:00:03,500`
                *   Speaker: `SPEAKER_SRT_1`
                *   Text: "Hello, this is the first line."
            *   **Segment 2:**
                *   Time: `00:00:04,000 - 00:00:06,000`
                *   Speaker: `SPEAKER_SRT_2`
                *   Text: "I am still speaking, and this should be grouped." (Note: "grouped" here refers to the original VTT line, it will be its own segment now)
            *   **Segment 3:**
                *   Time: `00:00:07,100 - 00:00:09,800`
                *   Speaker: `SPEAKER_SRT_3`
                *   Text: "Now it's my turn to say something interesting."
            *   **Segment 4:**
                *   Time: `00:00:10,000 - 00:00:12,500`
                *   Speaker: `SPEAKER_SRT_4`
                *   Text: "This is my second sentence, also to be grouped with my first."
            *   **Segment 5:**
                *   Time: `00:00:13,000 - 00:00:15,000`
                *   Speaker: `SPEAKER_SRT_5`
                *   Text: "I'm back with a final comment. This is a new block for SPEAKER_00."
            *   **Segment 6:**
                *   Time: `00:00:15,500 - 00:00:18,000`
                *   Speaker: `SPEAKER_SRT_6`
                *   Text: "If we allow students to use tablets in class, they'll soon forget how to write by hand."
                *   **Fallacy Check:** Observe the fallacy analysis result. This segment might trigger a fallacy.
            *   **Segment 7:**
                *   Time: `00:00:18,500 - 00:00:21,000`
                *   Speaker: `SPEAKER_SRT_7`
                *   Text: "Then literacy rates will plummet and society will collapse. This is a slippery slope."
                *   **Fallacy Check:** Observe the fallacy analysis result. This segment is designed to potentially trigger a "Slippery Slope" fallacy.
            *   **Segment 8:**
                *   Time: `00:00:25,000 - 00:00:27,000`
                *   Speaker: `SPEAKER_SRT_8`
                *   Text: "One more from me."
            *   **Segment 9:**
                *   Time: `00:00:28,000 - 00:00:30,000`
                *   Speaker: `SPEAKER_SRT_9`
                *   Text: "And one more from SPEAKER_01."
        6.  **API Call & Response:** For each segment, check if a fallacy type (or "No fallacy detected") and rationale (if applicable) are displayed.
        7.  Processing time per segment should be displayed.
        8.  A success message "Analysis complete for X segment(s)!" should appear.

## IV. Error Handling and Edge Cases

1.  **File Upload Errors:**
    *   **Video Only:** (Same as before)
    *   **Transcript Only:**
        *   **Action:** Refresh. Upload only `test_transcript.srt`. Click "Analyze Input".
        *   **Expected:** `st.error("Please upload both video and transcript files if you are using the file upload feature.")`
    *   **Wrong File Type (Video):** (Same as before)
    *   **Wrong File Type (Transcript):**
        *   **Action:** Refresh. Upload video. Upload a non-SRT file (e.g., `.jpg`) into "Upload SRT Transcript File (.srt)". Click "Analyze Input".
        *   **Expected:**
            *   "View Transcript Parsing Issues" expander should show an error like "The SRT file content could not be parsed by pysrt..." or "Failed to parse SRT file due to an unexpected error...".
            *   A warning "No valid transcript segments could be parsed..." should appear.
            *   No "Fallacy Analysis History".

2.  **Transcript Content Errors (SRT Specific):**
    *   **Empty Transcript File:**
        *   **Action:** Create `empty.srt`. Refresh. Upload video and `empty.srt`. Click "Analyze Input".
        *   **Expected:** `st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")`
    *   **Whitespace-Only Transcript File:**
        *   **Action:** Create `whitespace.srt` (only spaces/newlines). Refresh. Upload video and `whitespace.srt`. Click "Analyze Input".
        *   **Expected:** `st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")`
    *   **Completely Malformed SRT File (e.g., plain text):**
        *   **Action:** Create `malformed.srt` with "This is not an SRT file." Refresh. Upload video and `malformed.srt`. Click "Analyze Input".
        *   **Expected:**
            *   "View Transcript Parsing Issues" expander shows an error (e.g., "The SRT file content could not be parsed by pysrt...").
            *   Warning "No valid transcript segments could be parsed...".
            *   No "Fallacy Analysis History".
    *   **SRT File with Some Malformed Entries (but otherwise parsable structure):**
        *   **Action:** Create `partially_malformed.srt` (e.g., good entries, then one with bad time format). Refresh. Upload video and `partially_malformed.srt`. Click "Analyze Input".
        *   **Expected:** `pysrt` with `ERROR_PASS` should skip the bad entries. The "View Transcript Parsing Issues" expander might not show errors if `pysrt` silently skips them due to `ERROR_PASS`. Successfully parsed entries should appear in "Fallacy Analysis History". If `pysrt` cannot even parse the file structure due to severe errors, then it will behave like the "Completely Malformed" case.

## V. Fallback Single Sentence Analysis
    (This section remains largely the same, just ensure `test_transcript.srt` is used if testing the "With Files Uploaded" scenario)

1.  **No Files Uploaded:** (Same as before)
2.  **With Files Uploaded, but Choosing Single Sentence:**
    *   **Action:** Upload video and `test_transcript.srt`. Type a sentence. Click "Analyze Input".
    *   **Expected:** Transcript analysis should run; single sentence input ignored.
3.  **Empty Input for Single Sentence:** (Same as before)

## VI. General UI/UX
(Same as before)

This list should provide a good basis for thoroughly testing the application with SRT files.
