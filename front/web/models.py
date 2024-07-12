from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pytz

db = SQLAlchemy()

# 한국 표준시 (KST) 타임존 설정
KST = pytz.timezone('Asia/Seoul')

def current_kst_time():
    return datetime.now(KST)

# User 모델 정의
class User(db.Model):
    __tablename__ = "user"

    u_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(50), unique=True, nullable=False)
    pw = db.Column(db.String(256), nullable=False)
    nickname = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    authority = db.Column(db.Integer, nullable=False, default=1)  # admin = 3 / user = 1
    t_score = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id, pw, nickname, email):
        self.id = id
        self.pw = pw
        self.nickname = nickname
        self.email = email

    def getAuth(self):
        return self.authority

    def getIdx(self):
        return self.u_idx

    def has_solved(self, p_idx):
        return db.session.query(Solve).filter_by(u_idx=self.u_idx, p_idx=p_idx).count() > 0

    def solve_problem(self, problem):
        if not self.has_solved(problem.p_idx):
            Solve.record_solve(self.u_idx, problem.p_idx)
            self.t_score += problem.score
            db.session.commit()
            return True
        return False

# Problem 모델 정의
class Problem(db.Model):
    __tablename__ = "problem"

    p_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(300), nullable=False, unique=True)
    contents = db.Column(db.Text, nullable=False)  # db.String에서 db.Text로 변경
    hint = db.Column(db.String(300), nullable=False)
    connect = db.Column(db.String(2000), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    filepath = db.Column(db.String(500), nullable=False, default="")
    problem_type = db.Column(db.String(50), nullable=False)

    def __init__(self, category, title, contents, hint, connect, score, filepath, problem_type):
        self.category = category
        self.title = title
        self.contents = contents
        self.hint = hint
        self.connect = connect
        self.score = score
        self.filepath = filepath
        self.problem_type = problem_type

    def make_problem():
        print("Make!!")

    def getIdx(self):
        return self.p_idx

# Flag 모델 정의
class Flag(db.Model):
    __tablename__ = "flag"

    f_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_idx = db.Column(db.String(50), unique=True, nullable=False)
    flag = db.Column(db.String(500), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, p_idx, flag, score):
        self.p_idx = p_idx
        self.flag = flag
        self.score = score

    @staticmethod
    def check_flag(inflag, title):
        problem = Problem.query.filter_by(title=title).first()
        if problem:
            flag_entry = Flag.query.filter_by(flag=inflag, p_idx=problem.p_idx).first()
            if flag_entry:
                return problem
        return None

# Solve 모델 정의
class Solve(db.Model):
    __tablename__ = "solve"

    p_idx = db.Column(db.Integer, primary_key=True)
    u_idx = db.Column(db.Integer, primary_key=True)
    solve_date = db.Column(db.DateTime, default=current_kst_time)

    def __init__(self, p_idx, u_idx):
        self.p_idx = p_idx
        self.u_idx = u_idx
        self.solve_date = current_kst_time()

    @classmethod
    def record_solve(cls, user_id, problem_id):
        solve = cls(p_idx=problem_id, u_idx=user_id)
        db.session.add(solve)
        db.session.commit()

# Question 모델 정의
class Question(db.Model):
    __tablename__ = "Que"

    q_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)  # db.String에서 db.Text로 변경
    u_idx = db.Column(db.Integer, nullable=False)
    p_idx = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, default=current_kst_time)

    def __init__(self, title, content, u_idx, p_idx):
        self.title = title
        self.content = content
        self.u_idx = u_idx
        self.p_idx = p_idx

    def pri(self):
        print(self.content)

# Answer 모델 정의
class Answer(db.Model):
    __tablename__ = "Ans"

    a_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)  # db.String에서 db.Text로 변경
    u_idx = db.Column(db.Integer, nullable=False)
    q_idx = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, default=current_kst_time)

    def __init__(self, content, u_idx, q_idx):
        self.content = content
        self.u_idx = u_idx
        self.q_idx = q_idx

# Conn 모델 정의 1차 수정 
class Conn(db.Model):
    __tablename__ = "conn"

    c_idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_idx = db.Column(db.Integer, nullable=False)
    p_idx = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    container_name = db.Column(db.Text, nullable=False)
    connection_time = db.Column(db.DateTime, default=current_kst_time)

    def __init__(self, u_idx, p_idx, port, container_name):
        self.u_idx = u_idx
        self.p_idx = p_idx
        self.port = port
        self.container_name = container_name

