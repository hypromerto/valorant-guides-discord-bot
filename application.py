from infra.application.app import init_bot

client, token = init_bot()

client.run(token)
