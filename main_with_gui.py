import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google import genai
import PIL.Image
import tkinter as tk

# Define the folder path
folder_path = "path/to/folder"

# Define the API client
client = genai.Client(api_key="YOUR_APIKEY")

# Initialize Tkinter
root = tk.Tk()

# Set GUI location
root.geometry("500x250+1250+50")  

# Set Title
root.title("pp")

# Keep window on top so it doesn't dissapear while working
root.wm_attributes("-topmost", 1)  

# Create UI elements
label = tk.Label(root, text="poopoo", font=(14))
label.pack()

text_widget = tk.Text(root, height=11, width=55)
text_widget.pack()

# Global variable for observer
observer = None

def exit_program():
    """Stops the observer and closes the GUI."""
    if observer:
        observer.stop()
        observer.join()
    root.destroy()  # Close the Tkinter window

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

def update_gui(new_text):
    """Updates the Tkinter window with new text."""
    text_widget.delete("1.0", tk.END)  # Clear previous text
    text_widget.insert(tk.END, new_text)  # Insert new text
    root.update_idletasks()  # Update UI

# Define function to process the image and clear the folder after response
def process_screenshot(file_path):
    try:
        # Open the image
        image = PIL.Image.open(file_path)

        # Call the API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Search the screenshot for questions and the answer options. For each question, identify the correct answer and return the number of the correct option (e.g., '2' or '1'). Do not provide any explanations.", image])
            # The prompt above can and should be adjusted to fit your needs and improve responses
        
        gemini_response = response.text
        update_gui(gemini_response)  # Update GUI instead of creating a new window

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
        print(f"New file detected: {event.src_path}")
        process_screenshot(event.src_path)

# Watchdog observer setup
def start_watching():
    global observer
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    
    try:
        root.mainloop()  # Run Tkinter mainloop inside the monitoring function
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("Stopped monitoring folder.")

# Start monitoring the folder and GUI together
start_watching()
