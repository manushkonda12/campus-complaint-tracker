from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

init_db()

# Home page - Submit Complaint
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        category = request.form['category']
        description = request.form['description']

        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("INSERT INTO complaints (name, roll, category, description) VALUES (?, ?, ?, ?)",
                  (name, roll, category, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('index.html')

# View complaints (Admin)
@app.route('/complaints')
def complaints():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    complaints = c.fetchall()
    conn.close()
    return render_template('complaints.html', complaints=complaints)

# Update complaint status
@app.route('/update/<int:complaint_id>', methods=['GET', 'POST'])
def update_status(complaint_id):
    if request.method == 'POST':
        new_status = request.form['status']
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, complaint_id))
        conn.commit()
        conn.close()
        return redirect(url_for('complaints'))
    return render_template('status_update.html', complaint_id=complaint_id)

if __name__ == '__main__':
    app.run(debug=True)
