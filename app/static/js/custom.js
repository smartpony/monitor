// --- АВТОРЕФРЕШ СТРАНИЦЫ ----------------------
//$(document).ready(function() {
//    setInterval(function () {
//        $('#monitor-table').load("http://localhost:5000/update");  
//    }, 3000);
//});

// --- ВАЛИДАЦИЯ ДОБАВИЛЕНИЯ СЕРВЕРА ------------
function addSrvValidate(event) {
    res = true;

    // Введено ли имя сервера
    var $name = $("#name");
    if(!$name.val()) {
        $name.css({
            "border":"1px solid #f06565",
            "boxShadow":"0 0 1px 1px #f5b3b3"
        });
        res = false;
    }

    // Введён ли ip-адрес
    var $ip = $("#ip");
    if(!$ip.val()) {
        $ip.css({
            "border":"1px solid #f06565",
            "boxShadow":"0 0 1px 1px #f5b3b3"
        });
        res = false;
    }

    return res;
}
// server_add
$(document).on("submit", "#server-add-form", addSrvValidate);

// --- СНЯТИЕ ВЫДЕЛЕНИЯ -------------------------
function postingFormUnmark(event) {
  if($(this).val())
    $(this).css({
        "border": "1px solid #abadb3",
        "boxShadow": ""
    });
}
// server_add
$(document).on("keyup", "#name, #ip", postingFormUnmark);

// --- AJAX-ФУНКЦИЯ ДЛЯ ОБНОВЛЕНИЯ ТАБЛИЦЫ ------
function updateTable(event) {
    $.ajax({
    	url: '/index-ajax',
    	dataType: 'json'
    }).done(function(json) {
        alert(json.term11);
    }).fail(function() {
    	alert("Ajax fail!");
    });
}

$(document).on("click", "h1", updateTable);