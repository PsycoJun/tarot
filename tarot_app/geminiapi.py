import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import random

API_KEY='NOT_API_KEY'#실제 API 키가 아님

genai.configure(api_key=API_KEY)#Gemini API 키 설정
model=genai.GenerativeModel('gemini-pro')

deck = [
    "바보", "마술사", "여사제", "여황제", "황제",
    "교황", "연인", "전차", "힘", "은둔자",
    "운명의 수레바퀴", "정의", "매달린 사람", "죽음", "절제",
    "악마", "탑", "별", "달", "태양", "심판",
    "세계", "완드 에이스", "완드 2번", "완드 3번", "완드 4번",
    "완드 5번", "완드 6번", "완드 7번", "완드 8번", "완드 9번",
    "완드 10번", "완드 시종", "완드 기사", "완드 여왕", "완드 왕",
    "컵 에이스", "컵 2번", "컵 3번", "컵 4번", "컵 5번",
    "컵 6번", "컵 7번", "컵 8번", "컵 9번", "컵 10번",
    "컵 시종", "컵 기사", "컵 여왕", "컵 왕",
    "검 에이스", "검 2번", "검 3번", "검 4번",
    "검 5번", "검 6번", "검 7번", "검 8번",
    "검 9번", "검 10번", "검 시종", "검 기사",
    "검 여왕", "검 왕", "펜타클 에이스", "펜타클 2번",
    "펜타클 3번", "펜타클 4번", "펜타클 5번", "펜타클 6번",
    "펜타클 7번", "펜타클 8번", "펜타클 9번", "펜타클 10번",
    "펜타클 시종", "펜타클 기사", "펜타클 여왕", "펜타클 왕"
]



table_reset_tag=0
random_numbers=[]

@csrf_exempt
@require_POST
def table_reset(request):
    global table_reset_tag
    data=json.loads(request.body)
    tag=data.get('tablereset', [])
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
        count =data.get('clickedButtons', [])
        print(count)
        numbers=len(count)
        print(f'선택한수: {numbers}')
        
        if not isinstance(numbers, int) or numbers not in[1,2,3,4,5,6,7,8]:
            response={'error': '카드를 선택해야 합니다.'}
            return JsonResponse(response, status=400)
        
        if table_reset_tag==0:#태그가 0일 경우 카드 테이블을 초기화하고 다시 제작
            random_numbers=[]
            for _ in range(8):#0,1,2,3,4,5,6,7
                num=random.randint(1,78)
                while num in random_numbers:
                    num=random.randint(1,78)
                random_numbers.append(num)
            table_reset_tag=1
        print(random_numbers)
        #random_numbers의 index는 0~8까지
        cards=[]
        cards=[deck[random_numbers[i-1]] for i in count]#i: 0~7 / count: 1~8
        print(cards)
        #deck의 index는 0~77까지
        result=model.generate_content(f"""#입력문
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

        response={'result': result.text}
        
        
        
        return JsonResponse(response)
    
    except json.JSONDecodeError:
        response={'error': '잘못된 Json 형식입니다. '}
        return JsonResponse(response, status=400)
    except Exception as e:
        response={'error': f'서버 오류: {str(e)}'}
        return JsonResponse(response, status=500)
        