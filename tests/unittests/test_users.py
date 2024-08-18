from app import db
from models import UserModel
import bcrypt

def repeat_login(client):
    user = UserModel(
                username = "bazookas123",
                password = bcrypt.hashpw("bazookas12893".encode("utf-8"), bcrypt.gensalt()),
                email = "bazjkokas@gmail.com"
            )
    db.session.add(user)
    db.session.commit()
    response = client.post("/login", data={
        "username": "bazookas123",
        "password": "bazookas12893"
    })
    assert response.status_code == 302
    assert "/home" in response.location

#sign up functions
def test_get_sign_up(client):
    response = client.get("/sign_up")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "<title>ChatRoom: Sign Up</title>" in html
    assert '<form id = "sign-up" method="post">' in html

def test_sign_up(client):
    response = client.post("/sign_up", data={
        "username": "bazookas123",
        "email": "bazjkokas@gmail.com",
        "password": "bazookas12893"
    })
    assert response.status_code == 302
    response = client.post("/sign_up", data={
        "username": "bazookafs",
        "email": "bazookfas@gmail.com",
    })
    html = response.data.decode("utf-8")
    assert '<form id = "sign-up" method="post">' in html

def test_get_login(client):
    response = client.post("/login")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "<title>Personal ChatRoom</title>"

def test_login(client):
    response = repeat_login(client)
    cookie_check = client.get("/home")
    assert cookie_check.status_code == 200
    html = cookie_check.data.decode("utf-8")
    assert "<title>ChatRoom: Home</title>" in html
    response2 = client.post("/login", data={
        "username": "bazookas123",
        "password": "bazookas12812393"
    })
    assert response2.status_code != 302
    assert not response2.location
    response3 = client.post("/login", data={
        "username": "bazookas123",
    })
    assert response3.status_code != 302
    response4 = client.post("/login", data={
        "password" : "12312312"
    })
    assert response3.status_code != 302
    
def test_logout(client):
    response = repeat_login(client)
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.location

def test_edit_account_get(client):
    response = repeat_login(client)
    response = client.get("/edit_account")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "<title>Edit Account</title>" in html
    client.get("/logout")
    response = client.get("/edit_account")
    assert response.status_code == 302

def test_edit_username(client):
    response = repeat_login(client)
    response = client.put("/edit_account")
    assert response.status_code == 400
    response = client.put("/edit_account", json={
        "new_name": ""
    })
    assert response.status_code == 422
    response = client.put("/edit_account", json={
        "new_name": "timberlake"
    })
    assert response.status_code == 200
    response = client.put("/edit_account", json={
        "old_pass": "timberlake",
        "new_pass": "bumbojumbo"
    })
    assert response.status_code == 400
    response = client.put("/edit_account", json={
        "old_pass": "bazookas12893",
        "new_pass": "bumbojumbo"
    })
    assert response.status_code == 200
    response = client.put("/edit_account", json={
        "old_pass": "bumbojumbo",
        "new_pass": ""
    })
    assert response.status_code == 422
    response = client.put("/edit_account", json={
        "new_pass": "asdfasdfa"
    })
    assert response.status_code == 400

def test_user_delete(client):
    response = repeat_login(client)
    response = client.delete("/edit_account")
    assert response.status_code == 400
    response = client.delete("/edit_account", json={
        "old_pass": "chickens"
    })
    assert response.status_code == 400
    response = client.delete("/edit_account", json={
        "old_pass": "bazookas12893"
    })
    assert response.status_code == 204
    response = client.delete("/edit_account")
    assert response.status_code == 302
