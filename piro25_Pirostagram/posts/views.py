from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, PostImage

#[조회] 메인 피드 화면을 보여주는 함수
@login_required # 로그인해야 접근 가능
def feed(request):
    posts = Post.objects.all()   # DB에서 게시글 전부 가져오기
    # feed.html 템플릿에 posts를 넘겨서 화면을 그림
    return render(request, 'posts/feed.html', {'posts': posts})

#[작성] 새 게시글을 만드는 함수(Ajax로 호출됨)
@login_required
def post_create(request):
    # JS가 fetch로 보낸 요청은 POST 방식 -> 그때만 처리
    if request.method == 'POST':
        # 폼에서 보낸 문구 텍스트 꺼내기 (없으면 빈 문자열)
        caption = request.POST.get('caption', '')
        #업로드된 사진 꺼내기
        images = request.FILES.getlist('images')   # 여러 장
        
        #게시글 먼저 생성(작성자는 지금 로그인한 사람)
        post = Post.objects.create(author=request.user, caption=caption)
        #사진들을 하나씩 돌면서 게시글에 연결해 저장
        for img in images:
            PostImage.objects.create(post=post, image=img)

        # JS에게 결과를 JSON으로 돌려줌(화면 새로고침 없이 쓸 데이터)
        return JsonResponse({
            'id': post.id,
            'caption': post.caption,
            'author': post.author.username,
            'image_urls': [i.image.url for i in post.images.all()],
        })
    #POST가 아니면 에러
    return JsonResponse({'error': 'POST 요청만 허용'}, status=400)

#[수정] 게시글 문구를 고치는 함수
@login_required
def post_update(request, post_id):
    #해당 id의 글을 찾음, 없으면 404에러
    post = get_object_or_404(Post, id=post_id)
    # 남의 글 수정 방지
    if post.author != request.user:
        return JsonResponse({'error': '권한 없음'}, status=403)
    if request.method == 'POST':
        post.caption = request.POST.get('caption', '') #새 문구 교체
        post.save() #DB에 저장
        return JsonResponse({'id': post.id, 'caption': post.caption})
    return JsonResponse({'error': 'POST 요청만 허용'}, status=400)

#[삭제] 게시글을 지우는 함수
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #내 글만 삭제 가능
    if post.author != request.user:
        return JsonResponse({'error': '권한 없음'}, status=403)
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'success': True, 'id': post_id})
    return JsonResponse({'error': 'POST 요청만 허용'}, status=400)