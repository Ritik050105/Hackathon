# Automated Newspaper Summarization and Analysis

## Overview
This project automates the process of extracting, summarizing, and analyzing newspaper content using OCR, NLP, and text-to-speech technologies.

## Features
1. **Text Extraction**: Extracts text from newspaper images using Tesseract OCR.
2. **Text Cleaning**: Removes unnecessary characters and spaces.
3. **Summarization**: Summarizes the extracted text using the Sumy library.
4. **Sentiment Analysis**: Analyzes the sentiment of the summarized text using NLTK's SentimentIntensityAnalyzer.
5. **Keyword Extraction**: Extracts top keywords using CountVectorizer.
6. **Military Flair**: Adds a military-style intro and outro to the summarized text.
7. **Text-to-Speech**: Converts the final text into an audio file using pyttsx3.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/newspaper-summarization.git

Install the required dependencies:
bash
pip install -r requirements.txt
Usage
Place your newspaper image in the project directory.

Run the script:
bash
python main.py
The output files (extracted_text.txt, summarized_text.txt, final_output.txt, and output_audio.mp3) will be generated in the project directory.

Future Plans
Improve OCR accuracy using advanced preprocessing techniques.

Add support for multiple languages.

Develop a user-friendly web interface.

Integrate with news APIs for real-time updates.

Add visualizations for sentiment and keyword analysis.

License
This project is licensed under the MIT License. See the LICENSE file for details.
---

Let me know if you need further assistance!
