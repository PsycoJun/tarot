let clickedButtons = new Set();

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }



        function sendResult() {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            fetch('/send_result/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ count: clickedButtons.size })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                // API 결과를 처리합니다.
                console.log(data);
                alert(`타로 카드: ${JSON.stringify(data)}`);
            })
            .catch(error => console.error('Error:', error));
        }

function toggleButton(buttonId) {
            const button = document.getElementById(`button-${buttonId}`);

            if (clickedButtons.has(buttonId)) {
                clickedButtons.delete(buttonId);
                button.style.transform = ''; // 클릭된 버튼 표시 색상
                button.style.boxShadow = ''
            } else {
                console.log("clicked")
                clickedButtons.add(buttonId);
                button.style.transform = 'scale(1.1)'; // 클릭된 버튼 표시 색상
                button.style.boxShadow = '0 0 20px rgba(255, 255, 255, 0.5)'
            }
        }

