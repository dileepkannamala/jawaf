"""${project_name} Route Configuration

`routes` will be added following the Sanic app add_route arguments.

For example:

from views import main_view, sidequest_view

routes = [
    # Simple:
    {'handler': sidequest_view, 'uri': '/sidequest/'},

    # More arguments:
    {
        'handler': main_view,
        'uri': '/main/',
        'methods': {'GET', 'POST'}, (Optional - default is {'GET'})
        'host': None, # (Optional - leave out to use default host)
        'strict_slashes: False (Optional - will add version with and without slash if False),
        'websocket': False, # This is a jawaf specific convenience - treat this endpoint as a websocket.
    },

    # Include routes from a sub_directory.
    {'uri': '/options/', 'include': 'options_app'},
]
"""

from ${project_name}.views import LoginView

routes = [
    {'uri': '/login/', 'handler': LoginView.as_view},
    {'uri': '/admin/', 'include': 'jawaf.admin'},
    {'uri': '/auth/', 'include': 'jawaf.auth'},
]