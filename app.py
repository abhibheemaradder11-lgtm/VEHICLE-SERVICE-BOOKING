from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'elite_autocare_full_secure_key_2026'

FILES_DIR = os.path.join(os.getcwd(), 'files')
if not os.path.exists(FILES_DIR): os.makedirs(FILES_DIR)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gouri@1685", # <--- UPDATE THIS
        database="vehicle_service"
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'password123':
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        error = 'Invalid Credentials.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        query = "INSERT INTO vehicle_appointments (customer_name, contact_no, vehicle_type, service_type, time_slot) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (request.form['name'], request.form['contact'], request.form['v_type'], request.form['service'], request.form['slot']))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('dashboard'))
    return render_template('booking.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle_appointments ORDER BY id DESC")
    records = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('dashboard.html', records=records)

@app.route('/update_bill/<int:id>', methods=['POST'])
def update_bill(id):
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE vehicle_appointments SET total_bill=%s, payment_mode=%s, status='Completed' WHERE id=%s", (request.form['total_amount'], request.form['pay_mode'], id))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
def delete_entry(id):
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM vehicle_appointments WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/receipt/<int:id>')
def receipt(id):
    if not session.get('admin_logged_in'): return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle_appointments WHERE id = %s", (id,))
    r = cursor.fetchone()
    if r:
        path = os.path.join(FILES_DIR, f"receipt_{id}.txt")
        with open(path, "w") as f:
            f.write("------------------------------------------\n")
            f.write("            ELITE AUTOCARE                \n")
            f.write("        PREMIUM VEHICLE SERVICE           \n")
            f.write("------------------------------------------\n")
            f.write(f"BILL NO: {r['id']:<20} DATE: 2026-04-24\n")
            f.write(f"CUSTOMER: {r['customer_name']}\n")
            f.write(f"CONTACT: {r['contact_no']}\n")
            f.write("------------------------------------------\n")
            f.write(f"{'DESCRIPTION':<25} {'DETAILS':<15}\n")
            f.write(f"{'-'*40}\n")
            f.write(f"{'Vehicle Type':<25} {r['vehicle_type']:<15}\n")
            f.write(f"{'Service Performed':<25} {r['service_type']:<15}\n")
            f.write(f"{'Appointed Slot':<25} {r['time_slot']:<15}\n")
            f.write(f"{'Payment Method':<25} {r['payment_mode']:<15}\n")
            f.write(f"{'-'*40}\n")
            f.write(f"{'TOTAL AMOUNT PAID':<25} INR {r['total_bill']}\n")
            f.write("------------------------------------------\n")
            f.write("         THANK YOU - VISIT AGAIN!         \n")
            f.write("------------------------------------------\n")
        return send_file(path, as_attachment=True)
    return "Not Found", 404

if __name__ == '__main__':
    app.run(debug=True)