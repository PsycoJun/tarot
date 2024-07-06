<!-- 예시: AJAX 요청 -->

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // 쿠키 이름이 csrftoken인 경우 쿠키 값을 반환
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
        $('#submit-button').click(function(e) {
            e.preventDefault();
            var csrftoken = getCookie('csrftoken');
            console.log(clickedButtons)
            $.ajax({
                type: 'POST',
                url: '/process/',
                headers: {
                'X-CSRFToken': csrftoken
                },
                data: JSON.stringify({
                'clickedButtons': Array.from(clickedButtons)  // set을 배열로 변환하여 전송
                }),
                success: function(response) {
                    console.log(response);
                    // 성공 시 처리 로직
                },
                error: function(error) {
                    console.log(error);
                    // 오류 처리 로직
                }
            });
        });
    });
