from cwmt.models.roles import Role
from cwmt.models.users import User  
from cwmt.models.teams import Team  
from cwmt import core

db = core.app.db
app = core.app

def create_roles():
    roles = [
        "Sys Admin",
        "Owner",
        "Admin",
        "Instructor",
        "Student"
    ]
    for role in roles:
        Role.create(role)

def create_users():
    users = [
        {
            "first_name": "art",
            "last_name": "Ivanenko",
            "email": "ai@email.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Owner"]
        },
        {
            "first_name": "shy",
            "last_name": "Picard",
            "email": "sp@email.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Admin"]
        },
    ]
    for user in users:
        user_roles = user.pop("roles")
        user = User.create(user)
        for role in user_roles:
            role = Role.get_by_name(role)
            user.roles.append(role)
        db.session.commit()

def seed_data():
    create_roles()
    create_users()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
        print("Seed data inserted successfully.")
