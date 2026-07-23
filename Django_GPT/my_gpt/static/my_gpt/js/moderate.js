const btn = document.getElementById("moderate-btn");
const input = document.getElementById("moderate-input");
const loading = document.getElementById("moderate-loading");
const errorBox = document.getElementById("moderate-error");
const resultBox = document.getElementById("moderate-result");

btn.addEventListener("click", async () => {
    const text = input.value;

    errorBox.textContent = "";
    resultBox.innerHTML = "";

    btn.disabled = true;
    input.disabled = true;
    loading.style.display = "block";

    try {
        const response = await fetch("/moderate/run/", {
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

        let html = `<p>최고 위험 레이블: ${data.highest_label}</p><p>위험 점수: ${data.highest_score}%</p><ul>`;
        data.all_scores.forEach((item) => {
            html += `<li>${item.label}: ${item.score}%</li>`;
        });
        html += "</ul>";
        resultBox.innerHTML = html;
        addToHistory(text, data.highest_label);
    } catch (err) {
        errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
    } finally {
        btn.disabled = false;
        input.disabled = false;
        loading.style.display = "none";
    }
});

function addToHistory(inputText, outputLabel) {
    const historyList = document.getElementById("moderate-history");

    const placeholder = historyList.querySelector("li.no-history");
    if (placeholder) {
        placeholder.remove();
    }

    const li = document.createElement("li");
    const shortText = inputText.length > 30 ? inputText.slice(0, 30) + "..." : inputText;
    li.textContent = `${shortText} → ${outputLabel} (방금 실행)`;
    historyList.prepend(li);

    while (historyList.children.length > 5) {
        historyList.removeChild(historyList.lastChild);
    }
}