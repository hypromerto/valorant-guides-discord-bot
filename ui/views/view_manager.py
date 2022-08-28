import discord
from discord import SelectOption

from enums.view_type import ViewType
from ui.message_components.select import Select

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

            for guide in map['guides']:

                add_to_guide_options([agent['value'], map['value']], guide['value'], options, 'guide')

                for ability in guide['abilities']:

                    add_to_guide_options([agent['value'], map['value'], guide['value']], ability['value'], options,
                                         'ability')

                    for side in ability["sides"]:

                        add_to_guide_options([agent['value'], map['value'], guide['value'], ability['value']],
                                             side['value'], options, 'side')

                        for area in side["areas"]:
                            add_to_guide_options(
                                [agent['value'], map['value'], guide['value'], ability['value'], side['value']],
                                area, options, 'area')

    return options


def init_guides_view_components(components, agent_guides_data):
    view_components = {}

    options = get_guide_options(agent_guides_data)

    for component in components:
        if component["type"] == discord.ComponentType.select.name:

            for key, value in options[component['domain_type']].items():
                select_options = []

                for option in value:
                    select_options.append(SelectOption(label=option))

                select_object = Select(domain_type=component['domain_type'], placeholder=component['placeholder'],
                                       options=select_options, key=key)

                if component['domain_type'] not in view_components:
                    view_components[component['domain_type']] = {}

                view_components[component['domain_type']][key] = select_object

    return view_components


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
