from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    matriculation_number = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(100), nullable=False) # Studiengang
    degree_type = db.Column(db.String(50), nullable=False) # Bachelor / Master
    title = db.Column(db.String(255), nullable=True) # Topic of the thesis
    
    start_date = db.Column(db.Date, nullable=True) # Anmeldedatum
    submission_date = db.Column(db.Date, nullable=True) # Abgabedatum
    regular_meeting = db.Column(db.String(100), nullable=True) # Regeltermin
    
    expose_url = db.Column(db.String(500), nullable=True)
    thesis_url = db.Column(db.String(500), nullable=True)
    
    # Erste Idee, Schreibt Expose, Expose wartet auf Review, Anmeldung eingereicht, Angemeldet, Abgegeben, Bewertet
    status = db.Column(db.String(50), nullable=False, default="Erste Idee") 

    notes = db.relationship('Note', backref='student', lazy=True, cascade="all, delete-orphan")
    checklist_items = db.relationship('ChecklistItem', backref='student', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<ChecklistItem {self.task_name} for Student {self.student_id}>'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id} for Student {self.student_id}>'
