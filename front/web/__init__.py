from flask import Flask, render_template, request, jsonify , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db
from flask_bcrypt import Bcrypt
from datetime import timedelta
from cryptography.fernet import Fernet
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename


bcrypt = Bcrypt()
fkey = Fernet.generate_key()
cipher_suite = Fernet(fkey)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    UPLOAD_FOLDER = 'web/static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    with app.app_context():
        db.init_app(app)
        db.create_all()
        bcrypt.init_app(app)

    migrate = Migrate(app, db)

    from .views import base, user, board, problem, flag, error, manager
    app.register_blueprint(base.bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(board.board_bp)
    app.register_blueprint(problem.problem_bp)
    app.register_blueprint(flag.flag_bp)
    app.register_error_handler(404, error.page_not_found)  # 커스텀 404 에러 페이지 
    app.register_blueprint(manager.man_bp)
    app.permanent_session_lifetime = timedelta(hours=2)  # 2시간 동안 세션 유지


    @app.route('/')
    def index():
        return render_template('main.html')

    @app.route('/upload_image', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            file_url = url_for('static', filename=f'uploads/{unique_filename}')
            return jsonify({'url': file_url})

        return jsonify({'error': 'Failed to upload file'}), 500
    
    
    
    return app