from enums.domain_type import DomainType


def calculate_state_transitions_for_guides(current_state):
    if current_state == DomainType.agent.name:
        return DomainType.map
    elif current_state == DomainType.map.name:
        return DomainType.ability
    elif current_state == DomainType.ability.name:
        return DomainType.area
    elif current_state == DomainType.area.name:
        return DomainType.guide_result

class StateMachine:

    def __init__(self, view_data):
        self.view_data = view_data
        self.view_transitions = self.calculate_view_transitions(view_data)

    def calculate_view_transitions(self, view_data):
        view_transitions = {}

        for view, data in view_data.items():
            view_transitions[view] = data['next_view']

        return view_transitions

    def get_next_view(self, view_type):
        next_view_type = self.view_transitions[view_type]

        return self.view_data[next_view_type]
