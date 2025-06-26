# NLP Chat Application

A sophisticated chat application with natural language processing capabilities, featuring text and voice input with optional audio responses.

## Features

- **Natural Language Processing**: Built with NLTK and spaCy for advanced text processing
- **Voice Recognition**: Speech-to-text functionality for hands-free interaction
- **Audio Responses**: Option to receive responses as spoken audio
- **Modern Web Interface**: Responsive design with a clean, user-friendly interface
- **Django Backend**: Robust server-side processing with Django
- **Machine Learning**: Utilizes scikit-learn and transformers for intelligent responses

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nlp_chat_front
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required NLTK data and spaCy model:
   ```bash
   python -m nltk.downloader punkt
   python -m spacy download pt_core_news_sm
   ```

## Running the Application

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure

```
nlp_chat_front/
├── nlp_chat/             # Django project configuration
├── myapp/                # Main application
│   ├── static/           # Static files (JS, CSS, images)
│   ├── templates/        # HTML templates
│   ├── models.py         # Database models
│   ├── views.py          # Request handlers
│   └── ...
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## Dependencies

- Django 4.2.7
- NLTK
- spaCy
- scikit-learn
- PyAudio
- SpeechRecognition
- Transformers
- PyTorch

## Usage

1. Type your message in the text input or click the microphone button to use voice input
2. Toggle the speaker button to enable/disable audio responses
3. Press Enter or click the send button to submit your message
4. The chatbot will process your input and respond accordingly

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Django and modern web technologies
- Utilizes various NLP and machine learning libraries

