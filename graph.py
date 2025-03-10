from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from llm import llm_model
from context_manager import trim_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    # Trim messages to fit context window
    state["messages"] = trim_messages(state["messages"], max_tokens=4000)
    # Invoke LLM Model
    system_message = "You are a helpful assistant. You are a human being. Talk like a human."
    response = llm_model.invoke({"system_message": system_message, "messages": state["messages"]})
    return {"messages": [response]}
    
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph=graph_builder.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "123"}}

