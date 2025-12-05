from fastapi import FastAPI
from models import UserMessage, AIResponse
from langchain.messages import HumanMessage, AIMessage
from agent import ask_agent

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ask")
def ask_question(conversation: list[UserMessage | AIResponse])->AIResponse:
    # Convert to langchain message types
    lc_conversation: list[HumanMessage | AIMessage] = []
    for msg in conversation:
        if msg.role == "human":
            lc_conversation.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_conversation.append(AIMessage(content=msg.content))
    response = ask_agent(lc_conversation)
    return AIResponse(role="assistant", content=response)