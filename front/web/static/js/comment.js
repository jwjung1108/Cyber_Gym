    // 모달 창 열기
    function openModal() {
        document.getElementById('myModal').style.display = 'block';
    }

    // 모달 창 닫기
    function closeModal() {
        document.getElementById('myModal').style.display = 'none';
    }

    // 답변 제출
    function submitAnswer() {
        var answer = document.getElementById('answer-textarea').value;
        const currentUrl = new URL(window.location.href);
        const lastSegment = currentUrl.pathname.split('/').pop();
        fetch(currentUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                comment: answer,
                lastSegment: lastSegment
            })
        }).then((response) => response.json())
            .then((data) => alert(data.message)).then(() => {
                location.reload();
            })

        closeModal(); // 답변 작성 후 모달 창 닫기
    }
    function deleteAnswer(value) {
        const currentUrl = new URL(window.location.href);
        currentUrl.pathname += '/delete';
        fetch(currentUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "i": value,
            })
        }).then((response) => response.json())
            .then((data) => alert(data.message)).then(() => {
                location.reload();
            })
    }

    function confirmDelete() {
        var confirmation = confirm("정말로 삭제하시겠습니까?");
        if (confirmation) {
            document.getElementById("deleteForm").submit(); // 폼 제출
        }
    }

