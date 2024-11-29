from .auth import LoginResource, RegisterResource, LogoutResource
from .employees import ActiveEmployeesResource, AddEmployeeResource
from .changes import PendingChangesResource, ApproveChangeResource, RejectChangeResource
from .companies import CompaniesResource, CompanyProjectsResource
from .users import UserMeResource

def initialize_routes(api):
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LogoutResource, '/api/auth/logout')
    
    api.add_resource(ActiveEmployeesResource, '/api/active-employees')
    api.add_resource(AddEmployeeResource, '/api/employees')
    
    api.add_resource(PendingChangesResource, '/api/pending-changes')
    api.add_resource(ApproveChangeResource, '/api/pending-changes/<int:id>/approve')
    api.add_resource(RejectChangeResource, '/api/pending-changes/<int:id>/reject')
    
    api.add_resource(CompaniesResource, '/api/companies')
    api.add_resource(CompanyProjectsResource, '/api/companies/<int:id>/projects')
    
    api.add_resource(UserMeResource, '/api/users/me')