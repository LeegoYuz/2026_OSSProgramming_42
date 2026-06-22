# -*- coding: utf-8 -*-
"""tokenizer_model.py

KoELECTRA 기반 감정 분석 모듈
- app.py에서 tokenizer_model.predict(sentence) 호출 가능
"""

import torch
from transformers import ElectraTokenizer, ElectraForSequenceClassification
from CONSTANTS import EMOTIONS_LIST

# 토크나이저와 모델 로드 (사전 학습된 모델)
tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")
model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-base-v3-discriminator")

# GPU 사용 가능하면 GPU로 올리기
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def predict(sentence: str) -> int:
    """
    입력 문장을 받아 감정 클래스를 예측하고,
    EMOTIONS_LIST의 인덱스를 반환한다.
    """
    # 토큰화
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True).to(device)

    # 모델 추론
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = torch.argmax(logits, dim=-1).item()

    # 예측된 클래스 인덱스 반환
    return predicted_class_idx

def predict_emotion(sentence: str) -> str:
    """
    입력 문장을 받아 감정 라벨(문자열)을 반환한다.
    """
    idx = predict(sentence)
    if idx < len(EMOTIONS_LIST):
        return EMOTIONS_LIST[idx]
    else:
        return "알 수 없음"
