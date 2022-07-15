const Chat = (function(){
    const myName = "USER";
 
    // init 함수
    function init() {
        // enter 키 이벤트
        $(document).on('keydown', 'body', function(e){
            if(e.keyCode == 13 && !e.shiftKey  && $('input[type=text]').val() != '') {
                var req = $('input[type=text]').val()
                $('input[name=question]').val(req);
                $.ajax({
                    type:'get',
                    url: "/main/chat",
                    dataType: 'json',
                    data: {'req':req},

                    success:function(data){
                        var ans = data['ans']
                        if (ans == 'kozy_return') {
                            window.location.href = '/main';
                        } 
                        else if (ans == 'mypage_return') {
                            window.location.href = '/details';
                        } 
                        else if (ans == 'bookmark_return') {
                            window.location.href = '/details/bookmark';
                        } 
                        else {
                            e.preventDefault();
                            
                            $('input[name=answer]').val(ans);
                            // 메시지 전송
                            sendMessage(req, ans);
                            
                            // 입력창 clear
                            clearTextarea();
                        }
                    }
                });
            }
        });
    }
 
    // 메세지 태그 생성
    function createMessageTag(LR_className, senderName, message) {
        // 형식 가져오기
        let chatLi = $('div.chat.format ul li').clone();
 
        // 값 채우기
        chatLi.addClass(LR_className);
        chatLi.find('.sender span').text(senderName);
        chatLi.find('.message span').text(message);
 
        return chatLi;
    }
 
    // 메세지 태그 append
    function appendMessageTag(LR_className, senderName, message) {
        const chatLi = createMessageTag(LR_className, senderName, message);
 
        $('div.chat:not(.format) ul').append(chatLi);

         // 스크롤바 아래 고정
         $('body').scrollTop($('body').prop('scrollHeight'));
    }
 
    // 메세지 전송
    function sendMessage(message, ans) {
        user = $('input[type=hidden]').val()
        const data = {
            "senderName"    : user,
            "message"        : message
        };
 
        appendMessageTag("right", data.senderName, data.message);

        answer(ans);
    }
 
    // 메세지 입력박스 내용 지우기
    function clearTextarea() {
        $('div.input-div input[type=text]').val('');
    }
 
    // 메세지 수신
    function answer(ans) { 
        appendMessageTag("left", "KOZY", ans);
    }
 
    return {
        'init': init
    };
})();
 
$(document).ready(function() {
    let chatLi = $('div.chat.format ul li').clone();

    chatLi.addClass("left");
    chatLi.find('.sender span').text("KOZY");
    chatLi.find('.message span').text("안녕하세요. 나의 첫 금융 친구 KOZY 입니다. 무엇이든 물어보세요."); 
    
    $('div.chat:not(.format) ul').append(chatLi).css('opacity', '100%');

    Chat.init();
    $('.message_content').get(0).css('opacity', '0');
});

$(document).on("click", ".message", function(){ 
    var content = $(this).find('.message_content').text()
    var user_id = $('input[name=user_id]').val()
    $.ajax({
        type:'get',
        url: "/main/register",
        dataType: 'json',
        data: {
            'content':content,
            'user_id':user_id
        }
    });

    alert('북마크에 저장되었습니다')
});