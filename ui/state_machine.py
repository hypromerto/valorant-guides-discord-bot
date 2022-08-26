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
