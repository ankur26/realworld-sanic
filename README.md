# ![RealWorld Example App](logo.png)

> ### [Sanic](https://sanic.dev/en/) codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld) spec and API.

### [Demo](https://demo.realworld.io/)&nbsp;&nbsp;&nbsp;&nbsp;[RealWorld](https://github.com/gothinkster/realworld)


This codebase was created to demonstrate a backend API built with **Sanic** including CRUD operations, authentication, routing, pagination, and more.

We've gone to great lengths to adhere to the **Sanic** community styleguides & best practices.

For more information on how to this works with other frontends/backends, head over to the [RealWorld](https://github.com/gothinkster/realworld) repo.

**All contributions are welcome!**
# How it works

This is then general folder structure of the application

```
├── helpers (Offloaded repetitive function calls)
│   ├── __init__.py
│   ├── article_and_comment_fetch_helper.py
│   ├── jwt_token_helper.py
│   └── serializer_helper.py
├── middleware (Decorator style functions for middleware such as validation and token checks)
│   ├── __init__.py
│   ├── request_content_validator.py
│   └── request_header_and_body_validator.py
├── models (Database models - used to create and query)
│   ├── __init__.py
│   ├── article.py
│   ├── articletag.py
│   ├── base.py
│   ├── comment.py
│   ├── follower.py
│   ├── tag.py
│   ├── userfavorite.py
│   └── user.py
├── schemas (Used to validate incoming requests and serialize outgoing ones)
│   ├── __init__.py
│   ├── article_comment_schema.py
│   ├── profile_schema.py
│   └── user_schema.py
└── services (Core route blueprints, responsible for overall request response cycle)
    ├── __init__.py
    ├── article_comment_service.py
    ├── auth_service.py
    ├── profile_service.py
    └── tag_service.py
├── server.py (Core server file, has setup and configuration)
```

# Requirements
The application has been tested with version Python 3.10.12, we recommend you install at least 3.10 to best reproduce the results
# Getting started

1. Clone the repo
2. Create a virtual environment using venv, virtualenv inside the repo directory
> python -m venv .venv

3. Activate the virtual enviroment in 
    - Windows - using `./.venv/Scripts/activate`
    - Linux - using `source .venv/bin/activate`

4. Install the required dependencies using `pip install -r requirements.txt`
5. Launch the app locally using `sanic realworld.server:create_app --dev`(Dev mode) or `sanic realworld.server:create_app`(Production mode)
    1. To run unit tests using the API test script
        1. Install newman using [npm](https://www.npmjs.com/) (Requires [NodeJS](https://nodejs.org/en))
        2. In the project's root directory, run the test using `APIURL=http://localhost:8000/api ./run-api-tests.sh`
    2. To run the tests using pytest run `pytest tests/`
        1. For the verbose option use `pytest --verbose tests/`
        2. To see the code coverage use `pytest --cov=realworld/ tests/` (You can combine these two options)

## Specs tracker
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


## Additional Features (more generalized things)
- [x] Centralized logging using Sanic logger
- [x] Custom exception handler and logging using Sanic logger and Sanic exception
- [x] Segregation of services using Sanic Blueprints
- [x] Unit testing (Currently at 64%, contributions are welcome!)
- [ ] Containerization using docker (Simple docker file, for local runs - in progress)
``- [ ] OpenAPI spec``

# Libraries used
1. [Sanic](sanic.dev/) - asynchronous Python web framework
2. [Peewee](http://docs.peewee-orm.com/en/latest/) - easy to use ORM
3. [Pydantic](https://docs.pydantic.dev/latest/) - Fast and extensible validation library, most used validation library for Python
4. [Isort](https://pycqa.github.io/isort/index.html) and [Black](https://black.readthedocs.io/en/stable/) for import orders, and linting.
5. [Bcrpyt](https://pypi.org/project/bcrypt/) for password hashing and [PyJWT](https://pyjwt.readthedocs.io/en/stable/) for authentication.


