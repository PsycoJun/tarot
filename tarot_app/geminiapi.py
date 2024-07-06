import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import json
import random

API_KEY='AIzaSyBpTCz6Pj-M7walatYvGZLoYrwvy67QlNk'

genai.configure(api_key=API_KEY)#Gemini API 키 설정
model=genai.GenerativeModel('gemini-pro')

deck = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement",
    "The World", "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands",
    "Five of Wands", "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands",
    "Ten of Wands", "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords",
    "Five of Swords", "Six of Swords", "Seven of Swords", "Eight of Swords",
    "Nine of Swords", "Ten of Swords", "Page of Swords", "Knight of Swords",
    "Queen of Swords", "King of Swords", "Ace of Pentacles", "Two of Pentacles",
    "Three of Pentacles", "Four of Pentacles", "Five of Pentacles", "Six of Pentacles",
    "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]



@csrf_protect
@require_POST
def process_result(request):
    try:
        data = json.loads(request.body)
        count =data.get('count')
        
        if not isinstance(count, int) or count not in[1,2,3,4,5,6,7,8]:
            return JsonResponse({'error': '카드를 선택해야 합니다.'}, status=400)
        
        random_numbers=[]
        for _ in range(count):
            num=random.randint(1,78)
            while num in random_numbers:
                num=random.randint(1,78)
            random_numbers.append(num)
        
        cards=[deck[random_numbers[i]] for i in range(len(random_numbers))]
        result=model.generate_content(f"")
        
        response={'result': result}
        
        return JsonResponse
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 Json 형식입니다. '}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'서버 오류: {str(e)}'},status=500)
        