$(document).on("ready", arranque);

function arranque(name) {
    $('#busca').click(function(e) {
        e.preventDefault();
        qu = $('#q').val();
        $.getJSON("/buscar", { q:qu }, function(json){
            $("#results1").empty();
            console.log("entro");
            if (json.length != 0) {
                obj=json.slice(0,(json.length/2));
                esp=json.slice(json.length/2,json.length);
                $.each(obj, function(key,val){
                    $("#results1").append("<li><a href='/objeto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");                
                });
            }else{
                $("#results1").html('<h3>La búsqueda no arrojó resultados</h3>');
            }
        });
    });

    $('#busqueda').click(function(e) {
        e.preventDefault();
        tit = $('#id_lc1_titulo').val();
        idi = $('#id_lc1_idioma').val();
        $.getJSON("/busqueda", { tit:tit, idi:idi }, function(json){
            $("#results2").empty();
            if (json.length != 0) {
                obj=json.slice(0,(json.length/2));
                esp=json.slice(json.length/2,json.length);
                $.each(obj, function(key,val){
                    $("#results2").append("<li><a href='/objeto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");                
                });
            }else{
                $("#results2").html('<h3>La búsqueda no arrojó resultados</h3>');
            }
        });
    });
}

$(document).ajaxStart(function() {
    $('#cargando').show();
}).ajaxStop(function() {
    $('#cargando').hide();
});


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
var csrftoken = getCookie('csrftoken');
//console.log(csrftoken)


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
//function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
//    var host = document.location.host; // host + port
//    var protocol = document.location.protocol;
//    var sr_origin = '//' + host;
//    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
//    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
//        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
//        !(/^(\/\/|http:|https:).*/.test(url));
//}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


/* Ajax and formFields erros*/
function apply_form_field_error(fieldname, error) {
    var input = $("#id_" + fieldname),
        container = $("#div_id_" + fieldname),
        error_msg = $("<span />").addClass("help-inline ajax-error").text(error[0]);

    container.addClass("error");
    error_msg.insertAfter(input);
}

function clear_form_field_errors(form) {
    $(".ajax-error", $(form)).remove();
    $(".error", $(form)).removeClass("error");
}