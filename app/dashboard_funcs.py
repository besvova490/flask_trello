from app import db
from .models import User, Dashboard
from flask import jsonify


class DashboardFunc:

    @staticmethod
    def get_dashboards_list():
        dashboards_list = []
        for dashboard in Dashboard.query.all():
            dashboards_list.append({
                'dashboard_id': dashboard.id,
                'dashboard_name': dashboard.name,
                'dashboard_description': dashboard.description,
                'dashboard_admin': str(
                    User.query.get(dashboard.admin_id).username),
                'dashboard_tasks': tuple({'name': task.name, 'id': task.id} for task in dashboard.tasks),
                'dashboard_workers': tuple({'id': user.id, 'name': user.username} for user in dashboard.users),
            })
        return jsonify(dashboards=dashboards_list), 200

    @staticmethod
    def get_dashboard_tasks(dashboard_id):
        try:
            d1 = Dashboard.query.get(dashboard_id)
            dashboard = {
                'dashboard_id': dashboard_id,
                'dashboard_name': d1.name,
                'dashboard_workers': tuple({'id': user.id, 'name': user.username} for user in d1.users),
                'tasks': tuple({'name': task.name, 'id': task.id} for task in d1.tasks)
            }
            return jsonify(dashboard=dashboard), 200
        except AttributeError:
            return {'massage': 'No such dashboard'}, 404

    @staticmethod
    def create_dashboard(user_id, data):
        if user_id != 1:
            return {'error_massage': ''}, 404
        d = Dashboard(data['name'], data['description'], user_id)
        db.session.add(d)
        db.session.commit()
        return jsonify(dashboard_created=str(d)), 201

    @staticmethod
    def delete_dashboard(user_id, dashboard_id):
        if user_id != 1:
            return {'error_massage': ''}, 404
        d = Dashboard.query.get(dashboard_id)
        db.session.delete(d)
        db.session.commit()
        return jsonify(dashboard_deleted={'id': dashboard_id, 'name': d.name}), 201

    @staticmethod
    def update_dashboard(user_id, dashboard_id, data):
        if user_id != 1:
            return {'error_massage': ''}, 404
        d = Dashboard.query.get(dashboard_id)
        d.name = data['name']
        d.description = data['description']
        db.session.add(d)
        db.session.commit()
        return jsonify(dashboard_updated=d), 201