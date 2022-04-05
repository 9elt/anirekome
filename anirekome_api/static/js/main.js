function Errors(status, msg){
    if(status == 405){KeyErrors(msg); return;}
    $('#status--message').html(msg);
    $('.mal_connect').removeClass('mal_loaded');
    $('#status--message').addClass('error');
    $('.user_connect--container').addClass('error--input');
    if(status == 403 || status == 404){ListErrors()}
    $("#user_name").on("change paste keyup", function(){
        if($('#status--message').hasClass('error')){RemoveErrors();}
    });
    $('.mal_link--input').addClass('mal_link--active_input');
    $('.nav_icon--edit').addClass('nav_icon--editing');
};

function ListErrors(){
    $('.username--input').addClass('error');
    $('.mal_link--input').addClass('error');
    $('.nav_icon--edit').addClass('error--input');
};

function KeyErrors(msg){
    $('.access--input').addClass('error');
    $('.mal_connect').removeClass('mal_loaded');
    $('#accesskey--message').html(msg);
    $('#accesskey--message').addClass('error');
    $("#access_key").on("change paste keyup", function(){
        if($('#accesskey--message').hasClass('error')){RemoveKeyErrors();}
    });
};

function RemoveErrors(){
    $('#status--message').html('MyAnimeList');
    $('#status--message').removeClass('error')
    $('.connect_link--input').removeClass('error');
    $('.user_connect--container').removeClass('error--input')
    $('.mal_link--input').removeClass('error');
    $('.nav_icon--edit').removeClass('error--input');
};

function RemoveKeyErrors(){
    $('.access--input').removeClass('error');
    $('#accesskey--message').html('Alpha Access Key');
    $('#accesskey--message').removeClass('error');  
};

function NavBar(){
    $('.bruger_icon').off('click').on('click', function(){
        $('.header_nav').toggleClass('header_nav--active');
        $('.burger_1').toggleClass('cross_1');
        $('.burger_2').toggleClass('cross_2');
        $('.burger_3').toggleClass('cross_3');
    });
};

function CloseNav(){
    $('.header_nav').removeClass('header_nav--active');
    $('.burger_1').removeClass('cross_1');
    $('.burger_2').removeClass('cross_2');
    $('.burger_3').removeClass('cross_3');
};

function Rekome(){

    if(matchMedia('(pointer:coarse)').matches){
        clicked = false;

        $('.del_icon').off('click').on('click',function(){
            if(clicked == false){
                $('.trash_animation').addClass('trash_animated');
                $('.del_icon').addClass('trash_color');
                clicked = true;
            }else{            
                $('.trash_animation').removeClass('trash_animated');
                $('.del_icon').removeClass('trash_color');
                clicked = false;
            }
        });
        
    }else{
        $('.del_icon').mouseenter(function(){
            $('.trash_animation').addClass('trash_animated');
            $('.del_icon').addClass('trash_color');
        });
        $('.del_icon').mouseleave(function(){
            $('.trash_animation').removeClass('trash_animated');
            $('.del_icon').removeClass('trash_color');
        }).mouseleave();
    }

    $('.arrow_icon--up').off('click').on('click', function(){PrevRekome();});
    $('.arrow_icon--down').off('click').on('click', function(){NextRekome();});

};

function PrevRekome(){
    $('.rekome').each(function(){
        if($(this).hasClass('rekome--active')){
            prev = $(this).prev();
            $('.arrow_icon--up').removeClass('arrow_icon--inactive');
            $('.arrow_icon--down').removeClass('arrow_icon--inactive');
            $(this).addClass('rekome--next');
            $('.rekome--next').removeClass('rekome--active');
            $(prev).removeClass('rekome--prev')
            $(prev).addClass('rekome--active')
            if($(prev).hasClass('rekome--first')){$('.arrow_icon--up').addClass('arrow_icon--inactive');}
            return false;
        };
    });
};

function NextRekome(){
    $('.rekome').each(function(){
        if($(this).hasClass('rekome--active')){
            next = $(this).next();
            $('.arrow_icon--up').removeClass('arrow_icon--inactive');
            $('.arrow_icon--down').removeClass('arrow_icon--inactive');
            $(this).addClass('rekome--prev');
            $('.rekome--prev').removeClass('rekome--active');
            $(next).removeClass('rekome--next')
            $(next).addClass('rekome--active')
            $(next).attr('style','');
            if($(next).hasClass('rekome--last')){$('.arrow_icon--down').addClass('arrow_icon--inactive');}
            return false;
        };
    });
};

function DisconnectUser(token){
    disconnect = false
    $('#disconnect_user').off('click').on('click', function(e){
        if(disconnect == true){return};
        disconnect = true;
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/disconnect",
            data: {
                csrfmiddlewaretoken: token,
                },
            success:function(data, textStatus, xhr) {
                if(data['status'] == 200){
                    $('.burger_icon--container').addClass('disabled');
                    $('#main_section').html(data['section']);
                    $('#nav_bar').html(data['nav']);
                    token = token;
                    CloseNav();
                }
            }
        });
    });
};

function ConnectUser(key, username, plantowatch, token){
    if($('.mal_connect').hasClass('mal_loaded')){return};
    if($('#connect_user').hasClass('error--input')){return};
    if(username == ''){return};
    ptw = plantowatch;

    $('.mal_connect').addClass('mal_loaded');
    $.ajax({
        type: "POST",
        url: "/rekome",
        data: {
            csrfmiddlewaretoken: token,
            'alphakey': key,
            'user': username,
            'ptw': ptw
            },
        success:function(data, textStatus, xhr) {
            if(data['status'] == 200){
                $('.burger_icon--container').removeClass('disabled');
                $('.mal_connect').removeClass('mal_loaded');
                $('#main_section').html(data['section']);
                $('#nav_bar').html(data['nav']);
                token = token;
                NavBar();Rekome();
            }else{Errors(data['status'], data['message']);}
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) { 
            Errors(errorThrown);
        }
    });
};

function TrashRekome(id, token){
    rekome = $('.rekome[data-id="'+id+'"]');
    if($('.rekomes--container').children('div').length == 1){
        NextRekome();
        $('.arrow_icon--up').addClass('arrow_icon--inactive');
        $('.arrow_icon--down').addClass('arrow_icon--inactive');
    }else if(rekome.hasClass('rekome--last') && $('.rekomes--container').children('div').length != 2){
        PrevRekome();
        $(rekome).prev().addClass('rekome--last');
        $('.arrow_icon--down').addClass('arrow_icon--inactive');
    }else{
        NextRekome();
        if($(rekome).hasClass('rekome--first')){
            $(rekome).next().addClass('rekome--first');
            $('.arrow_icon--up').addClass('arrow_icon--inactive');
        }
    }
    setTimeout(function(){
        $(rekome).remove();
        $.ajax({
            type: "POST",
            url: "/trash",
            data: {
                csrfmiddlewaretoken: token,
                'id': id
                },
            success: function(){
                if($('.rekomes--container').children('div').length == 1){
                    loadRekome(token);Rekome();
                }
            }
        });
    }, 500);


};

function RefreshUser(token){
    is_refreshing = false;
    $('.nav_icon--refresh').off('click').on('click', function(e){
        e.preventDefault();
        if(is_refreshing === true){return}
        is_refreshing = true;

        $('.mal_link').addClass('mal_loaded');
        $('.nav_icon--refresh').addClass('nav_icon--rotating');

        angle=90;
        const rotate_icon = setInterval(iconRotate, 300);
        function iconRotate(){
            $(".nav_icon--refresh")
                .css('-webkit-transform', 'rotate('+angle+'deg)')
                .css('-moz-transform', 'rotate('+angle+'deg)')
                .css('-ms-transform', 'rotate('+angle+'deg)');
            angle+=45;
        }

        $.ajax({
            type: "POST",
            url: "/refresh",
            data: {csrfmiddlewaretoken: token,},
            success:function(data, textStatus, xhr) {
                if(data['status'] == 200){
                    $('#main_section').html(data['section']);
                    $('#nav_bar').html(data['nav']);
                    token = token;
                    NavBar();Rekome();EndRefreshign();
                }else{Errors(data['status'], data['message']);}      
            },
            error:function(XMLHttpRequest, textStatus, errorThrown) { 
                Errors(errorThrown);EndRefreshign();
            }
        });

        function EndRefreshign(){
            clearInterval(rotate_icon);
            $('.mal_link').removeClass('mal_loaded');
            $('.nav_icon--refresh').removeClass('nav_icon--rotating');
            is_refreshing = false;
        }

    });
};

function loadRekome(token){

    $(".load_more").removeClass('hidden');
    const load_animate = setInterval(loadAnimetion, 500);
    function loadAnimetion(){$(".load_more").toggleClass('loading_more');}

    $.ajax({
        type: "POST",
        url: "/more",
        data: {csrfmiddlewaretoken: token,},
        success:function(data, textStatus, xhr) {
            if(data['status'] == 200){
                clearInterval(load_animate);
                $(".load_more").addClass('hidden');
                setTimeout(function(){
                    $('.rekomes--container').append(data['section']);
                    $('.arrow_icon--down').removeClass('arrow_icon--inactive');
                    token = token;
                    NavBar();Rekome();
                }, 200);
            }else{
                clearInterval(load_animate);
                $(".load_more").html('NO MORE REKOMES');                
            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) { 
            return false;                        
        }
    });
};