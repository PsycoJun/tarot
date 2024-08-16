from pathlib import Path
from django.conf import settings

file_path = Path(settings.BASE_DIR) / 'static' / 'Prompt' / 'Cross.txt'

def clean_text(text):
    return text.encode('utf-8', 'ignore').decode('utf-8')

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        clean_content = clean_text(content)
        print("파일 내용:")
        print(clean_content)
except UnicodeEncodeError as e:
    print(f"문자 인코딩 오류 발생: {e}")
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
except IOError as e:
    print(f"파일을 여는 중 오류가 발생했습니다: {e}")
