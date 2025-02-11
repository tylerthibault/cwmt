from cwmt import AppCore
from cwmt.models.roles import Roles
from cwmt.models.users import User  # ...existing code: adjust import as necessary...
from cwmt.models.teams import Team  # ...existing code: adjust import as necessary...

db = AppCore.app.db
app = AppCore.app

def seed_data():
    # Seed roles
    for role_name in ['admin', 'user']:
        if not Roles.get_by_name(role_name):
            Roles.create(role_name)
    # Seed user "art"
    # Assuming User has a field 'username' and a class method get_by_username
    art_user = User.get_by_username("art")
    if not art_user:
        art_user = User(
            username="art",
            email="art@example.com",
            password=app.bcrypt.generate_password_hash("password").decode('utf-8')
            # ...other required fields...
        )
        db.session.add(art_user)
        db.session.commit()
    # Seed team for user "art"
    if not Team.query.filter_by(name="Team Art").first():
        team_art = Team(
            name="Team Art",
            owner_id=art_user.id  # Assuming 'owner_id' field exists
            # ...other required fields...
        )
        db.session.add(team_art)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
        print("Seed data inserted successfully.")
