# Live Fallacy Checker (Qwen3 Hackathon Project - openrouter-hackathon1)

This project is a real-time logical fallacy detector built for a Qwen3 Hackathon. It uses the Qwen3 32B model hosted on Cerebras via the OpenRouter API to identify a predefined list of common logical fallacies in sentences. It includes both a command-line interface (CLI) and a web interface built with Streamlit.

## Features

- Detects 5 common logical fallacies:
    - Ad Hominem
    - Straw Man
    - Slippery Slope
    - False Dichotomy
    - Appeal to Emotion
- Provides a brief rationale for detected fallacies.
- **Command-Line Interface (`fallacy_checker.py`):**
    - Interactive mode: Allows users to type sentences and get immediate feedback.
    - Batch mode: Can process a transcript of sentences from `transcript.txt` and log results to `results.log` (requires code modification to switch from interactive to batch mode).
- **Web Interface (`webapp.py`):**
    - User-friendly interface to enter sentences and view fallacy analysis.
    - Displays fallacy type, rationale, and processing time.
- Reports processing time per sentence for performance insight.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd openrouter-hackathon1 
    ```
    (Replace `<repository_url>` with the actual URL if known, otherwise user can fill this in.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (`requirements.txt` should include `requests` and `streamlit`)

4.  **API Key:**
    The scripts (`fallacy_checker.py` and `webapp.py`) currently have the hackathon API key hardcoded: `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`. For other uses, you would replace this with your own OpenRouter API key in both files.

## Usage

### 1. Web Application (Recommended)

The web application provides the most user-friendly way to interact with the fallacy checker.

To run the web app:
1.  Ensure you are in the project's root directory and have activated your virtual environment.
2.  Run the following command:
    ```bash
    streamlit run webapp.py
    ```
3.  Open the URL provided by Streamlit (usually `http://localhost:8501`) in your web browser.
4.  Enter a sentence in the text area and click "Analyze Sentence".

### 2. Command-Line Interface (CLI)

The CLI version (`fallacy_checker.py`) provides direct console-based interaction.

**Interactive Mode (Default for CLI):**
1.  Ensure you are in the project's root directory and have activated your virtual environment.
2.  Run the script:
    ```bash
    python fallacy_checker.py
    ```
3.  You will be prompted to enter sentences one by one. Type 'quit' to exit.

**Batch Mode (Transcript Processing):**
The `fallacy_checker.py` script contains commented-out code for processing a `transcript.txt` file. To use this mode:
1.  Create a `transcript.txt` file in the root directory with one sentence per line.
2.  Open `fallacy_checker.py` and modify the `if __name__ == "__main__":` block:
    *   Comment out the `while True:` loop for interactive mode.
    *   Uncomment the section that reads from `transcript_filepath` and writes to `results_log_filepath`.
3.  Run the script:
    ```bash
    python fallacy_checker.py
    ```
    Results will be printed to the console and saved in `results.log`.

## Performance Notes

- The target latency for the original hackathon challenge was ~200ms per sentence.
- Current observed latencies when using the `qwen/qwen3-32b` model via OpenRouter average around 500-600ms. Best-case latencies (e.g., for non-fallacious sentences or simpler cases) are around 350-450ms.
- Optimization efforts included prompt engineering (significant conciseness) and API parameter tuning (`temperature: 0.1`).

## Project Structure
- `fallacy_checker.py`: Core logic for API calls, fallacy detection parsing, and CLI interaction.
- `webapp.py`: Streamlit web interface.
- `requirements.txt`: Python dependencies.
- `transcript.txt`: Example input file for batch processing (if created by user/previous steps).
- `results.log`: Example output file from batch processing (if run).
- `README.md`: This file.
