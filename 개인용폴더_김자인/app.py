from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random

app=FastAPI()
# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.1:5500"],  # Live Server 주소 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

# [팀원 코드 임포트]
import emotions_db
from CONSTANTS import EMOTIONS_LIST, RELATING_WORDS_LIST
# import tokenizer_model  # AI 모델 연동 시 주석 해제


# 프론트엔드 정적 파일(CSS/JS) 및 HTML 템플릿 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# JSON 데이터베이스 초기화
emotions_db.init_db()

# 브라우저에 화면 띄워주기
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 프론트엔드가 보낸 데이터를 받기 위한 규격 정의
class DiaryRequest(BaseModel):
    sentence: str

# 일기 분석 API
@app.post("/api/analyze")
def analyze_diary(data: DiaryRequest):
    sentence = data.sentence
    
    ### [팀원 영역] 이 부분에 모델 토큰화 및 예측 로직이 들어갑니다 ###
    # predicted_class_idx = tokenizer_model.predict(sentence)
    # detected_emotion = EMOTIONS_LIST[predicted_class_idx]
    
    # 임시 테스트용 결과 (팀원분이 모델 연동을 완료하면 위 코드로 대체)
    detected_emotion = random.choice(EMOTIONS_LIST) 
    
    # 팀원이 만든 DB 모듈을 사용하여 파일에 저장
    emotions_db.add_emotion(detected_emotion)
    
    raw_quotes = RELATING_WORDS_LIST.get(detected_emotion, [])
    
    if isinstance(raw_quotes, set) and raw_quotes:
        quotes = list(raw_quotes)
    elif isinstance(raw_quotes, dict) and raw_quotes:
        quotes = list(raw_quotes.keys())
    else:
        quotes = []

    # 만약 해당하는 응원 문장이 비어있다면 기본 문장 출력
    if quotes:
        selected_quote = random.choice(quotes)
    else:
        selected_quote = f"오늘 하루도 고생 많으셨어요. 당신의 {detected_emotion}을 응원합니다."

    return {
        "emotion": detected_emotion,
        "message": selected_quote
    }

@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")
# 감정 기록 데이터 반환 API (그래프용)
@app.get("/api/history")
def get_emotions_history():
    # 팀원이 만든 DB 조회 함수 호출하여 JSON 데이터를 그대로 프론트에 전달
    return emotions_db.get_all_emotions()
