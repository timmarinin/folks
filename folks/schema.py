from marshmallow import fields, Schema, ValidationError, post_load
from models import Post, Hat, User

class UserSchema(Schema):
    class Meta:
        fields = ('username', 'registered_at', 'permissions', 'reader_feed')
    reader_feed = fields.Function(lambda user: user.reader_feed.id)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class HatSchema(Schema):
    class Meta:
        fields = (
            'username',
            'display_name',
            'about_me',
            'avatar_url',
            'created_at'
        )


hat_schema = HatSchema()
hats_schema = HatSchema(many=True)


class InviteSchema(Schema):
    class Meta:
        fields = ('invite_code', 'redeemed_at', 'redeemer')
    redeemer = fields.Nested(UserSchema)


invite_schema = InviteSchema()
invites_schema = InviteSchema(many=True)

class AttachmentSchema(Schema):
    class Meta:
        fields=  ('id', 'attach_type', 'url')

class PostSchema(Schema):
    class Meta:
        fields = ('id', 'body', 'posted_at', 'author', 'attachments')
    body = fields.Str(required=True)
    author = fields.Nested(HatSchema)
    attachments = fields.Nested(AttachmentSchema, many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class NewPostSchema(Schema):
    body = fields.Str(required=True)
    username = fields.Str(required=True)
    @post_load
    def make_post(self, data, **kwargs):
        return Post(body=data['body'])
new_post_schema = NewPostSchema()


class TokenSchema(Schema):
    class Meta:
        fields = ('token', 'expiration_date')
    token = fields.Str()


token_schema = TokenSchema()

class SinkSchema(Schema):
    posts = fields.Nested(PostSchema)
    sink_type = fields.Str()

sink_schema = SinkSchema()


class RegistrationSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    invite = fields.Str(required=True)


registration_schema = RegistrationSchema()

class PassAuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
pass_auth_schema = PassAuthSchema()
