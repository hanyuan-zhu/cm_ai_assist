from .resources import ActiveEmployeesResource, AddEmployeeResource

def init_employee_routes(api):    
    api.add_resource(ActiveEmployeesResource, '/api/active-employees')
    api.add_resource(AddEmployeeResource, '/api/employees')
