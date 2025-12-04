from langchain_ollama import ChatOllama
from prompts.planning_prompts import (
    daily_planner_prompt,
    academic_planner_prompt,
    finance_prompt
)
from prompts.routing_prompt import routing_prompt # Importación para consistencia
from graph.graph_builder import create_graph, PlannerState # Importar PlannerState
from memory.vector_memory import create_vector_memory
from tools.utils import print_pretty_result
import json

def build_chain(prompt, llm):
    return prompt | llm

def main():

    llm = ChatOllama(model="llama3.1", temperature=0)
    print("Inicializando LLM y Vector Store...")

    daily_chain = build_chain(daily_planner_prompt, llm)
    academic_chain = build_chain(academic_planner_prompt, llm)
    finance_chain = build_chain(finance_prompt, llm)

    memory = create_vector_memory()
    print("Vector Store cargado o inicializado.")

    graph = create_graph(
        daily_chain=daily_chain,
        academic_chain=academic_chain,
        finance_chain=finance_chain,
        llm=llm,
        memory=memory 
    )
    print("Grafo de flujo creado. ¡Listo para interactuar!")

    while True:
        query = input("\nTu solicitud: ").strip()
        if query.lower() in ["exit", "quit", "salir"]:
            break

        initial_state = PlannerState(
            query=query, 
            category=None, 
            result=None, 
            context="", 
            vectorstore=memory 
        )
        
        try:
            result = graph.invoke(initial_state)

            print("\nRESULTADO FINAL")
            print_pretty_result(result)
            
        except Exception as e:
            print(f"\n[!] Ocurrió un error al procesar la solicitud: {e}")
            print("Asegúrate de que el LLM está corriendo y generando JSONs válidos.")

if __name__ == "__main__":
    main()