from .resources import CompaniesResource, CompanyProjectsResource

def init_company_routes(api):
    api.add_resource(CompaniesResource, '/api/companies')
    api.add_resource(CompanyProjectsResource, '/api/companies/<int:id>/projects')