from flask import Blueprint, render_template, session, request, flash, redirect, abort
from ..models import User, Flag, Problem
from .. import db

flag_bp = Blueprint('flag', __name__, url_prefix='/')

@flag_bp.route('/flag', methods=['POST'])
@flag_bp.route('/flag/', methods=['POST'])
def check_flag():
    '''
    플래그 값을 받으면 정답 검증
    '''
    if request.method == "POST":
        inflag = request.form.get('flag', '')
        title = request.form.get('title', '')
        
        # 정답 확인 로직
        problem = Flag.check_flag(inflag, title)
        if problem:
            user_id = session.get('username')
            user = User.query.filter_by(id=user_id).first()
            if user:
                if user.solve_problem(problem):
                    flash("정답입니다.")
                else:
                    flash("이미 풀었던 문제입니다.")
            else:
                flash("사용자 정보를 찾을 수 없습니다.")
        else:
            flash("정답이 아닙니다")
        
        return redirect(request.referrer or '/')
    else:
        flash("정상적인 접근이 아닙니다")
        abort(404)

@flag_bp.route('/score/')
def score_board():
    '''
    Score 데이터 가져와서 유저 이름과 점수 리스트 만들어서 보내기
    '''
    scoreList = User.query.order_by(User.t_score.desc()).all()
    return render_template('score.html', list=scoreList)
