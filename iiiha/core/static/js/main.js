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
                        let contentArray = content.split(',');
                        if (contentArray.length == 1) {
                            content = contentArray[0].trim();
                            try {
                                choiceContentCalls[content]();
                            } catch {
                                generateChatGPT();
                            }
                        } else {
                            const services = document.getElementById('services');
                            contentArray.forEach((content) => {
                                content = content.trim();
                                if (filterContent(content)) {
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
                                }
                            });
                            $('#service-choice-modal').modal('show');
                        }

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

    const chatgpt_button = document.createElement('button');
    chatgpt_button.id = 'service-choice-button';
    chatgpt_button.setAttribute('onclick', 'generateChatGPT()');
    const chatgpt_div = document.createElement('div');
    chatgpt_div.className = 'service-card';
    const chatgpt_h2 = document.createElement('h2');
    chatgpt_h2.innerHTML = 'ChatGPT';
    const chatgpt_p = document.createElement('p');
    const chatgpt_small = document.createElement('small');
    chatgpt_small.innerHTML = '(Тексты)';
    chatgpt_p.appendChild(chatgpt_small);
    chatgpt_h2.appendChild(chatgpt_p);
    chatgpt_div.appendChild(chatgpt_h2);
    chatgpt_button.appendChild(chatgpt_div);

    const fusion_button = document.createElement('button');
    fusion_button.id = 'service-choice-button';
    fusion_button.setAttribute('onclick', 'generateFusion()');
    const fusion_div = document.createElement('div');
    fusion_div.className = 'service-card';
    const fusion_h2 = document.createElement('h2');
    fusion_h2.innerHTML = 'ImageFusion';
    const fusion_p = document.createElement('p');
    const fusion_small = document.createElement('small');
    fusion_small.innerHTML = '(Картинки)';
    fusion_p.appendChild(fusion_small);
    fusion_h2.appendChild(fusion_p);
    fusion_div.appendChild(fusion_h2);
    fusion_button.appendChild(fusion_div);

    services.appendChild(chatgpt_button);
    services.appendChild(fusion_button);
}

function resetContent() {
    let content = document.getElementById('content');
    if (content) {
        remove('#content');
    }
}

function filterContent(content) {
    let choice_services_array = Object.keys(choiceContentCalls);
    if (content in choice_services_array) {
        return content;
    }
}