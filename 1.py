from PIL import Image
import pytesseract
import pyttsx3

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Open the image and extract text using Tesseract OCR
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def separate_articles(text):
    # Split text into articles using double newlines
    articles = text.split("\n\n")
    # Filter out empty articles
    articles = [article.strip() for article in articles if article.strip()]
    return articles

def read_aloud(text):
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
    # Read the text aloud
    engine.say(text)
    engine.runAndWait()

def add_military_flair(article):
    # Add military-style intro and outro
    intro = "Incoming transmission! Stand by for news update!"
    outro = "Message complete. Over and out."
    return f"{intro}\n\n{article}\n\n{outro}"

def process_newspaper(image_path):
    # Extract text from the image
    text = extract_text_from_image(image_path)
    # Separate the text into articles
    articles = separate_articles(text)
    # Read each article aloud with military flair
    for article in articles:
        article_with_flair = add_military_flair(article)
        print(article_with_flair)  # Print the article for debugging
        read_aloud(article_with_flair)

# Example usage
if __name__ == "__main__":
    image_path = r"D:\UNSTOP\Hackathon\Delta Headlines\0fd2c2fe-925b-4b05-bef1-693a6021b016.jpg"# Use raw string for Windows paths
    process_newspaper(image_path)
