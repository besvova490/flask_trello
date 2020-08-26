from app import app, db
from .models import User, Dashboard, Task
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
jwt = JWTManager(app)


class UserFunc:

    @staticmethod
    def signup(data):
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User already exists'}, 409
        new_user = User(data['username'], data['email'],
                        data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id, 'name': new_user.username,
                'password': new_user.password}, 201

    @staticmethod
    def sign_in(data):
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {
                'message': f"User with the following email:"
                           f" {data['email']} does not exist"
            }, 404
        if user.check_password_hash(data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
        return {}, 403

    @staticmethod
    def log_out():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

    @staticmethod
    def get_users_list():
        users_list = []
        for user in User.query.all():
            users_list.append({
                'user_id': user.id,
                'user_name': user.username,
                'user_email': user.email,
                'user_tasks_admin': tuple({'name': task.name, 'id': task.id} for task in user.tasks_admin),
                'user_tasks': tuple({'name': task.name, 'id': task.id} for task in user.tasks),
                'user_dashboard_admin': tuple({'name': dashboard.name, 'id': dashboard.id} for dashboard in user.dashboards_admin),
                'user_dashboards': tuple({'name': dashboard.name, 'id': dashboard.id} for dashboard in user.dashboards)

            })
        return jsonify(users_list), 200

    @staticmethod
    def add_to_dashboard(user_id, dashboard_id):
        user = User.query.get(user_id)
        dashboard = Dashboard.query.get(dashboard_id)
        if user in dashboard.users:
            return {'error_massage': 'User already in this dashboard'}, 409
        dashboard.users.append(user)
        db.session.commit()
        return jsonify({'message': 'successful'}), 200

    @staticmethod
    def remove_from_dashboard(user_id, dashboard_id):
        user = User.query.get(user_id)
        dashboard = Dashboard.query.get(dashboard_id)
        if user not in dashboard.users:
            return {'error_massage': 'No such user in this dashboard'}, 409
        dashboard.users.remove(user)
        db.session.commit()
        return jsonify({'message': 'successful'}), 200

    @staticmethod
    def add_to_task(user_id, task_id):
        user = User.query.get(user_id)
        task = Task.query.get(task_id)
        if user in task.users:
            return {'error_massage': 'User already in this task'}, 409
        if task.dashboard not in user.dashboards:
            return {'error_massage': 'You can not add user to this task'}, 409
        task.users.append(user)
        db.session.commit()
        return jsonify({'message': 'successful'}), 200

    @staticmethod
    def remove_from_task(user_id, task_id):
        user = User.query.get(user_id)
        task = Task.query.get(task_id)
        if user not in task.users:
            return {'error_massage': 'No such user in this task'}, 409
        task.users.remove(user)
        db.session.commit()
        return jsonify({'message': 'successful'}), 200
