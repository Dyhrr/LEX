class Command:
    trigger = ["info"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "info response"
