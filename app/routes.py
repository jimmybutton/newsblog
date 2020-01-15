from flask import render_template, flash, redirect, url_for, request, current_app
from app import app, db
from app.forms import ArticleForm, ArticleDeleteForm
from app.models import Article
from werkzeug.utils import secure_filename
import os
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(imagefiledata):
    # get file and save it
    f = imagefiledata
    extension = secure_filename(f.filename).split('.')[-1]
    # generate a unique filename using UTC time
    filename = datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S') + "." + extension
    # check wheather upload folder exists
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.created.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=articles.next_num) if articles.has_next else None
    prev_url = url_for('index', page=articles.prev_num) if articles.has_prev else None
    return render_template('index.html', title='Home', articles=articles.items, next_url=next_url, prev_url=prev_url)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = upload_image(form.image.data)
        else:
            filename = ""
        # store article in db
        article = Article(
            title=form.title.data, 
            content=form.content.data, 
            category=form.category.data,
            image=filename
        )
        db.session.add(article)
        db.session.commit()
        flash('New article submitted: {}, category: {}'.format(
            form.title.data, form.category.data))
        return redirect(url_for('index'))
    return render_template('create.html', title='New Article', form=form)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    article = Article.query.filter_by(id=id).first_or_404()
    form = ArticleForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = upload_image(form.image.data)
            article.image = filename
        article.title = form.title.data
        article.content = form.content.data
        article.category = form.category.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
        form.category.data = article.category
    return render_template('update.html', title='Edit Article', form=form, article=article)

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    article = Article.query.filter_by(id=id).first_or_404()
    title = article.title
    if article:
        db.session.delete(article)
        db.session.commit()
        flash(f"The article {title} has been deleted.")
    return redirect(url_for('index'))
