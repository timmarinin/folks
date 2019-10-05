
class Permission(int):
    """
    Simple bit-based permission system.
    To check for whether user can do something, just do
    user_perms & needed_perms, and if the result is > 0,
    then it's OK.
    """
    NoRestrictions = 0b0000_0000
    Login = 0b0000_0001
    CreatePosts = 0b0000_0010
    UploadImages = 0b0000_0100
    CreateHats = 0b0000_1000
    InviteUsers = 0b0001_0000
    # placeholder  = 0b0010_0000
    Moderate = 0b0100_0000
    Administration = 0b1000_0000
    # presets
    User = Login | CreatePosts | UploadImages | CreateHats
    Admin = Administration | Moderate | CreateHats | UploadImages | CreatePosts | Login

    def __repr__(self):
        return "<Permission {0:b}>".format(self, zfill=8)

    def to_role(perms):
        return Permission(perms)

    def can(self, needed):
        return self & needed > 0
