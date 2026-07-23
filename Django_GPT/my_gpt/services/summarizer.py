from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-6-6",
        device=get_pipeline_device(),
    )


def run_summarize(text, do_sample=False):
    summarizer = get_summarizer_pipeline()

    kwargs = {
        "max_length": 180,
        "min_length": 40,
    }

    if do_sample:
        # 재생성 버튼 등에서 다른 결과를 얻고 싶을 때 사용
        kwargs.update(
            {
                "do_sample": True,
                "top_p": 0.9,
                "temperature": 0.8,
            }
        )

    raw_result = summarizer(text, **kwargs)[0]
    summary = raw_result["summary_text"].strip()

    original_length = len(text)
    summary_length = len(summary)
    summary_ratio = round((summary_length / original_length) * 100, 2)

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "summary_ratio": summary_ratio,
    }