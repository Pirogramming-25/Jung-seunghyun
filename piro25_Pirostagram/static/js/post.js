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
