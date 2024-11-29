from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    """
    EmployeeSchema类，用于序列化和反序列化Employee对象

    字段:
    - id: 员工ID
    - name: 员工姓名
    - position: 员工职位
    - hire_date: 入职日期
    - status: 员工状态
    - company_id: 所属公司ID
    - company_name: 所属公司名称（通过get_company_name方法获取）
    - project_id: 所属项目ID
    - project_name: 所属项目名称（通过get_project_name方法获取）
    - creator_id: 创建者ID
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    position = fields.Str()
    hire_date = fields.Date()
    status = fields.Str()
    company_id = fields.Int()
    company_name = fields.Method("get_company_name")
    project_id = fields.Int()
    project_name = fields.Method("get_project_name")
    creator_id = fields.Int()

    def get_company_name(self, obj):
        """
        获取公司名称
        :param obj: Employee对象
        :return: 公司名称
        """
        return obj.company.name if obj.company else None

    def get_project_name(self, obj):
        """
        获取项目名称
        :param obj: Employee对象
        :return: 项目名称
        """
        return obj.project.name if obj.project else None