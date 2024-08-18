from marshmallow import Schema, fields, post_dump, validate
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class UserForm(FlaskForm):
    username = StringField("username", [validators.Length(min=6, max=20, message="Username is a little too long there bud. 6-20 characters."), validators.InputRequired()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "username"})
    email = StringField("email", [validators.InputRequired(), validators.Email()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "johndoe@gmail.com"})
    password = StringField("password", [validators.Length(min=8, max=60, message="Password's gotta be between 8 and 60 characters long."), validators.InputRequired()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "password"})

class LoginForm(FlaskForm):
    username = StringField("username", [validators.InputRequired()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "username"})
    password = StringField("password", [validators.InputRequired()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "password"})

class RoomForm(FlaskForm): 
    name = StringField("Room Name", [validators.Length(min=6, max=20, message="Room name can only have 20 characters max."), validators.InputRequired()], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "Room Name"} )
    password = StringField("Password", [validators.Length(min=1, max=20, message="Password is 20 characters max"), validators.Optional(strip_whitespace=True)], render_kw={"autocorrect": "off", "autocapitalize": "off", "autocomplete": "off", "placeholder": "Password"} )

class RoomsReturnSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    password = fields.Str(load_only=True)
    password = fields.Bool(dump_only = True)
    people = fields.Int(dump_only = True)
    @post_dump
    def add_password_exists(self, data, many, **kwargs):
        data['password_exists'] = 'password' in data and bool(data['password'])
        return data
    
class CreateChannelSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    room = fields.Str(required=True)

class ReturnChannelSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    room_id = fields.Str(required=True)

class DeleteChannelSchema(Schema):
    channel_id = fields.Str(required=True)
    room = fields.Str(required=True)

class EditChannelSchema(Schema):
    new_name = fields.Str(required=True)
    channel_id = fields.Str(required=True)
    room = fields.Str(required=True)

class ReturnMessageSchema(Schema):
    text = fields.Str()
    username = fields.Str()

class EditAccountSchema(Schema):
    new_name = fields.Str(required=False, validate=validate.Length(min=6, max=20))
    old_pass = fields.Str(required=False)
    new_pass = fields.Str(required=False, validate=validate.Length(min=8, max=60))