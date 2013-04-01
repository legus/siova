$(document).on("ready", arranque);

function arranque(name) {
    $( "#id_lc2_fecha" ).datepicker({ dateFormat: "yy/mm/dd" });
    $('#busca').click(function(e) {
        e.preventDefault();
        qu = $('#q').val();
        $.getJSON("/buscar", { q:qu }, function(json){
            $("#results1").empty();
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
        nag = $('#id_lc1_nivel_agregacion').val();
        fec = $('#id_lc2_fecha').val();
        tin = $('#id_lc4_tipo_inter').val();
        tre = $('#id_lc4_tipo_rec').val();
        nin = $('#id_lc4_nivel_inter').val();
        $.getJSON("/busqueda", { tit:tit, idi:idi, nag:nag, fec:fec, tin:tin, tre:tre, nin:nin }, function(json){
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

    $('#btn_agr').click(function(e) {
        naut = $('#au_name').val();
        aaut = $('#au_last').val();
        raut = $('#au_rol').val();
        $.getJSON("/crearAutor", { naut:naut, aaut:aaut, raut:raut }, function(json){
            if (json.length != 0) {
                $.each(json, function(key,val){
                    $("#autores").append("<li>"+json[key]['fields']['nombres']+"</li>");
                });
            }else{
                $("#autores").append("<li>error</li>");
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