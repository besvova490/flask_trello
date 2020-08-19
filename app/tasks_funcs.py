from app import db
from .models import Task, User, Dashboard


class TaskFunc:

    @staticmethod
    def get_all():
        tasks_list = []
        for task in Task.query.all():
            tasks_list.append({
                'task_id': task.id,
                'task_name': task.name,
                'task_description': task.description,
                'task_admin': str(
                    User.query.get(task.admin_id).username),
                'task_workers': str(task.users),
                'task_dashboard': Dashboard.query.get(
                    task.dashboard_id).name
            })
        return tasks_list

    @staticmethod
    def create_task(dashboard_id, user_id, data):
        if user_id != 1:
            return {'error_massage': ''}, 404
        t = Task(data['name'], data['description'], 1, dashboard_id)
        db.session.add(t)
        db.session.commit()
        return t

    @staticmethod
    def delete_task(user_id, task_id):
        if user_id != 1:
            return {'error_massage': ''}, 404
        t = Task.query.get(task_id)
        db.session.delete(t)
        db.session.commit()
        return {'deleted_task': f'{task_id}'}, 200

    @staticmethod
    def update_task(user_id, task_id, data):
        t = Task.query.get(task_id)
        if user_id != t.admin.id:
            return {'error_massage': ''}, 404
        t.name = data['name']
        t.description = data['description']
        t.admin_id = data.get('admin_id', user_id)
        db.session.add(t)
        db.session.commit()
        return {'updated_task': f'{str(t)}'}, 200
