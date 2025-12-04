from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Inicializar embeddings globalmente
EMBEDDING_FUNCTION = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def create_vector_memory():
    """
    Inicializa o carga el Vector Store de Chroma.
    """
    vectorstore = Chroma(
        collection_name="planner_memory",
        embedding_function=EMBEDDING_FUNCTION,
        persist_directory="memory/db"
    )

    # Asegurarse de que el store no esté vacío (solo en la primera ejecución)
    if not vectorstore._collection.count():
        vectorstore.add_texts(["inicio de la conversación"])
    
    return vectorstore

def add_memory(vectorstore, query, result):
    """
    Almacena el resultado de la interacción para futuras consultas.
    Almacena la consulta del usuario y el resumen de la respuesta del LLM.
    """
    # Crear un documento de memoria conciso
    memory_doc = f"USUARIO: {query} -> RESPUESTA: {result}"
    
    # Guardar en el vector store
    vectorstore.add_texts([memory_doc])
    
    print(f"\n[ Memoria guardada para el futuro: '{memory_doc[:50]}...' ]")

def retrieve_memory(vectorstore, query, k=3):
    """
    Recupera los K documentos más relevantes para la consulta.
    """
    docs = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in docs])
    return context