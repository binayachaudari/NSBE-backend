from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from easy_lease.services.chat_service import App, Chatbot, Documents
from easy_lease.utils.sources import sources
import json

@csrf_exempt
def handle_request(request): 
    """
    Controller for chatbot application.
    """
    # Get the chatbot response
    if request.method == 'POST': 
      body = json.loads(request.body)
      quesn = body.get("message")
      docs = Documents(sources)
      chatbot_obj = Chatbot(docs)
      response = App(chatbot_obj).run(quesn)
      res_obj = {
        'text': response.text, 
        'generation_id': response.generation_id, 
        'citations': response.citations,
        'documents': response.documents,
        'is_search_required': response.is_search_required, 
        'search_results': response.search_results,
        'finish_reason': response.finish_reason,
        'chat_history': response.chat_history,
        'message':response.message, 
        'response_id':response.response_id,
        'token_count':response.token_count,
        'conversation_id':response.conversation_id, 
      }
      return JsonResponse(res_obj, safe=False)
    else: 
      return JsonResponse({"error": "Invalid request."})
