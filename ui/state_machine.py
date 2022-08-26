class StateMachine:

    def __init__(self):
        self.current_state = {}

    def update_state(self, domain_type, new_value):
        self.current_state[domain_type] = new_value
