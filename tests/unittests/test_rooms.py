from app import db
from models import RoomModel, UserModel

def test_create_room(logged_client):
    response = logged_client.post("/room/create")
    assert response.status_code == 400
    response = logged_client.post("/room/create", data = {
        "name": "hello1"
    })
    assert response.status_code == 200
    response = logged_client.post("room/create", data = {
        "name": "hello1"
    })
    assert response.status_code == 400
    assert response.json["error"] == "room name taken"
    response = logged_client.post("/room/create", data = {
        "name": ""
    })
    assert response.status_code == 400
    assert response.json["error"] == "Form not filled correctly"
    response = logged_client.post("/room/create", data = {
        "name": "123123123123123123123123123123123123123123123123123123"
    })
    assert response.status_code == 400
    assert response.json["error"] == "Form not filled correctly"
    response = logged_client.post("/room/create", data = {
        "name": "1231231231231",
        "password": "wagwan"
    })
    assert response.status_code == 200
    response = logged_client.post("/room/create", data = {
        "name": "wagwans",
        "password": ""
    })
    assert response.status_code == 200
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    #max room testing
    for i in range(0, 8):
        room = RoomModel(
                name = i,
                roles = {"Owner": f"{user.id}",
                         "Admins": []},
                people = 1
            )
        db.session.add(room)
        room.users.append(user)
        db.session.commit()
    
    response = logged_client.post("/room/create", data = {
        "name": "wagwansmyg",
        "password": ""
    })
    assert response.status_code == 400
    assert response.json["error"] == "Can't make any more rooms"

def test_load_rooms(logged_client):
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    #max room testing
    for i in range(0, 10):
        room = RoomModel(
                name = i,
                roles = {"Owner": f"{user.id}",
                         "Admins": []},
                people = 1
            )
        db.session.add(room)
        room.users.append(user)
        db.session.commit()
    response = logged_client.get("/rooms/")
    assert response.status_code == 200
    assert len(response.json) == 10

def test_my_rooms(logged_client):
    response = logged_client.get("/my_rooms")
    assert response.status_code == 200
    assert len(response.json) == 0
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    #max room testing
    for i in range(0, 10):
        room = RoomModel(
                name = i,
                roles = {"Owner": f"{user.id}",
                         "Admins": []},
                people = 1
            )
        db.session.add(room)
        room.users.append(user)
        db.session.commit()
    response = logged_client.get("/my_rooms")
    assert response.status_code == 200
    assert len(response.json) == 10

def test_delete_rooms(logged_client, false_client):
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    #max room testing
    for i in range(0, 10):
        room = RoomModel(
                name = i,
                roles = {"Owner": f"{user.id}",
                         "Admins": []},
                people = 1
            )
        db.session.add(room)
        room.users.append(user)
        db.session.commit()
    response = logged_client.get("/my_rooms")
    assert response.status_code == 200
    assert len(response.json) == 10
    id_list = [room["id"] for room in response.json]
    for id in id_list:
        response = logged_client.get(f"/delete_room/{id}")
        assert response.status_code == 200
    for id in id_list:
        response = logged_client.get(f"/delete_room/{id}")
        assert response.status_code == 400
        assert response.json["message"] == "Not in room"
    false_user = db.session.execute(db.select(UserModel).where(UserModel.username=="batman567")).scalar()
    room = RoomModel(
            name = "first",
            roles = {"Owner": f"{user.id}",
                        "Admins": []},
            people = 2
        )
    db.session.add(room)
    room.users.append(user)
    room.users.append(false_user)
    db.session.commit()
    room = db.session.execute(db.select(RoomModel).where(RoomModel.name=="first")).scalar()
    response = false_client.get(f'/delete_room/{room.id}')
    print (response.json)
    assert response.status_code == 200
    assert response.json["Status"]