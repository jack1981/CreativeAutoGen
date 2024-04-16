# Flask Application
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create SQLite database and table
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, liked TEXT)''')
conn.commit()
conn.close()

# Main page
@app.route('/')
def main():
    return render_template('main.html')

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        liked = request.form['liked']
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute('INSERT INTO feedback (liked) VALUES (?)', (liked,))
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))
    return render_template('feedback.html')

# Thank you page
@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

# Admin page
@app.route('/admin')
def admin():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)