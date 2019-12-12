from flask import render_template, flash, redirect, url_for, request, current_app
from app import app, db
from app.forms import ArticleForm
from app.models import Article
from werkzeug.utils import secure_filename
import os
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    articles = Article.query.order_by(Article.created.desc()).all()
    return render_template('index.html', title='Home', articles=articles)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        flash('New article submitted: {}, category: {}'.format(
            form.title.data, form.category.data))
        # get file and save it
        f = form.image.data
        filename = secure_filename(f.filename)
        # generate a unique filename using UTC time
        filename = datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S') + "." + filename.split('.')[-1]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # store article in db
        article = Article(
            title=form.title.data, 
            content=form.content.data, 
            category=form.category.data,
            image=filename
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', title='New Article', form=form)