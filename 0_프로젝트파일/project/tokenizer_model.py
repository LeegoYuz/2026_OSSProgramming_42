# tokenizer_model.py
import os
import torch
from transformers import ElectraTokenizer, ElectraForSequenceClassification
from CONSTANTS import EMOTIONS_LIST, EMOTION_LEXICON, EMPHASIS_WORDS
import re
import numpy as np

MODEL_DIR = "monologg/koelectra-base-v3-discriminator"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = ElectraTokenizer.from_pretrained(MODEL_DIR)
model = ElectraForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(DEVICE)
model.eval()

def normalize_text(text: str) -> str: # 전처리 함수
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_emotion_words(text: str): # 감정 단어 추출 후 사전 정의 키워드 매칭
    text_norm = normalize_text(text)
    found = {emotion: 0 for emotion in EMOTIONS_LIST}
    for emotion, keywords in EMOTION_LEXICON.items():
        for kw in keywords:
            # 단어 경계 매칭, 소문자/대소문자 무시
            if re.search(rf"\b{re.escape(kw)}\b", text_norm):
                found[emotion] += 1
    return found  # {emotion: count}

def predict_logits(text: str): # 모델 예측
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.squeeze().cpu().numpy()
    return logits  # numpy array length = num_labels

def apply_emphasis_boost(tokens, emotion_scores, emotion_keywords, boost=0.2): # 강조 단어 붙어있으면 해당 감정 가중치 제공
    """
    tokens: 토큰화된 단어 리스트
    emotion_scores: 감정별 점수 dict {emotion: score}
    emotion_keywords: 감정별 키워드 dict {emotion: [keywords]}
    boost: 강조 발견 시 추가 가중치
    """
    for i, tok in enumerate(tokens):
        for emotion, keywords in emotion_keywords.items():
            if tok in keywords and i > 0 and tokens[i-1] in EMPHASIS_WORDS:
                emotion_scores[emotion] += boost
    return emotion_scores

def predict(text: str, weight_model=0.7, weight_lexicon=0.3, emphasis_boost=0.2): # 후처리: 모델 점수와 키워드 점수를 결합
    """
    입력 문장을 받아 최종 감정 인덱스를 반환한다.
    - weight_model: 모델 점수 가중치
    - weight_lexicon: 감정 단어 점수 가중치
    - emphasis_boost: 강조 표현 발견 시 추가 가중치
    """

    # 1) 모델 추론
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256).to(DEVICE)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.squeeze().cpu().numpy()

    exp = np.exp(logits - np.max(logits))
    model_probs = exp / exp.sum()

    # 2) 감정 단어 점수
    lex_counts = {emotion: 0 for emotion in EMOTIONS_LIST}
    tokens = tokenizer.tokenize(text)

    for i, tok in enumerate(tokens):
        for emotion, keywords in EMOTION_LEXICON.items():
            if tok in keywords:
                lex_counts[emotion] += 1
                # 강조 표현 확인
                if i > 0 and tokens[i-1] in EMPHASIS_WORDS:
                    lex_counts[emotion] += emphasis_boost  # 강조 보정

    counts = np.array([lex_counts[e] for e in EMOTIONS_LIST], dtype=float)
    lex_scores = counts / counts.sum() if counts.sum() > 0 else np.zeros_like(counts)

    # 3) 모델 점수와 합산
    combined = weight_model * model_probs + weight_lexicon * lex_scores

    # 4) 최종 감정 선택
    pred_idx = int(np.argmax(combined))
    return pred_idx

def predict_emotion(text: str, weight_model=0.7, weight_lexicon=0.3, emphasis_boost=0.2): # 문자열 환산
    pred_idx = predict(text, weight_model, weight_lexicon, emphasis_boost)
    emotion = EMOTIONS_LIST[pred_idx]
    return emotion
