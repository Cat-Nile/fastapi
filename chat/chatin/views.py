import asyncio
import uuid
import os 

from openai import OpenAI
from dotenv import load_dotenv

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, StreamingHttpResponse

from chatin.models import Chat


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def home(request):
    return render(request, "chatin/home.html")


def advanced_home(request):
    chat_uuid = uuid.uuid4()  # 새 UUID 생성
    return render(request, "chatin/advanced.html", {'chat_uuid': chat_uuid})


def send(request):
    return HttpResponse("Hello, World!")


@csrf_exempt
@require_POST
def stream_response(request):
    async def content_generator():
        yield "콘텐츠 대기 중...\n"
        # 여기에서 지연을 시뮬레이션하거나 원하는 로직을 추가할 수 있습니다.
        # 지금은 그냥 "wait" 뒤에 메시지를 보내겠습니다.
        await asyncio.sleep(3)
        yield "채팅GPT 응답!"
        await asyncio.sleep(3)
        yield "채팅GPT 응답!"
        await asyncio.sleep(3)
        yield "채팅GPT 응답!"
        await asyncio.sleep(3)
        yield "채팅GPT 응답!"

    return StreamingHttpResponse(content_generator(), content_type='text/plain')


@csrf_exempt
@require_POST
def chatgpt_stream_response(request):
    def content_generator():
        completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 정신적으로 멍청하고 농담만 할 줄 아는 사람입니다... 누가 무슨 말을 하든 농담으로 받아들이고 또 다른 농담으로 대응합니다."},
            {"role": "user", "content": request.POST.get("message")}
        ],
        stream=True
        )
        for chunk in completion:
            
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                yield (str(delta_content))
    return StreamingHttpResponse(content_generator(), content_type='text/plain')


@csrf_exempt
@require_POST
def advanced_chatgpt_stream_response(request):
    def content_generator():
        chat_uuid = request.POST.get("chat_uuid")
        if chat_uuid is None:
            chat_uuid = uuid.uuid4()
        
        chat_history = []
        try:
            chat_obj = Chat.objects.get(uuid=chat_uuid)
            chat_history = chat_obj.conversation
        except Chat.DoesNotExist:
            chat_obj = None

        if not chat_history:
            chat_history = [{"role": "system", "content": "당신은 매우 똑똑한 비서이며 사람들을 돕는 것을 좋아합니다."}]
        chat_history.append({"role": "user", "content": request.POST.get("message")})

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=chat_history,
            stream=True
        )

        new_message = ''
        for chunk in completion:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                new_message += str(delta_content)
                yield (str(delta_content))

        chat_history.append({"role": "assistant", "content": new_message})

        if chat_obj:
            chat_obj.conversation = chat_history
            chat_obj.save(update_fields=["conversation"])
        else:
            Chat.objects.create(uuid=chat_uuid, conversation=chat_history)

    return StreamingHttpResponse(content_generator(), content_type='text/plain')
