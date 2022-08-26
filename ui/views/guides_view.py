import discord


class GuidesView(discord.ui.View):

    def __init__(self, components, base_component_domain_types):
        self.view_components = []
        self.base_component_domain_types = base_component_domain_types
        super().__init__()
        for component in components:
            if component.domain_type in self.base_component_domain_types:
                self.add_item(component)

            #The "view_components" data structure may not be an array,
            #just using it as an array temporarily as to remind that
            #we need such a structure, but its form might change.
            self.view_components.append(components)



