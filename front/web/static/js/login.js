document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('loginBtn');

    if (loginBtn) {
        loginBtn.addEventListener('click', function () {
            resetInputFields();
            let form = document.getElementsByClassName("form")[0];
            resetClass(form, "signup");
            resetClass(form, "reset");
            form.classList.add("signin");
            document.getElementById("submit-btn").innerText = "Sign In";
            document.getElementById("form").setAttribute("action", "/login");
            let formElements = document.querySelectorAll(".form-element:nth-child(n+3):nth-child(-n+5)");

            formElements.forEach(element => {
                element.style.display = "none";
            });

            document.getElementById('form').removeEventListener('submit', signUpSubmitHandler);
            document.getElementById('form').addEventListener('submit', signInSubmitHandler);
            document.getElementById('modal').style.display = 'block';
        });
    }
});

document.getElementById('close-modal').addEventListener('click', function () {
    document.getElementById('modal').style.display = 'none';
});

function resetClass(element, classname) {
    element.classList.remove(classname);
}

// 로그인 이벤트 리스너 등록
document.getElementsByClassName("show-signin")[0].addEventListener("click", function () {
    resetInputFields();
    let form = document.getElementsByClassName("form")[0];
    resetClass(form, "signup");
    resetClass(form, "reset");
    form.classList.add("signin");
    document.getElementById("submit-btn").innerText = "Sign In";
    document.getElementById("form").setAttribute("action", "/login");
    let formElements = document.querySelectorAll(".form-element:nth-child(n+3):nth-child(-n+5)");

    formElements.forEach(element => {
        element.style.display = "none";
    });

    // 기존에 등록된 회원가입 이벤트 리스너 제거
    document.getElementById('form').removeEventListener('submit', signUpSubmitHandler);

    // 로그인 폼에 대한 유효성 검사 함수 호출
    document.getElementById('form').addEventListener('submit', signInSubmitHandler);
});

// 회원가입 이벤트 리스너 등록
document.getElementsByClassName("show-signup")[0].addEventListener("click", function () {
    resetInputFields();
    let form = document.getElementsByClassName("form")[0];
    resetClass(form, "signin");
    resetClass(form, "reset");
    form.classList.add("signup");
    document.getElementById("submit-btn").innerText = "Sign Up";
    document.getElementById("form").setAttribute("action", "/signup");
    let formElements = document.querySelectorAll(".form-element:nth-child(n+3):nth-child(-n+5)");

    formElements.forEach(element => {
        element.style.display = "block";
    });

    // 기존에 등록된 로그인 이벤트 리스너 제거
    document.getElementById('form').removeEventListener('submit', signInSubmitHandler);

    // 회원가입 폼에 대한 유효성 검사 함수 호출
    document.getElementById('form').addEventListener('submit', signUpSubmitHandler);
});

// 로그인 폼에 대한 유효성 검사 함수
function signInSubmitHandler(event) {
    event.preventDefault(); // 기본 이벤트 제거

    // 아이디와 비밀번호 값 가져오기
    let username = document.querySelector('#username').value;
    let password = document.querySelector('#password').value;

    // 유효성 검사 실행
    if (validateSignInForm(username, password)) {
        // 유효성 검사 통과 시 로그인 요청 등 추가 처리 수행
        document.getElementById('form').submit();
    }
}


// 로그인 폼 유효성 검사 함수
function validateSignInForm(username, password) {
    // 아이디 길이 유효성 검사
    if (!idLength(username)) {
        showValidationMessage('아이디는 4자 이상, 12자 이하여야 합니다.');
        return false;
    }

    // 아이디가 영문자와 숫자로만 이루어져 있는지 검사
    if (!onlyNumberAndEnglish(username)) {
        showValidationMessage('아이디는 영문자와 숫자로만 이루어져야 합니다.');
        return false;
    }

    // 비밀번호 강력성 검사
    if (!strongPassword(password)) {
        showValidationMessage('비밀번호는 8자 이상이며, 영문자, 숫자, 특수문자(@$!%*#?&)를 최소 1개씩 포함해야 합니다.');
        return false;
    }

    // 모든 검증을 통과한 경우 true 반환
    return true;
}





// 회원가입 폼에 대한 유효성 검사 함수
function signUpSubmitHandler(event) {
    event.preventDefault(); // 기본 이벤트 제거

    if (validateSignUpForm()) {
        document.getElementById('form').submit();
    }
}

// 아이디 길이를 검증하는 함수
function idLength(value) {
    return value.length >= 4 && value.length <= 12;
}

// 영문자와 숫자로만 이루어진지 검증하는 함수
function onlyNumberAndEnglish(str) {
    return /^[A-Za-z0-9][A-Za-z0-9]*$/.test(str);
}

// 강력한 비밀번호인지 검증하는 함수
function strongPassword(str) {
    return /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/.test(str);
}

// 이메일 형식 검증 함수
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// 닉네임 길이 검증 함수
function isValidNickLength(nick) {
    return nick.length >= 2 && nick.length <= 20;
}

function isSamePassword(pw1, pw2)
{
    return pw1 == pw2
}


// 회원가입 폼 유효성 검사 함수
function validateSignUpForm() {
    let elInputUsername = document.querySelector('#username');
    let elInputPassword = document.querySelector('#password');
    let username = elInputUsername.value.trim();
    let password = elInputPassword.value;
    let email = document.querySelector('#email').value.trim();
    let nickname = document.querySelector('#nick').value.trim();
    let confirm = document.querySelector('#confirm').value.trim();

    if (!idLength(username)) {
        showValidationMessage('아이디는 4자 이상, 12자 이하여야 합니다.');
        return false;
    }

    if (!onlyNumberAndEnglish(username)) {
        showValidationMessage('아이디는 영문자와 숫자로만 이루어져야 합니다.');
        return false;
    }

    if (!strongPassword(password)) {
        showValidationMessage('비밀번호는 8자 이상이며, 영문자, 숫자, 특수문자(@$!%*#?&)를 최소 1개씩 포함해야 합니다.');
        return false;
    }

    if (!isValidEmail(email)) {
        showValidationMessage('유효한 이메일 주소를 입력해주세요.');
        return false;
    }

    if (!isValidNickLength(nickname)) {
        showValidationMessage('닉네임은 2자 이상, 20자 이하여야 합니다.');
        return false;
    }
    if(!isSamePassword(password,confirm))
    {
        showValidationMessage('비밀번호가 같지 않습니다.')
        return false;
    }

    // 모든 검증을 통과한 경우에만 true 반환
    return true;
}

// 입력 필드 초기화 함수
function resetInputFields() {
    // 아이디, 비밀번호, 이메일, 닉네임 입력 필드 초기화
    document.querySelector('#username').value = '';
    document.querySelector('#password').value = '';
    document.querySelector('#confirm').value = '';
    document.querySelector('#email').value = '';
    document.querySelector('#nick').value = '';
    // validation-message div 초기화
    document.getElementById('validation-message').innerText = '';
}


// 메시지를 표시하는 함수
function showValidationMessage(message) {
    // validation-message div에 메시지 추가
    document.getElementById('validation-message').innerText = message;
}