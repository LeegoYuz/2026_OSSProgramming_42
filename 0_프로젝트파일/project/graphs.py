# graphs.py
# 감정 데이터 시각화용 모듈, 표 형태로 반환

import json
import datetime

DB_PATH = "data/emotions.json"

def _load_db(): # DB 파일 읽기
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_weekly_emotions(): # 최근 7일 데이터 추출
    data = _load_db()
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())  # 이번 주 월요일
    
    week_days = ["월", "화", "수", "목", "금", "토", "일"]
    emotions_table = {day: None for day in week_days}
    
    for entry in data:
        entry_date = datetime.date.fromisoformat(entry["date"])
        # 이번 주 범위에 속하는 데이터만 반영
        if week_start <= entry_date <= week_start + datetime.timedelta(days=6):
            weekday_idx = entry_date.weekday()  # 0=월, 6=일
            emotions_table[week_days[weekday_idx]] = entry["emotion"]
    
    return emotions_table
