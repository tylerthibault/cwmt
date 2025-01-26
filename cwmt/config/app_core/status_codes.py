import inspect

class StatusCode():
    def __init__(self, data:dict):
        self.code = data['code']
        self.pub_msg = data['pub_msg']

        for key, value in data.items():
            setattr(self, key, value)


class StatusCodes():
    e_creating_course = StatusCode({
    'code': 'E0001',
    'pub_msg': 'Error creating course',
    'flash_color': 'error',
    })
    e_getting_courses = StatusCode({
    'code': 'E0002',
    'pub_msg': 'Error getting courses',
    'flash_color': 'error',
    })
    e_updating_course = StatusCode({
    'code': 'E0003',
    'pub_msg': 'Error updating course',
    'flash_color': 'error',
    })
    e_deleting_course = StatusCode({
    'code': 'E0004',
    'pub_msg': 'Error deleting course',
    'flash_color': 'error',
    })
    e_creating_course_session = StatusCode({
    'code': 'E0005',
    'pub_msg': 'Error creating course session',
    'flash_color': 'error',
    })
    e_getting_course_sessions = StatusCode({
    'code': 'E0006',
    'pub_msg': 'Error getting course sessions',
    'flash_color': 'error',
    })
    e_updating_course_session = StatusCode({
    'code': 'E0007',
    'pub_msg': 'Error updating course session',
    'flash_color': 'error',
    })
    e_deleting_course_session = StatusCode({
    'code': 'E0008',
    'pub_msg': 'Error deleting course session',
    'flash_color': 'error',
    })
    e_creating_instructor = StatusCode({
    'code': 'E0009',
    'pub_msg': 'Error creating instructor',
    'flash_color': 'error',
    })
    e_creating_user_role = StatusCode({
    'code': 'E0010',
    'pub_msg': 'Error creating user role',
    'flash_color': 'error',
    })
    e_creating_role = StatusCode({
    'code': 'E0011',
    'pub_msg': 'Error creating role',
    'flash_color': 'error',
    })
    e_creating_team = StatusCode({
    'code': 'E0012',
    'pub_msg': 'Error creating team',
    'flash_color': 'error',
    })
    e_getting_teams = StatusCode({
    'code': 'E0013',
    'pub_msg': 'Error getting teams',
    'flash_color': 'error',
    })
    e_creating_user = StatusCode({
    'code': 'E0014',
    'pub_msg': 'Error creating user',
    'flash_color': 'error',
    })
    e_hashing_password = StatusCode({
    'code': 'E0015',
    'pub_msg': 'Error hashing password',
    'flash_color': 'error',
    })
    e_validating_login = StatusCode({
    'code': 'E0016',
    'pub_msg': 'Error validating login',
    'flash_color': 'error',
    })
    e_controller = StatusCode({
    'code': 'E0017',
    'pub_msg': 'Controller error',
    'flash_color': 'error',
    })
    e_getting_instructors = StatusCode({
    'code': 'E0018',
    'pub_msg': 'Error getting instructors',
    'flash_color': 'error',
    })


    # Statuses
    s_deleting_course_session = StatusCode({
    'code': 'S0001',
    'pub_msg': 'Course session deleted successfully',
    'flash_color': 'error',
    })
    s_creating_course = StatusCode({
    'code': 'S0002',
    'pub_msg': 'Course created successfully',
    'flash_color': 'success',
    })
    s_getting_courses = StatusCode({
    'code': 'S0003',
    'pub_msg': 'Courses retrieved successfully',
    'flash_color': 'success',
    })
    s_updating_course = StatusCode({
    'code': 'S0004',
    'pub_msg': 'Course updated successfully',
    'flash_color': 'success',
    })
    s_deleting_course = StatusCode({
    'code': 'S0005',
    'pub_msg': 'Course deleted successfully',
    'flash_color': 'error',
    })
    s_creating_instructor = StatusCode({
    'code': 'S0006',
    'pub_msg': 'Instructor created successfully',
    'flash_color': 'success',
    })
    s_getting_instructors = StatusCode({
    'code': 'S0007',
    'pub_msg': 'Instructors retrieved successfully',
    'flash_color': 'success',
    })
    s_updating_instructor = StatusCode({
    'code': 'S0008',
    'pub_msg': 'Instructor updated successfully',
    'flash_color': 'success',
    })
    s_deleting_instructor = StatusCode({
    'code': 'S0009',
    'pub_msg': 'Instructor deleted successfully',
    'flash_color': 'error',
    })
    s_creating_user = StatusCode({
    'code': 'S0010',
    'pub_msg': 'User created successfully',
    'flash_color': 'success',
    })
    s_getting_users = StatusCode({
    'code': 'S0011',
    'pub_msg': 'Users retrieved successfully',
    'flash_color': 'success',
    })
    s_updating_user = StatusCode({
    'code': 'S0012',
    'pub_msg': 'User updated successfully',
    'flash_color': 'success',
    })
    s_deleting_user = StatusCode({
    'code': 'S0013',
    'pub_msg': 'User deleted successfully',
    'flash_color': 'error',
    })
    s_creating_course_session = StatusCode({
    'code': 'S0014',
    'pub_msg': 'Course session created successfully',
    'flash_color': 'success',
    })
    s_getting_course_sessions = StatusCode({
    'code': 'S0015', 
    'pub_msg': 'Course sessions retrieved successfully',
    'flash_color': 'success',
    })
    s_updating_course_session = StatusCode({
    'code': 'S0016',
    'pub_msg': 'Course session updated successfully', 
    'flash_color': 'success',
    })