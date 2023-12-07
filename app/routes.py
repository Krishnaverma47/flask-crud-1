from flask import jsonify, request
from app import app, db, jwt
from app.models import Employee, Admin
from app.schemas import employee_schema, employees_schema, admin_schema
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# admin sign up
@app.route('/signup_admin', methods=['POST'])
def signup_admin():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'username and email are password'}), 400
    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        return jsonify({'message': 'Admin already exist.'}), 400
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_admin = Admin(username, hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201


#admin login 
@app.route('/login_admin', methods=['POST'])
def login_admin():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    admin = Admin.query.filter_by(username=username).first()

    if not admin or not check_password_hash(admin.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=admin.id)
    return jsonify(access_token=access_token), 200

# createing the employee 
@app.route('/add_employee', methods=['POST'])
@jwt_required()
def add_employee():
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user).first()
    if not admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    name = request.json.get('name')
    email = request.json.get('email')
    if not name or not email:
        return jsonify({'message': 'Name and email are required'}), 400
    existing_employee = Employee.query.filter_by(email=email).first()
    if existing_employee:
        return jsonify({'message': 'Employee already exists'}), 400
    employee = Employee(name, email,admin.id)
    db.session.add(employee)
    db.session.commit()
    return employee_schema.jsonify(employee)


# getting all employee details 
@app.route('/all_employees', methods=['GET'])
def get_all_employee_details():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)


# getting employee details by id
@app.route('/employee/<id>/', methods=['GET'])
@jwt_required()
def get_employee_details_by_id(id):
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user).first()
    if not admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not exist with this id.'}), 400
    return employee_schema.jsonify(employee)


# update the employee details 
@app.route('/employee/<id>/', methods=['PUT'])
@jwt_required()
def update_employee_by_id(id):
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user).first()
    if not admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'message': 'Employee not exist with this id.'}), 400
    name = request.json['name']
    email = request.json['email']
    if Employee.query.filter_by(email=email).first():
        return jsonify({'message': 'Employee already exist with this email'}), 400
    if admin.id != employee.admin_id:
        return jsonify({'message': 'You have not created this employee.'}), 400
    employee.name = name
    employee.email = email
    db.session.commit()
    return employee_schema.jsonify(employee)


# delete the employee details
@app.route('/employee/<id>/', methods=['DELETE'])
@jwt_required()
def delete_employee_by_id(id):
    current_user = get_jwt_identity()
    admin = Admin.query.filter_by(id=current_user).first()
    if not admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    employee = Employee.query.get(id)
    if employee:
        if admin.id != employee.admin_id:
            return jsonify({'message': 'You have not created this employee.'}), 400
        db.session.delete(employee)
        db.session.commit()
        return employee_schema.jsonify(employee)
    return jsonify({'message': 'Employee not exist with this id.'}), 400


