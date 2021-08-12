from flask import Blueprint, render_template, request
from news_app.models.news_model import get_news
from news_app.models.news_model import News
from news_app.utils import main_funcs
from news_app import db

import csv
import pandas as pd

bp = Blueprint('main', __name__)

@bp.route('/', methods=["GET", "POST"])
def index():
    news = News.query.all()

    news_dict = {
             'date' : [], #첫 값을 빈칸으로 두기위해 ''추가`
    }

    for new in news:
        if new.date not in news_dict['date']:
            news_dict['date'].append(new.date)

    #정렬 및 불필요정보 삭제
    news_dict['date'].sort()
    news_dict['date'].insert(0,'날짜를 선택해주세요.')

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    date_data = None
    if request.method == "POST":
        date = request.form.get('dates')

        try:
            date_data = News.query.filter(News.date == date).all()
        except:
            pass

    return render_template('index.html', dates=news_dict, alert_msg=alert_msg, date_data=date_data)