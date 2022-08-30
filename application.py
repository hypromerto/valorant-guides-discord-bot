from infra.application.app import init_bot
from infra.config.global_values import token

client = init_bot()

client.run(token)
