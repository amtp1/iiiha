function generateChatGPT() {
    let contentText = document.getElementById("textarea");
    if (contentText.value == "") {
        return alert("Поле не должно оставаться пустым!");
    } else {
        let generateBtn = document.getElementById("generate-btn");
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>'
        let data = new FormData();
        data.append("content", contentText.value);

        fetch("generate_chatgpt", {
            method: "POST",
            body: data,
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
          }).then(function (response) {
            response.json().then(
                function (data) {
                    let content = data['choices'][0]['message']['content'];
                    document.getElementById("content-text").innerHTML = content;
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = "Generate";
                }
            )
          })
    }
}