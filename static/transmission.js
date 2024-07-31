

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
document.addEventListener('DOMContentLoaded', function() {
    // 클릭 이벤트 리스너를 설정합니다.
    document.getElementById('submit-button').addEventListener('click', function(e) {
        e.preventDefault();
        
        // .search-input 클래스를 가진 요소를 선택합니다.
        const searchInput = document.getElementById('search-input');

        // 요소의 value 속성에서 값을 가져옵니다.
        var spread = detectShapeFromClickedButtons(clickedButtons);
        const inputValue = searchInput.value;
        var csrftoken = getCookie('csrftoken');
        console.log(window.order);
        
        const loading = document.getElementById('loading');
        loading.style.display = "block";

        // AJAX 요청을 보냅니다.
        fetch('/process_result/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'question': inputValue,
                'clickedButtons': window.order,
                'spread': spread,
            })
        })
        .then(response => response.json())
        .then(data => {
            let i = 0;
            Object.entries(data.cards).forEach(([card, imageUrl]) => {
                let spl = imageUrl.split("~");

                console.log(`Card: ${card}, Image URL: ${spl[1]}`);
                const tarotImage = document.getElementById('button-' + card);
                
                // 이미지 뒤집기 클래스 추가
                tarotImage.style.transform = "rotateY(180deg)";

                // 0.6초 후에 이미지 변경 (CSS 애니메이션 시간과 일치)
                setTimeout(() => {
                    tarotImage.style.transform = "";
                    tarotImage.style.transform = 'scale(1.0)'; // 클릭된 버튼 표시 색상
                    tarotImage.style.backgroundImage = `url(${spl[1]})`;
                    tarotImage.style.textAlign = "center";
                    tarotImage.style.fontWeight = "bold";
                    tarotImage.style.border = "3px solid gray"
                    tarotImage.textContent = spl[0];
                }, 600);
            });

            document.getElementById('result-container').style.display = 'block';
            document.getElementById('result').innerHTML = '<p>해석: ' + data.result + '</p>';
            loading.style.display = "none";
        })
        .catch(error => {
            console.error(error);
            document.getElementById('result-container').style.display = 'block';
            document.getElementById('result').innerHTML = '<p>타로 결과를 보여드릴 수 없어요. ' + error.message + '</p>';
        });
    });
});
