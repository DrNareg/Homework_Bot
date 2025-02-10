import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google import genai
import PIL.Image

folder_path = "path/to/folder"

# Setup Gemini API
client = genai.Client(api_key="YOUR_APIKEY")

# Function to process the image and clear the folder after response
def process_screenshot(file_path):
    try:
        # Open the image
        image = PIL.Image.open(file_path)

        # Call the API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Search the screenshot for questions and the answer options. For each question, identify the correct answer and return the number of the correct option (e.g., '2' or '1'). Do not provide any explanations.", image])
            # The prompt above can and should be adjusted to fit your needs and improve responses

        # Print the response
        print(response.text)
        
        # Clear the folder after processing
        clear_folder(folder_path)
    except Exception as e:
        print(f"Error processing screenshot: {e}")

# Function to clear all files in the folder
def clear_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("Folder cleared.")

# Watchdog event handler for file creation
class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        # Process the new screenshot
        print(f"New file detected: {event.src_path}")
        process_screenshot(event.src_path)

# Watchdog observer setup
def start_watching():
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)  # Keep the observer running
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped monitoring folder.")
    observer.join()

# Start monitoring the folder
start_watching()
