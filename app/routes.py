from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ArticleForm

@app.route('/')
@app.route('/index')
def index():
    articles = [
        {
            'title': 'Labour to win elections',
            'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            'category': 'politics'
        }, {
            'title': 'Eklat at Cybertruck presentation',
            'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            'category': 'technology'
        }, {
            'title': 'Ansys shares increase by 6.7%',
            'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            'category': 'economy'
        }
    ]
    return render_template('index.html', title='Home', articles=articles)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        flash('New article submitted: {}, category: {}'.format(
            form.title.data, form.category.data))
        return redirect(url_for('index'))
    return render_template('create.html', title='New Article', form=form)