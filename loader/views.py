from flask import Blueprint, request, render_template
from loader.utils import *
from functions import *
from json import JSONDecodeError
import logging

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post')
def post_page():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return "Нет картинки или текста"
    if picture.filename.split('.')[-1] not in ['jpeg', 'png']:
        logging.info('Загруженный файл не картинка')
        return 'Неверное расширение файла'

    try:
        picture_path: str = '/' + save_picture(picture)
    except FileNotFoundError:
        logging.error('Фай не найден')
        return 'Файл не найден'
    except JSONDecodeError:
        return 'Невалидный файл'
    post = add_post({'pic': picture_path, 'content': content})
    return render_template('post_uploaded.html', post=post)