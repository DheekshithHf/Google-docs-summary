import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from .slack import verify_slack_request, send_slack_response
from .ai_summary import generate_summary
from .gdrive_utils import GoogleDriveDownloader
import json
import logging



@csrf_exempt
def slack_events(request):
    try:
        content_type = request.META.get('CONTENT_TYPE', '')
        if 'application/x-www-form-urlencoded' in content_type:
            if 'payload' in request.POST:
                print('Interactive component payload:', request.POST['payload'])
                return JsonResponse({'ok': True})
            else:
                print('Slash command:', request.POST)
                content =handle_slash_command(request)

                return JsonResponse({'ok': True})
        elif 'application/json' in content_type:
            print('Event subscription payload:', request.body.decode())
            return JsonResponse({'ok': True})
        else:
            return HttpResponse("Unsupported content type", status=400)
    except Exception as e:
        print(f"Error in slack_event_handler: {str(e)}")
        return HttpResponse("Internal server error", status=500)



def handle_slash_command(request):
    """
    Handle Slack slash commands
    
    Args:
        request: Django HTTP request containing form data
        
    Returns:
        JsonResponse with Slack-formatted response
    """
    try:
        # Parse form data
        payload = {
            'token': request.POST.get('token'),
            'team_id': request.POST.get('team_id'),
            'team_domain': request.POST.get('team_domain'),
            'channel_id': request.POST.get('channel_id'),
            'channel_name': request.POST.get('channel_name'),
            'user_id': request.POST.get('user_id'),
            'user_name': request.POST.get('user_name'),
            'command': request.POST.get('command'),
            'text': request.POST.get('text'),
            'response_url': request.POST.get('response_url'),
            'trigger_id': request.POST.get('trigger_id'),
        }
        
        # logger.info(f"Received slash command: {payload.get('command')} from user {payload.get('user_id')}")
        command = payload.get('command', '').lower()
        text = payload.get('text', '').strip()
        user_id = payload.get('user_id')
        channel_id = payload.get('channel_id')
        print('------------------------------------')
        print(f"Received slash command: {command} with text: {text} from user: {user_id} in channel: {channel_id}")
        print('------------------------------------')
        from .ai_summary import generate_summary
        from .gdocs_utils import get_doc_content
        if command == '/summarize-doc':
            print("hello")
            content =generate_summary(text)
            
            
            return JsonResponse(content)
        
        
     
        
    except Exception as e:
        # logger.error(f"Error handling slash command: {str(e)}")
        return JsonResponse({
            "response_type": "ephemeral",
            "text": "❌ An error occurred while processing your command. Please try again later."
        })
