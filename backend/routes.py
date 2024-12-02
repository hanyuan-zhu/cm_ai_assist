from modules.auth import init_auth_routes
from modules.employee import init_employee_routes
from modules.change import init_change_routes
from modules.company import init_company_routes

def initialize_routes(api):
    init_auth_routes(api)
    init_employee_routes(api)
    init_change_routes(api)
    init_company_routes(api)