const btn = document.getElementById("sentiment-btn");
const input = document.getElementById("sentiment-input");
const loading = document.getElementById("sentiment-loading");
const errorBox = document.getElementById("sentiment-error");
const resultBox = document.getElementById("sentiment-result");

btn.addEventListener("click", async () => {
    const text = input.value;

    errorBox.textContent = "";
    resultBox.innerHTML = "";

    btn.disabled = true;
    input.disabled = true;
    loading.style.display = "block";

    try {
        const response = await fetch("/sentiment/run/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ text: text }),
        });

        const data = await response.json();

        if (!response.ok) {
            errorBox.textContent = data.error || "오류가 발생했습니다.";
            return;
        }

        let html = `<p>감정: ${data.label}</p><p>신뢰도: ${data.score}%</p>`;
        html += "<ul>";
        data.all_scores.forEach((item) => {
            html += `<li>${item.label}: ${item.score}%</li>`;
        });
        html += "</ul>";
        resultBox.innerHTML = html;
        addToHistory(text, data.label);
    } catch (err) {
        errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
    } finally {
        btn.disabled = false;
        input.disabled = false;
        loading.style.display = "none";
    }
});

function addToHistory(inputText, outputLabel) {
    const historyList = document.getElementById("sentiment-history");

    // "기록이 없습니다." 플레이스홀더 제거
    const placeholder = historyList.querySelector("li.no-history");
    if (placeholder) {
        placeholder.remove();
    }

    const li = document.createElement("li");
    const shortText = inputText.length > 30 ? inputText.slice(0, 30) + "..." : inputText;
    li.textContent = `${shortText} → ${outputLabel} (방금 실행)`;
    historyList.prepend(li);

    // 최근 5개까지만 화면에 유지
    while (historyList.children.length > 5) {
        historyList.removeChild(historyList.lastChild);
    }
}