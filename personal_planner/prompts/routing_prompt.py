from langchain_core.prompts import PromptTemplate

routing_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
Clasifica la solicitud del usuario según la CATEGORÍA MÁS ADECUADA:

- "daily": Para solicitudes de horarios, rutinas, distribución de tiempo fijo (clases, almuerzo, trabajo, horas de estudio), agenda diaria.
- "academic": Para solicitudes de planes de estudio, estrategias de aprendizaje, preparación de exámenes.
- "finance": Para solicitudes de ingresos, gastos, presupuestos, balances o ahorro.

Solo devuelve la categoría como una sola palabra en minúsculas.

Solicitud del usuario:
{query}
"""
)
