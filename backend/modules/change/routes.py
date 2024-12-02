from .resources import PendingChangesResource, ApproveChangeResource, RejectChangeResource, EmployeeTransferResource, EmployeeResignResource
def init_change_routes(api):
    api.add_resource(EmployeeTransferResource, '/api/pending-changes/<int:id>/transfer')
    api.add_resource(EmployeeResignResource, '/api/pending-changes/<int:id>/resign')
    api.add_resource(PendingChangesResource, '/api/pending-changes')
    api.add_resource(ApproveChangeResource, '/api/pending-changes/<int:id>/approve')
    api.add_resource(RejectChangeResource, '/api/pending-changes/<int:id>/reject')
    