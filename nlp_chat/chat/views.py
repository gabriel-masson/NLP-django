from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from chat.nlp import Chat

# Initialize the chat model once when the module loads
chat_instance = Chat()

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """
    API endpoint to handle chat messages.
    Expects a JSON payload with a 'message' field.
    """
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'status': 'error',
                'message': 'Message cannot be empty'
            }, status=400)
        
        # Get response from the chat model
        bot_response = chat_instance.answer(user_message)
        
        return JsonResponse({
            'status': 'success',
            'message': bot_response
        })
        
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
