document.addEventListener('DOMContentLoaded', () => {

    // --- Dashboard: Context Menu for Deletion ---
    const contextMenu = document.getElementById('contextMenu');
    let targetStudentId = null;

    if (contextMenu) {
        // Right click on student cards
        document.querySelectorAll('.student-card:not(.add-card)').forEach(card => {
            card.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                targetStudentId = card.getAttribute('data-id');

                contextMenu.style.left = `${e.pageX}px`;
                contextMenu.style.top = `${e.pageY}px`;
                contextMenu.classList.add('active');
            });
        });

        // Hide context menu on click elsewhere
        document.addEventListener('click', (e) => {
            if (!contextMenu.contains(e.target)) {
                contextMenu.classList.remove('active');
            }
        });

        // Navigate on card click (excluding url-links)
        document.querySelectorAll('.student-card[data-href]').forEach(card => {
            card.addEventListener('click', (e) => {
                // If the click is on an anchor tag or its children, don't navigate
                if (e.target.closest('a')) {
                    return;
                }
                if (!e.target.closest('.url-links')) {
                    window.location.href = card.getAttribute('data-href');
                }
            });
        });

        // Delete Action
        document.getElementById('deleteStudentContextBtn').addEventListener('click', () => {
            if (targetStudentId && confirm('Are you sure you want to delete this student and all associated notes?')) {
                fetch(`/api/students/${targetStudentId}`, {
                    method: 'DELETE'
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            window.location.reload();
                        }
                    });
            }
            contextMenu.classList.remove('active');
        });
    }

    // --- Dashboard: Add Student Modal ---
    const addModal = document.getElementById('addStudentModal');
    if (addModal) {
        document.getElementById('addStudentBtn').addEventListener('click', () => {
            addModal.classList.add('active');
        });

        document.getElementById('closeModalBtn').addEventListener('click', () => {
            addModal.classList.remove('active');
        });

        document.getElementById('cancelModalBtn').addEventListener('click', () => {
            addModal.classList.remove('active');
        });

        document.getElementById('addStudentForm').addEventListener('submit', (e) => {
            e.preventDefault();

            // Prevent double submission
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Saving...';

            const data = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                matriculation_number: document.getElementById('matriculation_number').value,
                program: document.getElementById('program').value,
                degree_type: document.getElementById('degree_type').value,
                title: document.getElementById('title').value,
                start_date: document.getElementById('start_date').value,
                submission_date: document.getElementById('submission_date').value,
                regular_meeting: document.getElementById('regular_meeting').value,
                expose_url: document.getElementById('expose_url').value,
                thesis_url: document.getElementById('thesis_url').value,
                status: document.getElementById('status').value,
                supervisor: document.getElementById('supervisor').value,
                kennziffer: document.getElementById('kennziffer').value,
                cloudfolder_url: document.getElementById('cloudfolder_url').value,
            };

            fetch('/api/students', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
                .then(res => res.json())
                .then(resData => {
                    if (resData.success) {
                        window.location.reload();
                    } else {
                        submitBtn.disabled = false;
                        submitBtn.textContent = 'Save Student';
                    }
                })
                .catch(err => {
                    console.error(err);
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Save Student';
                });
        });
    }

    // --- Detail View: Edit Student Data ---
    const editForm = document.getElementById('editStudentForm');
    if (editForm && typeof STUDENT_ID !== 'undefined') {
        editForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const data = {
                title: document.getElementById('edit_title').value,
                first_name: document.getElementById('edit_first_name').value,
                last_name: document.getElementById('edit_last_name').value,
                matriculation_number: document.getElementById('edit_matriculation').value,
                program: document.getElementById('edit_program').value,
                degree_type: document.getElementById('edit_degree').value,
                start_date: document.getElementById('edit_start').value,
                submission_date: document.getElementById('edit_submission').value,
                regular_meeting: document.getElementById('edit_meeting').value,
                expose_url: document.getElementById('edit_expose_url').value,
                thesis_url: document.getElementById('edit_thesis_url').value,
                status: document.getElementById('edit_status').value,
                supervisor: document.getElementById('edit_supervisor').value,
                kennziffer: document.getElementById('edit_kennziffer').value,
                cloudfolder_url: document.getElementById('edit_cloudfolder_url').value,
            };

            fetch(`/api/students/${STUDENT_ID}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
                .then(res => res.json())
                .then(resData => {
                    if (resData.success) {
                        // Show save indicator
                        const saveStatus = document.getElementById('saveStatus');
                        saveStatus.classList.add('show');
                        setTimeout(() => saveStatus.classList.remove('show'), 2000);

                        // Update header badge
                        const badge = document.getElementById('headerStatus');
                        badge.textContent = data.status;
                        badge.className = `status-badge status-${data.status.replace(/ /g, '-').toLowerCase()}`;
                    }
                });
        });
    }

    // --- Detail View: Notes Management ---
    const addNoteBtn = document.getElementById('addNoteBtn');
    if (addNoteBtn && typeof STUDENT_ID !== 'undefined') {
        addNoteBtn.addEventListener('click', () => {
            const titleInput = document.getElementById('newNoteTitle');
            const contentInput = document.getElementById('newNoteContent');

            if (!contentInput.value.trim()) return;

            fetch(`/api/students/${STUDENT_ID}/notes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: titleInput.value,
                    content: contentInput.value
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Real simple reload to show note, or could prepend DOM element. Let's just reload.
                        window.location.reload();
                    }
                });
        });

        // Delete notes
        document.querySelectorAll('.delete-note-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (confirm('Delete this note?')) {
                    const noteCard = e.target.closest('.note-card');
                    const noteId = noteCard.getAttribute('data-id');

                    fetch(`/api/notes/${noteId}`, { method: 'DELETE' })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                noteCard.remove();
                            }
                        });
                }
            });
        });

        // Edit notes
        document.querySelectorAll('.edit-note-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const noteCard = e.target.closest('.note-card');
                noteCard.querySelector('.note-text-display').style.display = 'none';
                noteCard.querySelector('.note-edit-form').style.display = 'block';
            });
        });

        document.querySelectorAll('.cancel-edit-note').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const noteCard = e.target.closest('.note-card');
                noteCard.querySelector('.note-text-display').style.display = 'block';
                noteCard.querySelector('.note-edit-form').style.display = 'none';
            });
        });

        document.querySelectorAll('.save-edit-note').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const noteCard = e.target.closest('.note-card');
                const noteId = noteCard.getAttribute('data-id');
                const newTitle = noteCard.querySelector('.edit-note-title').value;
                const newContent = noteCard.querySelector('.edit-note-content').value;

                fetch(`/api/notes/${noteId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: newTitle, content: newContent })
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            window.location.reload();
                        }
                    });
            });
        });

        // Search Notes
        const searchInput = document.getElementById('searchNotes');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                document.querySelectorAll('.note-card').forEach(card => {
                    const text = card.textContent.toLowerCase();
                    if (text.includes(term)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        }
    }

    // --- Detail View: Wimi Checklist ---
    document.querySelectorAll('.checklist-checkbox').forEach(checkbox => {
        checkbox.addEventListener('click', (e) => {
            const isCompleted = e.target.checked;

            if (!isCompleted) {
                if (!confirm("Are you sure you want to uncheck this item?")) {
                    e.preventDefault();
                    return;
                }
            }
        });

        checkbox.addEventListener('change', (e) => {
            const itemId = e.target.getAttribute('data-id');
            const isCompleted = e.target.checked;

            fetch(`/api/checklist/${itemId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_completed: isCompleted })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        const label = e.target.closest('.checklist-item');
                        const dateSpan = document.getElementById(`date-${itemId}`);

                        if (data.is_completed) {
                            label.classList.add('completed');
                            dateSpan.textContent = data.completed_at;
                        } else {
                            label.classList.remove('completed');
                            dateSpan.textContent = '';
                        }
                    }
                });
        });
    });
});
