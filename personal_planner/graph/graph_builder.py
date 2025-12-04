from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from prompts.routing_prompt import routing_prompt
from memory.vector_memory import retrieve_memory, add_memory # Importar funciones de memoria

class PlannerState(TypedDict):
    query: str
    category: str | None
    context: str 
    result: dict | None
    vectorstore: object 

def retrieve_memory_node(state: PlannerState):
    vectorstore = state["vectorstore"]
    query = state["query"]
    
    context = retrieve_memory(vectorstore, query)
    
    return {**state, "context": context}

def router_node(state, llm):
    chain = routing_prompt | llm
    resp = chain.invoke({"query": state["query"]})
    
    raw = resp.content.lower().strip()

    if "daily" in raw:
        decision = "daily"
    elif "academic" in raw:
        decision = "academic"
    elif "finance" in raw:
        decision = "finance"
    else:
        decision = "daily"

    return {**state, "category": decision}

def daily_node(state: PlannerState, daily_chain=None):
    """Genera el plan diario usando la memoria."""
    llm_input = {
        "user_input": state["query"],
        "context": state["context"]
    }
    
    tasks = ["trabajo", "estudio", "ejercicio"]
    
    llm_answer = daily_chain.invoke(llm_input)
    state["result"] = {"modelo": llm_answer}
    return state

def academic_node(state: PlannerState, academic_chain=None):
    llm_input = {
        "user_input": state["query"],
        "context": state["context"]
    }

    llm_answer = academic_chain.invoke(llm_input)
    state["result"] = {"modelo": llm_answer}
    return state

def finance_node(state: PlannerState, finance_chain=None):
    llm_input = {
        "user_input": state["query"],
        "context": state["context"]
    }

    llm_answer = finance_chain.invoke(llm_input)
    
    state["result"] = {"modelo": llm_answer}
    return state

def update_memory_node(state: PlannerState):
    vectorstore = state["vectorstore"]
    query = state["query"]
    
    llm_response_content = state["result"]["modelo"].content
    
    memory_summary = f"Query: {query} | Output Summary: {llm_response_content[:150]}..."
    
    add_memory(vectorstore, query, memory_summary)
    
    return state

def router_edge(state):
    category = state.get("category", "")
    
    if category == "daily":
        return "daily"
    if category == "academic":
        return "academic"
    if category == "finance":
        return "finance"
    
    return "daily" 

def create_graph(daily_chain, academic_chain, finance_chain, llm, memory):
    
    builder = StateGraph(PlannerState)
    
    builder.add_node("retrieve_memory", retrieve_memory_node)
    builder.add_node("router", lambda s: router_node(s, llm=llm))
    builder.add_node("daily", lambda s: daily_node(s, daily_chain=daily_chain))
    builder.add_node("academic", lambda s: academic_node(s, academic_chain=academic_chain))
    builder.add_node("finance", lambda s: finance_node(s, finance_chain=finance_chain))
    builder.add_node("update_memory", update_memory_node) # Nuevo nodo para guardar
    
    builder.add_edge(START, "retrieve_memory")
    builder.add_edge("retrieve_memory", "router")
    
    builder.add_conditional_edges("router", router_edge, {
        "daily": "daily",
        "academic": "academic",
        "finance": "finance",
    })
    
    builder.add_edge("daily", "update_memory")
    builder.add_edge("academic", "update_memory")
    builder.add_edge("finance", "update_memory")
    
    builder.add_edge("update_memory", END) 
    
    return builder.compile()