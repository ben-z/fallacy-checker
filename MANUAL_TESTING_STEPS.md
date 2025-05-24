# Manual Testing Steps for Video Fallacy Checker

## I. Prerequisites
1.  Ensure Python environment is set up with all dependencies from `requirements.txt` installed.
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure the OpenRouter API Key (`API_KEY`) and Model ID (`MODEL_ID`) in `webapp.py` are correctly configured if live API calls are to be tested. (Note: For pure UI and parsing tests, this might not be strictly necessary if dummy functions are robust).
3.  Have a sample video file ready (e.g., `sample.mp4`, `sample.mov`). Any short video will do for testing the upload and display functionality.
4.  Use the provided `test_transcript.vtt` for transcript-related tests.

## II. Running the Application
1.  Open a terminal in the repository root.
2.  Run the Streamlit application using the command:
    ```bash
    streamlit run webapp.py
    ```
3.  The application should open in your default web browser.

## III. Core Functionality Testing: Transcript and Video Analysis

1.  **Successful Upload and Analysis Path:**
    *   **Action:** Locate the "Upload Video File" widget. Click "Browse files" (or drag and drop) and select your sample video file (e.g., `sample.mp4`).
    *   **Expected:** The file name should appear under the uploader.
    *   **Action:** Locate the "Upload Timestamped Transcript File" widget. Click "Browse files" and select `test_transcript.vtt`.
    *   **Expected:** The file name `test_transcript.vtt` should appear.
    *   **Action:** Click the "Analyze Input" button.
    *   **Expected UI Updates & Checks:**
        1.  A spinner message "Analyzing X grouped segment(s)..." should appear.
        2.  The uploaded video should be displayed and playable under "Transcript Analysis Results". Verify by playing a few seconds.
        3.  **Parsing Errors:** Check for an expander "View Transcript Parsing Issues".
            *   **Expected:** It should contain one warning: "Skipped line 8: 'This is a malformed line, it will be skipped.' - did not match expected format."
        4.  **Fallacy Analysis History:** A subheader "Fallacy Analysis History" should appear.
        5.  **Speaker Grouping & Content Verification:**
            *   **Segment 1 (SPEAKER_00):**
                *   Time: `00:00:01,000 - 00:00:06,000`
                *   Speaker: `SPEAKER_00`
                *   Text: "Hello, this is the first line. I am still speaking, and this should be grouped."
            *   **Segment 2 (SPEAKER_01):**
                *   Time: `00:00:07,100 - 00:00:12,500`
                *   Speaker: `SPEAKER_01`
                *   Text: "Now it's my turn to say something interesting. This is my second sentence, also to be grouped with my first."
            *   **Segment 3 (SPEAKER_00):**
                *   Time: `00:00:13,000 - 00:00:15,000`
                *   Speaker: `SPEAKER_00`
                *   Text: "I'm back with a final comment. This is a new block for SPEAKER_00."
            *   **Segment 4 (SPEAKER_01):**
                *   Time: `00:00:15,500 - 00:00:21,000` (Note: end time from the last segment of this speaker block)
                *   Speaker: `SPEAKER_01`
                *   Text: "If we allow students to use tablets in class, they'll soon forget how to write by hand. Then literacy rates will plummet and society will collapse. This is a slippery slope."
                *   **Fallacy Check:** Observe the fallacy analysis result. This segment is designed to potentially trigger a "Slippery Slope" fallacy. Verify if a fallacy is detected and if the rationale is displayed. (Actual fallacy detection depends on the model's performance).
            *   **Segment 5 (SPEAKER_00):**
                *   Time: `00:00:25,000 - 00:00:27,000`
                *   Speaker: `SPEAKER_00`
                *   Text: "One more from me."
            *   **Segment 6 (SPEAKER_01):**
                *   Time: `00:00:28,000 - 00:00:30,000`
                *   Speaker: `SPEAKER_01`
                *   Text: "And one more from SPEAKER_01."
        6.  **API Call & Response:** For each segment, check if a fallacy type (or "No fallacy detected") and rationale (if applicable) are displayed. Note any API errors if the backend connection fails.
        7.  Processing time per segment should be displayed.
        8.  A success message "Analysis complete for X segment(s)!" should appear above the history.

## IV. Error Handling and Edge Cases

1.  **File Upload Errors:**
    *   **Video Only:**
        *   **Action:** Upload only a video file. Do not upload a transcript. Click "Analyze Input".
        *   **Expected:** An error message `st.error("Please upload both video and transcript files if you are using the file upload feature.")` should appear.
    *   **Transcript Only:**
        *   **Action:** Refresh the page. Upload only `test_transcript.vtt`. Do not upload a video. Click "Analyze Input".
        *   **Expected:** An error message `st.error("Please upload both video and transcript files if you are using the file upload feature.")` should appear.
    *   **Wrong File Type (Video):**
        *   **Action:** Refresh the page. Attempt to upload a non-video file (e.g., a `.txt` or `.jpg`) into the "Upload Video File" widget.
        *   **Expected:** The file uploader should ideally restrict selection or show an error if an incorrect type is forced (Streamlit's behavior might vary). If it uploads, the `st.video` call might fail gracefully or show an error.
    *   **Wrong File Type (Transcript):**
        *   **Action:** Refresh the page. Upload a video file. Upload a non-transcript file (e.g., a `.jpg`) into the "Upload Timestamped Transcript File" widget. Click "Analyze Input".
        *   **Expected:** The application will attempt to decode and parse.
            *   Parsing errors should be displayed in the "View Transcript Parsing Issues" expander (likely all lines will be errors).
            *   A warning "No valid transcript segments could be parsed..." should appear.
            *   No "Fallacy Analysis History" should be generated.

2.  **Transcript Content Errors:**
    *   **Empty Transcript File:**
        *   **Action:** Create an empty file named `empty.vtt`. Refresh the page. Upload a video file and `empty.vtt`. Click "Analyze Input".
        *   **Expected:** An error message `st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")` should appear.
    *   **Whitespace-Only Transcript File:**
        *   **Action:** Create a file `whitespace.vtt` containing only spaces and newlines. Refresh the page. Upload a video file and `whitespace.vtt`. Click "Analyze Input".
        *   **Expected:** An error message `st.error("Uploaded transcript file is empty or contains only whitespace. Cannot proceed with analysis.")` should appear.
    *   **Completely Malformed Transcript File:**
        *   **Action:** Create a file `malformed.vtt` with content like "This is not a transcript." Refresh the page. Upload a video file and `malformed.vtt`. Click "Analyze Input".
        *   **Expected:**
            *   The "View Transcript Parsing Issues" expander should show errors for each line.
            *   A warning "No valid transcript segments could be parsed..." should appear.
            *   No "Fallacy Analysis History" should be generated.

## V. Fallback Single Sentence Analysis

1.  **No Files Uploaded:**
    *   **Action:** Refresh the page. Ensure no files are uploaded.
    *   **Action:** In the "Sentence to analyze:" text area, type a sentence (e.g., "Everyone loves this product, so it must be good."). Click "Analyze Input".
    *   **Expected:**
        *   The "Single Sentence Analysis Results" subheader should appear.
        *   The input sentence should be displayed.
        *   A spinner "Analyzing your sentence..." should appear.
        *   Fallacy analysis results (fallacy type or no fallacy, rationale) for the single sentence should be displayed.
        *   Processing time should be displayed.
2.  **With Files Uploaded, but Choosing Single Sentence:**
    *   The current design prioritizes file uploads. To test single sentence analysis when files *are* also uploaded, one would typically need to clear the file uploaders first or the application logic would need a way to switch modes. Test that if files are uploaded, the single sentence input is ignored.
    *   **Action:** Upload a video and `test_transcript.vtt`. Also, type a sentence in the "Sentence to analyze:" text area. Click "Analyze Input".
    *   **Expected:** The application should process the transcript files. The single sentence input should be ignored. Verify that "Transcript Analysis Results" and "Fallacy Analysis History" are shown, not "Single Sentence Analysis Results".
3.  **Empty Input for Single Sentence:**
    *   **Action:** Refresh the page. Ensure no files are uploaded. Leave the text area empty. Click "Analyze Input".
    *   **Expected:** A warning `st.warning("Please upload a transcript or enter a sentence to analyze.")` should appear.

## VI. General UI/UX
1.  **Responsiveness:** Check if the layout is usable on different screen sizes (if possible).
2.  **Clarity of Instructions:** Ensure all labels, help texts, and messages are clear.
3.  **Spinner/Progress:** Verify spinners and progress bars appear during long operations and disappear afterward.
4.  **No Console Errors:** Open the browser's developer console and check for any JavaScript errors during interaction.

This list should provide a good basis for thoroughly testing the application.
