const btn = document.getElementById("summarize-btn");
const input = document.getElementById("summarize-input");
const loading = document.getElementById("summarize-loading");
const errorBox = document.getElementById("summarize-error");
const resultBox = document.getElementById("summarize-result");

btn.addEventListener("click", async () => {
    const text = input.value;

    errorBox.textContent = "";
    resultBox.innerHTML = "";

    btn.disabled = true;
    input.disabled = true;
    loading.style.display = "block";

    try {
        const response = await fetch("/summarize/run/", {
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

        resultBox.innerHTML = `
            <p>원문 길이: ${data.original_length}자</p>
            <p>요약문 길이: ${data.summary_length}자</p>
            <p>요약 비율: ${data.summary_ratio}%</p>
            <p>요약 결과:</p>
            <p>${data.summary}</p>
        `;
        addToHistory(text, data.summary);
    } catch (err) {
        errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
    } finally {
        btn.disabled = false;
        input.disabled = false;
        loading.style.display = "none";
    }
});

function addToHistory(inputText, outputText) {
    const historyList = document.getElementById("summarize-history");

    const placeholder = historyList.querySelector("li.no-history");
    if (placeholder) {
        placeholder.remove();
    }

    const li = document.createElement("li");
    const shortInput = inputText.length > 30 ? inputText.slice(0, 30) + "..." : inputText;
    const shortOutput = outputText.length > 30 ? outputText.slice(0, 30) + "..." : outputText;
    li.textContent = `${shortInput} → ${shortOutput} (방금 실행)`;
    historyList.prepend(li);

    while (historyList.children.length > 5) {
        historyList.removeChild(historyList.lastChild);
    }
}