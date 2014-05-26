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
    	dataType: 'json',
        success: function(json) {
            $.each(json, function(server_id, sensors) {
                $.each(sensors, function(sensor_id, sensor_data) {
                    $cell = $('#srv'+server_id+"-snr"+sensor_id);
                    if(sensor_data)
                        $cell.html('<i class="glyphicon glyphicon-ok text-success"></i>');
                    else
                        $cell.html('<i class="glyphicon glyphicon-remove text-danger"></i>');
                })
            })
        }
    });
    // Авторефреш каждые 3 секунды
    //setTimeout(updateTable, 3000);
}
//$(function() {
//    updateTable();
//});
// Рефреш по клику на заголовок
$(document).on("click", "h1", updateTable)