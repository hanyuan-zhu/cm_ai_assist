from flask_restful import Resource
from .models import Company, Project
from .schemas import CompanySchema, ProjectSchema

company_schema = CompanySchema(many=True)
project_schema = ProjectSchema(many=True)

class CompaniesResource(Resource):
    def get(self):
        try:
            companies = Company.query.all()
            return {'companies': company_schema.dump(companies)}, 200
        except Exception as e:
            return {'message': f'获取公司列表时出错 (Error retrieving company list): {str(e)}'}, 500

class CompanyProjectsResource(Resource):
    def get(self, id):
        try:
            company = Company.query.get(id)
            if not company:
                return {'message': '未找到公司 (Company not found)'}, 404
            projects = company.projects
            return {'projects': project_schema.dump(projects)}, 200
        except Exception as e:
            return {'message': f'获取项目列表时出错 (Error retrieving project list): {str(e)}'}, 500