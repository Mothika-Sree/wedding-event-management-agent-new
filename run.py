import asyncio
import uvicorn

asyncio.set_event_loop_policy(
    asyncio.WindowsProactorEventLoopPolicy()
)

uvicorn.run(
    "app.main:app",
    host="127.0.0.1",
    port=8000
)