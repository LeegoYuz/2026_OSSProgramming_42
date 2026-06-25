#app.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random

import emotions_db
import tokenizer_model  # AI 모델 모듈 연결
import graphs           # 주간 통계 모듈 연결 (확장용)
from CONSTANTS import EMOTIONS_LIST, RELATING_WORDS_LIST

app = FastAPI()

# CORS 설정 (Live Server 등 외부 접근 허용 유지)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프론트엔드 정적 파일(CSS/JS) 및 HTML 템플릿 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# JSON 데이터베이스 초기화
emotions_db.init_db()

# 1. 메인 화면 띄워주기
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 2. 대시보드 화면 띄워주기
@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

# 프론트엔드가 보낸 데이터를 받기 위한 규격 정의
class DiaryRequest(BaseModel):
    sentence: str

# 3. 일기 분석 API
@app.post("/api/analyze")
def analyze_diary(data: DiaryRequest):
    sentence = data.sentence
    
    # 모델을 돌려 감정 텍스트를 추출합니다.
    detected_emotion = tokenizer_model.predict_emotion(sentence)
    
    # 만약 모델이 범위를 벗어나 "알 수 없음"을 뱉으면 기본값 처리
    if detected_emotion == "알 수 없음":
        detected_emotion = "평온/안정"
    
    # 추출된 감정을 emotions.json에 누적 저장합니다.
    emotions_db.add_emotion(detected_emotion)
    
    # CONSTANTS에서 해당 감정에 맞는 위로/응원 문장 가져오기
    quotes = list(RELATING_WORDS_LIST.get(detected_emotion, ["오늘 하루도 고생 많으셨어요."]))
    selected_quote = random.choice(quotes) if quotes else "당신의 하루를 응원합니다."

    return {
        "emotion": detected_emotion,
        "message": selected_quote
    }

# 4. 감정 기록 데이터 반환 API (대시보드 그래프용)
@app.get("/api/history")
def get_emotions_history():
    return emotions_db.get_all_emotions()
