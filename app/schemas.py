from app import ma
# from app.models import Employee

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'date')

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id','username', 'password')

admin_schema = AdminSchema()
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


