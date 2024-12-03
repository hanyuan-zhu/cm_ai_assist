from modules.auth.resources import LoginResource, RegisterResource, LogoutResource
def init_auth_routes(api):
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LogoutResource, '/api/auth/logout')
