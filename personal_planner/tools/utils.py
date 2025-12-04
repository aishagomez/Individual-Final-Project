import json
import re

def print_pretty_result(result):
    
    if not result or "result" not in result:
        print("No hay resultado disponible.")
        return

    # Extraer el contenido JSON del AIMessage
    modelo = result["result"].get("modelo")
    bloques = result["result"].get("bloques", {})
    
    content = ""
    if hasattr(modelo, "content"):
        content = modelo.content
    elif isinstance(modelo, str):
        content = modelo

    # Limpiar backticks y extraer JSON (crucial para eliminar texto basura)
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    
    if not json_match:
        print("\n[!] ERROR DE FORMATO LLM: No se pudo extraer JSON estricto del modelo.")
        print("--- RESPUESTA CRUDA DEL LLM (Esperaba JSON estricto) ---")
        print(content)
        print("---------------------------------------------------------")
        return

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"\n[!] ERROR DE DECODIFICACIÓN JSON: Error al decodificar JSON del modelo: {e}")
        print("--- RESPUESTA CRUDA DEL LLM ---")
        print(content)
        print("-------------------------------")
        return

    # ===================== MEMORIA RECUPERADA =====================
    context = result.get("context", "Ninguno")

    # ===================== DAILY =====================
    if "rutina_tareas" in data: # Cambio clave: buscar la nueva clave
        print("\n=== AGENDA DIARIA ===")
        
        # Validación de tipo para 'rutina_tareas'
        rutina_tareas = data.get("rutina_tareas", [])
        if isinstance(rutina_tareas, list):
            for t in rutina_tareas:
                # Asegura que cada elemento de la lista es un diccionario antes de llamar .get()
                if isinstance(t, dict):
                    print(f"- {t.get('tipo', 'N/A')}: {t.get('duracion', 'N/A')} ({t.get('horario', 'N/A')})")
                    print(f"  Descripción: {t.get('descripcion', 'N/A')}")
                    if t.get("notas"):
                        print(f"  Notas: {t.get('notas')}")
                else:
                    print(f"[!] ADVERTENCIA: Elemento en rutina_tareas no es un diccionario ({type(t).__name__}).")

        else:
            print(f"[!] ADVERTENCIA: 'rutina_tareas' no es una lista ({type(rutina_tareas).__name__}).")
            
        # Validación de tipo para 'prioridades'
        prioridades = data.get("prioridades", [])
        if prioridades and isinstance(prioridades, list):
            print("\n=== PRIORIDADES ===")
            for p in prioridades:
                print(f"- {p}") # Asumiendo que es una lista de strings
        
        # Validación de tipo para 'recomendaciones'
        recomendaciones = data.get("recomendaciones", [])
        if recomendaciones and isinstance(recomendaciones, list):
            print("\n=== RECOMENDACIONES ===")
            for r in recomendaciones:
                print(f"- {r}")



    # ===================== ACADEMIC =====================
    elif "plan_estudio" in data:
        print("\n=== PLAN DE ESTUDIO ===")
        # ... (resto del código ACADEMIC se mantiene igual)
        
        # Validación de tipo para 'plan_estudio'
        plan_estudio = data.get("plan_estudio", [])
        if isinstance(plan_estudio, list):
            for item in plan_estudio:
                print(f"- {item}")
        else:
            print(f"[!] ADVERTENCIA: 'plan_estudio' no es una lista ({type(plan_estudio).__name__}).")

        horas = data.get("horas_estudio")
        if horas:
            print(f"\nHoras de estudio: {horas}")

        # Validación de tipo para 'estrategias'
        estrategias = data.get("estrategias", [])
        if estrategias and isinstance(estrategias, list):
            print("\nEstrategias:")
            for e in estrategias:
                print(f"- {e}")

        # Validación de tipo para 'recordatorios'
        recordatorios = data.get("recordatorios", [])
        if recordatorios and isinstance(recordatorios, list):
            print("\nRecordatorios:")
            for r in recordatorios:
                print(f"- {r}")

    # ===================== FINANCE =====================
    elif "resumen_financiero" in data:
        print("\n=== PLAN FINANCIERO ===")

        # Manejar si 'resumen_financiero' es un objeto o un string
        # Manejar 'resumen_financiero' como dict para imprimir bonito
        resumen = data.get("resumen_financiero", {})

        if isinstance(resumen, dict):
            print("\n=== RESUMEN FINANCIERO DETALLADO ===")
            
            # Ingresos
            ingresos = resumen.get("ingresos", {})
            if ingresos:
                print("\nIngresos:")
                for k, v in ingresos.items():
                    print(f"- {k}: {v} USD")
            
            # Gastos fijos
            gastos_fijos = resumen.get("gastos_fijos", [])
            if gastos_fijos:
                print("\nGastos fijos:")
                for g in gastos_fijos:
                    nombre = g.get("nombre", "N/A")
                    monto = g.get("monto", "N/A")
                    print(f"- {nombre}: {monto} USD")
            
            # Gastos variables
            gastos_variables = resumen.get("gastos_variables", [])
            if gastos_variables:
                print("\nGastos variables:")
                for g in gastos_variables:
                    nombre = g.get("nombre", "N/A")
                    monto = g.get("monto", "N/A")
                    print(f"- {nombre}: {monto} USD")
            
        else:
            # Si no es dict, lo imprimimos tal cual
            print(f"\nResumen: {resumen}")


        ahorro = data.get("ahorro_sugerido")
        if ahorro:
            print(f"Ahorro sugerido: {ahorro}")

        # Corrección crítica: asegurar que 'gastos_recortables' sea una lista
        gastos = data.get("gastos_recortables", [])
        if gastos and isinstance(gastos, list):
            print("\nGastos recortables:")
            for g in gastos:
                print(f"- {g}")
        elif gastos:
            # Imprime una advertencia si no es una lista pero tiene contenido
            print(f"[!] ADVERTENCIA: 'gastos_recortables' no es una lista ({type(gastos).__name__}). Contenido: {gastos}")
        

    else:
        print("No se reconoció el tipo de resultado.")