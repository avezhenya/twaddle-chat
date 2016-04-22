var isStoped = false;
var currentUser = null;
var currentRoom = null;
var preg = null;
var lang = 'en';
var ignoreList = [];
var userList= [];
var locales = {
    'en': {
        'submit':'Send',
        'placeholder':'Your text here...',
        'login':'You are not authorized!',
        'save':'Save!',
        'settings': {
            'showtime': 'Show time',
            'me':'For me',
            'my':'My messages'
        }
    },
    'ru': {
        'submit':'Отправить',
        'placeholder':'Текст сообщения...',
        'login':'Вы не авторизованы!',
        'save':'Сохранить!',
        'settings': {
            'showtime': 'Показать время',
            'me':'Мне',
            'my':'Мои сообщения'
        }
    }
};
$(document).ready(function () {
     //iframe detection
    //if (window.self === window.top) {
    //
    //}

    currentUser = '@'+getParameterByName('u');
    currentRoom = getParameterByName('r');
    preg = new RegExp('[^\w]?\\'+currentUser+'([^\w]+|$)');
    // locales
    lang = currentRoom.substr(0,2).toLowerCase();
    if (!locales[lang]) lang = 'en';
    $('#message').attr('placeholder', locales[lang]['placeholder']);
    $('.form-submit').html(locales[lang]['submit']);
    $('#settings_showTime_lbl').html(locales[lang]['settings']['showtime']);
    $('.settings_lbl_color').each(function(){
        $(this).html(locales[lang]['settings'][$(this).attr('data-rel')]);
    });
    $('#saveIgnore').val(locales[lang]['save']);

    if (!window.console) window.console = {};
    if (!window.console.log)
        window.console.log = function () {};
    $('.handlerWrap').hide();
    if (currentUser.length > 1) {
        $('.handlerWrap').on('click', function(){
            $('.smile-list-wrap, .settings-wrap').removeClass('active');
            $('.handlerWrap').hide();
        });
        $('body').on('keyup', function(e){
            if (e.keyCode == 27) {
                $('.smile-list-wrap, .settings-wrap').removeClass('active');
                $('.handlerWrap').hide();
                return false;
            }
        });
        $("#messageform")
            .on("submit", function () {
                newMessage($(this));
                return false;
            })
            .on("keypress", function (e) {
                if (e.keyCode == 13) {
                    newMessage($(this));
                    return false;
                }
            });
        $('.form-submit').on('click',function(){ newMessage($("#messageform")); return false; });
        // colorize messages
        $('.from').each(function(){
            if ($(this).html() == currentUser) {
                $(this)
                    .addClass('myMessage')
                    .parent()
                    .find('.message')
                    .addClass('myMessage');
            }
            else {
                $(this)
                    .bind('click',fromHandler)
                    .css('cursor','pointer');
            }
        });
        $('.message').each(function(){
            if (preg.test($(this).html())) {
                $(this).addClass('meMessage');
                $(this).parent().find('.from').addClass('meMessage');
            }
        });
        $('.time').each(function(){
            $(this).html((new Date($(this).attr('data-rel')*1000)).HHii());
        });

        $('#settings_showTime').bind('click',function(){
            $.cookie('showTime',$('#settings_showTime').prop('checked'),{path:'/'});
            showTime();
        });
        $('.online').click(function(e){showUserList(true);});
        $('#saveIgnore').click(function(e){saveIgnoreList();});
        showUserList(true, true);

        if ($.cookie('showTime') && $.cookie('showTime') != 'false') $('#settings_showTime')[0].checked = true;
        showTime();

        $('.smile-link').on('click', function(e){
            e.preventDefault();
            $('.smile-list-wrap').toggleClass('active');
            $('.handlerWrap').show();
        });

        $('.settings-link, .close-settings').on('click', function(e){
            e.preventDefault();
            $('.settings-wrap').toggleClass('active');
            $('.handlerWrap').toggle();
        });

        $('.myColorList a').bind('click',function(){
            setMyMessageColor($(this).css('background-color'));
            $('.myColorList a.active').removeClass('active');
            $(this).addClass('active');
        });
        $('.meColorList a').bind('click',function(){
            setMeMessageColor($(this).css('background-color'));
            $('.meColorList a.active').removeClass('active');
            $(this).addClass('active');
        });
        if ($.cookie('myMessageColor')) {
            $('.myColorList a').each(function(){
                if ($(this).css('background-color') == $.cookie('myMessageColor'))
                    $(this).click();
            });
        }else $($('.myColorList a')[0]).click();
        if ($.cookie('meMessageColor')){
            $('.meColorList a').each(function(){
                if ($(this).css('background-color') == $.cookie('meMessageColor'))
                    $(this).click();
            });
        }else $($('.meColorList a')[1]).click();

    } else {
        $('.smile-link, .settings-link, .online').addClass('none');
        $("#message").attr('disabled','disabled');
        $('.form-submit').html(locales[lang]['login']).bind('click',function(e){e.preventDefault();return false;});
        $('#message, .form-submit').click(function(){
           if (parent && parent.showSignUpForm) parent.showSignUpForm();
        });
        showTime();
    }

    $('.btn-stop').bind('click', function () {
        $(this).addClass('resume-link');//.removeClass('stop-link');
        // reload if need to resulme chat.
        if (isStoped) window.location.reload();
        else {
            isStoped = true;
            updater.socket.close();
        }
    });

    $("#message").select();
    updater.start();

    // scroll list
    $('.wrapper').scrollTop($('#chat-lines').height());


    function chatHeight(){
        var $chatLines = $('.chat-scroll');
        $chatLines.height('auto');
        $chatLines.height(($('.chat-iframe-inner').height() - $('.comment-form').outerHeight()+10).toFixed());
        $chatLines.mCustomScrollbar({
            theme:"minimal-dark",
            scrollInertia: 0,
            callbacks:{
                onUpdate:function(){
                    $chatLines.mCustomScrollbar("scrollTo", 'bottom');
                }
            }
        });
    }
    chatHeight();
    $(window).resize(function(event) {
        chatHeight();
    }).load(function(event) {
        chatHeight();
    });
});

function newMessage(form) {
    var message = form.formToDict();
    if (message.body == "" || updater.socket.readyState == 3) {
        form.find("textarea").val("").select();
        return;
    }
    // send message to server socket.send()
    updater.socket.send(JSON.stringify(message));
    form.find("textarea").val("").select();
    $('.handlerWrap').trigger('click');
}

var updater = {
    socket: null,

    start: function () {
        var url = "ws://" + location.host + "/chatsocket" + location.search;
        updater.socket = new WebSocket(url);
        // wait response from server socket.onmessage()
        updater.socket.onmessage = function (event) {
            var message = JSON.parse(event.data);
            if ('len' in message) $('.online').html(message['len']);
            else updater.showMessage(message);
        };
    },

    showMessage: function (message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        var from  = node.find('.from');
        if ($.inArray(from.html(),ignoreList) != -1) return;
        $('#chat-lines').append(node);
        if (from.html() == currentUser) {
            from
                .addClass('myMessage')
                .parent()
                    .find('.message')
                    .addClass('myMessage');
        }
        else {
            from
                .bind('click',fromHandler)
                .css('cursor','pointer');
        }
        var msg = node.find('.message');
        if (preg.test(msg.html())) {
            msg.addClass('meMessage');
            msg.parent().find('.from').addClass('meMessage');
        }
        var time = node.find('.time');
        time.html((new Date(time.attr('data-rel')*1000)).HHii());
    }

};

jQuery.fn.formToDict = function () {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;

};

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function fromHandler(){
    var currentText = $('#message').val();
    if ($.trim(currentText)) currentText += " ";
    currentText += $(this).html();
    $('#message')
        .focus()
        .val('')
        .val(currentText+', ');
}

function showTime(){
    if ($.cookie('showTime') && $.cookie('showTime') != 'false')
        $('<style>span.time {display: inline;}</style>').appendTo('head');
    else
        $('<style>span.time {display: none;}</style>').appendTo('head');
}

Date.prototype.HHii = function(){
    var HH = this.getHours().toString();
    var ii = this.getMinutes().toString();
    return (HH[1] ? HH : "0" + HH[0]) + ':' + (ii[1] ? ii : "0" + ii[0]);
};

function setMyMessageColor(color){
    $('<style>.myMessage{color: '+color+';}</style>').appendTo('head');
    $.cookie('myMessageColor', color, { path: '/' });
}
function setMeMessageColor(color){
    $('<style>.meMessage{color: '+color+';}</style>').appendTo('head');
    $.cookie('meMessageColor', color, { path: '/' });
}

function addSmile(smile) {
    var currentText = $('#message').val();
    $('#message')
        .focus()
        .val('')
        .val(currentText+ ' ' + smile + ' ');
}

function showUserList(flag, ignore){
    $('.user-list li').remove();
    if (flag) {
        $.ajax({
            url: '/ignore',
            method: 'get',
            data: {'user': currentUser.substr(1,currentUser.length), 'room': currentRoom},
            success: function (data) {
                try {
                    data = JSON.parse(data)
                } catch (e) {
                }
                if (data.ignore) ignoreList = data.ignore;
                if (data.users_list) userList = data.users_list;
                $('.from').each(function(){
                    if ( $.inArray($(this).html(), ignoreList) != -1){
                        $(this).parent().remove();
                    }
                });
                if (!ignore) showUserList(false);
            }
        });
    }else{
        $.each(userList, function(i,item){
            if ('@'+item != currentUser) {
                var li = $('<li>');
                var checkbox = $('<input type="checkbox" class="form-checkbox ignoreItem" style="margin-right: 3px">');
                checkbox.prop('checked', $.inArray('@'+item, ignoreList) != -1);
                var span = $('<span class="user-li">');
                span.html(item);
                $('.user-list').append(li.append(checkbox, span));
            }
        });
        $('.online').unbind('click');
        $('.user-list-wrap').show();
    }
}
function saveIgnoreList(){
    ignoreList = [];
    $('.ignoreItem').each(function(){
        if ($(this).prop('checked')){
            ignoreList.push('@'+$(this).parent().find('.user-li').html());
        }
    });
    $.ajax({
        url: '/ignore',
        method: 'post',
        data: {'user': currentUser.substr(1,currentUser.length),
               'ignore': JSON.stringify(ignoreList)},
        success: function (data) {
            if (data.status) {
                $('.user-list-wrap').hide();
                $('.online').click(function(e){showUserList(true);});
            }
        }
    }).error(function(e){console.log(e)});
}