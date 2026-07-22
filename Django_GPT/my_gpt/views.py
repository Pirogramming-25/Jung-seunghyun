import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .decorators import model_login_required
from .models import InferenceHistory

from .services.sentiment import run_sentiment
from .services.summarizer import run_summarize
from .services.moderator import run_moderate

logger = logging.getLogger(__name__)

SENTIMENT_MIN_LENGTH = 1
SENTIMENT_MAX_LENGTH = 1000

SUMMARIZE_MIN_LENGTH = 100
SUMMARIZE_MAX_LENGTH = 5000

MODERATE_MIN_LENGTH = 1
MODERATE_MAX_LENGTH = 1000

def _recent_histories(request, task, limit=5):
    if not request.user.is_authenticated:
        return []
    return list(
        InferenceHistory.objects.filter(
            user=request.user,
            task=task,
        ).order_by("-created_at")[:limit]
    )
    
def _parse_json_body(request):
    try:
        return json.loads(request.body), None
    except(json.JSONDecodeError, TypeError):
        return None, JsonResponse(
            {"error": "잘못된 요청입니다."},
            status=400,
            )

# 감정분석
def sentiment_view(request):
    """감정분석 페이지 비로그인 접근 가능"""
    histories = _recent_histories(request, InferenceHistory.Task.SENTIMENT)
    return render(
        request,
        "my_gpt/sentiment.html",
        {"histories": histories},
    )

@require_http_methods(["POST"])
def sentiment_run(request):
    """/sentiment/run/ fetch로 호출되는 실제 실행 endpoint"""
    body, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    text = body.get("text", "")
    
    #예상하지 못한 데이터 타입 방어
    if not isinstance(text, str):
        return JsonResponse(
            {"error": "분석할 문장을 입력해주세요."},
            status=400,
        )
    
    stripped = text.strip()
    
    if not stripped:
        return JsonResponse(
            {"error": "분석할 문장을 입력해주세요."},
            status=400,
        )
    
    if len(stripped) > SENTIMENT_MAX_LENGTH:
        return JsonResponse(
            {"error": f"문장은 {SENTIMENT_MAX_LENGTH}자 이하로 입력해주세요."},
            status=400,
        )
    
    try:
        result = run_sentiment(stripped)
    except Exception:
        logger.exception("Sentiment model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )
    
    if request.user.is_authenticated:
        InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=stripped,
            output_text=result["label"],
            result_data=result,
        )
    return JsonResponse(result)

# 문서요약
@model_login_required
def summarize_view(request):
    histories = _recent_histories(request, InferenceHistory.Task.SUMMARIZE)
    return render(
        request,
        "my_gpt/summarize.html",
        {"histories": histories},
    )

@model_login_required
@require_http_methods(["POST"])
def summarize_run(request):
    body, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "요약할 문서를 입력해주세요."}, status=400)

    stripped = text.strip()

    if not stripped:
        return JsonResponse({"error": "요약할 문서를 입력해주세요."}, status=400)

    if len(stripped) < SUMMARIZE_MIN_LENGTH:
        return JsonResponse(
            {"error": f"요약할 문서는 {SUMMARIZE_MIN_LENGTH}자 이상 입력해주세요."},
            status=400,
        )

    if len(stripped) > SUMMARIZE_MAX_LENGTH:
        return JsonResponse(
            {"error": f"문서는 {SUMMARIZE_MAX_LENGTH}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_summarize(stripped)
    except Exception:
        logger.exception("Summarize model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=stripped,
        output_text=result["summary"],
        result_data=result,
    )
    return JsonResponse(result)

#유해표현분석
@model_login_required
def moderate_view(request):
    histories = _recent_histories(request, InferenceHistory.Task.MODERATE)
    return render(
        request,
        "my_gpt/moderate.html",
        {"histories": histories},
    )

@model_login_required
@require_http_methods(["POST"])
def moderate_run(request):
    body, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    text = body.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    stripped = text.strip()

    if not stripped:
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    if len(stripped) > MODERATE_MAX_LENGTH:
        return JsonResponse(
            {"error": f"문장은 {MODERATE_MAX_LENGTH}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_moderate(stripped)
    except Exception:
        logger.exception("Moderate model inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=stripped,
        output_text=result["highest_label"],
        result_data=result,
    )
    return JsonResponse(result)