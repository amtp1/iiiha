function generateAssistantRequest() {
    $('#content').remove();
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerText = 'Идёт генерация ...';

        // Assistant ChatGpt generate request (POST)
        $.post('generate_assistant_request', {'content': textArea.val()},
            function(data) {
                resetPreGenerateButton();
                let content = data['choices'][0]['message']['content'];
                    try {
                      if (content == 'chatgpt') {
                        generateChatGPT();
                      } else if (content == 'fusion') {
                        console.log(user_is_auth);
                        if (user_is_auth == 'False') {
                          generateFusion();
                        } else {
                          generateFlux();
                        }
                      } else if (content == 'smartcamera') {
                        window.location.replace('smartcamera');
                      } else if (content == 'menu') {
                        $('#service-choice-modal').modal('show');
                      } else {
                        let contentDiv = document.getElementById('content-div');
                        const contentP = document.createElement('p');
                        contentDiv.style.overflow = 'auto';
                        contentP.id = 'content';
                        contentP.innerHTML = convertMarkdownToHTML(content);
                        contentDiv.appendChild(contentP);
                        scrollIntoView('content-div');
                      }
                    } catch (e) {
                      alert(e);
                    }
                    localStorage.setItem('isAssistant', true);
            }
        )
    }
}

function generateChatGPT() {
    try {
      $('#service-choice-modal').modal('hide');
    } catch(e) {
      null;
    }
    $('#content').remove();
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerText = 'Идёт генерация ...';

        // ChatGpt generate request (POST)
        $.post('generate_chatgpt', {'content': textArea.val()},
          function(data){
            try{
                resetPreGenerateButton();
                let content = data['choices'][0]['message']['content'];
                let contentDiv = document.getElementById('content-div');
                const contentP = document.createElement('p');
                contentDiv.style.overflow = 'auto';
                contentP.id = 'content';
                contentP.innerHTML = convertMarkdownToHTML(content);
                contentDiv.appendChild(contentP);
                scrollIntoView('content-div');
            } catch(e) {
                return alert(`Ошибка: ${e}`);
            }
        });
    }
}

function generateFusion() {
    try {
      $('#service-choice-modal').modal('hide');
    } catch(e) {
      null;
    }
    let textArea = $('textarea');
    if (textArea.val() == "") {
        return alert('Поле не должно оставаться пустым!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerText = 'Идёт генерация ...';

        $.post('generate_fusion', {'prompt': textArea.val()},
            function(data) {
                try{
                    resetPreGenerateButton();
                    let image = data['image'][0];
                    const parent = document.querySelector('.info-content');
                    let fadeImage = document.querySelector('#fade-in-image-result');
                    let imageResult = document.createElement('img');
                    imageResult.id = 'fade-in-image-result';
                    imageResult.src = `data:image/png;base64, ${image}`;
                    imageResult.style.width = '100%';
                    imageResult.style.height = '310px';
                    imageResult.style.borderRadius = '8px';
                    parent.replaceChild(imageResult, fadeImage);
                } catch(e) {
                    return alert(`Ошибка: ${e}`);
                }
            }
        )
    }
}

function generateSmartCamera() {
    var file = document.querySelector('input[type=file]').files[0];
    if (file == undefined) {
        return alert('Загрузите изображение для определения!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerText = 'Идёт генерация ...';

        let data = new FormData();
        data.append('file', file);

        $.post({url: 'generate_smartcamera',
                data: data,
                processData: false,
                contentType: false,
                success: function(data) {
                    resetPreGenerateButton(is_check_button=true);
                    let asst_name = data['asst_name'] 
                    let content = data['content'];
                    let yandex_content = data['yandex_data'];
                    if (content == null && yandex_content == null) {
                        content = 'Не удалось распознать объект!';
                    } else if (content == null && yandex_content != null) {
                        content = `<b>Товар: ${yandex_content['name']}</b>
                                    Минимальная цена: ${yandex_content['minPrice']}
                                    Максимальная цена: ${yandex_content['maxPrice']}`;
                    } else if (content != null && yandex_content != null){
                        content += `<br><br><b>Товар: ${yandex_content['name']}</b>
                                    Минимальная цена: ${yandex_content['minPrice']} руб.
                                    Максимальная цена: ${yandex_content['maxPrice']} руб.`;
                    }
                    let contentDiv = document.getElementById('content-div');
                    const contentP = document.createElement('p');
                    contentDiv.style.overflow = 'auto';
                    contentP.id = 'content';
                    contentP.innerHTML = `<span class="badge text-bg-success">Подключен: ${asst_name}${yandex_content ? ' и Товаровед' : ''}</span><br>
                    <span class="badge text-bg-info"><h5>Результат:</h5></span> ${convertMarkdownToHTML(content)}<br>`;
                    contentDiv.appendChild(contentP);
                    scrollIntoView('content-div');
                }
        })
    }
}

function generateFreeSmartCamera() {
  var file = document.querySelector('input[type=file]').files[0];
    if (file == undefined) {
        return alert('Загрузите изображение для определения!');
    } else {
        let generateBtn = document.getElementById('pre-generate-btn');
        generateBtn.disabled = true;
        generateBtn.innerText = 'Идёт генерация ...';

        let data = new FormData();
        data.append('file', file);

        $.post({url: 'generate_freesmartcamera',
                data: data,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data);
                    resetPreGenerateButton(is_check_button=true);
                    let contentDiv = document.getElementById('content-div');
                    const contentP = document.createElement('p');
                    contentDiv.style.overflow = 'auto';
                    contentP.id = 'content';
                    contentP.innerHTML = `<span class="badge text-bg-info"><h5>Результат:</h5></span><br><b>Товар: ${data['name']}</b><br>
                                          Минимальная цена: ${data['minPrice']} руб.<br>
                                          Максимальная цена: ${data['maxPrice']} руб.`;
                    contentDiv.appendChild(contentP);
                    scrollIntoView('content-div');
                }
        })
    }
}

function generateFlux() {
  let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerText = 'Идёт генерация ...';

      $.post(
        'generate_flux', {'prompt': textArea.val()},
          function(data) {
            try{
              resetPreGenerateButton();
              resetPreGenerateButton();
              let image = data['images'][0]['url'];
              const parent = document.querySelector('.info-content');
              let fadeImage = document.querySelector('#fade-in-image-result');
              let imageResult = document.createElement('img');
              imageResult.id = 'fade-in-image-result';
              imageResult.src = image;
              imageResult.style.width = '100%';
              imageResult.style.height = '310px';
              imageResult.style.borderRadius = '8px';
              parent.replaceChild(imageResult, fadeImage);
            } catch(e) {
              return alert(`Ошибка: ${e}`);
            }
          }
      )
  }
}

function signUp() {
    $.post('signup', {'email': $("input[name=email]").first().val(),
                      'password': $("input[name=password]").first().val(),
                      'retry_password': $("input[name=retry_password]").first().val()},
      function(data) {
        if (data['status_code'] == 200) {
          document.cookie = `auth_temp_data=${JSON.stringify(
            {'email': $("input[name=email]").first().val(),
             'password': $("input[name=password]").first().val(),
             'retry_password': $("input[name=retry_password]").first().val()
          })}`;
          return window.location.replace('tariff');
        } else if (data['status_code'] == 400) {
          let alertDanger = $('#auth-alert');
          alertDanger.text(data['message']);
          alertDanger.show();
        }}
    )
}

function signIn() {
    $.post('signin', {'email': $("input[name=email]").first().val(),
                      'password': $("input[name=password]").first().val()},
      function(data) {
        if (data['status_code'] == 200) {
          return window.location.replace('/');
        } else if (data['status_code'] == 400) {
          let alertDanger = $('#auth-alert');
          alertDanger.text(data['message']);
          alertDanger.show();
        }}
    )
}

function logOut() {
    $.post('logout', {},
      function(data) {
        if (data['status_code'] == 200)
          return window.location.replace('/');
      }
    )
}

function selectTariff(tariff_id) {
    $.post('select_tariff', {'tariff_id': tariff_id}, function(data) {
      if (data['status_code'] == 200)
        return window.location.replace('/');
    })
}