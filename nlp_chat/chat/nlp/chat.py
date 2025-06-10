import json
from pathlib import Path
from joblib import dump, load
from .chat_model import ChatModel
import random

class Chat:
    """
    Main chat class that handles the conversation flow using different domain models.
    """
    
    def __init__(self, base_dir=None):
        """
        Initialize the chat system with all required models.
        
        Args:
            base_dir (str, optional): Base directory for model and data files.
                                   If None, uses the default location in the package.
        """
        if base_dir is None:
            # Get the directory where this file is located
            base_dir = Path(__file__).parent
            
        self.base_dir = Path(base_dir)
        self.models_dir = self.base_dir / 'models'
        self.data_dir = self.base_dir / 'data'
        
        # Define model tags
        self.tags = ['arbovirose', 'chikungunya', 'dengue', 'zika']
        
        # Initialize all models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all the domain-specific models."""
        # Main domain model
        self.model = self._load_model(
            self.models_dir / 'modelo_dominio.joblib',
            self.data_dir / 'intents.json'
        )
        
        # Disease-specific models
        self.model_zika = self._load_model(
            self.models_dir / 'modelo_zika.joblib',
            self.data_dir / 'intents_zika.json'
        )
        
        self.model_dengue = self._load_model(
            self.models_dir / 'modelo_dengue.joblib',
            self.data_dir / 'intents_dengue.json'
        )
        
        self.model_chikungunya = self._load_model(
            self.models_dir / 'modelo_chika.joblib',
            self.data_dir / 'intents_chikungunya.json'
        )
        
        self.model_arbovirose = self._load_model(
            self.models_dir / 'modelo_arboviroses.joblib',
            self.data_dir / 'intents_arboviroses.json'
        )
    
    def _load_model(self, model_path, intents_path):
        """Helper method to load a model with error handling."""
        try:
            return ChatModel(model_path, intents_path)
        except Exception as e:
            print(f"Error loading model from {model_path}: {str(e)}")
            raise
    
    def answer(self, ask):
        """
        Generate a response to the user's input.
        
        Args:
            ask (str): The user's input text
            
        Returns:
            str: The generated response
        """
        try:
            if not ask or not ask.strip():
                return "Por favor, faça uma pergunta sobre zika, dengue, chikungunya ou arboviroses."
                
            # Preprocess the input
            text = self.model.preprocess_text(ask)
            
            # Get prediction from the main domain model
            vec = self.model.vectorizer.transform([text])
            tag_predict = self.model.classifier.predict(vec)[0]
            confidence = self.model.classifier.predict_proba(vec).max()
            
            print(f'Tag predicted: {tag_predict}')
            print(f'Confidence: {confidence}')
            
            # Map of tags to their corresponding models
            model_map = {
                'zika': self.model_zika,
                'dengue': self.model_dengue,
                'chikungunya': self.model_chikungunya,
                'arboviroses': self.model_arbovirose
            }
            
            if tag_predict in model_map:
                model = model_map[tag_predict]
                print(f"Usando modelo específico para {tag_predict.capitalize()}")
                
                # Preprocess and predict using the specific model
                text = model.preprocess_text(ask)
                vec = model.vectorizer.transform([text])
                tag_predict = model.classifier.predict(vec)[0]
                confidence = model.classifier.predict_proba(vec).max()
                
                print(f'Tag model predicted: {tag_predict}')
                print(f'Confidence model: {confidence}')
                
                # Find and return a random response for the predicted tag
                if hasattr(model, 'data') and 'intents' in model.data:
                    for intent in model.data['intents']:
                        if intent.get('tag') == tag_predict and 'responses' in intent:
                            return random.choice(intent['responses'])
                
                # If we get here, the tag wasn't found in the intents
                return f"Desculpe, não encontrei informações específicas sobre '{tag_predict}'. Posso ajudar com outras dúvidas?"
                
            return "Desculpe, não reconheci o tópico da sua pergunta. Poderia reformular?"
            
        except Exception as e:
            print(f"Error in answer method: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente."
        
        # Default response if no matching tag is found
        return "Desculpe, não entendi sua pergunta. Poderia reformular?"

# Example usage
if __name__ == "__main__":
    chat = Chat()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        response = chat.answer(user_input)
        print(f"Bot: {response}")
