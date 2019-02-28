from app import db, VIDEO_DIR
from app.main import bp
from flask import render_template, url_for, redirect, request, flash, jsonify
from app.main.forms import TranslationForm, EditWordForm
from flask_login import current_user, login_required
from app.models import User, Word
from config import Config
import os
from app.translate import translate
import random


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = TranslationForm()
    if form.validate_on_submit():
        word = Word(word=form.input_text.data.lower(), translate=form.output_text.data.lower(), user_id=int(current_user.get_id()))
        db.session.add(word)
        db.session.commit()
        flash('"{}" added to your dictionary'.format(word.word))
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])})


@bp.route('/my_dictionary/<letter>')
@login_required
def my_dictionary(letter):
    my_words = current_user.word.filter(Word.word.startswith(letter.lower())).all()
    return render_template('my_dictionary.html', title='My Dictionary', my_words=my_words, letter=letter)


@bp.route('/videos/<series>')
@login_required
def videos(series):
    list_of_series = sorted(os.listdir(VIDEO_DIR))
    list_of_episodes = sorted([ file for file in os.listdir(os.path.join(VIDEO_DIR, series)) if file.endswith('mp4')])
    return render_template('videos.html', title='Videos', list_of_series=list_of_series, list_of_episodes=list_of_episodes, series=series)


@bp.route('/delete_word/<int:id>')
@login_required
def delete_word(id):
    word = current_user.word.filter_by(id=id).first()
    db.session.delete(word)
    db.session.commit()
    return redirect(url_for('main.my_dictionary', letter='A'))


@bp.route('/check_youself/<int:word_count>')
@login_required
def check_youself(word_count):
    user_word_list = current_user.word.all()
    if len(user_word_list) < word_count:
        word_count = len(user_word_list)
    word_list = random.sample(user_word_list, word_count)
    return render_template('check_youself.html',title='Check Youself', word_list=word_list)


@bp.route('/edit_word/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_word(id):
    word = Word.query.get(id)
    form = EditWordForm()
    if form.validate_on_submit():
        word.word = form.word.data
        word.translate = form.translate.data.lower()
        word.sentence = form.sentence.data
        word.comment = form.comment.data
        db.session.commit()
        flash('Word in your Dictionary update')
        return redirect(url_for('main.my_dictionary', letter='A'))
    elif request.method == 'GET':
        form.word.data = word.word
        form.translate.data = word.translate
        form.sentence.data = word.sentence
        form.comment.data = word.comment
        return render_template('edit_word.html', title='Edit Word', form=form)
