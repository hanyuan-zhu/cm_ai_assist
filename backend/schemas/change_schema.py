from marshmallow import Schema, fields
from backend.models.employee import Employee
from backend.models.company import Company
from backend.models.project import Project

class ChangeSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str()
    employee_id = fields.Int()
    # 保留原有的ID字段
    from_company_id = fields.Int()
    to_company_id = fields.Int()
    from_project_id = fields.Int()
    to_project_id = fields.Int()
    # 添加名称字段
    from_company_name = fields.Method("get_from_company_name")
    to_company_name = fields.Method("get_to_company_name")
    from_project_name = fields.Method("get_from_project_name") 
    to_project_name = fields.Method("get_to_project_name")
    effective_date = fields.Date()
    status = fields.Str()
    # 添加员工名称
    employee_name = fields.Method("get_employee_name")

    def get_from_company_name(self, obj):
        company = Company.query.get(obj.from_company_id)
        return company.name if company else None

    def get_to_company_name(self, obj):
        company = Company.query.get(obj.to_company_id)
        return company.name if company else None

    def get_from_project_name(self, obj):
        project = Project.query.get(obj.from_project_id)
        return project.name if project else None

    def get_to_project_name(self, obj):
        project = Project.query.get(obj.to_project_id)
        return project.name if project else None

    def get_employee_name(self, obj):
        """获取员工姓名"""
        employee = Employee.query.get(obj.employee_id)
        return employee.name if employee else None