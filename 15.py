from PIL import Image
import pytesseract
import pyttsx3
import os
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import cv2
import argparse
from tkinter import Tk, filedialog

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Download NLTK data (if not already downloaded)
def download_nltk_data():
    """Download required NLTK data for sumy and sentiment analysis."""
    try:
        # Download 'punkt' tokenizer
        nltk.download('punkt', quiet=True)
        # Download 'vader_lexicon' for sentiment analysis
        nltk.download('vader_lexicon', quiet=True)
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")

# Step 1: Extract text from the image and save it to a file
def extract_text_from_image(image_path, output_file):
    """Extract text from the image using Tesseract OCR and save it to a file."""
    try:
        # Open the image and extract text
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Save the extracted text to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

        print(f"Extracted text saved to {output_file}")
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

# Step 2: Clean the extracted text
def clean_text(text):
    """Clean the extracted text by removing special characters and extra spaces."""
    try:
        # Remove extra newlines and spaces
        text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

        # Remove special characters (keep only letters, numbers, and basic punctuation)
        text = re.sub(r'[^\w\s.,!?]', '', text)

        return text.strip()
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return ""

# Step 3: Summarize the extracted text using sumy
def summarize_text(input_file, output_file, sentences_count=3):
    """Summarize the text using the sumy library and save it to a file."""
    try:
        # Read the extracted text from the file
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()

        # Clean the text before summarization
        text = clean_text(text)

        # Skip summarization if the input text is too short or empty
        input_length = len(text.split())
        if input_length < 10:  # Skip summarization for very short texts
            print("Text is too short to summarize. Using original text as summary.")
            summary = text
        else:
            # Use sumy for summarization
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary_sentences = summarizer(parser.document, sentences_count)
            summary = " ".join(str(sentence) for sentence in summary_sentences)

        # Save the summarized text to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(summary)

        print(f"Summarized text saved to {output_file}")
        return summary
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return ""

# Step 4: Extract keywords from the summarized text
def extract_keywords(text, top_n=5):
    """Extract top keywords from the text using CountVectorizer."""
    try:
        vectorizer = CountVectorizer(stop_words='english')
        word_count_matrix = vectorizer.fit_transform([text])
        word_counts = word_count_matrix.sum(axis=0)
        word_frequencies = [(word, word_counts[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
        sorted_word_frequencies = sorted(word_frequencies, key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_word_frequencies[:top_n]]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# Step 5: Analyze sentiment of the summarized text
def analyze_sentiment(text):
    """Analyze the sentiment of the text using NLTK's SentimentIntensityAnalyzer."""
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(text)
        return sentiment_score
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {}

# Step 6: Add military-style intro and outro to the summarized text
def add_military_flair(text):
    """Add military-style intro and outro to the text."""
    intro = "Incoming transmission! Stand by for news update!"
    outro = "Message complete. Over and out."
    return f"{intro}\n\n{text}\n\n{outro}"

# Step 7: Read aloud the summarized text and save it as an audio file
def read_aloud(text, output_audio_file):
    """Read the text aloud using pyttsx3 and save it as an audio file."""
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        # Set speech rate (words per minute)
        engine.setProperty('rate', 150)
        # Set a military-style voice (if available)
        voices = engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower():  # Choose an English voice
                engine.setProperty('voice', voice.id)
                break
        # Save speech to an audio file
        engine.save_to_file(text, output_audio_file)
        engine.runAndWait()

        print(f"Audio saved to {output_audio_file}")
    except Exception as e:
        print(f"Error reading text aloud: {e}")

# Function to select an image file
def select_image():
    """Open a file dialog to select an image file."""
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    return file_path

# Main function to process the newspaper
def process_newspaper(image_path):
    """Process the newspaper image: extract text, summarize, and read aloud."""
    try:
        # Step 1: Extract text from the image and save it to a file
        extracted_text_file = "extracted_text.txt"
        extracted_text = extract_text_from_image(image_path, extracted_text_file)

        if not extracted_text:
            print("No text extracted from the image. Exiting.")
            return

        # Step 2: Summarize the extracted text and save it to a file
        summarized_text_file = "summarized_text.txt"
        summary = summarize_text(extracted_text_file, summarized_text_file)

        if not summary:
            print("Summarization failed. Exiting.")
            return

        # Step 3: Extract keywords from the summarized text
        keywords = extract_keywords(summary)
        print(f"Top Keywords: {keywords}")

        # Step 4: Analyze sentiment of the summarized text
        sentiment_score = analyze_sentiment(summary)
        print(f"Sentiment Analysis: {sentiment_score}")

        # Step 5: Add military flair to the summarized text
        final_text = add_military_flair(summary)

        # Step 6: Save the final output to a file
        final_output_file = "final_output.txt"
        with open(final_output_file, "w", encoding="utf-8") as file:
            file.write(final_text)

        print(f"Final output saved to {final_output_file}")

        # Step 7: Read aloud the summarized text and save it as an audio file
        output_audio_file = "output_audio.mp3"
        read_aloud(final_text, output_audio_file)

    except Exception as e:
        print(f"Error processing newspaper: {e}")

# Download NLTK data before running the pipeline
download_nltk_data()

# Command-line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a newspaper image and generate a summary.")
    parser.add_argument("image_path", help="Path to the input image file", nargs="?", default=None)
    args = parser.parse_args()

    if args.image_path:
        # Process the newspaper using the provided image path
        process_newspaper(args.image_path)
    else:
        # Ask the user to select an image file
        image_path = select_image()
        if not image_path:
            print("No image selected. Exiting.")
        else:
            print(f"Selected image: {image_path}")
            # Process the newspaper
            process_newspaper(image_path)
