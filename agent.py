from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict
from tools import all_tools


# Base model
base_model = ChatOllama(model="llama3.2", temperature=0.3)
tool_model = base_model.bind_tools(all_tools)


# ------------------
# STATE
# ------------------
class ChatState(TypedDict):
    messages: list[dict]


# ------------------
# LLM NODE
# ------------------
def llm_node(state: ChatState):
    messages = state["messages"]
    print("LLM INPUT →", messages)

    response = tool_model.invoke(messages)
    return {"messages": messages + [response]}


# ------------------
# ROUTER
# ------------------
def router(state: ChatState):
    last = state["messages"][-1]

    if isinstance(last, AIMessage) and last.tool_calls:
        return "tool"

    if isinstance(last, ToolMessage):
        return "final"
    
    if isinstance(last,dict):
        return "tool" if getattr(last,"tools_calls",False) else "final"

    return "final"



# ------------------
# BUILD AGENT GRAPH
# ------------------

Tool_Interface = ToolNode(all_tools)


def tools_node(state):
    result = Tool_Interface.invoke(state)
    return {
        'messages': state['messages'] + result['messages']
    }

def create_agent():
    graph = StateGraph(ChatState)
    
    graph.add_node("llm", llm_node)
    graph.add_node("tool", tools_node)

    graph.add_edge(START, "llm")
    graph.add_edge("tool", "llm")

    graph.add_conditional_edges(
        "llm",
        router,
        {
            "tool": "tool",
            "final": END,
        }
    )

    return graph.compile()


# ------------------
# SYSTEM MESSAGE
# ------------------
system_msg = {"role": "system", "content":"""
You are Mandy, a tool-dependent manufacturing assistant.

RULES:
1. Use tools for ANY factual company data.
2. Never guess values.
3. If user asks for an ID → use get_*_by_id tool.
4. If filtering is needed → use appropriate tool.
5. Use get_all_* tools if unsure.
6. Only answer based on tool results.
7. After tool execution, give a clean natural-language answer.
8. If no data found, respond with "No data found."

STYLE:
- concise
- factual
- no hallucinations
"""
}

agent = create_agent()


# ------------------
# ASK FUNCTION
# ------------------
def ask_agent(conversation:list[dict]):
    state:ChatState = {
        "messages": [
            system_msg,
            *conversation
        ]
    }
    try:
        final = agent.invoke(state)
        return final["messages"][-1].content
    except Exception as e:
        return f"Error: {e}"



if __name__ == "__main__":
    query = "How many suppliers are there?"
    try:
        answer = ask_agent([{"role": "user", "content": query}])
        print("Agent Answer →", answer)
    except Exception as e:
        print(f"Error: {e}")