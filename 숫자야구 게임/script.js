//html 요소 불러오기
const inputs = document.querySelectorAll("input"); //html에서 input 태그 3개 가져오기
const submitButton = document.querySelector(".submit-button"); //버튼 가져오기
const resultImg = document.getElementById("game-result-img"); //결과 사진 가져오기
const attemptText = document.querySelector("#attempts"); //시도 횟수 가져오기
const results = document.getElementById("results"); //결과

let answer = []; //정답 숫자 3개(바뀌는 값이라 let으로)
let attempts = 9; //남은 기회(9로 초기화)(바뀌는 값이라 let으로)

//숫자 3개 만드는 함수
function makeAnswer(){
    answer = [];

    while(answer.length < 3){
        const randomNumber = Math.floor(Math.random() * 10);

        //중복되지 않는 3개의 랜덤숫자 설정
        if(!answer.includes(randomNumber)){
            answer.push(randomNumber);
        }
    }
    console.log("정답:", answer);
}

//게임 초기화 함수
function initGame(){
    attempts = 9;
    makeAnswer(); //새 정답 만들기

    //값 비우기
    inputs.forEach((input) => {
        input.value = "";
    });

    //이미지 지우기, 버튼 활성화
    resultImg.src ="";
    submitButton.disabled = false;
    attemptText.textContent = attempts;
    result.innerHTML = "";
}

//input 초기화 함수
function clearInputs(){
    inputs.forEach((input) => {
        input.value = "";
    });
}

//결과 출력 함수
function addResult(inputNumbers, strike, ball) {
    const resultLine = document.createElement("div");
    resultLine.style.marginBottom = "10px";
    resultLine.style.letterSpacing = "2px";
    resultLine.style.wordSpacing = "8px";

    const userInput =
        String(inputNumbers[0]) +
        String(inputNumbers[1]) +
        String(inputNumbers[2]);

    if (strike === 0 && ball === 0) {
        resultLine.textContent = userInput + " : O";
    } else {
        resultLine.textContent = userInput + " : " + strike + " S " + ball + " B";
    }

    results.appendChild(resultLine);
}

//입력된 숫자 확인함수
function check_numbers(){
    for (let i=0; i<inputs.length; i++){
        if(inputs[i].value === ""){
            clearInputs();
            return;
        }
    }

    const inputNumbers = [];

    inputs.forEach((input) => {
        inputNumbers.push(Number(input.value));
    });

    //시도 횟수 줄이기
    attempts--;
    attemptText.textContent = attempts;

    //스트라이크, 볼 계산로직
    let strike = 0;
    let ball = 0;

    for(let i=0; i<3; i++){
        if(inputNumbers[i]==answer[i]){
            strike++;
        }else if(answer.includes(inputNumbers[i])) {
            ball++;
        }
    }

    //결과 화면에 추가
    addResult(inputNumbers, strike, ball);

    //결과 화면에 출력했으니 input 비우기
    clearInputs();

    //승리
    if(strike === 3){
        resultImg.src = "success.png";
        submitButton.disabled = true;
        return;
    }
    //패배
    if(attempts === 0){
        resultImg.src = "fail.png";
        submitButton.disabled = true;
    }
}
//페이지 열 때 initGame함수 실행
window.onload = initGame;



