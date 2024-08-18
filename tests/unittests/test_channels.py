from app import db
from models import RoomModel, UserModel, ChannelModel

def test_create_channel(logged_client, false_client):
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    room = RoomModel(
            name = "first",
            roles = {"Owner": f"{user.id}",
                        "Admins": []},
            people = 1
        )
    db.session.add(room)
    room.users.append(user)
    db.session.commit()
    room = db.session.execute(db.select(RoomModel).where(RoomModel.name=="first")).scalar()
    response = logged_client.post("/create_channel", json={
        "name": "first_channel",
        "room": f"{room.id}"
    })
    assert response.status_code == 200
    response = logged_client.post("/create_channel", json={
        "name": "third_channel",
        "room": "123lkdjasflkjasfd"
    })
    assert response.status_code == 400
    assert response.json["message"] == "Wrong room."
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="batman567")).scalar()
    response = false_client.post("/create_channel", json={
        "name": "second_channel",
        "room": f"{room.id}"}
        )
    assert response.status_code == 400
    assert response.json["message"] == "You don't have the necessary role."

def test_delete_channel(logged_client, false_client):
    # test case 1 wrong room
    response = logged_client.delete("/delete_channel/", json = {
        "room": "123123",
        "channel_id": "fake"
    })
    assert response.status_code == 404

    #make and get room and user and make channel
    user = db.session.execute(db.select(UserModel).where(UserModel.username=="bazookas123")).scalar()
    room = RoomModel(
            name = "first",
            roles = {"Owner": f"{user.id}",
                        "Admins": []},
            people = 1
        )
    db.session.add(room)
    room.users.append(user)
    db.session.commit()
    room = db.session.execute(db.select(RoomModel).where(RoomModel.name=="first")).scalar()
    channel = ChannelModel(name="first", room_id=room.id)
    room.channels.append(channel)
    db.session.add(room)
    db.session.commit()
    channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.name=="first")).scalar()
    # end of making it

    #test case 2 right room and wrong user
    response = false_client.delete("/delete_channel/", json = {
        "room": room.id,
        "channel_id": channel.id
    })
    assert response.status_code == 400
    assert response.json["message"] == "Room does not exist or you don't have the necessary role."

    #test case 3 right room, right user, one channel
    response = logged_client.delete("/delete_channel/", json = {
        "room": room.id,
        "channel_id": channel.id
    })
    assert response.status_code == 400
    assert response.json["message"] == "Can't delete last channel"

    #second channel for further test cases
    channel = ChannelModel(name="second", room_id=room.id)
    room.channels.append(channel)
    db.session.add(room)
    db.session.commit()
    channel = db.session.execute(db.select(ChannelModel).where(ChannelModel.name=="second")).scalar()

    #test case 4 right room, right user, wrong channel
    response = logged_client.delete("/delete_channel/", json = {
        "room": room.id,
        "channel_id": "1728"
    })
    assert response.status_code == 400
    assert response.json["message"] == "Channel doesn't exist."
    #test case 5 right room, right user, right channel
    response = logged_client.delete("/delete_channel/", json = {
        "room": room.id,
        "channel_id": channel.id
    })
    assert response.status_code == 200
