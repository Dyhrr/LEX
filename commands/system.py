class Command:
    trigger = ["system"]

    def __init__(self, context):
        self.context = context

    async def run(self, args: str) -> str:
        return "system response"
