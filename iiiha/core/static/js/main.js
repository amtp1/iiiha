function generateAssistentRequest() {
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>'

        let data = new FormData();
        data.append('content', textArea.val());

        fetch('generate_assistent_request', {
            method: 'POST',
            body: data,
            contentType: 'application/json',
            headers: {
                "X-Requested-With": 'XMLHttpRequest',
                "X-CSRFToken": $.cookie('csrftoken')
            },
          }).then(function (response) {
            response.json().then(
                function (data) {
                    let content = data['choices'][0]['message']['content'];
                    console.log(content);
                    if (content == 'Unknow') {
                        $('#service-choice-modal').modal('show');
                    } else {
                        if (content == 'ChatGPT') {
                            generateChatGPT();
                        } else {
                            $('#service-choice-modal').modal('show');
                        }
                    }
                }
            )
          });
    }
}

function generateChatGPT() {
    $('#service-choice-modal').modal('hide');
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let data = new FormData();
        data.append("content", textArea.val());

        fetch("generate_chatgpt", {
            method: "POST",
            body: data,
            contentType: 'application/json',
            headers: {
                'X-Requested-With': "XMLHttpRequest",
                'X-CSRFToken': $.cookie("csrftoken")
            },
            }).then(function (response) {
            response.json().then(
                function (data) {
                    resetPreGenerateButton();
                    let content = data['choices'][0]['message']['content'];
                    document.getElementById("content").innerHTML = content;
                    scrollIntoView('content-div');
                }
            )
        })
    }
}

function generateFusion() {
    $('#service-choice-modal').modal('hide');
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let data = new FormData();
        data.append('prompt', textArea.val());

        fetch('generate_fusion', {
            method: 'POST',
            body: data,
            contentType: 'application/json',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken')
            },
          }).then(function (response) {
            response.json().then(
                function (data) {
                    resetPreGenerateButton();
                    let image = data['image'][0];
                    let contentImage = document.getElementById('content');
                    let fusionImageResult = document.getElementById('fusion-image-result');
                    if (fusionImageResult){
                        fusionImageResult.remove();
                    }
                    const newImage = document.createElement('img');
                    newImage.id = 'fusion-image-result';
                    newImage.src = `data:image/png;base64,${image}`;
                    contentImage.appendChild(newImage);
                    scrollIntoView('fusion-image-result');
                }
            )
          })
    }
}

function scrollIntoView(id) {
    document.getElementById(id).scrollIntoView({ block: "center", behavior: "smooth" });
}

function resetPreGenerateButton() {
    let generateBtn = document.getElementById("pre-generate-btn");
    generateBtn.disabled = false;
    generateBtn.innerHTML = "Генерировать";
}