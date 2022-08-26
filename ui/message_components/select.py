import discord.ui

from ui.state_machine import previous_states_of_state


class Select(discord.ui.Select):

    def __init__(self, domain_type, options, placeholder, key):
        super().__init__(options=options, placeholder=placeholder)
        self.domain_type = domain_type
        self.key = key

    async def callback(self, interaction: discord.Interaction):

        previous_choices = self.key.split('_')

        content_message = ''

        previous_states = previous_states_of_state(self.domain_type)

        for index, previous_state in enumerate(previous_states):
            content_message += f'**{previous_state.name.capitalize()}:**   {previous_choices[index]}\n'

        content_message += f'**{self.domain_type.capitalize()}:**   {self.values[0]}\n'

        await interaction.message.edit(content=content_message,
                                       view=self.view.update_view(self.domain_type, self.key, self.values[0]))

        await interaction.response.defer()
