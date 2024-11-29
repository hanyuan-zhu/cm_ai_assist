from flask_restful import Resource
from backend.models.company import Company
from backend.models.project import Project
from schemas.company_schema import CompanySchema
from schemas.project_schema import ProjectSchema

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
            return {'message': 'Company not found'}, 404
        projects = company.projects
        return project_schema.dump(projects), 200