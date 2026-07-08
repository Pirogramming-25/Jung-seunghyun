from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, PostImage, Like, Comment
from django.utils import timezone
from datetime import timedelta
from stories.models import Story
import json
from collections import OrderedDict

#[조회] 메인 피드 화면을 보여주는 함수
@login_required # 로그인해야 접근 가능
def feed(request):    
    # 내가 팔로우하는 사람들의 id 목록
    following_ids = request.user.following.values_list('to_user_id', flat=True)
    author_ids = list(following_ids) + [request.user.id]
    # 팔로우한 사람들 + 나 자신의 글만 보이게
    posts = Post.objects.filter(
        author_id__in = author_ids
    )
    
    # 스토리: 팔로우한 사람 + 나, 그리고 최근 24시간 이내만
    day_ago = timezone.now() - timedelta(hours=24)
    active_stories = Story.objects.filter(
        author_id__in=author_ids,
        created_at__gte=day_ago,          # 24시간 안에 올린 것만
    ).order_by('created_at')
    
    grouped = OrderedDict()
    for story in active_stories:
        author = story.author
        grouped.setdefault(author, [])
        for img in story.images.all():
            grouped[author].append(img.image.url)
    
    story_list=[]
    for author, image_urls in grouped.items():
        story_list.append({
            'username': author.username,
            # 프로필 사진이 있으면 그걸, 없으면 첫 스토리 사진을 썸네일로
            'thumb': author.profile_image.url if author.profile_image else image_urls[0],
            'images_json': json.dumps(image_urls),   # 뷰어가 넘길 사진 목록(JSON)
        })
    
    #내가 좋아요 누른 게시글들의 id 목록을 미리 구함(User -> Like 역방향)
    liked_posts = request.user.likes.values_list('post_id', flat=True)
    
    # feed.html 템플릿에 posts를 넘겨서 화면을 그림
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'liked_posts': liked_posts,
        'story_list': story_list,
    })

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

@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    #get_pr_create = 있으면 가져오고 없으면 새로 만듦
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
        # created=True 방금 새로 만들어진 상태
        # 좋아요 누른 상태
        liked=True
    else:
        # created=False 이미 있었음
        # 다시 누른 것이므로 삭제
        like.delete()
        liked=False
    #총 좋아요 수 세기(Post -> Like 역방향)
    count = post.likes.count()
    
    #JS에게 현재 상태와 개수 알려줌
    return JsonResponse({'liked': liked, 'count': count})

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id) # 어느 글에 달지 찾기
    if request.method == 'POST':
        content = request.POST.get('content', '')
        comment = Comment.objects.create(
            user = request.user,
            post = post,
            content = content
        )
        return redirect('posts:feed')

@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return JsonResponse({'error': '권한 없음'}, status=403)
    if request.method == 'POST':
        comment.content = request.POST.get('content', '')
        comment.save()
        return redirect('posts:feed')

# 댓글 삭제
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('posts:feed')
    if request.method == 'POST':
        comment.delete()
        return redirect('posts:feed')
