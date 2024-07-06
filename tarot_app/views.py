import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# views.py
from django.http import JsonResponse

def process(request):
    try:
        if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            data = json.loads(request.body)
            clickedButtons = set(data.get('clickedButtons', []))

            # 받아온 데이터 처리 로직
            print(clickedButtons)  # 콘솔에 출력해보기
            # 데이터 처리 로직
            return JsonResponse({'message': '데이터 처리 성공'})
        else:
            return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def index(request):
    button_range = range(1, 9)
    return render(request, 'tarot_app/index.html', {'button_range': button_range})

@csrf_exempt
def send_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        count = data.get('count', 0)
        
        # 타로 카드를 뽑기 위한 Open API 호출 로직
        tarot_cards = []
        for _ in range(count):
            response = requests.get('https://example.com/tarot-api')  # 타로 카드 API URL로 변경
            if response.status_code == 200:
                tarot_cards.append(response.json())

        return JsonResponse({'tarot_cards': tarot_cards})

    return JsonResponse({'error': 'Invalid request'}, status=400)
