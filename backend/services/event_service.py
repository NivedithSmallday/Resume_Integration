import asyncio
from typing import List


class EventService:
    """Handles Server-Sent Events (SSE) subscriptions and notifications."""

    def __init__(self):
        self.subscribers: List[asyncio.Queue[str]] = []

    async def event_generator(self):
        """Yields data for SSE clients."""
        queue: asyncio.Queue[str] = asyncio.Queue()
        self.subscribers.append(queue)
        try:
            while True:
                data = await queue.get()
                yield f"data: {data}\n\n"
        finally:
            self.subscribers.remove(queue)

    def notify(self, message: str):
        """Notify all connected clients."""
        for queue in self.subscribers:
            queue.put_nowait(message)
