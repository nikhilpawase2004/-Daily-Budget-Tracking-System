from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB initialization
def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add transaction
@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.get_json()
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, description, date) VALUES (?, ?, ?, ?)",
              (data['type'], data['amount'], data['description'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# Fetch transactions
@app.route('/transactions')
def get_transactions():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()

    # Calculate totals
    total_income = sum(row[2] for row in rows if row[1] == 'income')
    total_expense = sum(row[2] for row in rows if row[1] == 'expense')
    balance = total_income - total_expense

    return jsonify({
        "transactions": [{"id": row[0], "type": row[1], "amount": row[2], "description": row[3], "date": row[4]} for row in rows],
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    })

if __name__ == '__main__':
    app.run(debug=True)
