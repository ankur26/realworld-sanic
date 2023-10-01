# This is all the sample data that we would need to run the tests


create_users = [
    {
        "username": f"testuser{i}",
        "password": f"testpassword{i}",
        "email": f"test{i}@test.com",
    }
    for i in range(1, 6)
]

single_user = {
    "user": {
        "password": f"testpassword1",
        "email": f"test1@test.com",
    }
}
updated_user = {"user": {"email": "test100@email.com"}}


user_for_profile_1 = {"user": {"email": "jake@jake.jake", "password": "jakejake"}}

user_for_profile_1_registration = {
    "user": {"username": "Jacob", "email": "jake@jake.jake", "password": "jakejake"}
}
user_for_profile_2 = {"user": {"email": "ankur@ankur.ankur", "password": "ankurankur"}}

user_for_profile_2_registration = {
    "user": {
        "username": "Ankur",
        "email": "ankur@ankur.ankur",
        "password": "ankurnakur",
    }
}

article_1 = {
    "article": {
        "title": "How to train your dragon part 1",
        "description": "Ever wonder how? how can you?",
        "body": "You have to believe",
        "tagList": ["reactjs", "angularjs", "dragons"],
    }
}
article_2 = {
    "article": {
        "title": "How to train your dragon part 2",
        "description": "Ever wonder how? you can! Toothless is here for you",
        "body": "You have to believe",
        "tagList": ["reactjs", "angularjs", "dragons", "vuejs", "sanic"],
    }
}

update_article = {"article": {"title": "Did you train your dragon?"}}

comment_1 = {"comment": {"body": "It takes a Jacobian"}}


comment_2 = {"comment": {"body": "I like Sanic"}}
