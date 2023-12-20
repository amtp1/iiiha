const choiceContentCalls = {
    'ChatGPT': generateChatGPT,
    'ImageFusion': generateFusion,
}

const remove = (sel) => document.querySelectorAll(sel).forEach(el => el.remove());

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
                    if (content == 'Unknow') {
                        $('#service-choice-modal').modal('show');
                    } else {
                        $('#service-choice-modal').modal('show');
                        /*let contentArray = content.split(',');
                        if (contentArray.length == 1) {
                            content = contentArray[0].trim();
                            choiceContentCalls[content]();
                        } else {
                            const services = document.getElementById('services');
                            contentArray.forEach((content) => {
                                content = content.trim();
                                const button = document.createElement('button');
                                button.id = 'service-choice-button';
                                button.setAttribute('onclick', choiceCalls[content]);
                                const div = document.createElement('div');
                                div.className = 'service-card';
                                const h2 = document.createElement('h2');
                                h2.innerHTML = content;
                                div.appendChild(h2);
                                button.appendChild(div);
                                services.appendChild(button);
                            });
                            $('#service-choice-modal').modal('show');
                        }*/

                    }
                }
            )
          });
    }
}

function generateChatGPT() {
    $('#service-choice-button').on('click', resetServices());
    resetContent();
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let data = new FormData();
        data.append('content', textArea.val());

        fetch('generate_chatgpt', {
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
                    let content = data['choices'][0]['message']['content'];
                    let contentDiv = document.getElementById('content-div');
                    const contentP = document.createElement('p');
                    contentP.id = 'content';
                    contentP.innerHTML = content;
                    contentDiv.appendChild(contentP);
                    scrollIntoView('content-div');
                }
            )
        });
    }
}

function generateFusion() {
    $('#service-choice-button').on('click', resetServices());
    resetContent();
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
                    let contentDiv = document.getElementById('content-div');
                    const contentP = document.createElement('p');
                    contentP.id = 'content';
                    let fusionImageResult = document.getElementById('fusion-image-result');
                    if (fusionImageResult){
                        fusionImageResult.remove();
                    }
                    const newImage = document.createElement('img');
                    newImage.id = 'fusion-image-result';
                    newImage.src = `data:image/png;base64,${image}`;
                    contentP.appendChild(newImage);
                    contentDiv.appendChild(contentP);
                    scrollIntoView('fusion-image-result');
                }
            )
          });
    }
}

function scrollIntoView(id) {
    document.getElementById(id).scrollIntoView({ block: 'center', behavior: 'smooth' });
}

function resetPreGenerateButton() {
    let generateBtn = document.getElementById('pre-generate-btn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = 'Генерировать';
}

function resetServices() {
    $('#service-choice-modal').modal('hide');
    remove('#service-choice-button');

    const services = document.getElementById('services');
    const button = document.createElement('button');
    button.id = 'service-choice-button';
    button.setAttribute('onclick', 'generateChatGPT()');
    const div = document.createElement('div');
    div.className = 'service-card';
    const h2 = document.createElement('h2');
    h2.innerHTML = 'ChatGPT';
    div.appendChild(h2);
    button.appendChild(div);
    services.appendChild(button);
}

function resetContent() {
    let content = document.getElementById('content');
    if (content) {
        remove('#content');
    }
}