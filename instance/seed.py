from cwmt.models.roles import Role
from cwmt.models.users import User  
from cwmt.models.teams import Team  
from cwmt.models.locations import Location
from cwmt.models.templates import Template
from cwmt.models.cohorts import Cohort


from cwmt import core

db = core.app.db
app = core.app

def create_roles():
    roles = [
        "Sys Admin",
        "Owner",
        "Instructor",
        "Student",
    ]
    for role in roles:
        Role.create(role)

def create_users():
    users = [
        {
            "first_name": "Art",
            "last_name": "Ivanenko",
            "email": "ai@email.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Owner"]
        },
        {
            "first_name": "Shy",
            "last_name": "Pickard",
            "email": "sp@email.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Instructor"]
        },
        {
            "first_name": "Alice",
            "last_name": "Rider",
            "email": "alice@motorclass.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Student"]
        },
        {
            "first_name": "Emily",
            "last_name": "Instructor",
            "email": "emily.instructor@motorclass.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Instructor"],
        },
        {
            "first_name": "Michael",
            "last_name": "Instructor",
            "email": "michael.instructor@motorclass.com",
            "password": "password",
            "is_active": True,
            "has_verified_email": True,
            "roles": ["Instructor"],
        }
    ]
    for user_data in users:
        user_roles = user_data.pop("roles")
        user_obj = User.create(user_data)
        if not user_obj:  # if creation returned None, fetch by email
            user_obj = User.query.filter_by(email=user_data["email"]).first()
        for role_name in user_roles:
            role = Role.get_by_name(role_name)
            if role not in user_obj.roles:
                user_obj.roles.append(role)
    db.session.commit()

# New team creation function
def create_teams():
    team_data = {
        "name": "Default Motorcycle Training Team",
        "description": "Seed team for motorcycle training classes"
    }
    Team.create(team_data)
    db.session.commit()

def create_locations():
    locations = [
        {
            "name": "Main Training Ground",
            "description": "Primary location for motorcycle training sessions",
            "street": "101 Rider Ave",
            "city": "Motorville",
            "state": "TX",
            "zip_code": "75001"
        },
        {
            "name": "Downtown Training Facility",
            "description": "Secondary site for advanced training classes",
            "street": "202 Engine St",
            "city": "Motorville",
            "state": "TX",
            "zip_code": "75002"
        }
    ]
    for location in locations:
        Location.create(location)

def create_templates():
    templates = [
        {
            "default_name": "Basic Motorcycle Training",
            "description": "Introduction to motorcycle basics and safety",
            "default_max_capacity": 12,
            "default_number_of_days": 7
        },
        {
            "default_name": "Advanced Riding Techniques",
            "description": "In-depth training on advanced motorcycle handling skills",
            "default_max_capacity": 10,
            "default_number_of_days": 5
        }
    ]
    for template in templates:
        Template.create(template)

def create_cohorts():
    cohorts = [
        {
            "name": "Summer Motorcycle Training 2023",
            "max_capacity": 12,
            "description": "Summer training program for new riders",
            "start_date": "2023-07-01",
            "number_of_days": 7,
            "team_id": 1
        },
        {
            "name": "Fall Motorcycle Training 2023",
            "max_capacity": 10,
            "description": "Fall training focusing on safety and advanced techniques",
            "start_date": "2023-10-01",
            "number_of_days": 5,
            "team_id": 1
        }
    ]
    for cohort in cohorts:
        Cohort.create(cohort)

def seed_data():
    create_roles()
    create_users()
    create_teams()  # Insert default training team
    create_locations()
    create_templates()
    create_cohorts()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
        print("Seed data inserted successfully.")
