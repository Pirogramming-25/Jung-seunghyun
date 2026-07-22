from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,
        device=get_pipeline_device(),
    )


def run_moderate(text):
    moderator = get_moderator_pipeline()
    # sentiment와 동일하게 [0]으로 겉껍질 한 겹 벗겨야 함
    raw_result = moderator(text)[0]

    sorted_scores = sorted(
        raw_result,
        key=lambda item: item["score"],
        reverse=True,
    )

    top = sorted_scores[0]

    return {
        "highest_label": top["label"],
        "highest_score": round(top["score"] * 100, 2),
        "all_scores": [
            {
                "label": item["label"],
                "score": round(item["score"] * 100, 2),
            }
            for item in sorted_scores
        ],
    }