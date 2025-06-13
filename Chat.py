from joblib import dump, load
import json
import random
import speech_recognition as sr
from pathlib import Path
from Chat_model import Chat_model
import time
import speech_recognition as sr


# Caminho absoluto da pasta onde está o script atual (em src/)
src_dir = Path(__file__).resolve().parent
print(src_dir)
# Caminho para script.py um nível acima
path_modelo_dominio = src_dir.parent / 'modelo_dominio.joblib'
path_modelo_arbovirose = src_dir.parent / 'modelo_arboviroses.joblib'
path_modelo_chikungunya = src_dir.parent / 'modelo_chika.joblib'
path_modelo_dengue = src_dir.parent / 'modelo_dengue.joblib'
path_modelo_zika = src_dir.parent / 'modelo_zika.joblib'

path_intents = src_dir.parent / 'intents.json'
path_intents_zika = src_dir.parent / 'intents_zika.json'
path_intents_dengue = src_dir.parent / 'intents_dengue.json'
path_intents_chikungunya = src_dir.parent / 'intents_chikungunya.json'
path_intents_arboviroses = src_dir.parent / 'intents_arboviroses.json'


class Chat:
    def __init__(self):
        self.tags = ['arbovirose', 'chikungunya', 'dengue', 'zika']

        self.model = Chat_model(
            path_modelo_dominio, path_intents)

        self.model_zika = Chat_model(
            path_modelo_zika, path_intents_zika)

        self.model_dengue = Chat_model(
            path_modelo_dengue, path_intents_dengue)

        self.model_chikungunya = Chat_model(
            path_modelo_chikungunya, path_intents_chikungunya)

        self.model_arbovirose = Chat_model(
            path_modelo_arbovirose, path_intents_arboviroses)

    def get_audio(self, timeout=5, phrase_time_limit=10):
        """
        Captures audio from the microphone and converts it to text using speech recognition.
        
        Args:
            timeout (int): Maximum time in seconds to wait for speech input
            phrase_time_limit (int): Maximum time in seconds for a single phrase
            
        Returns:
            str: Recognized text or None if recognition fails
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Ajustando o ruído ambiente...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("Pode falar! Estou ouvindo...")
                audio = recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processando áudio...")
                # Recognize speech using Google's speech recognition
                text = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Nenhum áudio detectado.")
            return None
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio")
            return None
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de fala: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None


# generate a response based on the user's input
    def answer(self, ask):
        text = self.model.preprocess_text(ask)
        vec = self.model.vectorizer.transform([text])
        tag_predict = self.model.classifier.predict(vec)[0]

        print(f'Tag predicted: {tag_predict}')
        print(f'confiança: {self.model.classifier.predict_proba(vec)}')

        if tag_predict == 'zika':
            print("Usando modelo específico para Zika")
            text = self.model_zika.preprocess_text(ask)
            vec = self.model_zika.vectorizer.transform([text])
            tag_predict = self.model_zika.classifier.predict(vec)[0]
            print(f'Tag predicted: {tag_predict}')
            print(
                f'confiança: {self.model_zika.classifier.predict_proba(vec)}')
            for intent in self.model_zika.data['intents']:
                if intent['tag'] == tag_predict:
                    return random.choice(intent['responses'])
        elif tag_predict == 'dengue':
            print("Usando modelo específico para Dengue")
            text = self.model_dengue.preprocess_text(ask)
            vec = self.model_dengue.vectorizer.transform([text])
            tag_predict = self.model_dengue.classifier.predict(vec)[0]
            print(f'Tag predicted: {tag_predict}')
            print(
                f'confiança: {self.model_dengue.classifier.predict_proba(vec)}')
            for intent in self.model_dengue.data['intents']:
                if intent['tag'] == tag_predict:
                    return random.choice(intent['responses'])
        elif tag_predict == 'chikungunya':
            print("Usando modelo específico para Chikungunya")
            text = self.model_chikungunya.preprocess_text(ask)
            vec = self.model_chikungunya.vectorizer.transform([text])
            tag_predict = self.model_chikungunya.classifier.predict(vec)[0]
            print(f'Tag predicted: {tag_predict}')
            print(
                f'confiança: {self.model_chikungunya.classifier.predict_proba(vec)}')
            for intent in self.model_chikungunya.data['intents']:
                if intent['tag'] == tag_predict:
                    return random.choice(intent['responses'])
        elif tag_predict == 'arboviroses':
            print("Usando modelo específico para Arbovirose")
            text = self.model_arbovirose.preprocess_text(ask)
            vec = self.model_arbovirose.vectorizer.transform([text])
            tag_predict = self.model_arbovirose.classifier.predict(vec)[0]
            print(f'Tag predicted: {tag_predict}')
            print(
                f'confiança: {self.model_arbovirose.classifier.predict_proba(vec)}')
            for intent in self.model_arbovirose.data['intents']:
                if intent['tag'] == tag_predict:
                    return random.choice(intent['responses'])
        else:
            return "Desculpe, não entendi sua pergunta. Poderia reformular?"
