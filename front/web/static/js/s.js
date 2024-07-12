document.addEventListener("DOMContentLoaded", function() {
    const serverActionBtn = document.getElementById("server-action-btn");
    const resultDiv = document.getElementById("result");

    function setLoading(isLoading) {
        if (isLoading) {
            serverActionBtn.disabled = true;
            serverActionBtn.textContent = '연결 중...';
            serverActionBtn.classList.add('loading');
        } else {
            serverActionBtn.disabled = false;
            serverActionBtn.classList.remove('loading');
        }
    }

    function updateButton(status, port, title, connUrl) {
        serverActionBtn.onclick = null; // 기존의 클릭 이벤트 핸들러 제거
        if (status === "connected") {
            serverActionBtn.textContent = '서버 닫기';
            resultDiv.textContent = `문제: ${title} , 접속URL = ${connUrl}${port}`;
            serverActionBtn.onclick = function() {
                // 서버 닫기 요청 보내기
                const cUrl = window.location.href + "/close-server";
                setLoading(true);
                fetch(cUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ port: port })
                })
                .then(response => response.json())
                .then(data => {
                    setLoading(false);
                    if (data.success) {
                        updateButton("disconnected");
                        resultDiv.textContent = `닫기 성공`;
                    } else {
                        resultDiv.textContent = `닫기 실패`;
                    }
                })
                .catch(error => {
                    setLoading(false);
                    updateButton("disconnected");
                });
            };
        } else {
            serverActionBtn.textContent = '서버 연결 요청 하기';
            serverActionBtn.onclick = function() {
                const currentUrl = window.location.href;

                // 서버 열기 요청 보내기
                setLoading(true);
                fetch(currentUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => response.json())
                .then(data => {
                    setLoading(false);
                    if (data.port) {
                        updateButton("connected", data.port, data.title, data.conn);
                        resultDiv.textContent = `문제: ${data.title} , 접속URL = ${data.conn}${data.port}`;
                    } else {
                        resultDiv.textContent = `연결 실패`;
                    }
                })
                .catch(error => {
                    setLoading(false);
                    updateButton("disconnected");
                });
            };
        }
    }

    // 서버 상태 확인 요청 보내기
    fetch('/server-status', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "connected") {
            updateButton("connected", data.port, data.title, data.conn);
        } else {
            updateButton("disconnected");
        }
    })
    .catch(error => {
        console.error('There was an error!', error);
    });
});
