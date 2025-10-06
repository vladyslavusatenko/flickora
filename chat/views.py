from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import ChatConversation, ChatMessage
from services.chat_service import ChatService
from django.views.decorators.csrf import csrf_exempt 

@csrf_exempt
@require_POST
def chat_message(request):
    data = json.loads(request.body)
    message = data.get('message')
    movie_id = data.get('movie_id')
    
    conversation = ChatConversation.objects.create(
        conversation_type='movie' if movie_id else 'global',
        movie_id=movie_id
    )
    
    ChatMessage.objects.create(
        conversation=conversation,
        role='user',
        content=message
    )
    
    chat_service = ChatService()
    result = chat_service.chat(message, movie_id)
    
    ChatMessage.objects.create(
        conversation=conversation,
        role='assistant',
        content=result['message']
    )
    
    return JsonResponse({
        'message': result['message'],
        'sources': result['sources']
    })
