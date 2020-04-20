from flask import render_template, flash, redirect, url_for, request, current_app
from app import app, db
from app.forms import ArticleForm, ArticleDeleteForm
from app.models import Article, Category
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

def delete_upload_image(imagename):
    # delete image from upload folder
    filename = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
    if os.path.exists(filename):
        os.remove(filename)

@app.route('/')
@app.route('/index')
def index():
    category_id = request.args.get('category', 0, type=int)
    page = request.args.get('page', 1, type=int)
    if category_id == 0:  # 0 meaning all categories
        articles = Article.query.order_by(Article.created.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('index', page=articles.next_num) if articles.has_next else None
        prev_url = url_for('index', page=articles.prev_num) if articles.has_prev else None
        category_name = None
    else:
        category = Category.query.get(category_id)
        if not category:
            flash('Category does not exist.'.format(category_id))
            return redirect(url_for('index'))
        articles = Article.query.filter_by(category=category).order_by(Article.created.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('index', page=articles.next_num, category=category.id) if articles.has_next else None
        prev_url = url_for('index', page=articles.prev_num, category=category.id) if articles.has_prev else None
        category_name = category.name
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('index.html', title='Home', articles=articles.items, categories=categories, 
                            category_name=category_name, next_url=next_url, prev_url=prev_url)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = upload_image(form.image.data)
        else:
            filename = ""
        category = Category.query.get(int(form.category.data))
        # store article in db
        article = Article(
            title=form.title.data, 
            content=form.content.data, 
            category=category,
            image=filename
        )
        db.session.add(article)
        db.session.commit()
        flash('New article submitted: {}, category: {}'.format(
            form.title.data, category.name))
        return redirect(url_for('index'))
    return render_template('create.html', title='New Article', form=form)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    article = Article.query.get(id)
    form = ArticleForm()
    if form.validate_on_submit():
        if form.image.data:
            # first delete image from upload folder!
            delete_upload_image(article.image)
            # upload new image
            filename = upload_image(form.image.data)
            article.image = filename
        article.title = form.title.data
        article.content = form.content.data
        article.category = Category.query.get(int(form.category.data))
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
        form.category.data = str(article.category.id)
    return render_template('update.html', title='Edit Article', form=form, article=article)

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    article = Article.query.get(id)
    if article:
        title = article.title
        # first delete image from upload folder!
        delete_upload_image(article.image)
        # flash(f"Image {filename} has been deleted.")
        # remove article from db
        db.session.delete(article)
        db.session.commit()
        flash(f"The article {title} has been deleted.")
    return redirect(url_for('index'))
