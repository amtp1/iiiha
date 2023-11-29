function generateChatGPT() {
    let contentText = document.getElementById("chatgpt-textarea");
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

function generateFusion() {
    let contentText = document.getElementById("fusion-textarea");
    if (contentText.value == "") {
        return alert("Поле не должно оставаться пустым!");
    } else {
        let generateBtn = document.getElementById("generate-btn");
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>'
        let data = new FormData();
        data.append("prompt", contentText.value);

        fetch("generate_fusion", {
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
                    let image = data['image'][0];
                    let contentImage = document.getElementById("content-image");
                    const newImage = document.createElement('img');
                    newImage.src = `data:image/png;base64,${image}`;
                    newImage.width = 600;
                    newImage.height = 300;
                    contentImage.appendChild(newImage);
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = "Generate";
                }
            )
          })
    }
}