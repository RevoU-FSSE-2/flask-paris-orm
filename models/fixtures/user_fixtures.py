from models.users import User
import faker

from config.settings import create_app
from instance.database import db

app = create_app("config.local")
fake = faker.Faker()


def create_users_fixture():
    with app.app_context():
        users = []
        for _ in range(10):
            email = fake.email()
            user = User(
                name=fake.name(),
                email=email,
            )
            user.set_password(f"password|{email}")
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print("INSERTED USERS")
        return users
