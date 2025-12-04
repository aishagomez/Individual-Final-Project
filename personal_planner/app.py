import streamlit as st
from langchain_ollama import ChatOllama
from prompts.planning_prompts import daily_planner_prompt, academic_planner_prompt, finance_prompt
from prompts.routing_prompt import routing_prompt
from graph.graph_builder import create_graph, PlannerState
from memory.vector_memory import create_vector_memory
from tools.utils import print_pretty_result

def build_chain(prompt, llm):
    return prompt | llm

# -------------------- SETUP --------------------
st.set_page_config(page_title="Planner Assistant", layout="wide")
st.title("Planner Assistant")

st.markdown(
    """
    Enter your request below. The system will automatically categorize it as **Daily**, **Academic**, or **Finance** 
    and generate a structured plan.
    """
)

@st.cache_resource
def initialize_system():
    llm = ChatOllama(model="gemma3:1b", temperature=0)
    memory = create_vector_memory()

    daily_chain = build_chain(daily_planner_prompt, llm)
    academic_chain = build_chain(academic_planner_prompt, llm)
    finance_chain = build_chain(finance_prompt, llm)

    graph = create_graph(
        daily_chain=daily_chain,
        academic_chain=academic_chain,
        finance_chain=finance_chain,
        llm=llm,
        memory=memory
    )

    return llm, memory, graph

llm, memory, graph = initialize_system()

# -------------------- USER INPUT --------------------
user_input = st.text_area("Your request:", height=120)

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a query.")
    else:
        initial_state = PlannerState(
            query=user_input, 
            category=None, 
            result=None, 
            context="", 
            vectorstore=memory
        )

        try:
            result = graph.invoke(initial_state)

            st.subheader("Result")
            # Capturar el resultado en texto para mostrarlo en Streamlit
            import io
            import sys

            buffer = io.StringIO()
            sys.stdout = buffer
            print_pretty_result(result)
            sys.stdout = sys.__stdout__
            st.text(buffer.getvalue())

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Ensure the LLM is running and producing valid JSON outputs.")
