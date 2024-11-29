from marshmallow import Schema, fields
from backend.models.employee import Employee
from backend.models.company import Company
from backend.models.project import Project

class ChangeSchema(Schema):
    """
    ChangeSchema类，用于序列化和反序列化ChangeRequest对象
    
    字段说明:
    - id: 变动请求ID
    - type: 变动类型（入职/调岗/离职）
    - employee_id: 员工ID
    - employee_name: 员工姓名（通过关系获取）
    - from_company_id: 原公司ID
    - from_company_name: 原公司名称（通过关系获取）
    - to_company_id: 目标公司ID
    - to_company_name: 目标公司名称（通过关系获取）
    - from_project_id: 原项目ID
    - from_project_name: 原项目名称（通过关系获取）
    - to_project_id: 目标项目ID
    - to_project_name: 目标项目名称（通过关系获取）
    - effective_date: 生效日期
    - status: 状态（待确认/已确认/已拒绝）
    - creator_id: 创建者ID
    """
    
    # 基本字段
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)
    employee_id = fields.Int(required=True)
    from_company_id = fields.Int(allow_none=True)
    to_company_id = fields.Int(allow_none=True)
    from_project_id = fields.Int(allow_none=True)
    to_project_id = fields.Int(allow_none=True)
    effective_date = fields.Date(required=True)
    status = fields.Str(required=True)
    creator_id = fields.Int(required=True)
    
    # 通过关系获取的名称字段
    employee_name = fields.Method("get_employee_name")
    from_company_name = fields.Method("get_from_company_name")
    to_company_name = fields.Method("get_to_company_name")
    from_project_name = fields.Method("get_from_project_name")
    to_project_name = fields.Method("get_to_project_name")

    def get_employee_name(self, obj):
        """获取员工姓名"""
        return obj.employee.name if obj.employee else None

    def get_from_company_name(self, obj):
        """获取原公司名称"""
        return obj.from_company.name if obj.from_company else None

    def get_to_company_name(self, obj):
        """获取目标公司名称"""
        return obj.to_company.name if obj.to_company else None

    def get_from_project_name(self, obj):
        """获取原项目名称"""
        return obj.from_project.name if obj.from_project else None

    def get_to_project_name(self, obj):
        """获取目标项目名称"""
        return obj.to_project.name if obj.to_project else None

"""
使用示例：

# 1. 创建schema实例
change_schema = ChangeSchema()
changes_schema = ChangeSchema(many=True)

# 2. 序列化单个对象
change = ChangeRequest.query.get(1)
result = change_schema.dump(change)

# 3. 序列化多个对象
changes = ChangeRequest.query.filter_by(status='待确认').all()
results = changes_schema.dump(changes)

# 4. 反序列化数据创建新的变动请求
change_data = {
    'type': '调岗',
    'employee_id': 1,
    'to_company_id': 2,
    'to_project_id': 3,
    'effective_date': '2024-03-20',
    'status': '待确认'
}
change = change_schema.load(change_data)
"""