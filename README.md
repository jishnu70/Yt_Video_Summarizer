# YouTube Video Summarizer

A web application built with Django that allows users to input a YouTube video URL, download its audio, transcribe it, and generate a summary of the transcript using the BART Large model from the Hugging Face Transformers library.

## Features

- Enter a YouTube video URL to get its transcript and summary.
- Audio is downloaded and transcribed using Whisper.
- Summary is generated using the BART model.
- Responsive design for easy access on desktop and mobile devices.

## Technologies Used

- Django: A high-level Python web framework for building web applications.
- Whisper: An automatic speech recognition (ASR) model for transcribing audio.
- BART: A transformer model for text summarization.
- PyTube & yt-dlp: Libraries for downloading YouTube videos.
- HTML/CSS/JavaScript: For frontend development and interactivity.
- Axios: For making HTTP requests from the frontend to the Django backend.

## Installation

### Prerequisites

Make sure you have Python installed on your machine. This project requires Python 3.7 or higher.

### Clone the repository

```bash
git clone https://github.com/jishnu70/Yt_Video_Summarizer.git
cd Yt_Video_Summarizer
```

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install the dependencies
```bash
pip install -r requirements.txt
```
### Run the application
```bash
python manage.py runserver
```
## Usage
- Enter the YouTube video URL in the provided input field.
- Click the "Summarize Video" button.
- Wait for the processing to complete. The transcript and summary will be displayed on the same page.
## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to create an issue or submit a pull request.
## License
This project is open-source and free to use. Feel free to use, modify, and distribute it.
## Acknowledgments
- **OpenAI**: for the development of Whisper and other models.
- **Hugging Face**: for providing the Transformers library.
- **Django**: for the web framework.
