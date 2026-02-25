import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Student, Note, ChecklistItem

WIMI_TASKS = [
    "Expose Template zugeschickt",
    "Expose reviewed",
    "Angaben in Tabelle in TUBCloud eingetragen, Ordner angelegt",
    "Anmeldung beim Prüfungsamt angeregt",
    "Antrag auf Themenausgabe geprüft und Thema eingetragen",
    "Regeltermin ausgemacht",
    "Arbeit reviewed",
    "Unterlagen in TUBCloud vervollständigt, Tabelle Gutachtendatum ergänzt",
    "Verteidigungstermin ausgemacht",
    "Gutachten erstellt und Enrico um Gutachten gebeten",
    "Gutachten an Prüfungsamt geschickt",
    "Nachgespräch"
]

app = Flask(__name__)
# Database Configuration
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'theses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    all_students = Student.query.all()
    today = datetime.now().date()

    # Collect unique supervisors (non-empty)
    all_supervisors = sorted(set(
        s.supervisor for s in all_students if s.supervisor and s.supervisor.strip()
    ))

    selected_supervisor = request.args.get('supervisor', 'Alle')

    def matches(s):
        if selected_supervisor == 'Alle':
            return True
        return (s.supervisor or '').strip() == selected_supervisor

    active_students = [s for s in all_students if s.status != 'Bewertet' and matches(s)]
    graded_students = [s for s in all_students if s.status == 'Bewertet' and matches(s)]

    active_students.sort(key=lambda s: s.submission_date or datetime.max.date())
    graded_students.sort(key=lambda s: s.submission_date or datetime.min.date(), reverse=True)

    return render_template(
        'index.html',
        students=active_students,
        graded_students=graded_students,
        today=today,
        all_supervisors=all_supervisors,
        selected_supervisor=selected_supervisor
    )

@app.route('/table')
def table_view():
    students = Student.query.all()
    # Sort by ID or whichever makes sense
    students.sort(key=lambda s: s.id)
    return render_template('table.html', students=students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    
    # Parse dates if provided
    start_date = None
    submission_date = None
    if data.get('start_date'):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if data.get('submission_date'):
        submission_date = datetime.strptime(data['submission_date'], '%Y-%m-%d').date()
        
    student = Student(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        matriculation_number=data.get('matriculation_number'),
        program=data.get('program'),
        degree_type=data.get('degree_type'),
        title=data.get('title', ''),
        start_date=start_date,
        submission_date=submission_date,
        regular_meeting=data.get('regular_meeting', ''),
        expose_url=data.get('expose_url', ''),
        thesis_url=data.get('thesis_url', ''),
        status=data.get('status', 'Erste Idee'),
        supervisor=data.get('supervisor', ''),
        kennziffer=data.get('kennziffer', ''),
        cloudfolder_url=data.get('cloudfolder_url', '')
    )
    
    db.session.add(student)
    db.session.commit()
    return jsonify({"success": True, "id": student.id}), 201

@app.route('/student/<int:id>')
def student_detail(id):
    student = Student.query.get_or_404(id)
    notes = Note.query.filter_by(student_id=id).order_by(Note.date.desc()).all()
    
    # Ensure all checklist items are created
    existing_items = {item.task_name: item for item in student.checklist_items}
    checklist = []
    added_new = False
    for task_name in WIMI_TASKS:
        if task_name not in existing_items:
            new_item = ChecklistItem(student_id=student.id, task_name=task_name)
            db.session.add(new_item)
            checklist.append(new_item)
            added_new = True
        else:
            checklist.append(existing_items[task_name])
            
    if added_new:
        db.session.commit()
    
    return render_template('detail.html', student=student, notes=notes, checklist=checklist)

@app.route('/api/students/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_student(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        return jsonify({"success": True})
        
    if request.method == 'PUT':
        data = request.json
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.matriculation_number = data.get('matriculation_number', student.matriculation_number)
        student.program = data.get('program', student.program)
        student.degree_type = data.get('degree_type', student.degree_type)
        student.title = data.get('title', student.title)
        student.regular_meeting = data.get('regular_meeting', student.regular_meeting)
        student.expose_url = data.get('expose_url', student.expose_url)
        student.thesis_url = data.get('thesis_url', student.thesis_url)
        student.status = data.get('status', student.status)
        student.supervisor = data.get('supervisor', student.supervisor)
        student.kennziffer = data.get('kennziffer', student.kennziffer)
        student.cloudfolder_url = data.get('cloudfolder_url', student.cloudfolder_url)
        
        if data.get('start_date'):
            student.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        elif 'start_date' in data and not data['start_date']:
            student.start_date = None
            
        if data.get('submission_date'):
            student.submission_date = datetime.strptime(data['submission_date'], '%Y-%m-%d').date()
        elif 'submission_date' in data and not data['submission_date']:
            student.submission_date = None
            
        db.session.commit()
        return jsonify({"success": True})

@app.route('/api/students/<int:student_id>/notes', methods=['POST'])
def add_note(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json
    note = Note(
        student_id=student.id,
        title=data.get('title', 'Meeting Note'),
        content=data.get('content', '')
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({
        "success": True, 
        "id": note.id,
        "date": note.date.strftime('%Y-%m-%d %H:%M')
    }), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT', 'DELETE'])
def update_delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True})
        
    if request.method == 'PUT':
        data = request.json
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify({"success": True})

@app.route('/api/checklist/<int:item_id>', methods=['PUT'])
def update_checklist_item(item_id):
    item = ChecklistItem.query.get_or_404(item_id)
    data = request.json
    
    is_completed = data.get('is_completed', False)
    item.is_completed = is_completed
    
    if is_completed:
        item.completed_at = datetime.now()
    else:
        item.completed_at = None
        
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "is_completed": item.is_completed, 
        "completed_at": item.completed_at.strftime('%d.%m.%Y %H:%M') if item.completed_at else None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
