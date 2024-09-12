$(document).ready(function(){
  "use strict";

  var window_width = $(window).width(),
  window_height = window.innerHeight,
  header_height = $(".default-header").height(),
  header_height_static = $(".site-header.static").outerHeight(),
  fitscreen = window_height - header_height;

  $(".fullscreen").css("height", window_height)
  $(".fitscreen").css("height", fitscreen);

  if(document.getElementById("default-select")){
        $('select').niceSelect();
  };

  $('.img-pop-up').magnificPopup({
      type: 'image',
      gallery:{
      enabled:true
      }
  });

  jQuery(document).ready(function($) {
  $('.popup-content').magnificPopup({
      type: 'inline'
  });
  });

  $('.play-btn').magnificPopup({
      type: 'iframe',
      mainClass: 'mfp-fade',
      removalDelay: 160,
      preloader: false,
      fixedContentPos: false
  });


  //  Counter Js 

  $('.counter').counterUp({
      delay: 10,
      time: 1000
  });


  // Initiate superfish on nav menu
  $('.nav-menu').superfish({
    animation: {
      opacity: 'show'
    },
    speed: 400
  });

  // Mobile Navigation
  if ($('#nav-menu-container').length) {
    var $mobile_nav = $('#nav-menu-container').clone().prop({
      id: 'mobile-nav'
    });
    $mobile_nav.find('> ul').attr({
      'class': '',
      'id': ''
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" id="mobile-nav-toggle"><i class="lnr lnr-menu"></i></button>');
    $('body').append('<div id="mobile-body-overly"></div>');
    $('#mobile-nav').find('.menu-has-children').prepend('<i class="lnr lnr-chevron-down"></i>');

    $(document).on('click', '.menu-has-children i', function(e) {
      $(this).next().toggleClass('menu-item-active');
      $(this).nextAll('ul').eq(0).slideToggle();
      $(this).toggleClass("lnr-chevron-up lnr-chevron-down");
    });

    $(document).on('click', '#mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
      $('#mobile-body-overly').toggle();
    });

    $(document).click(function(e) {
      var container = $("#mobile-nav, #mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
          $('#mobile-body-overly').fadeOut();
        }
      }
    });
  } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
    $("#mobile-nav, #mobile-nav-toggle").hide();
  }

  // Smooth scroll for the menu and links with .scrollto classes
  $('.nav-menu a, #mobile-nav a, .scrollto').on('click', function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        var top_space = 0;

        if ($('#header').length) {
          top_space = $('#header').outerHeight();

          if( ! $('#header').hasClass('header-fixed') ) {
            top_space = top_space;
          }
        }

        $('html, body').animate({
          scrollTop: target.offset().top - top_space
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu').length) {
          $('.nav-menu .menu-active').removeClass('menu-active');
          $(this).closest('li').addClass('menu-active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('#mobile-nav-toggle i').toggleClass('lnr-times lnr-bars');
          $('#mobile-body-overly').fadeOut();
        }
        return false;
      }
    }
  });


    $(document).ready(function() {

    $('html, body').hide();

        if (window.location.hash) {

        setTimeout(function() {

        $('html, body').scrollTop(0).show();

        $('html, body').animate({

        scrollTop: $(window.location.hash).offset().top

        }, 1000)

        }, 0);

        }

        else {

        $('html, body').show();

        }

    });
  

  // Header scroll class
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  })


    $('.active-course-carusel').owlCarousel({
        items:3,
        loop:true,
        margin:30,
        dots: true,
        nav:true,
        navText: ["<span class='lnr lnr-arrow-up'></span>",
        "<span class='lnr lnr-arrow-down'></span>"],        
            responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1,
            },
            768: {
                items: 2,
            },
            900: {
                items: 3,
            }

        }
    });

        $('.active-tstimonial-carusel').owlCarousel({
        items:3,
        margin:30,
        autoplay:true,
        loop:true,
        dots: true,       
            responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1,
            },
            768: {
                items: 2,
            },
            900: {
                items: 3,
            }

        }
    });




    //  Start Google map 

            // When the window has finished loading create our google map below

            if(document.getElementById("map")){
            
            google.maps.event.addDomListener(window, 'load', init);
        
            function init() {
                // Basic options for a simple Google Map
                // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
                var mapOptions = {
                    // How zoomed in you want the map to start at (always required)
                    zoom: 11,

                    // The latitude and longitude to center the map (always required)
                    center: new google.maps.LatLng(40.6700, -73.9400), // New York

                    // How you would like to style the map. 
                    // This is where you would paste any style found on Snazzy Maps.
                    styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
                };

                // Get the HTML DOM element that will contain your map 
                // We are using a div with id="map" seen below in the <body>
                var mapElement = document.getElementById('map');

                // Create the Google Map using our element and options defined above
                var map = new google.maps.Map(mapElement, mapOptions);

                // Let's also add a marker while we're at it
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(40.6700, -73.9400),
                    map: map,
                    title: 'Snazzy!'
                });
            }
    }


        $(document).ready(function() {
            $('#mc_embed_signup').find('form').ajaxChimp();
        });
 });

 const choiceContentCalls = {
  'ChatGPT': generateChatGPT,
  'ImageFusion': generateFusion,
}

const remove = (sel) => document.querySelectorAll(sel).forEach(el => el.remove());

function generateAssistentRequest() {
  /*let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      //generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>';

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
                  localStorage.setItem('isAssistent', true);
              }
          )
        });
  }
  */
  $('#service-choice-modal').modal('show');
}

function generateChatGPT() {
  try {
    $('#service-choice-modal').modal('hide');
  } catch(e) {
    null;
  }
  resetContent();
  let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerText = 'Идёт генерация ...';

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
                  contentDiv.style.overflow = 'auto';
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
  try {
    $('#service-choice-modal').modal('hide');
  } catch(e) {
    null;
  }
  resetContent();
  let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerText = 'Идёт генерация ...';

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
                try{
                  resetPreGenerateButton();
                  let image = data['image'][0];
                  let fadeImage = document.getElementById('fusion-result');
                  fadeImage.style.backgroundImage = `url('data:image/png;base64, ${image}')`;
                  fadeImage.style.maxWidth = '100%';

                  /*
                  let contentDiv = document.getElementById('content-div');
                  const contentP = document.createElement('p');
                  contentDiv.style.overflow = 'hidden';
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
                  */
                } catch(e) {
                  return alert(`Ошибка: ${e}`);
                }
              }
          )
        });
  }
}

function generatePlusVector() {
  resetContent();
  let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>';

      let data = new FormData();
      data.append('prompt', textArea.val());

      fetch('generate_plusvector', {
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
                  let contentDiv = document.getElementById('content-div');
                  const contentP = document.createElement('p');
                  contentDiv.style.overflow = 'hidden';
                  contentP.id = 'content';
                  const carouselPlusVector = document.getElementById('carouselPlusVectorIndicators');
                  const carouselInner = carouselPlusVector.getElementsByClassName('carousel-inner')[0];
                  let activeItem = 0;
                  data['images'].forEach((image) => {
                      activeItem += 1;
                      let carouselItem = document.createElement('div');
                      if (activeItem == 1){
                          carouselItem.className = 'carousel-item active';
                      } else {
                          carouselItem.className = 'carousel-item';
                      }
                      let carouselImage = document.createElement('img');
                      carouselImage.className = 'd-block w-100';
                      carouselImage.src = image;
                      carouselImage.width = 200;
                      carouselImage.height = 240;
                      carouselItem.appendChild(carouselImage);
                      carouselInner.appendChild(carouselItem);
                      contentP.appendChild(carouselPlusVector);
                      contentDiv.appendChild(contentP);
                  })
                  scrollIntoView('content-div');
              }
          )
        });
  }
}

function generateChatGPTPlus() {
  resetContent();
  let textArea = $('textarea');
  if (textArea.val() == "") {
      return alert('Поле не должно оставаться пустым!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerHTML = '<span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>';

      let data = new FormData();
      data.append('content', textArea.val());

      fetch('generate_chatgptplus', {
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
                  contentDiv.style.overflow = 'auto';
                  contentP.id = 'content';
                  contentP.innerHTML = content;
                  contentDiv.appendChild(contentP);
                  scrollIntoView('content-div');
              }
          )
      });
  }
}

function generateSmartCamera() {
  resetContent();
  var file = document.querySelector('input[type=file]').files[0];
  if (file == undefined) {
      return alert('Загрузите изображение для определения!');
  } else {
      let generateBtn = document.getElementById('pre-generate-btn');
      generateBtn.disabled = true;
      generateBtn.innerText = 'Идёт генерация ...';

      let data = new FormData();
      data.append('file', file);

      fetch('generate_smartcamera', {
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
                  resetPreGenerateButton(is_check_button=true);
                  let content = data['content'];
                  if (content == null) {
                      content = 'Не удалось распознать объект!';
                  }
                  let contentDiv = document.getElementById('content-div');
                  const contentP = document.createElement('p');
                  contentDiv.style.overflow = 'auto';
                  contentP.id = 'content';
                  contentP.innerHTML = `<span class="badge text-bg-info">Результат:</span> ${content}<br>`;
                  contentDiv.appendChild(contentP);
                  scrollIntoView('content-div');
              }
          )
        });
  }
}

function scrollIntoView(id) {
  document.getElementById(id).scrollIntoView({ block: 'center', behavior: 'smooth' });
}

function resetPreGenerateButton(is_check_button=false) {
  $('#service-choice-modal').modal('hide');
  let generateBtn = document.getElementById('pre-generate-btn');
  generateBtn.disabled = false;
  if (is_check_button) {
      generateBtn.innerHTML = 'Определить';
  } else {
      generateBtn.innerHTML = 'Генерировать';
  }
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

  localStorage.removeItem('isAssistent');
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

$('#close-popup-btn').on('click', function() {
  $('#service-choice-modal').modal('hide');
})
