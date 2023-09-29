# ![RealWorld Example App](logo.png)

> ### [Sanic](https://sanic.dev/en/) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.


### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld) (Work in progress, these are the original links)


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


# Getting started

1. Clone the repo
2. Create a virtual environemnt using venv, virtualenv inside the repo directory
> python -m venv .venv

3. Activate the virtual enviroment in 
    - Windows - using `./.venv/Scripts/activate`
    - Linux - using `source .venv/bin/activate`

4. Install the required dependencies using `pip install -r requirements.txt`
5. Launch the app locally using `sanic server:create_app --factory (--dev:optional)`

