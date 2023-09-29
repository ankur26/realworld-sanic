# ![RealWorld Example App](logo.png)

> ### [Sanic](https://sanic.dev/en/) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a backend API built with **Sanic** including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the **Sanic** community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.


# How it works

This is then general folder structure of the application

```.
├── conduit.db (This is the database that gets created on app startup)
├── helpers ( Helpers to offload repeated code from services )
│   ├── article_and_comment_fetch_helper.py
│   ├── jwt_token_helper.py
│   └── serializer_helper.py
├── middleware ( Middleware for every request )
│   ├── __init__.py
│   ├── requestcontentvalidator.py
│   └── requestvalidator.py
├── models (Database ORM models)
│   ├── __init__.py
│   ├── Article.py
│   ├── Base.py
│   ├── Comments.py
│   ├── FavoritedArticlesByUser.py
│   ├── Followers.py
│   ├── Tags.py
│   ├── TagToArticle.py
│   └── User.py
├── requirements.txt 
├── schemas (Validation and serialization schemas for incoming and outgoing data)
│   ├── __init__.py
│   ├── ArticleAndCommentValidationAndSerializationSchema.py
│   ├── ProfileSerializationSchemas.py
│   └── UserValidationAndSerializationSchemas.py
├── server.py (startup file for sanic to load the app)
└── services (core files which cover all the routes for API)
    ├── __init__.py
    ├── articleandcomment.py
    ├── auth.py
    ├── profile.py
    └── tag.py
```

# Libraries used
1. [Sanic](sanic.dev/) - asynchronous Python web framework
2. [Peewee](http://docs.peewee-orm.com/en/latest/) - easy to use ORM
3. [Pydantic](https://docs.pydantic.dev/latest/) - Fast and extensible validation library, most used validation library for Python
4. [Isort](https://pycqa.github.io/isort/index.html) and [Black](https://black.readthedocs.io/en/stable/) for import orders, and linting.
5. [Bcrpyt](https://pypi.org/project/bcrypt/) for password hashing and [PyJWT](https://pyjwt.readthedocs.io/en/stable/) for authentication.

# Getting started

1. Clone the repo
2. Create a virtual environment using venv, virtualenv inside the repo directory
> python -m venv .venv

3. Activate the virtual enviroment in 
    - Windows - using `./.venv/Scripts/activate`
    - Linux - using `source .venv/bin/activate`

4. Install the required dependencies using `pip install -r requirements.txt`
5. Launch the app locally using `sanic server:create_app --factory (--dev:optional)`


# Specs tracker
- Auth
    - [x] Registration
    - [x] Authentication
    - [x] Get current user
    - [x] Update User
- Profile
    - [x] Get Profile
    - [x] Follow User
    - [x] Unfollow User
- Articles
    - [x] List Articles
    - [x] Get Articles
    - [x] Get Feed
    - [x] Fitler Articles
    - [x] Get Article
    - [x] Create Article
    - [x] Update Article
    - [x] Delete Article
- Comments
    - [x] Get Comments
    - [x] Add Comments
    - [x] Delete Comments
- Tags
    - [x] Get Tags


- Additional Features (as mentioned in Sanic's best practices docs and some more generic stuff)
- [x] Centralized logging using Sanic logger
- [x] Custom exception handler and logging using Sanic logger and Sanic exception
- [x] Segregation of services using Sanic Blueprints
- [ ] Unit testing
- [ ] Containerization using docker
- [ ] OpenAPI spec
- [ ] Migration to poetry for package manager and script setup

