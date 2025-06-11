import time
import pytesseract
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import pyperclip  

# Ensure Tesseract is properly configured
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Adjust for your system path

SCREENSHOT_FOLDER = os.path.expanduser("/Users/syed/Desktop")  # Adjust if needed

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Event detected: {event.src_path}")  # Debug print to see if event is triggered
        if event.is_directory:
            return
        if event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"New image detected: {event.src_path}")
            time.sleep(1)  # Wait a moment for the file to be saved completely
            self.process_image(event.src_path)

    def process_image(self, image_path):
        try:
            # Check if the file exists before processing
            if not os.path.isfile(image_path):
                print(f"Invalid file path: {image_path}")
                return

            # Open the image
            img = Image.open(image_path)

            # Convert the image to grayscale (improves OCR accuracy)
            img = img.convert('L')

            # Run OCR to extract text
            custom_config = r'--oem 3 --psm 6'  # Customize Tesseract's behavior
            text = pytesseract.image_to_string(img, config=custom_config)

            # Check if text was extracted
            if text.strip():
                print(f"Extracted text:\n{text}")
                # Automatically copy the extracted text to the clipboard
                pyperclip.copy(text)
                print("\n--- Text copied to clipboard! ---")
            else:
                print("No text found in image.")

        except Exception as e:
            print(f"Error processing image: {e}")

if __name__ == "__main__":
    print(f"Monitoring folder: {SCREENSHOT_FOLDER}")
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, SCREENSHOT_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
