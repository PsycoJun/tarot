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
                url: '/process_result/',
                headers: {
                'X-CSRFToken': csrftoken
                },
                data: JSON.stringify({
                'clickedButtons': Array.from(clickedButtons)  // set을 배열로 변환하여 전송
                }),
                success: function(response) {
                    console.log(response.cards);
                    let i = 0;
                    Object.entries(response.cards).forEach(([card, imageUrl]) => {
                        console.log(`Card: ${card}, Image URL: ${imageUrl}`);
                        const tarotImage = document.getElementById('button-'+card);
                        // 이미지 뒤집기 클래스 추가
                        tarotImage.style.transform="rotateY(180deg)"

                        // 0.6초 후에 이미지 변경 (CSS 애니메이션 시간과 일치)
                        setTimeout(() => {
                            tarotImage.style.transform=""
                            tarotImage.style.transform = 'scale(1.0)'; // 클릭된 버튼 표시 색상
                            tarotImage.style.backgroundImage =  `url(${imageUrl})`;
                            tarotImage.style.textAlign = "center"
                            tarotImage.style.fontWeight = "bold"
                            tarotImage.textContent = response.cardsName[i++];

                            // 이미지 뒤집기 클래스 제거 (다음 애니메이션을 위해)

                        }, 600);
                            // 이미지 변경

                            // 여기서 다른 작업 수행 가능
                    });
                    $('#result-container').show();
                    $('#result').html('<p>해석: ' + response.result + '</p>')
                },
                error: function(response) {
                    console.error(response);
                    $('#result-container').show()
                    $('#result').html('<p>타로 결과를 보여드릴 수 없어요. ') + response.error + '</p>'
                    // 오류 처리 로직
                }
            });
        });
    });
