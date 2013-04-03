$(document).on("ready", arranque);

function arranque(name) {
    var autores=[]
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
        $("#error").css('display','none');
        naut = $('#au_name').val();
        aaut = $('#au_last').val();
        raut = $('#au_rol').val();
        if(naut.length>0 & aaut.length>0 & raut.length>0){
            var flag = false;
            $( "li" ).each(function( index ) {
                var t = $(this).text().split(" ");
                flag=validar(t,naut,aaut,raut);
            });
            if(flag){
                $("#error").html("Autor ya existe");
                $("#error").fadeIn();
            }else{
                $("#autores").append('<li id="autors'+naut+aaut+raut+'">'+ naut+' '+aaut+' - '+raut+'</li>');
                $("#autors"+naut+aaut+raut).append(function() {
                    return $('<span class="autori" id="'+naut+aaut+raut+'"> (-) </span>').click(function() {
                        var e=$(this).context.id;
                        $("#autors"+e).remove();
                    });
                });
                var a = naut+" "+aaut+" "+raut;
                autores.push(a);
                $('#au_name').val("");
                $('#au_last').val("");
                $('#au_rol').val("");
                $('#autores1').val(autores);
            }
        }else{
            $("#error").html("Debes digitar todos los campos del Autor");
            $("#error").fadeIn();
        }
    });
}

function validar(ar,nam,las,rol) {
    var b1=false;
    var b2=false;
    var b3=false;
    for (var i = 0; i < ar.length; i++) {
        if(ar[i]==nam){
            b1=true;
        }
        if(ar[i]==las){
            b2=true;
        }
        if(ar[i]==rol){
            b3=true;
        }        
    }
    if(b1 & b2 & b3){
        return true;
    }else{
        return false;
    }
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