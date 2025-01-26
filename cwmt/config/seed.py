from cwmt.models.users import User
from cwmt.models.roles import Role, UserRole
from cwmt.models.teams import Team
from cwmt.models.instructors import Instructor
from cwmt.models.courses import Course, CourseSession
from datetime import date, time

def seed_roles():
    """Create system roles if they don't exist."""
    admin_role = Role.query.filter_by(name='sys-admin').first()
    if not admin_role:
        admin_role = Role.create({'name': 'admin', 'description': 'Administrator'})

    instructor_role = Role.query.filter_by(name='instructor').first()
    if not instructor_role:
        instructor_role = Role.create({'name': 'instructor', 'description': 'Instructor'})
    
    return admin_role

def seed_admin_user(admin_role):
    """Create admin user and associated team if they don't exist."""
    admin_user = User.query.filter_by(username='art').first()
    if not admin_user:
        admin_user = User.create({
            'username':'art',
            'email':'art@email.com',
            'password':'Pass123!!'
        })

        team = Team.create({'name': 'Art\'s Team', 'owner_id': admin_user.id})
        UserRole.create({'user_id': admin_user.id, 'role_id': admin_role.id})
        return admin_user, team
    
    team = Team.query.filter_by(owner_id=admin_user.id).first()
    return admin_user, team

def seed_instructors(team):
    """Create instructor users if they don't exist."""
    instructors = [
        {
            'first_name': 'Tyler',
            'last_name': 'Tbo',
            'email': 'tt@email.com',
            'password': 'Pass123!!',
            'phone': '123123123',
        },
        {
            'first_name': 'Joe', 
            'last_name': 'Tbo', 
            'email': 'jt@email.com',
            'password':'Pass123!!',
            'phone': '123123123'
        },
        {
            'first_name': 'Curtis',
            'last_name': 'Tbo',
            'email': 'ct@email.com', 
            'password': 'Pass123!!',
            'phone': '123123123'
        }
    ]

    for instructor_data in instructors:
        instructor = User.query.filter_by(email=instructor_data['email']).first()
        if not instructor:
            Instructor.create_new_instructor({
                'first_name': instructor_data['first_name'],
                'last_name': instructor_data['last_name'],
                'email': instructor_data['email'],
                'phone_number': instructor_data['phone'],
                'team_id': team.id
            })

def seed_courses():
    """Create courses if they don't exist."""
    courses = [
        {
            'name': 'Introduction to Riding',
            'description': 'Learn the basics of Motorcycles',
            'max_students': 20,
            'total_days': 5
        },
        {
            'name': 'Basic Fundamentals',
            'description': 'Basic Riding Fundamentals',
            'max_students': 15,
            'total_days': 10
        },
        {
            'name': 'Advanced Riding',
            'description': 'Advanced Riding Techniques',
            'max_students': 12,
            'total_days': 8
        }
    ]

    created_courses = []
    for course_data in courses:
        course = Course.query.filter_by(name=course_data['name']).first()
        if not course:
            course = Course.create(course_data)
            if course:
                created_courses.append(course)
    
    return created_courses

def seed_course_sessions(courses):
    """Create course sessions if they don't exist."""
    if not courses:
        return

    # Get some instructor IDs for the sessions
    instructors = Instructor.query.all()
    if not instructors:
        return

    # Create sample sessions for each course
    for course in courses:
        # Create 3 sessions for each course as an example
        for i in range(3):
            session_data = {
                'course_id': course.id,
                'date': date(2024, 1, i+10),  # Sessions on Jan 10, 11, 12
                'start_time': time(9, 0),  # 9:00 AM
                'primary_instructor_id': instructors[0].id if instructors else None,
                'secondary_instructor_id': instructors[1].id if len(instructors) > 1 else None,
                'location': f'Room {i+101}',
                'notes': f'Session {i+1} of {course.name}'
            }
            
            # Check if session already exists
            existing_session = CourseSession.query.filter_by(
                course_id=session_data['course_id'],
                date=session_data['date']
            ).first()
            
            if not existing_session:
                CourseSession.create(session_data)

def seed_db():
    """Main function to orchestrate database seeding."""
    admin_role = seed_roles()
    admin_user, team = seed_admin_user(admin_role)
    if admin_user:
        seed_instructors(team)
        courses = seed_courses()
        seed_course_sessions(courses)