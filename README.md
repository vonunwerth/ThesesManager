# ThesesManager

A sleek, premium Python Flask application designed to help university supervisors efficiently manage their students' theses processes.

## Features

- **Student Dashboard**: Visually rich cards displaying key student information, current progress status, and a countdown to their submission deadline.
- **Workflow & Status Tracking**: Update statuses dynamically from "Erste Idee" (First Idea) all the way to "Bewertet" (Graded) with distinct visual badges.
- **Meeting Diary**: A per-student chronological meeting log with inline editing (pencil icon) and real-time word search.
- **Wimi Checklist**: A dedicated predefined milestones checklist. Includes completion timestamps and safety confirmations to prevent accidental unchecking.
- **Direct Link Integrations**: Save and instantly access your students' Exposé or Thesis URLs (e.g., Overleaf links) directly from the dashboard card.
- **Premium Glassmorphism UI**: Beautifully designed responsive frontend utilizing CSS variables, blur filters, and smooth micro-animations.

## Tech Stack

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy
- **Database**: SQLite (local `theses.db`)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism design system), Vanilla JavaScript (Fetch API for dynamic updates)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:vonunwerth/ThesesManager.git
   cd ThesesManager
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

4. **Initialize and run the application:**
   The database (`theses.db`) will be created automatically on the first run.
   ```bash
   python app.py
   ```

5. **Access the Application:**
   Open your web browser and navigate to `http://127.0.0.1:5000`

## Usage Guide

- **Adding a Student**: Click the large "+" bounding box on the dashboard to register a new student with their details (matriculation number, dates, program, links).
- **Editing Details**: Click on any student card to enter the Detail View. From there, you can edit properties on the left-hand panel.
- **Managing Notes**: On the right side of the Detail View, use the "Meeting Diary" to add or search past consultation notes.
- **Deleting a Student**: Right-click any student card on the main dashboard to open a context menu for deletion.

## License
MIT License.
