# 🤖 Django GPT — Hugging Face AI 웹 서비스

피로그래밍 25기 5주차 화요일 과제

## 🧠 사용 모델

### 1. 감정 분석

- **기능:** 영어 문장의 감정 분석 (positive / neutral / negative)
- **Model ID:** [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- **Task:** `text-classification`
- **License:** CC-BY-4.0
- **입력 언어:** 영어
- **출력 형태:** 라벨(positive/neutral/negative) + 전체 라벨별 신뢰도(%)

#### 입력 예시
```
Today I'm going to shopping
```

#### 출력 예시
```
감정: neutral
신뢰도: 50.91%

neutral: 50.91%
positive: 40.82%
negative: 8.27%
```

---

### 2. 문서 요약

- **기능:** 긴 영어 문서를 요약
- **Model ID:** [`sshleifer/distilbart-cnn-6-6`](https://huggingface.co/sshleifer/distilbart-cnn-6-6)
- **Task:** `summarization`
- **License:** Apache 2.0
- **입력 언어:** 영어
- **출력 형태:** 요약문 + 원문/요약문 길이 + 요약 비율(%)

#### 입력 예시
```
Artificial intelligence has rapidly transformed the way businesses operate
over the past decade. Companies across various industries are now leveraging
machine learning models to automate repetitive tasks, analyze large datasets,
and make data-driven decisions faster than ever before...
```

#### 출력 예시
```
원문 길이: 520자
요약문 길이: 98자
요약 비율: 18.85%

요약 결과:
AI has transformed how businesses operate by automating tasks and
enabling faster, data-driven decisions.
```

---

### 3. 유해 표현 분석

- **기능:** 영어 문장의 유해성(독성) 분석
- **Model ID:** [`unitary/toxic-bert`](https://huggingface.co/unitary/toxic-bert)
- **Task:** `text-classification` (multi-label)
- **License:** Apache 2.0
- **입력 언어:** 영어
- **출력 형태:** 최고 위험 라벨 + 점수 + 전체 라벨별 점수(정렬)

#### 입력 예시
```
You are such an idiot, nobody wants to hear your opinion.
```

#### 출력 예시
```
최고 위험 레이블: insult
위험 점수: 78.43%

insult: 78.43%
toxic: 66.21%
obscene: 31.29%
threat: 4.82%
```

## ⚙️ 실행 방법

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env.example`을 복사해서 `.env` 파일 생성:
```bash
cp .env.example .env
```
`.env` 파일 안에 `DJANGO_SECRET_KEY` 값을 채워넣습니다. (Gated 모델을 쓰지 않는 한 `HUGGINGFACE_TOKEN`은 비워둬도 됩니다.)

### 4. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 관리자 계정 생성 (로그인 테스트용)
```bash
python manage.py createsuperuser
```

### 6. 서버 실행
```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/sentiment/` 접속

## 🔗 URL 및 접근 권한

| URL | 기능 | 접근 권한 |
| --- | --- | --- |
| `/sentiment/` | 감정 분석 | 비로그인 허용 |
| `/summarize/` | 문서 요약 | 로그인 필요 |
| `/moderate/` | 유해 표현 분석 | 로그인 필요 |
| `/combo/` | 복합 모델 기능 (챌린지) | 로그인 필요 |
| `/accounts/login/` | 로그인 | - |
| `/accounts/logout/` | 로그아웃 | - |

## 🧱 프로젝트 구조

```
Django_GPT/
├─ config/
│  ├─ settings.py
│  └─ urls.py
├─ my_gpt/
│  ├─ services/
│  │  ├─ common.py
│  │  ├─ sentiment.py
│  │  ├─ summarizer.py
│  │  └─ moderator.py
│  ├─ templates/
│  │  ├─ registration/login.html
│  │  └─ my_gpt/
│  ├─ static/my_gpt/
│  ├─ decorators.py       # 로그인 필요 커스텀 데코레이터
│  ├─ models.py           # InferenceHistory
│  ├─ urls.py
│  └─ views.py
├─ .env
├─ .env.example
└─ requirements.txt
```