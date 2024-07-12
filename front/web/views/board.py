from flask import Blueprint, jsonify, render_template,session,abort,request,redirect,url_for,flash
from sqlalchemy import delete, desc
from ..models import Problem, User,Question,Answer,Solve
from .. import db
from .. import cipher_suite
from .. import fkey
import base64
board_bp = Blueprint('board',__name__,url_prefix='/')

# @user_bp.route('/login/')
@board_bp.route('/board/<category>')
def category(category):
    '''
    카테고리에 해당하는 값이 들어오면 출력
    아니면 오류 발생
    '''
    valid_categories = ['system', 'web', 'malware', 'misc']
    if category not in valid_categories:
        abort(404)  # 404 오류 발생

    user_id = session.get('username')
    user = User.query.filter_by(id=user_id).first()
    problem = Problem.query.filter_by(category=category).with_entities(Problem.p_idx, Problem.title,Problem.score).order_by(desc(Problem.p_idx)).all()
    solved_problem_ids=[]
    if user:
        solved_problems = db.session.query(Solve.p_idx).filter_by(u_idx=user.u_idx).all()
        solved_problem_ids = [p.p_idx for p in solved_problems]
        print(solved_problem_ids)
    return render_template('/category.html', pro=problem, title=category, solved_problem_ids=solved_problem_ids)
    

# Q and A Pages!
@board_bp.route('/board/QNA')
def qanda():
    '''
    데이터베이스에서 QNA 리스트가 있으면 반환
    아니면 빈 리스트 반환
    '''
    
    qnaList = []
    # DB에서 데이터 뽑기
    qnaList = Question.query.join(User, User.u_idx==Question.u_idx).join(Problem, Problem.p_idx==Question.p_idx).add_columns(User.id, Problem.title ).order_by(desc(Question.q_idx)).all()
    
    for item in qnaList:
        item[0].title = truncate_title(item[0].title)
    return render_template("/community/list.html" , list = qnaList)



@board_bp.route('/board/QNA/<int:number>', methods=['GET','POST'])
def pages(number):
    '''
    만약에 number의 qna글이 존재한다면 보여주기
    존재 안하면 오류 페이지로
    '''
    if request.method =='POST':
        
            if session.get('username') is not None:    
                data = request.get_json()
                comment = data['comment']
                last_segment = data['lastSegment']
                username = session.get('username')
                cur_user = User.query.filter(User.id == username).first()
                cur_q = Question.query.order_by(Question.q_idx).all()[int(last_segment)-1]
                
                new_answer = Answer(comment , cur_user.u_idx, cur_q.q_idx)
                db.session.add(new_answer)
                try:
                    db.session.commit()
                    return jsonify(message = '댓글 작성 완료')
                except Exception as e:
                    db.session.rollback()
                    return jsonify(message = '오류 발생')
                
            else:
                return jsonify(message = '로그인 필요')
    else:
        qList = Question.query.join(User, User.u_idx==Question.u_idx).add_columns(User.id).order_by(Question.q_idx).all()
        
        data = None
        if len(qList) >= number and number > 0:
            data = qList[number-1]
        isAuthor = False
        if data is not None:
            if data[1] == session.get('username') or session.get('logged_in'):
                isAuthor = True
            comment = Answer.query.join(User, User.u_idx==Answer.u_idx).add_columns(User.nickname).filter(Answer.q_idx == data[0].q_idx).order_by(Answer.a_idx).all()
            
            return render_template("/community/QA.html", data=data, isAuthor = isAuthor , number = number,comment = comment )
        else:
            abort(404)
    


@board_bp.route('/board/write', methods=['GET','POST'])
def write():
    
    if session.get('username') is not None:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            p_idx = Problem.query.filter_by(title=request.form['numbers']).first()
            if not p_idx:
                flash("문제 제목을 확인해주세요.")
                return redirect(url_for("board.board"))  # Redirect to the write page
            username = session.get('username')
            u = User.query.filter_by(id=username).first()
            new_q = Question(title,content,u.getIdx(),p_idx.getIdx())
            db.session.add(new_q)
            
            try:
                db.session.commit()

                flash("글 작성 성공.")
                
            except Exception as e:
                db.session.rollback()
                flash("오류가 발생했습니다.")
            
            return redirect(url_for("board.qanda"))
            
        else:
            pro = []
            pro = Problem.query.order_by(Problem.p_idx).all()
            tmp = {
                'title': '',
                'problem': '',
                'content': ''
            }
            return render_template('/community/write.html',url="/board/write" , title='글작성',problem = pro, tmp = tmp ,number='' )
        
    else:
        flash('로그인이 필요합니다.')
        return redirect(url_for('board.qanda'))
    

@board_bp.route('/board/delete-post', methods=['POST'])
def delete_post():
    number = int(request.form['postId'])
    
   


    qList = Question.query.order_by(Question.q_idx).all()
    if len(qList) >= number and number > 0:
        q_idx = qList[number-1].q_idx
    else:
        abort(404) 
    
    q = Question.query.filter(Question.q_idx == q_idx ).first()
    user = User.query.filter(User.u_idx == q.u_idx).first()
    if session.get('logged_in') or session.get('username') == user.id :
        # 글삭제하는 로직 작성
        db.session.delete(q)
        delete_query = delete(Answer).where(Answer.q_idx == q_idx)
        db.session.execute(delete_query)
        try:
            db.session.commit()
            flash("삭제 완료")
        except Exception as e:
            
            db.session.rollback()
            flash("오류 발생")
            
        return redirect(url_for("board.qanda"))
    else :
        flash("오류가 발생했습니다.")
        return redirect(request.referrer or '/')
    
    
@board_bp.route('/board/re-post', methods=['POST'])
def repost():
    if request.method == 'POST':
        number = int(request.form['postId'])
       
        q = Question.query.order_by(Question.q_idx).all()
        
        if number > 0 and number <= len(q):
            q = q[number-1]
            user = User.query.filter(User.u_idx == q.u_idx).first()
            
            if session.get('username') == user.id:
                pro = []
                pro = Problem.query.order_by(Problem.p_idx).all()
                p = Problem.query.filter(Problem.p_idx == q.p_idx).first()
                tmp = {
                        'title': q.title,
                        'problem': p.title,
                        'content': q.content 
                    }
                return render_template('/community/write.html',url="/board/re",title='글작성',problem = pro, tmp = tmp, number = number  )
                
            else:
                flash("권한 없음")
                return redirect(request.referrer or '/')
            
        else:
            flash('오류 발생')
            return redirect(request.referrer or '/')
        
    
    
@board_bp.route('/board/re', methods=['POST'])
def update():
    
        if request.method == 'POST':
            number =int(request.form['number'])
            q = Question.query.all()[number-1]
            q.title = request.form['title']
            q.content = request.form['content']
            name = request.form['numbers']
            p= Problem.query.filter(Problem.title == name).first()
            if p is not None:
                q.p_idx = p.getIdx()
                try:
                    db.session.commit()

                    flash("글 업데이트 성공.")
                    
                except Exception as e:
                    
                    db.session.rollback()
                    flash("오류가 발생했습니다")
                
                return redirect(url_for("board.qanda"))
            else:
                abort(404)
        else:
            return redirect(request.referrer or '/')

@board_bp.route('/board/QNA/<int:number>/delete', methods=['POST'])
def answerDelete(number):
    
    if request.method == 'POST':
        username = session.get('username')
        if username is not None:
            data = request.get_json()
            index = int(data['i'])
            questionData = Question.query.order_by(Question.q_idx).all()
            if len(questionData) >= number and number > 0:
                q_idx = questionData[number-1].q_idx
                print(q_idx)
                answerData = Answer.query.filter(Answer.q_idx == q_idx ).all()
                print(answerData)
                userData = User.query.filter(User.id == username).first()
                print(userData)
                if userData is not None and len(answerData) >= index and index > 0:
                    cur_answer = answerData[index - 1]
                    db.session.delete(cur_answer)
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                    return jsonify(message='댓글 삭제')
                
                
@board_bp.route('/board',methods=['GET'])
def board():
    return  render_template('/board.html')


def truncate_title(title, length=10):
    if len(title) > length:
        return title[:length] + '...'
    return title



# 에디터 뷰어 테스트용 코드
# @board_bp.route('/QNA/<int:number>', methods=['GET'])
# def view_question(number):
#     '''
#     만약에 number의 qna글이 존재한다면 보여주기
#     존재 안하면 오류 페이지로
#     '''
#     qList = Question.query.join(User, User.u_idx == Question.u_idx).add_columns(User.nickname).order_by(Question.q_idx).all()

#     data = None
#     if len(qList) >= number and number > 0:
#         data = qList[number - 1]

#     if data is not None:
#         return render_template("view_question.html", question=data[0], author=data[1])
#     else:
#         abort(404)