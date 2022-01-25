let media_file = [];
let image_list = [];
let form_data = new FormData();


function getCookie(name) {

    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

let csrftoken = getCookie('csrftoken');

$(document).on('click', '#submit-mou', function (e) {


   

    mp4_file = $('#mp4')[0].files[0]
    form_data.append('mp4_file', mp4_file)
 
    // let imageLen = $('#image')[0].files.length;
    // for (let i = 0; i < imageLen; i++) {

    //     image_list = $('#image')[0].files[i];
    //     form_data.append('image_list', image_list)
    // }
    form_data.append('mou_title_input', $("#mou_title_input").val())
    form_data.append('mou_content_input', $("#mou_content_input").val())
    form_data.append('mou_date_input', new Date($("#mou_date_input").val()).toISOString())

    $.ajaxSetup({

        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({

        url: "/index/mou",
        type: 'POST',
        contentType: false,
        processData: false,
        data: form_data,
        success: function (data) {
            if (data.result) {
                alert("之前已經有一筆創建的讀書會名稱已重複")
                //這裡拿到後端傳過來的exam_id，寫進data裡面
            }
            else {
                window.location.href = '/home'
            }
        }
    });
    e.preventDefault();
})