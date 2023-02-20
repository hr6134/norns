from enum import Enum


class UserRoles(Enum):
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER = 'user'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(self.value) == other

    @classmethod
    def choices(cls):
        return tuple((role.value, role.name.lower()) for role in cls)


print(UserRoles.choices())
print(UserRoles.USER)
