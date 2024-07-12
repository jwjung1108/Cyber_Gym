from flask import Blueprint, render_template, request, session, redirect, url_for,flash ,current_app 
from ..models import User
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from .. import bcrypt
user_bp = Blueprint('user',__name__,url_prefix='/')



# @user_bp.route('/login/')
@user_bp.route('/login', methods=['POST'])
@user_bp.route('/login/', methods=['POST'])
def login():
        id = request.form['id']
        pw = request.form['pw']

        user = User.query.filter_by(id=id).first()
        if user and bcrypt.check_password_hash(user.pw,pw):
            session['username'] = user.id
            
            if(user.getAuth() == 2):
                session['logged_in'] = True
            else:
                session['logged_in'] = False
            flash('로그인 성공')
            return  redirect(request.referrer or '/')
        else:
            flash('로그인 실패')
            return  redirect(request.referrer or '/')
    
@user_bp.route('/logout')
@user_bp.route('/logout/')
def logout():
    if session.pop('username', None) is None:
        flash("로그인을 먼저 진행해 주세요")
        return  redirect(request.referrer or '/')
    else:
        session.pop('logged_in', None)
        flash("로그아웃 성공")
        return  redirect(request.referrer or '/')

# 회원가입 페이지 라우트
@user_bp.route('/signup', methods=['POST'])
def signup():
    id = request.form['id']
    pw = request.form['pw']
    confirm_pw = request.form['confirm']
    email = request.form['email']
    nick = request.form['nick']

    # 백엔드 유효성 검사
    if not re.match(r"^[a-zA-Z0-9_]+$", id):
        flash("아이디는 알파벳, 숫자, 밑줄만 포함할 수 있습니다.")
        return redirect(request.referrer or '/')

    if len(id) < 4 or len(id) > 12:
        flash("아이디는 4자 이상, 12자 이하여야 합니다.")
        return redirect(request.referrer or '/')

    if len(pw) < 8:
        flash("비밀번호는 최소 8자 이상이어야 합니다.")
        return redirect(request.referrer or '/')

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash("유효한 이메일 주소를 입력해주세요.")
        return redirect(request.referrer or '/')

    if len(nick) < 2 or len(nick) > 20:
        flash("닉네임은 2자 이상, 20자 이하여야 합니다.")
        return redirect(request.referrer or '/')

    if pw != confirm_pw:
        flash("비밀번호가 일치하지 않습니다.")
        return redirect(request.referrer or '/')

    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', pw):
        flash("비밀번호는 8자 이상이며, 영문자, 숫자, 특수문자(@$!%*#?&)를 최소 1개씩 포함해야 합니다.")
        return redirect(request.referrer or '/')

    existing_user = User.query.filter_by(id=id).first()
    if existing_user:
        flash("이미 존재하는 아이디입니다.")
        return redirect(request.referrer or '/')
    else:
        new_user = User(id, bcrypt.generate_password_hash(pw).decode('utf-8'), nick, email)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("회원가입하였습니다.")
            return redirect(request.referrer or '/')
        except Exception as e:
            db.session.rollback()
            flash("오류가 발생했습니다.")
            return redirect(request.referrer or '/')
        
        
@user_bp.route('/prfl', methods=['GET'])
def profile():
        username = session.get('username')
        if username is not None:
            user = User.query.filter(User.id == username).first()
            return render_template('mypage/profile.html', data = user)