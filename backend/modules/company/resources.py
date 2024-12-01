from flask_restful import Resource
from .models import Company,Project
from .schemas import CompanySchema, ProjectSchema

company_schema = CompanySchema(many=True)
project_schema = ProjectSchema(many=True)

class CompaniesResource(Resource):
    def get(self):
        companies = Company.query.all()
        return company_schema.dump(companies), 200

class CompanyProjectsResource(Resource):
    def get(self, id):
        company = Company.query.get(id)
        if not company:
            return {'message': '未找到公司 (Company not found)'}, 404
        projects = company.projects
        return project_schema.dump(projects), 200