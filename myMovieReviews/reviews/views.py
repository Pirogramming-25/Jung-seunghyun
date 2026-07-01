from django.shortcuts import render, get_object_or_404, redirect
from .models import Review 

#시간단위 변환 함수
def convert_running_time(minutes):
    hours = int(minutes) // 60
    remaining_minutes = int(minutes) % 60
    
    if hours == 0:
        return f"{remaining_minutes}분"
    elif remaining_minutes == 0:
        return f"{hours}시간"
    else:
        return f"{hours}시간 {remaining_minutes}분"
    
#리뷰 리스트 페이지
def review_list(request):
    #Review 테이블에 있는 모든 리뷰데이터를 가져옴
    reviews = Review.objects.all()
    # 각 리뷰마다 보여줄 러닝타임 문자열 추가
    for review in reviews:
        review.running_time_text = convert_running_time(review.running_time)
    # review_list.html 화면을 보여줌
    # reviews라는 이름으로 리뷰 목록 데이터를 넘겨줌
    return render(request, 'reviews/review_list.html', {'reviews':reviews})

#리뷰 디테일 페이지
def review_detail(request, pk):
    
    # DB에서 pk번호에 해당하는 리뷰를 찾음
    review = get_object_or_404(Review, pk=pk)
    
    # 각 리뷰마다 보여줄 러닝타임 문자열 추가
    review.running_time_text = convert_running_time(review.running_time)
    
    #디테일 html 화면을 보여주면서 review라는 이름으로 리뷰 하나의 데이터 넘겨줌
    return render(request, 'reviews/review_detail.html', {'review':review})


#리뷰 생성 페이지
def review_create(request):
    
    # POST 요청이면 사용자가 입력한 값을 DB에 저장
    if request.method == 'POST':
        # Review 테이블에 새 리뷰 데이터를 생성
        Review.objects.create(
            title=request.POST['title'],
            release_year=request.POST['release_year'],
            director=request.POST['director'],
            actor=request.POST['actor'],
            genre= request.POST['genre'],
            rating= request.POST['rating'],
            running_time=request.POST['running_time'],
            content=request.POST['content'],
        )
        
        # 새 리뷰 작성이 끝나면 리뷰 리스트 페이지로 이동
        return redirect('reviews:review_list')
    
    # 빈 리뷰 작성 폼을 보여줌
    return render(request, 'reviews/review_form.html')

# 리뷰 수정 페이지
def review_update(request, pk):
    #수정할 리뷰 찾음
    #없으면 404에러 페이지 보여줌
    review = get_object_or_404(Review, pk=pk)
    
    #수정 폼에서 저장 버튼 눌렀을 때
    if request.method == 'POST':
        # 기존 review 객체 값을 사용자가 입력한 값으로 바꿈
        review.title=request.POST['title']
        review.release_year=request.POST['release_year']
        review.director=request.POST['director']
        review.actor=request.POST['actor']
        review.genre= request.POST['genre']
        review.rating= request.POST['rating']
        review.running_time=request.POST['running_time']
        review.content=request.POST['content']
        
        # 바꾼 내용을 DB에 저장
        review.save()
        # 수정이 끝나면 디테일 페이지로 이동
        return redirect('reviews:review_detail', pk=review.pk)
    
    # 기존에 저장해 둔 정보들로 form이 채워진 채로 나타남
    return render(request, 'reviews/review_form.html', {'review':review})

# 리뷰 삭제
def review_delete(request, pk):
    
    # 삭제할 리뷰 찾음
    # 없으면 404에러 페이지 보여줌
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    
    # 삭제 후 리뷰 페이지로 이동
    return redirect('reviews:review_list')