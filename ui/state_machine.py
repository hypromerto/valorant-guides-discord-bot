from enums.domain_type import DomainType


def calculate_state_transitions_for_guides(current_state):
    if current_state == DomainType.agent.name:
        return DomainType.map
    elif current_state == DomainType.map.name:
        return DomainType.guide
    elif current_state == DomainType.guide.name:
        return DomainType.ability
    elif current_state == DomainType.ability.name:
        return DomainType.side
    elif current_state == DomainType.side.name:
        return DomainType.area


def previous_states_of_state(current_state):
    all_states = [DomainType.agent, DomainType.map, DomainType.guide, DomainType.ability, DomainType.side,
                  DomainType.area]

    if current_state == DomainType.area.name:
        return all_states[:-1]

    all_states.pop()

    if current_state == DomainType.side.name:
        return all_states[:-1]

    all_states.pop()

    if current_state == DomainType.ability.name:
        return all_states[:-1]

    all_states.pop()

    if current_state == DomainType.guide.name:
        return all_states[:-1]

    all_states.pop()

    if current_state == DomainType.map.name:
        return all_states[:-1]

    all_states.pop()

    if current_state == DomainType.agent.name:
        return all_states[:-1]


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
