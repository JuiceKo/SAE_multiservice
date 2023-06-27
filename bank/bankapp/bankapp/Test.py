import asyncio
import nats

async def handle_message(msg):
    subject = msg.subject
    data = msg.data.decode()

    if subject == "notification":
        # Montre la demande
        print(f"Question: {data}")

        # Une réponse de l'utilisateur
        response = await ask_user("Procéder au virement ? (oui/non): ")

        # Réponse de l'utilisateur
        await nc.publish("response", response.encode())

async def ask_user(prompt):
    response = input(prompt)
    return response.lower().strip()

async def main():
    nc = await nats.connect("10.128.7.30:4222")

    # Subscribe to question subject
    await nc.subscribe("question", cb=handle_message)

    print("NATS server is running...")
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
