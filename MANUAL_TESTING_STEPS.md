# Manual Testing Steps for Video Fallacy Checker

## I. Prerequisites
1.  Ensure Python environment is set up with all dependencies from `requirements.txt` installed (including `pysrt`).
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure the OpenRouter API Key (`API_KEY`) and Model ID (`MODEL_ID`) in `webapp.py` are correctly configured if live API calls are to be tested.
3.  Have a sample video file ready (e.g., `sample.mp4`, `sample.mov`). Any short video will do. Ensure the video is longer than the timestamps in `test_transcript.srt` for effective seek testing (e.g., > 30 seconds).
4.  Use the provided `test_transcript.srt` for transcript-related tests.

## II. Running the Application
1.  Open a terminal in the repository root.
2.  Run the Streamlit application using the command:
    ```bash
    streamlit run webapp.py
    ```
3.  The application should open in your default web browser.

## III. Core Functionality Testing: Transcript and Video Analysis

### 1. Successful Upload and Analysis Path with `test_transcript.srt`
    *   **Action:** Locate the "Upload Video File" widget. Click "Browse files" and select your sample video file.
    *   **Expected:** The file name should appear.
    *   **Action:** Locate the "Upload SRT Transcript File (.srt)" widget. Click "Browse files" and select `test_transcript.srt`.
    *   **Expected:** The file name `test_transcript.srt` should appear.
    *   **Action:** Click the "Analyze Input" button.
    *   **Expected UI Updates & Checks:**
        1.  A spinner message "Analyzing X grouped segment(s)..." should appear (where X is the number of entries in the SRT, e.g., 9).
        2.  The uploaded video should be displayed and playable under "Transcript Analysis Results". **Initially, it should start from 0 seconds (or `st.session_state.video_seek_time`'s initial value).**
        3.  **Parsing Errors:** Check for an expander "View Transcript Parsing Issues".
            *   **Expected:** For `test_transcript.srt` (which is now valid SRT), this expander should either not appear or show no errors.
        4.  **Fallacy Analysis History:** A subheader "Fallacy Analysis History" should appear.
        5.  **Segment Verification (Each SRT entry is a segment):**
            *   **Segment 1:** Time: `00:00:01,000 - 00:00:03,500`, Speaker: `SPEAKER_SRT_1`, Text: "Hello, this is the first line."
            *   **Segment 2:** Time: `00:00:04,000 - 00:00:06,000`, Speaker: `SPEAKER_SRT_2`, Text: "I am still speaking, and this should be grouped."
            *   **Segment 3:** Time: `00:00:07,100 - 00:00:09,800`, Speaker: `SPEAKER_SRT_3`, Text: "Now it's my turn to say something interesting."
            *   **Segment 4:** Time: `00:00:10,000 - 00:00:12,500`, Speaker: `SPEAKER_SRT_4`, Text: "This is my second sentence, also to be grouped with my first."
            *   **Segment 5:** Time: `00:00:13,000 - 00:00:15,000`, Speaker: `SPEAKER_SRT_5`, Text: "I'm back with a final comment. This is a new block for SPEAKER_00."
            *   **Segment 6:** Time: `00:00:15,500 - 00:00:18,000`, Speaker: `SPEAKER_SRT_6`, Text: "If we allow students to use tablets in class, they'll soon forget how to write by hand." (Potential fallacy)
            *   **Segment 7:** Time: `00:00:18,500 - 00:00:21,000`, Speaker: `SPEAKER_SRT_7`, Text: "Then literacy rates will plummet and society will collapse. This is a slippery slope." (Potential fallacy)
            *   **Segment 8:** Time: `00:00:25,000 - 00:00:27,000`, Speaker: `SPEAKER_SRT_8`, Text: "One more from me."
            *   **Segment 9:** Time: `00:00:28,000 - 00:00:30,000`, Speaker: `SPEAKER_SRT_9`, Text: "And one more from SPEAKER_01."
        6.  **API Call & Response:** For each segment, check if a fallacy type (or "No fallacy detected") and rationale (if applicable) are displayed.
        7.  Processing time per segment should be displayed.
        8.  A success message "Analysis complete for X segment(s)!" should appear.
        9.  "Jump to video at HH:MM:SS,mmm" buttons should be visible for each segment.

### 2. Video Seeking Functionality Tests
    *   **Prerequisites:** Successfully complete step "III.1. Successful Upload and Analysis Path with `test_transcript.srt`". The video player and "Fallacy Analysis History" should be visible.
    *   **Test Case 2.1: Basic Seek**
        *   **Action:** Identify Segment 3 (starts at `00:00:07,100`). Click its "Jump to video at 00:00:07,100" button.
        *   **Expected:** The video player should jump to approximately 7 seconds and may start playing automatically (behavior can vary by browser/Streamlit version). Verify the video's current time is at or very near 7 seconds.
        *   **Action:** Identify Segment 7 (starts at `00:00:18,500`). Click its "Jump to video at 00:00:18,500" button.
        *   **Expected:** The video player should jump to approximately 18-19 seconds. Verify the video's current time.
    *   **Test Case 2.2: Seek Accuracy**
        *   **Action:** For each seek performed in Test Case 2.1, observe the video player's timeline.
        *   **Expected:** The video should start playing from a point that is reasonably close to the requested timestamp (e.g., within +/- 1 second is often acceptable). Note any significant deviations.
    *   **Test Case 2.3: Multiple Consecutive Seeks**
        *   **Action:** Click the "Jump" button for Segment 5 (`00:00:13,000`). Let the video play for a second or two.
        *   **Expected:** Video jumps to ~13s.
        *   **Action:** Immediately click the "Jump" button for Segment 2 (`00:00:04,000`).
        *   **Expected:** Video jumps back to ~4s.
        *   **Action:** Immediately click the "Jump" button for Segment 8 (`00:00:25,000`).
        *   **Expected:** Video jumps forward to ~25s.
    *   **Test Case 2.4: Seek then Play/Pause**
        *   **Action:** Click the "Jump" button for Segment 4 (`00:00:10,000`).
        *   **Expected:** Video jumps to ~10s.
        *   **Action:** Manually pause the video using the video player's controls.
        *   **Action:** Click the "Jump" button for Segment 6 (`00:00:15,500`).
        *   **Expected:** Video jumps to ~15-16s. The video might remain paused or start playing depending on the player's behavior after a programmatic seek. The key is that the seek operation itself was successful.
        *   **Action:** Manually play the video. Then click the "Jump" button for Segment 1 (`00:00:01,000`).
        *   **Expected:** Video jumps to ~1s.
    *   **Test Case 2.5: Seek to Zero (or near zero)**
        *   **Action:** Click the "Jump" button for Segment 1 (`00:00:01,000`).
        *   **Expected:** Video jumps to ~1s. If the first segment started at `00:00:00,000`, test that too.
    *   **Test Case 2.6: Page Interaction and State Preservation**
        *   **Action:** Perform a seek (e.g., to Segment 4, ~10s).
        *   **Action:** Interact with another part of the page if possible (though in this app, most interactions outside the history list might not be available or might trigger a new analysis).
        *   **Expected:** The video should remain at the seeked position (~10s) until another "Jump" button is pressed or the "Analyze Input" button is pressed again (which would reset `video_seek_time` to 0 before analysis if files are re-selected, or re-display with current seek time if files are not changed).
        *   **Action:** If you press "Analyze Input" again *without changing the uploaded files*, observe the video start time.
        *   **Expected:** The video should start from the last seeked position because `st.session_state.video_seek_time` is preserved across reruns triggered by the same "Analyze Input" button press, as long as the files themselves aren't re-uploaded (which would trigger a fresh analysis path where `video_seek_time` is effectively reset for display purposes *before* the history is shown again). *Correction*: The video will actually start from `st.session_state.video_seek_time` which persists. If "Analyze Input" is pressed, the video is redisplayed with this current `video_seek_time`.

## IV. Error Handling and Edge Cases
(This section remains largely the same, focusing on file uploads and transcript content issues.)

1.  **File Upload Errors:** (Same as before)
2.  **Transcript Content Errors (SRT Specific):** (Same as before)

## V. Fallback Single Sentence Analysis
    (This section remains largely the same)

## VI. General UI/UX
(Same as before)

This list should provide a good basis for thoroughly testing the application with SRT files.
