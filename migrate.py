import sqlite3

def migrate():
    conn = sqlite3.connect('theses.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE student ADD COLUMN expose_url VARCHAR(500)')
    except sqlite3.OperationalError:
        pass # Column might already exist
    
    try:
        c.execute('ALTER TABLE student ADD COLUMN thesis_url VARCHAR(500)')
    except sqlite3.OperationalError:
        pass

    try:
        c.execute('ALTER TABLE student ADD COLUMN cloudfolder_url VARCHAR(500)')
    except sqlite3.OperationalError:
        pass

    try:
        c.execute('ALTER TABLE student ADD COLUMN supervisor VARCHAR(150)')
    except sqlite3.OperationalError:
        pass

    try:
        c.execute('ALTER TABLE student ADD COLUMN kennziffer VARCHAR(50)')
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()
    print("Migration successful.")

if __name__ == '__main__':
    migrate()
