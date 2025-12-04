# Personal Planner & Finance Assistant

A modular AI-powered assistant for personal productivity, academic planning, and financial management. Built using LLM-based multi-agent coordination and LangGraph for workflow orchestration.

## Features

- Daily Planner: Organizes tasks, priorities, recommendations, and calculates time blocks.
- Academic Planner: Generates study plans, suggested hours, strategies, and reminders.
- Finance Planner: Provides a detailed financial overview, suggested savings, and budget allocation using the 50/30/20 rule.
- Memory Integration: Stores and retrieves user queries for context-aware planning.
- Workflow Routing: Automatically routes user requests to the appropriate agent (daily, academic, finance) using LangGraph.

## Installation

1. Clone the repository:

```

git clone [https://github.com/aishagomez/Individual-Final-Project](https://github.com/aishagomez/Individual-Final-Project)
cd Individual-Final-Project

```

2. Install dependencies:

```

pip install -r requirements.txt

```

3. Ensure you have access to an LLM (e.g., Ollama or compatible LangChain LLM backend).

## Usage

Run the main application:

```
cd personal_planner
python main.py

```

Then enter your queries interactively:

```

Tu solicitud: Quiero organizar mi estudio para el examen de matemáticas el viernes

```

Supported query categories:

- Daily tasks and schedule
- Academic planning
- Financial planning and budgeting

Type `exit`, `quit`, or `salir` to end the session.

## Example Outputs

**Daily Planner**:

```

=== AGENDA DIARIA ===

  * Trabajo: 4h (09:00-13:00)
      Descripción: Terminar reporte
  * Estudio: 3h (14:00-17:00)
      Descripción: Repaso matemáticas
      === PRIORIDADES ===
  * Alta: Preparar examen
      === RECOMENDACIONES ===
  * Tomar descansos cada 2 horas
      === BLOQUES DE TIEMPO CALCULADOS ===
  * trabajo: 4 horas
  * estudio: 3 horas
  * ejercicio: 5 horas


```

**Academic Planner**:

```

=== PLAN DE ESTUDIO ===

  * Repaso general hoy
  * Ejercicios mañana
      Horas de estudio: 4
      === Estrategias ===
  * Técnica Pomodoro
  * Subrayado de apuntes
      === Recordatorios ===
  * Revisar notas antes de dormir


```

**Finance Planner**:

```
=== PLAN FINANCIERO ===

Resumen (Detalle):

Inicio de trabajo: lunes a viernes de 7:00 AM a 11:00 AM

Gastos fijos:
- Alquiler: 500
- Servicios públicos: 150
- Comida: 300

Ingresos:
- Salario: 2000

Gastos variables:
- Transporte: 100
- Entretenimiento: 200

Ahorro sugerido: 300

Distribución 50/30/20:
- Needs: 1000
- Wants: 600
- Savings: 400

```
