from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict

from tools import all_tools

# Base model + binding tools
chat_model = init_chat_model("llama3.2", model_provider="ollama").bind_tools(all_tools)


class ChatState(TypedDict):
    messages: list

def llm_response(state: ChatState) -> dict:
    response = chat_model.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}




def router(state: ChatState):
    last = state["messages"][-1]

    if isinstance(last, AIMessage) and last.tool_calls:
        return "tool"

    if isinstance(last, ToolMessage):
        return "llm_answer"

    return "end"


# def summary(state: ChatState) :
#     messages = state["messages"] + [
#         SystemMessage(content="Provide a concise summary based on the messages.")
#     ]
#     response = chat_model.invoke(messages)
#     return {"messages": messages + [response]}


def create_agent():
    graph = StateGraph(ChatState)

    tool_node = ToolNode(all_tools)

    graph.add_node("llm_answer", llm_response)
    graph.add_node("tool", tool_node)

    graph.add_edge(START, "llm_answer")
    graph.add_edge("tool", "llm_answer")

    graph.add_conditional_edges(
        "llm_answer",
        router,
        {
            "tool": "tool",
            "end": END
        }
    )

    return graph.compile()



system_msg = SystemMessage(content="""You are Mandy, a tool-dependent manufacturing assistant.  

You MUST use tools whenever the answer requires company data.  
You MUST NOT fabricate or guess details.

RULES:
1. If the user asks for any operational fact (counts, stock, supplier info, materials, batches, purchase orders), call a tool.
2. If the question references an ID → use the matching get_*_by_id tool.
3. If it requires filtering (date, shift, product) → use the corresponding specialized tool.
4. If multiple tools are needed, call them step-by-step.
5. If a question cannot be answered using given tools, ask the user for missing information.
6. you can get_all_* to explore data before filtering.
7. Always provide answers based on the tool responses only.

IMPORTANT: Follow these guidelines strictly to ensure accurate and reliable responses.

RESPONSE STYLE:
- Concise  
- Accurate  
- Do not expose internal tool names  
- Do not invent values  

""")

agent = create_agent()  

def ask_agent(question: str) -> str:
    initial_state: ChatState = {
        "messages": [
            system_msg,
            HumanMessage(content=question)
        ]
    }
    final_state = agent.invoke(initial_state)
    return final_state["messages"][-1].content