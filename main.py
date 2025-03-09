from fastapi import FastAPI,WebSocket
from fastapi.responses import HTMLResponse
from graph import graph
from pydantic import BaseModel
from template import html

app = FastAPI()

class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str

@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content


# Streaming

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{thread_id}")     
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for event in graph.astream({"messages": [data]}, config=config, stream_mode="messages"):
            await websocket.send_text(event[0].content)