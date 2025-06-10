import json
from joblib import load


class Chat_model:
    def __init__(self, path_modelo, path_intents):
        # Carrega modelo base
        self.model = load(path_modelo)

        # Carrega os dados de intents
        with open(path_intents, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Extrai os componentes do modelo
        self.spacy = self.model.get('spacyPT')
        self.stemmer = self.model.get('stemmer')
        self.vectorizer = self.model.get('vectorizer')
        self.classifier = self.model.get('model')

        # Verificação opcional de integridade dos componentes
        if not all([self.spacy, self.stemmer, self.vectorizer, self.classifier]):
            raise ValueError(
                "Componentes essenciais do modelo não foram carregados corretamente.")

    def preprocess_text(self, text):
        doc = self.spacy(text)
        tokens = [
            token.text for token in doc if not token.is_stop and not token.is_punct]
        stemmed = [self.stemmer.stem(token) for token in tokens]
        return " ".join(stemmed)
