// CSRF 토큰 읽기
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// 게시글 작성
//폼이 제출될 때 실행
document.getElementById('post-form').addEventListener('submit', async (e) => {
    e.preventDefault(); //1. 새로고침 막기-> Ajax 시작
    //2. 폼 안의 값(사진,문구)을 한 번에 담는 객체
    const formData = new FormData(e.target);
    //3. fetch = 서버에 백그라운드로 요청 보내기 
    const res = await fetch('/create/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') }, //보안 토큰 첨부
        body: formData, //사진+문구 전송
    });
    const data = await res.json(); //4. 서버가 준 JSON 응답 받기
    if (res.ok) {
        location.reload(); //5. 화면 갱신
    } else {
        alert(data.error);
    }
});

// 게시글 삭제
document.querySelectorAll('.delete-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
        if (!confirm('삭제할까요?')) return;
        const id = btn.dataset.id;
    
        const res = await fetch(`/${id}/delete/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
        });
        if (res.ok) {
            document.querySelector(`.post[data-id="${id}"]`).remove();  // 화면에서 제거
        }
    });
});

// 좋아요 토클
document.querySelectorAll('.like-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
        const id = btn.dataset.id;   //몇 번 글인지

        //서버에 좋아요 토글 요청
        const res = await fetch(`/${id}/like/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        });
        const data = await res.json();   // { liked: true/false, count: 숫자 }

        // 1. 하트 색 토글: liked 값에 따라 'liked' 클래스를 켜고 끔
        btn.classList.toggle('liked', data.liked);

        // 2. 개수 갱신: 같은 data-id를 가진 like-count의 숫자를 바꿈
        document.querySelector(`.like-count[data-id="${id}"]`).textContent = data.count;
    });
});

// ===== 스토리 뷰어 (자동 넘김) =====
const viewer = document.getElementById('story-viewer');
const viewerImg = document.getElementById('viewer-img');
const progressBars = document.getElementById('progress-bars');

let images = [];      // 현재 스토리의 사진 URL 목록
let index = 0;        // 지금 보고 있는 사진 번호
let timer = null;     // 자동 넘김 타이머

// 스토리 썸네일 클릭 → 뷰어 열기
document.querySelectorAll('.story-item').forEach((item) => {
    item.addEventListener('click', () => {
        images = JSON.parse(item.dataset.images);   // 심어둔 사진 목록 읽기
        index = 0;
        openViewer();
    });
});

function openViewer() {
    viewer.classList.remove('hidden');   // 뷰어 보이기
    buildProgressBars();
    showImage();
}

// 현재 index의 사진을 보여주고, 3초 뒤 자동으로 다음 장
function showImage() {
    viewerImg.src = images[index];
    updateProgressBars();

    clearTimeout(timer);                 // 이전 타이머 취소
    timer = setTimeout(nextImage, 3000); // 3초 후 다음 사진
}

function nextImage() {
    if (index < images.length - 1) {
        index++;
        showImage();
    } else {
        closeViewer();   // 마지막 사진이면 뷰어 닫기
    }
}

function prevImage() {
    if (index > 0) {
        index--;
        showImage();
    }
}

function closeViewer() {
    viewer.classList.add('hidden');
    clearTimeout(timer);   // 타이머 정리 (안 하면 닫아도 계속 돌아감)
}

// 진행 바를 사진 수만큼 만들기
function buildProgressBars() {
    progressBars.innerHTML = '';
    images.forEach(() => {
        const bar = document.createElement('div');
        bar.className = 'progress-bar';
        progressBars.appendChild(bar);
    });
}

// 현재 보고 있는 사진의 진행 바만 흰색으로
function updateProgressBars() {
    document.querySelectorAll('.progress-bar').forEach((bar, i) => {
        bar.classList.toggle('active', i === index);
    });
}

// 버튼 연결
document.getElementById('viewer-next').addEventListener('click', nextImage);
document.getElementById('viewer-prev').addEventListener('click', prevImage);
document.getElementById('viewer-close').addEventListener('click', closeViewer);