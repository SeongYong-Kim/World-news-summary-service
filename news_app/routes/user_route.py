from flask import Blueprint, request, redirect, url_for, Response, render_template
from news_app.models import news_model
from news_app.utils import main_funcs

bp = Blueprint('user', __name__)


@bp.route('/user', methods=['POST'])
def renew():
    
    #recent news
    news_model.renew_news()

    return redirect(url_for('main.index', msg_code=3))