import base64
import json
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transformers import AutoTokenizer, VitsModel
import torch
import soundfile as sf
from io import BytesIO
import os
from chat.nlp import Chat

# Initialize the chat model once when the module loads
chat_instance = Chat()

# Initialize TTS model and tokenizer
try:
    tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-por")
    tts_model = VitsModel.from_pretrained("facebook/mms-tts-por")
    TTS_AVAILABLE = True
except Exception as e:
    print(f"Failed to load TTS model: {str(e)}")
    TTS_AVAILABLE = False

def text_to_speech_pt_br(text):
    """Convert text to Portuguese speech using MMS-TTS"""
    if not TTS_AVAILABLE:
        print("TTS not available")
        return None
        
    try:
        print(f"Generating speech for text: {text}")
        
        # Tokenize and generate speech
        print("Tokenizing text...")
        inputs = tts_tokenizer(text, return_tensors="pt")
        
        print("Generating waveform...")
        with torch.no_grad():
            output = tts_model(**inputs).waveform
        
        print(f"Waveform shape: {output.shape}")
        
        # Convert to 16-bit PCM WAV format
        print("Converting to 16-bit PCM...")
        audio_int16 = (output * 32767).numpy().astype(np.int16)
        
        # Save to bytes buffer
        print("Saving to WAV buffer...")
        buffer = BytesIO()
        sf.write(buffer, audio_int16[0], 22050, format='WAV', subtype='PCM_16')
        audio_bytes = buffer.getvalue()
        
        print(f"Generated audio size: {len(audio_bytes)} bytes")
        return audio_bytes
        
    except Exception as e:
        import traceback
        print(f"Error in text-to-speech: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return None

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """
    API endpoint to handle chat messages.
    Expects a JSON payload with 'message' and 'response_type' fields.
    'response_type' can be 'text' or 'audio'.
    """
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        response_type = data.get('response_type', 'text')  # Default to text
        
        if not user_message:
            return JsonResponse({
                'status': 'error',
                'message': 'Message cannot be empty'
            }, status=400)
        
        # Get response from the chat model
        bot_response = chat_instance.answer(user_message)
        
        response_data = {
            'status': 'success',
            'message': bot_response,
            'response_type': 'text'  # Default response type
        }
        
        # If audio response is requested and TTS is available
        if response_type == 'audio' and TTS_AVAILABLE:
            audio_data = text_to_speech_pt_br(bot_response)
            if audio_data:
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                response_data.update({
                    'audio': audio_base64,
                    'response_type': 'audio'
                })
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
