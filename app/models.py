from app import db
from passlib.hash import sha256_crypt
import json


tasks = db.Table(
    "tasks_mtm",
    db.Column("tasks_id", db.Integer, db.ForeignKey("tasks.id"), primary_key=True),
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)
dashboards = db.Table(
    "dashboards_mtm",
    db.Column(
        "dashboards_id", db.Integer, db.ForeignKey("dashboards.id"), primary_key=True
    ),
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    tasks = db.relationship(
        "Task", secondary=tasks,
        lazy="subquery", backref=db.backref("users", lazy=True)
    )
    dashboards = db.relationship(
        "Dashboard", secondary=dashboards,
        lazy="subquery", backref=db.backref("users", lazy=True),
    )
    tasks_admin = db.relationship("Task", backref="admin", lazy=True)
    dashboards_admin = db.relationship("Dashboard", backref="admin", lazy=True)

    def __init__(self, username, email, password, dashboard):
        self.username = username
        self.email = email
        self.password = sha256_crypt.hash(password)
        self.dashboards.append(dashboard)

    def check_password_hash(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f"{self.id} {self.username} {self.email}"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(500))
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id"))

    def __init__(self, name, description, admin_id, dashboard_id):
        self.name = name
        self.description = description
        self.admin_id = admin_id
        self.dashboard_id = dashboard_id

    def __repr__(self):
        return f"{self.id} {self.name}"


class Dashboard(db.Model):
    __tablename__ = "dashboards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(500))
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tasks = db.relationship("Task", backref="dashboard", lazy=True)

    def __init__(self, name, description, admin_id):
        self.name = name
        self.description = description
        self.admin_id = admin_id

    def __repr__(self):
        return f"{self.id} {self.name}"
