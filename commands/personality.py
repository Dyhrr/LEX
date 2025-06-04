class Command:
    trigger = ["personality"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "personality response"
