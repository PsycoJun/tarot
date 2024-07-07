import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
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



@csrf_exempt
@require_POST
def process_result(request):
    print("Received request body:", request.body)
    try:
        data = json.loads(request.body)
        print("Parsed data:", data)
        count =data.get('clickedButtons', [])
        print(count)
        count=len(count)
        
        if not isinstance(count, int) or count not in[1,2,3,4,5,6,7,8]:
            response={'error': '카드를 선택해야 합니다.'}
            return JsonResponse(response, status=400)
        
        random_numbers=[]
        for _ in range(count):
            num=random.randint(1,78)
            while num in random_numbers:
                num=random.randint(1,78)
            random_numbers.append(num)
        
        cards=[deck[random_numbers[i]] for i in range(len(random_numbers))]
        result=model.generate_content(f"""#입력문
너는 타로 점을 보는 사람이다. 어떤 사람이 선택한 타로 카드를 보고 그 타로 카드의 의미와 연관지어서 점을 보면 된다. 그 사람이 선택한 타로 카드는 [#카드]에 있다. 어떻게 대답해야 하는지는 [#출력형식]과 [#예시]를 참고한다. 
#카드
{cards}
#출력형식
-선택된 카드의 의미를 순차적으로 설명한 뒤 종합적인 해석을 설명한다. 
-사람이 사람에게 말을 하듯이 설명해야 한다. 즉 문단을 나누거나 제목을 다는 등의 행동을 해서는 안된다. 
-결과 해석 이외의 다른 말은 하지 않는다. 
-카드의 이름은 영어로 말해서는 안된다. 
-해석에서 한글과 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 만을 사용한다. 특히 마이너 아르카나의 숫자는 반드시 아라비아 숫자로만 표현한다. 
-한자, 영어, 가나 문자 등 한글 이외의 언어 문자는 사용하지 않는다. 
#예시
당신이 선택한 카드는 광대, 마술사, 검 6번 입니다. 광대는 새로운 시작, 순수함, 무모함 믿음의 도약을 의미하며 마술사는 능숙함, 의지력, 창의성, 가능성. 잠재력을 의미하죠. 검 6번은 평화, 조화 갈등 해결, 과거 극복, 용서를 의미합니다. 흥미로운 조합이에요. 광대는 새로운 시작과 무모한 도약을 상징하며, 마술사는 능숙함과 창의성으로 그 여정을 이끌어갈 것을 의미합니다. 검 6번은 갈등 해결과 용서를 통해 마음의 평화를 찾을 수 있음을 나타내요. 이 카드들은 당신이 새로운 도전을 앞에 두고 있다고 말하는군요. 당신에게는 뛰어난 능숙함과 창의성이 있으니 자신감을 가지고 앞으로 나아가야 해요. 그 여정에 있는 갈등에 얽매이지 말고 용서와 조화를 통해 마음의 평화 또한 얻을 수 있을 것입니다. """)

        response={'result': result.text}
        
        
        
        return JsonResponse(response)
    
    except json.JSONDecodeError:
        response={'error': '잘못된 Json 형식입니다. '}
        return JsonResponse(response, status=400)
    except Exception as e:
        response={'error': f'서버 오류: {str(e)}'}
        return JsonResponse(response, status=500)
        