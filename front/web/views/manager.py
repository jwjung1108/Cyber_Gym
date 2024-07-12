from flask import Blueprint, render_template, request, session, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from ..models import Problem, Flag
from .. import db
from flask import jsonify
import os
UPLOAD_FOLDER = os.getcwd() + '/upload'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


man_bp = Blueprint('manager',__name__,url_prefix='/')


# @user_bp.route('/login/')
@man_bp.route('/manager', methods=['POST','GET'])
def manager():
        if 'logged_in' in session and session['logged_in']:
        
                if request.method == 'POST':
                        category = request.form.get('category')
                        title = request.form.get('title')
                        content = request.form.get('content')
                        hint = request.form.get('hint')
                        conn = request.form.get('connect')
                        score = int(request.form.get('score'))
                        file = request.files.get('file')
                        flag = request.form.get('flag')
                        ptype = request.form.get('ptype')
                        if title and content:  # title과 content가 모두 존재하는지 확인
                                # 여기다가 db에 넣는거 작성
                                if file and allowed_file(file.filename):
                                        filename = secure_filename(file.filename)
                                        file_path = os.path.join(UPLOAD_FOLDER, filename)
                                        file.save(file_path)
                                        p = Problem(category,title,content,hint,conn,score,file_path,ptype)
                                        
                                else:
                                        p = Problem(category,title,content,hint,conn,score,"파일없음",ptype)
                                
                                db.session.add(p)
                                db.session.commit()
                                
                                f = Flag(p.p_idx,flag,score)
                                db.session.add(f)
                                db.session.commit()
                                flash("문제 생성 완료")
                                return redirect(request.referrer or '/')

                return render_template('manager.html')
        else :
                abort(404)

@man_bp.route('/manager/list')
def list():
      if 'logged_in' in session and session['logged_in']: 
        p = Problem.query.all()
        return render_template('m_list.html', problems=p)
      else:
            abort(404)


@man_bp.route('/edit_problem/<int:p_idx>', methods=['GET', 'POST'])
def edit_problem(p_idx):

        if 'logged_in' in session and session['logged_in']:
                problem = Problem.query.filter_by(p_idx = p_idx).first()
                flag = Flag.query.filter_by(p_idx = p_idx).first()
                if problem is None:
                        abort(404)

                if request.method == 'POST':
                
                        problem.category = request.form['category']
                        problem.title = request.form['title']
                        problem.contents = request.form['content']
                        problem.hint = request.form['hint']
                        problem.connect = request.form['connect']
                        problem.score = int(request.form['score'])
                        flag.flag = request.form['flag']
                        
                        # 파일 업로드 처리
                        file = request.files.get('file')
                        if file:
                                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                                file.save(filepath)
                                problem.filepath = filepath
                        try:
                                db.session.commit()
                                return redirect(url_for('manager.list'))
                        except Exception as e:
                                db.session.rollback()
                                return jsonify({"error": str(e)}), 500
        
                # 문제 데이터를 수정 페이지에 전달
                return render_template('edit_problem.html', problem=problem, flag=flag)
        
        else:
               abort(404)
