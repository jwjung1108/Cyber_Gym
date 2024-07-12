document.getElementById('qnaForm').addEventListener('submit', function(event) {
    var input = document.getElementById('numbers').value;
    var dataList = document.getElementById('list').getElementsByTagName('option');
    var found = false;

    for (var i = 0; i < dataList.length; i++) {
        if (input === dataList[i].value) {
            found = true;
            break;
        }
    }

    if (!found) {
        alert('유효하지 않은 문제 제목입니다. 다시 확인해주세요.');
        event.preventDefault(); // 폼 제출을 중단합니다.
    }
});