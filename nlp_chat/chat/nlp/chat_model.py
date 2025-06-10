import json
from pathlib import Path
from joblib import load

class ChatModel:
    """
    A class to handle the chat model and its predictions.
    """
    def __init__(self, path_modelo, path_intents):
        """
        Initialize the chat model with the given model and intents files.
        
        Args:
            path_modelo (str): Path to the trained model file (.joblib)
            path_intents (str): Path to the intents JSON file
        """
        # Convert to Path objects for better path handling
        self.model_path = Path(path_modelo)
        self.intents_path = Path(path_intents)
        
        # Validate paths
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.intents_path.exists():
            raise FileNotFoundError(f"Intents file not found: {self.intents_path}")
        
        # Load the model
        self.model = load(self.model_path)
        
        # Load the intents data
        with open(self.intents_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Extract model components
        self.spacy = self.model.get('spacyPT')
        self.stemmer = self.model.get('stemmer')
        self.vectorizer = self.model.get('vectorizer')
        self.classifier = self.model.get('model')
        
        # Verify all components were loaded
        if not all([self.spacy, self.stemmer, self.vectorizer, self.classifier]):
            raise ValueError(
                "Essential model components were not loaded correctly. "
                "Check the model file for completeness."
            )

    def preprocess_text(self, text):
        """
        Preprocess the input text for prediction.
        
        Args:
            text (str): The input text to preprocess
            
        Returns:
            str: The preprocessed text
        """
        doc = self.spacy(text)
        tokens = [
            token.text for token in doc 
            if not token.is_stop and not token.is_punct
        ]
        stemmed = [self.stemmer.stem(token) for token in tokens]
        return " ".join(stemmed)
