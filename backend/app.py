from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function to connect to the database
def get_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection

# Route to create an employee
@app.route('/create_employee_form', methods=['GET'])
def create_employee_form():
    return render_template('create_employee.html')

@app.route('/submit_employee', methods=['POST'])
def submit_employee():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "dob": request.form['dob'],
        "gender": request.form['gender'],
        "occupation": request.form['occupation'],
        "department": request.form['department'],
        "comments": request.form['comments']
    }

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO employee_info (name, email, phone, address, dob, gender, occupation, department, comments)
        VALUES (:name, :email, :phone, :address, :dob, :gender, :occupation, :department, :comments)
    """, data)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('view_employees'))

# Route to view all employees
@app.route('/view_employees', methods=['GET'])
def view_employees():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee_info")
    employees = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_employees.html', employees=employees)

# Route to edit an employee

@app.route('/edit_employee/<int:employee_id>', methods=['GET'])
def edit_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee_info WHERE employee_id = ?", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()
    connection.close()

    if employee:
        # Convert sqlite3.Row to a dictionary
        employee = dict(employee)
        
        # Convert 'dob' to datetime if it's a valid date
        if employee.get('dob'):
            try:
                employee['dob'] = datetime.strptime(employee['dob'], '%Y-%m-%d')
            except ValueError:
                employee['dob'] = None  # Handle invalid date format

    return render_template('edit_employee.html', employee=employee)

@app.route('/update_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "dob": request.form['dob'],
        "gender": request.form['gender'],
        "occupation": request.form['occupation'],
        "department": request.form['department'],
        "comments": request.form['comments'],
        "employee_id": employee_id
    }

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE employee_info
        SET name = :name, email = :email, phone = :phone, address = :address, dob = :dob,
            gender = :gender, occupation = :occupation, department = :department, comments = :comments
        WHERE employee_id = :employee_id
    """, data)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('view_employees'))

# Route to delete an employee
@app.route('/delete_employee/<int:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employee_info WHERE employee_id = ?", (employee_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('view_employees'))

@app.route('/employee/name/<string:employee_name>', methods=['GET'])
def read_employee_by_name(employee_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employee_info WHERE name = ?", (employee_name,))
    employee = cursor.fetchone()
    connection.close()

    if not employee:
        return f"No employee found with name {employee_name}", 404  # Return a 404 if not found

    return render_template('read_employee.html', employee=employee)


if __name__ == "__main__":
    app.run(debug=True)



