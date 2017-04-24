from jawaf.admin.views import DataView, ManageAccessView, SearchView

routes = [
    {'uri': 'manage_access/', 'handler': ManageAccessView.as_view()}, # GET, POST, PUT, DELETE
    {'uri': '<table_name:string>/', 'handler': DataView.as_view()}, # GET, POST, PUT, DELETE
    {'uri': '<table_name:string>/search/', 'handler': SearchView.as_view()}, # GET
]
