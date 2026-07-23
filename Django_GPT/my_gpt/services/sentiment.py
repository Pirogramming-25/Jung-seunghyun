from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        top_k=None,
        device=get_pipeline_device(),
    )

def run_sentiment(text):
    classifier = get_sentiment_pipeline()
    # top_k=None + 단일 문자열 입력이면 [{"label":..., "score":...}, ...] 형태로 바로 반환됨
    raw_result = classifier(text)[0]

    # raw_result 예시: [{"label": "positive", "score": 0.92}, ...]
    sorted_scores = sorted(
        raw_result,
        key=lambda item: item["score"],
        reverse=True,
    )

    top = sorted_scores[0]

    return {
        "label": top["label"],
        "score": round(top["score"] * 100, 2),
        "all_scores": [
            {
                "label": item["label"],
                "score": round(item["score"] * 100, 2),
            }
            for item in sorted_scores
        ],
    }