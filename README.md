# Screenshot Processing with Gemini API

## Overview
This project monitors a folder for new screenshots and processes them using the **Google Gemini API** to extract and identify correct answers from multiple-choice questions in the images. There are two implementations:

1. **main.py** - A command-line version that prints results to the console.
2. **mainwithgui.py** - A GUI-based version using Tkinter to display results in a text window.

## Features
- Uses **Watchdog** to monitor a specified folder for new images.
- Processes the image using **Google Gemini API**.
- Extracts correct answer choices from multiple-choice questions.
- Deletes images after processing.
- GUI version displays results dynamically in a Tkinter window.

## Requirements
Make sure you have the following packages installed:
```bash
pip install watchdog google-generativeai pillow tkinter
```

## Usage
### 1. Configure the Folder Path
Edit both `main.py` and `mainwithgui.py` to set the folder to be monitored:
```python
folder_path = "path/to/folder"  # Change this to your actual folder path
```

### 2. Set Up Your API Key
Replace `YOUR_APIKEY` with your actual **Google Gemini API key** in both files:
```python
client = genai.Client(api_key="YOUR_APIKEY")
```

### 3. Running the Program
#### Command-Line Version:
Run `main.py` for console-based output:
```bash
python main.py
```

#### GUI Version:
Run `mainwithgui.py` to launch the Tkinter window:
```bash
python mainwithgui.py
```

### 4. Exiting the Program
- **For `main.py`**, press `CTRL+C` to stop monitoring.
- **For `mainwithgui.py`**, click the **Exit** button in the GUI.

## Notes
- The prompt for the Gemini API can be modified to improve response accuracy.
- The folder is automatically cleared after processing each image.
- The GUI version ensures the window stays on top for visibility.