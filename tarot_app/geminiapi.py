import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import random
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")

genai.configure(api_key=API_KEY)#Gemini API 키 설정
model=genai.GenerativeModel('gemini-pro')

# deck = [
#     "바보", "마술사", "여사제", "여황제", "황제",
#     "교황", "연인", "전차", "힘", "은둔자",
#     "운명의 수레바퀴", "정의", "매달린 사람", "죽음", "절제",
#     "악마", "탑", "별", "달", "태양", "심판",
#     "세계", "완드 에이스", "완드 2번", "완드 3번", "완드 4번",
#     "완드 5번", "완드 6번", "완드 7번", "완드 8번", "완드 9번",
#     "완드 10번", "완드 시종", "완드 기사", "완드 여왕", "완드 왕",
#     "컵 에이스", "컵 2번", "컵 3번", "컵 4번", "컵 5번",
#     "컵 6번", "컵 7번", "컵 8번", "컵 9번", "컵 10번",
#     "컵 시종", "컵 기사", "컵 여왕", "컵 왕",
#     "검 에이스", "검 2번", "검 3번", "검 4번",
#     "검 5번", "검 6번", "검 7번", "검 8번",
#     "검 9번", "검 10번", "검 시종", "검 기사",
#     "검 여왕", "검 왕", "펜타클 에이스", "펜타클 2번",
#     "펜타클 3번", "펜타클 4번", "펜타클 5번", "펜타클 6번",
#     "펜타클 7번", "펜타클 8번", "펜타클 9번", "펜타클 10번",
#     "펜타클 시종", "펜타클 기사", "펜타클 여왕", "펜타클 왕"
# ]

# 기존의 tarot_cards 리스트와 빈 값으로 초기화된 tarot_cards_dict
deck = [
    'the-fool', 'the-magician', 'the-high-priestess', 'the-empress',
    'the-emperor', 'the-hierophant', 'the-lovers', 'the-chariot',
    'strength', 'the-hermit', 'wheel-of-fortune', 'justice',
    'the-hanged-man', 'death', 'temperance', 'the-devil',
    'the-tower', 'the-star', 'the-moon', 'the-sun',
    'judgement', 'the-world',
    'ace-of-wands', 'two-of-wands', 'three-of-wands', 'four-of-wands',
    'five-of-wands', 'six-of-wands', 'seven-of-wands', 'eight-of-wands',
    'nine-of-wands', 'ten-of-wands', 'page-of-wands', 'knight-of-wands',
    'queen-of-wands', 'king-of-wands',
    'ace-of-cups', 'two-of-cups', 'three-of-cups', 'four-of-cups',
    'five-of-cups', 'six-of-cups', 'seven-of-cups', 'eight-of-cups',
    'nine-of-cups', 'ten-of-cups', 'page-of-cups', 'knight-of-cups',
    'queen-of-cups', 'king-of-cups',
    'ace-of-swords', 'two-of-swords', 'three-of-swords', 'four-of-swords',
    'five-of-swords', 'six-of-swords', 'seven-of-swords', 'eight-of-swords',
    'nine-of-swords', 'ten-of-swords', 'page-of-swords', 'knight-of-swords',
    'queen-of-swords', 'king-of-swords',
    'ace-of-coins', 'two-of-coins', 'three-of-coins', 'four-of-coins',
    'five-of-coins', 'six-of-coins', 'seven-of-coins', 'eight-of-coins',
    'nine-of-coins', 'ten-of-coins', 'page-of-coins', 'knight-of-coins',
    'queen-of-coins', 'king-of-coins'
]

tarot_cards_dict = {
    'the-fool': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/0.jpg',
    'the-magician': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/1.jpg',
    'the-high-priestess': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/2.jpg',
    'the-empress': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/3.jpg',
    'the-emperor': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/4.jpg',
    'the-hierophant': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/5.jpg',
    'the-lovers': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/6.jpg',
    'the-chariot': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/7.jpg',
    'strength': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/8.jpg',
    'the-hermit': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/9.jpg',
    'wheel-of-fortune': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/10.jpg',
    'justice': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/11.jpg',
    'the-hanged-man': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/12.jpg',
    'death': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/13.jpg',
    'temperance': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/14.jpg',
    'the-devil': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/15.jpg',
    'the-tower': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/16.jpg',
    'the-star': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/17.jpg',
    'the-moon': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/18.jpg',
    'the-sun': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/19.jpg',
    'judgement': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/20.jpg',
    'the-world': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/21.jpg',
    'ace-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/22.jpg',
    'two-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/23.jpg',
    'three-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/24.jpg',
    'four-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/25.jpg',
    'five-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/26.jpg',
    'six-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/27.jpg',
    'seven-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/28.jpg',
    'eight-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/29.jpg',
    'nine-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/30.jpg',
    'ten-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/31.jpg',
    'page-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/32.jpg',
    'knight-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/33.jpg',
    'queen-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/34.jpg',
    'king-of-wands': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/35.jpg',
    'ace-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/36.jpg',
    'two-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/37.jpg',
    'three-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/38.jpg',
    'four-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/39.jpg',
    'five-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/40.jpg',
    'six-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/41.jpg',
    'seven-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/42.jpg',
    'eight-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/43.jpg',
    'nine-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/44.jpg',
    'ten-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/45.jpg',
    'page-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/46.jpg',
    'knight-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/47.jpg',
    'queen-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/48.jpg',
    'king-of-cups': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/49.jpg',
    'ace-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/50.jpg',
    'two-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/51.jpg',
    'three-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/52.jpg',
    'four-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/53.jpg',
    'five-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/54.jpg',
    'six-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/55.jpg',
    'seven-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/56.jpg',
    'eight-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/57.jpg',
    'nine-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/58.jpg',
    'ten-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/59.jpg',
    'page-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/60.jpg',
    'knight-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/61.jpg',
    'queen-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/62.jpg',
    'king-of-swords': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/63.jpg',
    'ace-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/64.jpg',
    'two-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/65.jpg',
    'three-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/66.jpg',
    'four-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/67.jpg',
    'five-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/68.jpg',
    'six-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/69.jpg',
    'seven-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/70.jpg',
    'eight-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/71.jpg',
    'nine-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/72.jpg',
    'ten-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/73.jpg',
    'page-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/74.jpg',
    'knight-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/75.jpg',
    'queen-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/76.jpg',
    'king-of-coins': 'https://gfx.tarot.com/images/site/decks/universal-waite/full_size/77.jpg',
}




table_reset_tag=0
random_numbers=[]

@csrf_exempt
@require_POST
def table_reset(request):
    global table_reset_tag
    data=json.loads(request.body)
    tag=data.API_KEY('tablereset', [])
    tag=tag[0]
    if tag==1:
        table_reset_tag=0
    return


@csrf_exempt
@require_POST
def process_result(request):
    global table_reset_tag
    global random_numbers
    print("Received request body:", request.body)

    try:
        data = json.loads(request.body)
        print("Parsed data:", data)
        count = data.get('clickedButtons', [])
        print(count)
        numbers = len(count)
        print(f'선택한수: {numbers}')

        if not isinstance(numbers, int) or numbers not in [1, 2, 3, 4, 5, 6, 7, 8]:
            response = {'error': '카드를 선택해야 합니다.'}
            return JsonResponse(response, status=400)

        if table_reset_tag == 0:  # 태그가 0일 경우 카드 테이블을 초기화하고 다시 제작
            random_numbers = []
            for _ in range(8):  # 0,1,2,3,4,5,6,7
                num = random.randint(1, 78)
                while num in random_numbers:
                    num = random.randint(1, 78)
                random_numbers.append(num)
            table_reset_tag = 1
        print(random_numbers)
        # random_numbers의 index는 0~8까지
        cards = []
        cards = [deck[random_numbers[i - 1]] for i in count]  # i: 0~7 / count: 1~8
        print(cards)
        # deck의 index는 0~77까지
        result = model.generate_content(f"""#입력문
너는 타로 점을 보는 사람이다. 어떤 사람이 선택한 타로 카드를 보고 그 타로 카드의 의미와 연관지어서 점을 보면 된다. 그 사람이 선택한 타로 카드는 [#카드]에 있다. 어떻게 대답해야 하는지는 [#출력형식]과 [#예시]를 참고한다. 
#카드
{cards}
#출력형식
-선택된 카드의 의미를 순차적으로 설명한 뒤 종합적인 해석을 설명한다. 
-사람이 사람에게 말을 하듯이 설명해야 한다. 즉 문단을 나누거나 제목을 다는 등의 행동을 해서는 안된다. 
-결과 해석 이외의 다른 말은 하지 않는다. 
-카드의 이름은 영어로 말해서는 안된다. 
-해석에서 한글과 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 만을 사용한다. 
-한자, 영어, 가나 문자 등 한글 이외의 언어 문자는 사용하지 않는다. 
#예시
당신이 선택한 카드는 광대, 마술사, 검 6번 입니다. 광대는 새로운 시작, 순수함, 무모함 믿음의 도약을 의미하며 마술사는 능숙함, 의지력, 창의성, 가능성. 잠재력을 의미하죠. 검 6번은 평화, 조화 갈등 해결, 과거 극복, 용서를 의미합니다. 흥미로운 조합이에요. 광대는 새로운 시작과 무모한 도약을 상징하며, 마술사는 능숙함과 창의성으로 그 여정을 이끌어갈 것을 의미합니다. 검 6번은 갈등 해결과 용서를 통해 마음의 평화를 찾을 수 있음을 나타내요. 이 카드들은 당신이 새로운 도전을 앞에 두고 있다고 말하는군요. 당신에게는 뛰어난 능숙함과 창의성이 있으니 자신감을 가지고 앞으로 나아가야 해요. 그 여정에 있는 갈등에 얽매이지 말고 용서와 조화를 통해 마음의 평화 또한 얻을 수 있을 것입니다. """)

        resultCard = {}
        for idx, cardName in enumerate(cards):
            resultCard[count[idx]] = cardName+"~"+tarot_cards_dict[cardName]

        response = {'result': result.text, 'cards': resultCard }

        return JsonResponse(response)

    except json.JSONDecodeError:
        response = {'error': '잘못된 Json 형식입니다. '}
        return JsonResponse(response, status=400)
    except Exception as e:
        response = {'error': f'서버 오류: {str(e)}'}
        return JsonResponse(response, status=500)
