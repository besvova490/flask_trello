from app import app
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from .dashboard_funcs import DashboardFunc
from .tasks_funcs import TaskFunc
from .user_func import UserFunc


@app.route('/', methods=['GET'])
def index():
    resp = make_response({'message': 'Hello world)))',
                    'title': 'Trello by besvova490'})
    resp.set_cookie('hello', 'test')
    return resp, 200


@app.route('/users', methods=['GET'])
def get_users_list():
    return UserFunc.get_users_list()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    return UserFunc.signup(data)


@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.json['data']
    return UserFunc.sign_in(data)


@app.route('/logout', methods=['GET'])
def log_out():
    return UserFunc.log_out()


@app.route('/tasks', methods=['GET'])
@jwt_required
def get_tasks_list():
    return jsonify({'tasks_list': TaskFunc.get_all()}), 200


@app.route('/dashboards', methods=['GET'])
@jwt_required
def get_dashboards_list():
    return DashboardFunc.get_dashboards_list()


@app.route('/dashboards/<int:dashboard_id>', methods=['GET'])
@jwt_required
def get_dashboard_tasks(dashboard_id):
    return DashboardFunc.get_dashboard_tasks(dashboard_id)


@app.route('/dashboards/<int:dashboard_id>/create-task', methods=['POST'])
@jwt_required
def create_task(dashboard_id):
    user_id = get_jwt_identity()
    data = request.json
    return {'new_task': f'{TaskFunc.create_task(dashboard_id, user_id, data)}'}, 200


@app.route('/dashboards/<int:dashboard_id>/<int:task_id>', methods=['DELETE'])
@jwt_required
def delete_task(task_id, **kwargs):
    user_id = get_jwt_identity()
    return TaskFunc.delete_task(user_id, task_id)


@app.route('/dashboards/<int:dashboard_id>/<int:task_id>', methods=['PATCH'])
@jwt_required
def update_task(task_id, **kwargs):
    user_id = get_jwt_identity()
    data = request.json
    return TaskFunc.update_task(user_id, task_id, data)


@app.route('/tasks/<int:task_id>/<user_id>', methods=['POST'])
@jwt_required
def add_user_to_task(task_id, user_id):
    return UserFunc.add_to_task(user_id, task_id)


@app.route('/tasks/<int:task_id>/<user_id>', methods=['DELETE'])
@jwt_required
def delete_user_from_task(task_id, user_id):
    return UserFunc.remove_from_task(user_id, task_id)


@app.route('/dashboards', methods=['POST'])
@jwt_required
def create_dashboard():
    user_id = get_jwt_identity()
    data = request.json
    return DashboardFunc.create_dashboard(user_id, data)


@app.route('/dashboards/<int:dashboard_id>/<int:user_id>', methods=['POST'])
@jwt_required
def add_user_to_dashboard(user_id, dashboard_id):
    return UserFunc.add_to_dashboard(user_id, dashboard_id)


@app.route('/dashboards/<int:dashboard_id>/<int:user_id>', methods=['DELETE'])
@jwt_required
def delete_user_from_dashboard(user_id, dashboard_id):
    return UserFunc.remove_from_dashboard(user_id, dashboard_id)


@app.route('/dashboards/<int:dashboard_id>', methods=['DELETE'])
@jwt_required
def delete_dashboard(dashboard_id):
    user_id = get_jwt_identity()
    return DashboardFunc.delete_dashboard(user_id, dashboard_id)


@app.route('/dashboards/<int:dashboard_id>', methods=['PATCH'])
@jwt_required
def update_dashboard(dashboard_id):
    user_id = get_jwt_identity()
    data = request.json
    return DashboardFunc.update_dashboard(user_id, dashboard_id, data)
