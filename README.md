# 2026년도 1학기 오픈소스프로그래밍 42조

## 팀원
- 박지우: LeegoYuz, pjw0512 (둘 다 본인 계정입니다.)
- 김자인: jahin3856
- (팀원 1분이 개인 사정으로 중도 하차하셨습니다.)  

## 개요
이 프로젝트는 한국어 문장의 감정을 분류하기 위해 **KoELECTRA 기반 파인튜닝 모델**을 활용합니다. (https://github.com/monologg/KoELECTRA)  
데이터셋(`train.csv`, `valid.csv`)을 이용해 감정 라벨(행복, 우울, 불안, 분노, 설렘, 외로움, 평온)을 학습하고, 저장된 모델을 통해 문장의 감정을 예측할 수 있습니다.

---

## 폴더 구조
```
project/
├─ CONSTANTS.py          # 감정 라벨 정의
├─ tokenizer_model.py    # 모델 로드 및 예측 함수
├─ model_test.py         # 예시 실행 스크립트
├─ dataset/              # 학습용 CSV 데이터셋
└─ model/                # 파인튜닝된 모델 (Git LFS 관리)
```

---

## 설치 및 실행
```bash
git clone <레포지토리 URL>
cd project
pip install -r requirements.txt
python app.py
```

---

## 협업 지침
- **모델 파일(`model.safetensors`)은 Git LFS로 관리**됩니다.  
  팀원은 반드시 아래 명령으로 LFS를 설치해야 합니다:
  ```bash
  git lfs install
  ```
- 모델 파일은 자동으로 LFS를 통해 다운로드됩니다.  
- 데이터셋(`train.csv`, `valid.csv`)은 소규모 예시이며, 필요 시 확장 가능합니다.

---

## 감정 라벨 매핑
| 라벨 번호 | 감정 |
|-----------|------|
| 0 | 행복/만족 |
| 1 | 우울/피곤 |
| 2 | 불안/걱정 |
| 3 | 분노/짜증 |
| 4 | 설렘/흥분 |
| 5 | 외로움/공허 |
| 6 | 평온/안정 |

---
