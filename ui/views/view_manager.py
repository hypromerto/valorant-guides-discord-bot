
from enums.view_type import ViewType

"""Manages all the views of the commands.

    This file injects all the properties of a view, but it does not instantiate them.
    This is because view instantiation must be done during runtime, in an event loop.
"""


def add_to_guide_options(join_list, value, options, domain_type):
    option_key = ''
    if join_list:
        option_key = "_".join(join_list)

    if domain_type not in options:
        options[domain_type] = {}

    if option_key not in options[domain_type]:
        options[domain_type][option_key] = [value]
    else:
        options[domain_type][option_key].append(value)


def get_guide_options(agent_guides_data):
    options = {}

    for agent in agent_guides_data:

        add_to_guide_options([], agent['value'], options, 'agent')

        for map in agent['maps']:

            add_to_guide_options([agent['value']], map['value'], options, 'map')

            for ability in map['abilities']:

                add_to_guide_options([agent['value'], map['value']], ability['value'], options,
                                     'ability')

                for area in ability["areas"]:
                    add_to_guide_options(
                        [agent['value'], map['value'], ability['value']], area, options, 'area')

    return options


def inject_views(views, agent_guides_data):
    view_map = {}

    for view in views:
        view_map[view['view_type']] = {'next_view': view['next_view']}

        if view['view_type'] == ViewType.guides_view.name:
            options = get_guide_options(agent_guides_data)

            view_map[view['view_type']]['base_component_domain_types'] = view['base_component_domain_types']
            view_map[view['view_type']]['components'] = view['components']
            view_map[view['view_type']]['options'] = options

    return view_map
