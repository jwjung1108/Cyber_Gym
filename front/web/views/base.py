from flask import Blueprint, render_template

bp = Blueprint('base',__name__,url_prefix='/')



'''
    테스트용 파일 삭제할 예정
'''


@bp.route('/base')
def base():
    return render_template('base.html')

@bp.route('/test')
def test():
    return render_template('test.html')