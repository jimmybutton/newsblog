# newsblog
A simple news blog with CRUD functionality based on flask and bootstrap

### Functionality
* Add, edit and delete articles with feature image
* Filter articles based on categories
* Show notifications of user actions (flash)
* Show confirm modal before deleting articles
* Delete uploaded images when deleting or updating an article
* Pagination
* Display create date with flask-moment

### ToDo
* add search functionality (elasticsearch)
* use blueprints to avoid circular dependencies
* return to last page viewed when canceling a form

## Setup

### Install dependencies
```
pip install -r requirements.txt
```

Uses:
- flask
- flask-wtf
- flask-sqlalchemy
- flask-migrate
- flask-dotenv

### run application
```
run flask
```

