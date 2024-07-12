function showChangePassword() {
    var container = document.getElementById('changePasswordContainer');
    if (container.style.display === 'block') {
        resetChangePassword(container);
        container.style.display = 'none';
    } else {
        container.style.display = 'block';
    }
}

document.getElementById('changePasswordForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        alert('새 비밀번호와 확인 비밀번호가 일치하지 않습니다.');
        return;
    }
    if (!strongPassword(newPassword)) {
        alert('비밀번호는 최소 8자 이상이어야 하며, 영문자, 숫자, 특수문자를 포함해야 합니다.');
        return;
    }

    
    fetch('/change-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            currentPassword: currentPassword,
            newPassword: newPassword
        }),
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('비밀번호가 성공적으로 변경되었습니다.');
              // 필요한 경우 페이지를 리다이렉트합니다.
              document.getElementById('changePasswordContainer').style.display = 'none';
          } else {
              alert('비밀번호 변경에 실패했습니다: ' + data.message);
          }
      }).catch(error => {
          console.error('Error:', error);
          alert('비밀번호 변경 중 오류가 발생했습니다.');
      });
});

function resetChangePassword(container) {
    // 폼 내의 특정 입력 필드를 초기화
    var inputs = container.querySelectorAll('#currentPassword, #newPassword, #confirmPassword');
    inputs.forEach(function(input) {
        input.value = '';
    });
}

function strongPassword(str) {
    return /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/.test(str);
}