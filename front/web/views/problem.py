from flask import Blueprint, render_template, abort,send_file,redirect,session,request,jsonify , url_for
from ..models import Problem, User ,Conn
from sqlalchemy import desc
import os
import requests
from .. import db
import json
problem_bp = Blueprint('problem',__name__,url_prefix='/')

            

@problem_bp.route('/<category>/problem<int:id>', methods=['GET','POST'] )
def p(category,id):
    
    if request.method == "POST":
        
        user = session.get('username')
        if user is not None:    
            u  = User.query.filter(User.id == user).first()
            
            if u is not None:    # 
                conn = Conn.query.filter(Conn.u_idx == u.u_idx).first()
                if conn is not None : 
                    ''' 유저가 이미 연결 정보를 가지고 있을때의 처리'''
                    return jsonify({"message": "Already connected", "port": conn.port})
                else:    
                    
                    p = Problem.query.filter_by(category=category).order_by(desc(Problem.p_idx)).all()
                    if id >0  and id <= len(p):
                        pro = p[id-1]
                        server_url = "http://example.com/create/" + category +"/"+ pro.connect
                        print(server_url)
                        
                        try:                        
                        # 서버에 POST 요청
                            response = requests.post(server_url)
                            
                        # 요청이 성공했을 경우
                            
                            if response.status_code == 201:
                                server_info = response.json()
                               
                                port = int(server_info.get("port"))
                                port_info = {"conn": "This is your AWS EC2 IP:" , "port": port , "title":pro.title}
                                container_name = server_info.get("container_name")
                                newconn = Conn(u.u_idx , pro.p_idx, port, container_name)
                               
                                db.session.add(newconn)
                                try:
                                    db.session.commit()
                                except Exception as e:
                                    db.session.rollback()
                                
                                return jsonify(port_info)
                            else:
                            # 요청이 실패한 경우, 오류를 반환합니다.
                                return jsonify({"error": "Failed to get server info"}), response.status_code
                        except Exception as e:
                        # 예외가 발생한 경우, 오류를 반환합니다.
                            print(e)
                            return jsonify({"error": str(e)}), 500
                    else:
                        abort(404)
            else: 
                return jsonify({"error": "No user information"})
        else:
            return jsonify({"error": "No user"})
    
    
    else :
        problem = Problem.query.filter_by(category=category).order_by(desc(Problem.p_idx)).all()
        user =  session.get('username')
        if user is not None:
            user = User.query.filter_by(id = user).first()
        if id >0  and id <= len(problem):
            pro = problem[id-1]
            check = False

            if user and user.has_solved(pro.p_idx):
                check = True
            
            return render_template('problem.html', pro = pro, number = id, check = check, user = user)
        else:
            abort(404)
            
   
@problem_bp.route('/download/problem/<int:problem_number>' , methods=['POST'])
def download_problem(problem_number):
    id = problem_number
    problem = Problem.query.order_by(desc(Problem.p_idx)).all()
    
    if id >0  and id <= len(problem):
        pro = problem[id-1]
    return send_file(pro.filepath , as_attachment=True)
   




@problem_bp.route('/server-status', methods=['GET'])
def server_status():
    user = session.get('username')
    if user is not None:
        u = User.query.filter(User.id == user).first()
        if u is not None:
            conn = Conn.query.filter(Conn.u_idx == u.u_idx).first()
            if conn is not None:
                p = Problem.query.filter(Problem.p_idx == conn.p_idx).first()
                return jsonify({"status": "connected", "port": conn.port, "title": p.title , "conn": "This is your AWS EC2 IP:"})
            else:
                return jsonify({"status": "disconnected"})
        else:
            return jsonify({"error": "No user information"}), 404
    else:
        return jsonify({"error": "No user"}), 404
    
    
    
@problem_bp.route('/<category>/problem<int:id>/close-server', methods=['POST'])
def close_server(category, id):
    data = request.get_json()
    port = data.get('port')
    user = session.get('username')
    if user is not None:    
        u  = User.query.filter(User.id == user).first()
        if u is not None:  
            p = Problem.query.filter_by(category=category).order_by(desc(Problem.p_idx)).all()
            if id >0  and id <= len(p):
                pro = p[id-1]
                conn = Conn.query.filter(Conn.u_idx == u.u_idx).first()
                server_url = "http://example.com/down/" + conn.container_name
                try:                        
                # 서버에 POST 요청
                    response = requests.post(server_url)
                # 요청이 성공했을 경우
                    if response.status_code == 200:
                        db.session.delete(conn)
                        try:
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                        
                        return jsonify({"success": "삭제성공"}), 200
                    else:
                    # 요청이 실패한 경우, 오류를 반환합니다.
                        return jsonify({"error": "Failed to get server info"}), response.status_code
                except Exception as e:
                # 예외가 발생한 경우, 오류를 반환합니다.
                    return jsonify({"error": str(e)}), 500
            else:
                abort(404)    
        else: 
            return jsonify({"error": "No user information"})
    else:
        return jsonify({"error": "No user"})
    


    
@problem_bp.route('/disconnect/', methods=['POST'])
def disconn():
    try:
        data = json.loads(request.data)
        container_name = data.get('container_name')
        print(container_name)
        c = Conn.query.filter_by(container_name=container_name).first()
        print(c)
        if c:
            db.session.delete(c)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        return jsonify({"success": "삭제성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400