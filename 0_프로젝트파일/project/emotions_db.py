# emotion_db.py
# JSON 기반 DB 모듈, 결과는 emotions.json에 저장됩니다.
# (emotions_example.js는 예시용 파일임)

import json
import os
from datetime import date

DB_PATH = "data/emotions.json" # 모델 연결 없이 테스트할 경우 경로를 data/emotions_example.json으로 변경

def init_db(): # 파일 없으면 빈 리스트로 초기화
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def _load_db(): # DB 파일 읽기
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(data): # DB 파일 저장
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_emotion(emotion): # 새로운 감정 기록 추가
    data = _load_db()
    new_id = (data[-1]["id"] + 1) if data else 1
    today = date.today().isoformat()

    entry = {"id": new_id, "date": today, "emotion": emotion}
    data.append(entry)
    _save_db(data)

def get_all_emotions(): # 전체 감정 기록 반환
    return _load_db()