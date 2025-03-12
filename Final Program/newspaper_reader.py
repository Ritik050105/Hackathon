import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import pytesseract
import pyttsx3
from playsound import playsound
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Military-style sound effects
INTRO_SOUND = "intro.mp3"  # Add a sound file for intro
OUTRO_SOUND = "outro.mp3"  # Add a sound file for outro

class NewspaperReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Newspaper Reader")
        self.root.geometry("800x600")

        # UI Elements
        self.label = tk.Label(root, text="Upload a Newspaper Image", font=("Arial", 16))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=10)

        self.read_button = tk.Button(root, text="Read Aloud", command=self.read_aloud)
        self.read_button.pack(pady=10)

    def upload_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            try:
                # Extract text from the image
                text = self.extract_text_from_image(file_path)
                # Display the extracted text
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {e}")

    def extract_text_from_image(self, image_path):
        # Open the image and extract text using Tesseract OCR
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def read_aloud(self):
        # Get the text from the text area
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            try:
                # Add military flair
                article_with_flair = self.add_military_flair(text)
                # Play intro sound
                if os.path.exists(INTRO_SOUND):
                    playsound(INTRO_SOUND)
                # Read the text aloud
                engine.say(article_with_flair)
                engine.runAndWait()
                # Play outro sound
                if os.path.exists(OUTRO_SOUND):
                    playsound(OUTRO_SOUND)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read aloud: {e}")
        else:
            messagebox.showwarning("Warning", "No text to read!")

    def add_military_flair(self, article):
        # Add military-style intro and outro
        intro = "Incoming transmission! Stand by for news update!"
        outro = "Message complete. Over and out."
        return f"{intro}\n\n{article}\n\n{outro}"

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NewspaperReaderApp(root)
    root.mainloop()
