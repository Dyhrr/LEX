class Command:
    trigger = ["tools"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "tools response"
