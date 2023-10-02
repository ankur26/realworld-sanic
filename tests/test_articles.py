from sample_data import article_1, article_2, slug1, slug2, update_article, user_for_profile_1, user_for_profile_2, user_for_profile_1_registration, user_for_profile_2_registration
from sanic_testing.reusable import ReusableClient

"""
This test we'll try to follow this procedure
Each user creates an article, we then make them
We then look at this articles anonymously
We then also look at these articles with a logon
And then finally we will filter the articles by the query params to see if things match
The testing approach will also be just a little different as we're going to use a totally independent test client 
"""


    
def test_create_article(app):
    client = ReusableClient(app)
    # We have one article created by default from the fixture.
    with client:
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)

        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        assert response.status == 200
        token = response.json.get("user").get("token")
        # Test an invalid response
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json={"article": {"title": "123"}})
        assert response.status == 422
        # Test a valid create
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        assert response.status == 200

        # Now do the same for user 2
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        assert response.status == 200
        token = response.json.get("user").get("token")
        # Test an invalid response
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json={"article": {"title": "123"}})
        assert response.status == 422
        # Test a valid create
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        assert response.status == 200

        # We should have two articles now at the end of this, two simple checks to ensure that we got the right info returned
        assert response.json.get("article").get(
            "title") == article_2.get("article").get("title")
        assert response.json.get("article").get("author").get(
            "username") == user_for_profile_2_registration["user"]["username"]

def test_get_article_anonymous(app):
    client = ReusableClient(app)
    with client:
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        # Test a valid create
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        _, response = client.get("api/articles/{}".format(slug1))
        assert response.status == 200
        assert response.json.get("article").get(
            "title") == article_1["article"]["title"]

def test_get_article_non_anonymous(app):
    client = ReusableClient(app)
    with client:
        # create the two users
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        # Now get article for user 1 in user 2's scope
        _,response = client.get("api/articles/{}".format(slug1),headers={"Authorization":f"Token {token}"})
        assert response.status == 200
        assert response.json.get("article").get('title') == article_1["article"]["title"]

def test_favorites_and_favorited_count(app):
    client = ReusableClient(app)
    with client:
        # create the two users
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        # Now get article for user 1 in user 2's scope
        _,response = client.get("api/articles/{}".format(slug1),headers={"Authorization":f"Token {token}"})

        #Favorite the article for user 1 using user 2's token 
        _,response = client.post("api/articles/{}/favorite".format(slug1),headers={"Authorization":f"Token {token}"})
        assert response.status == 200
        assert response.json.get('article').get('favorited') == True
        assert response.json.get('article').get('favoritesCount') == 1

def test_unfavorited_and_favorited_count(app):
    client = ReusableClient(app)
    with client:
        # create the two users
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        # Now get article for user 1 in user 2's scope
        _,response = client.get("api/articles/{}".format(slug1),headers={"Authorization":f"Token {token}"})

        #Favorite the article for user 1 using user 2's token 
        _,response = client.post("api/articles/{}/favorite".format(slug1),headers={"Authorization":f"Token {token}"})
        assert response.status == 200
        assert response.json.get('article').get('favorited') == True
        assert response.json.get('article').get('favoritesCount') == 1
        _,response = client.delete("api/articles/{}/favorite".format(slug1),headers={"Authorization":f"Token {token}"})
        assert response.json.get('article').get('favorited') == False
        assert response.json.get('article').get('favoritesCount') == 0


def test_filters(app):
    client = ReusableClient(app)
    with client:
        # create the two users
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        
        _, response = client.get("api/articles", params={"tag":"reactjs"})
        assert response.status == 200
        assert "articles" in response.json
        assert "articlesCount" in response.json
        assert len(response.json.get("articles")) == 2

        #Filter by author
        _,response = client.get("api/articles",params={"author":"Jacob"})
        assert "articles" in response.json
        assert "articlesCount" in response.json
        assert len(response.json.get("articles")) == 1

        #Filter by favorites - there's none so we should expect 0
        _,response = client.get("api/articles",params={"favorited":"Jacob"})
        assert "articles" in response.json
        assert "articlesCount" in response.json
        assert len(response.json.get("articles")) == 0

def test_update_article(app):
    client = ReusableClient(app)
    with client:
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)
        
        _,response = client.delete("api/articles/{}".format(slug2),headers={"Authorization": f"Token {token}"})
        assert response.status == 200
        assert "status" in response.json
        assert response.json.get("status") == True
        
        _,response = client.delete("api/articles/{}".format(slug1),headers={"Authorization": f"Token {token}"})
        assert response.status == 403 # We should not be allowed to delete someone elses slug

def test_update_article(app):
    client = ReusableClient(app)
    with client:
        client.post("/api/users",json=user_for_profile_1_registration)
        client.post("/api/users",json=user_for_profile_2_registration)
        #Create two articles
        _, response = client.post(
            "/api/users/login", json=user_for_profile_1)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_1)
        # second article
        _, response = client.post(
            "/api/users/login", json=user_for_profile_2)
        token = response.json.get("user").get("token")
        _, response = client.post(
            "/api/articles", headers={"Authorization": f"Token {token}"}, json=article_2)

        _,response = client.put("/api/articles/{}".format(slug2),headers={"Authorization": f"Token {token}"},json=update_article)

        assert response.status == 200
        assert "article" in response.json
        assert response.json.get("article").get("title") == update_article["article"]["title"]

