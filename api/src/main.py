from domain.users.user import User

user = User(1, "test")


def test(user):
    user.messages.append({"1": "rere"})


test(user)

print(user)
