from enums.view_type import ViewType
from infra.config.config import settings
from ui.state_machine import StateMachine
from ui.views.guides_view import GuidesView
from ui.views.view_manager import inject_views

view_map = inject_views(settings.views, settings.agent_guides_data)

# This variable is declared globally, as not all commands utilise views.
# The commands that wish to utilise views can access this variable separately,
# without having to inject the view manager into each command.

def init_view(view_type):
    if view_type in view_map:

        if view_type == ViewType.guides_view.name:
            return GuidesView(view_map[view_type]['components'], view_map[view_type]['options'],
                              view_map[view_type]['base_component_domain_types'])
