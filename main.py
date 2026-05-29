import os
import sys
from dotenv import load_dotenv
from firecrawl import Firecrawl
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# 1. Cargar variables de entorno del archivo .env local
load_dotenv(r"c:\Users\armon\DEV\react-search-agent\.env")

# Asegurar compatibilidad absoluta con LangSmith en Windows (limpiando prefijos 'export' y comillas)
for key, value in list(os.environ.items()):
    if key.startswith("export "):
        clean_key = key.replace("export ", "").strip()
        os.environ[clean_key] = value.strip('"').strip("'")

# Verificar variables de entorno cruciales
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY") or os.getenv("export DASHSCOPE_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY") or os.getenv("export FIRECRAWL_API_KEY")

if not DASHSCOPE_API_KEY:
    print("Error: DASHSCOPE_API_KEY no está configurado en tu archivo .env.")
    sys.exit(1)

if not FIRECRAWL_API_KEY:
    print("Error: FIRECRAWL_API_KEY no está configurado en tu archivo .env.")
    sys.exit(1)

# Confirmar estado de conexión con LangSmith
tracing_active = os.getenv("LANGSMITH_TRACING")
project_name = os.getenv("LANGSMITH_PROJECT", "react-search-agent")
if tracing_active == "true":
    print(f" LangSmith: Activado y conectado (Proyecto: '{project_name}')")
else:
    print(" LangSmith: Desactivado")

# Inicializar cliente de Firecrawl
firecrawl_app = Firecrawl(api_key=FIRECRAWL_API_KEY)

# 2. Herramienta de búsqueda inmobiliaria optimizada para el Investigador
@tool
def web_search(query: str) -> str:
    """Busca en la web información de inmuebles, precios, ofertas y listados en tiempo real.
    
    Args:
        query: Los términos o palabras clave de búsqueda inmobiliaria.
    """
    try:
        results = firecrawl_app.search(query, limit=10)
        if not results or not getattr(results, "web", None):
            return "No se encontraron ofertas inmobiliarias en la web para esta consulta."
        
        output_lines = []
        for idx, item in enumerate(results.web, 1):
            title = getattr(item, "title", "Sin título")
            url = getattr(item, "url", "Sin URL")
            description = getattr(item, "description", "Sin descripción")
            output_lines.append(f"[{idx}] {title}\nURL: {url}\nDetalles: {description}\n")
            
        return "\n".join(output_lines)
    except Exception as e:
        return f"Error al ejecutar la búsqueda web con Firecrawl: {str(e)}"

# Listar las herramientas
tools = [web_search]

# 3. Configurar el modelo DeepSeek-v3.2 en DashScope
llm = ChatOpenAI(
    model="deepseek-v3.2",
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    temperature=0.1,  # Temperatura muy baja para asegurar precisión analítica
)

# 4. Definición de la Cadena de Multi-Agentes utilizando la arquitectura ReAct más moderna de LangChain 1.x (create_agent)

# Agente 1: Investigador ReAct (Recopila la información cruda vía Firecrawl)
investigator_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "Eres un Agente Investigador de Mercado Inmobiliario experto en Lecheria (Anzoategui, Venezuela). "
        "Tu única tarea es recopilar datos duros, reales y crudos del mercado de apartamentos actual en Lecheria "
        "utilizando la herramienta 'web_search'. Realiza búsquedas exhaustivas enfocadas en apartamentos en venta. "
        "Debes extraer de cada oferta encontrada:\n"
        "- Nombre del conjunto residencial o zona (ej. Pueblo Viejo, Cerro El Morro, Av. Américo Vespucio, Marina Mar).\n"
        "- Precio en dólares americanos (USD).\n"
        "- Dimensiones en metros cuadrados (m²).\n"
        "- Número de habitaciones/baños.\n"
        "- URL de la oferta para validación futura.\n"
        "\n"
        "Presenta esta lista de forma muy clara, estructurada y sin hacer análisis, para que el Agente Validador "
        "pueda realizar los cálculos. No utilices emojis para evitar fallos de visualización."
    )
)

# Agente 2: Validador / Analista ReAct (Valida, calcula promedios y detecta oportunidades de inversión MVP)
validator_agent = create_agent(
    model=llm,
    tools=[],  # Este agente no necesita herramientas de búsqueda directa ya que analiza los datos entregados
    system_prompt=(
        "Eres un Agente Validador y Analista Financiero Inmobiliario experto de Lecheria (Anzoategui, Venezuela). "
        "Tu tarea es recibir los listados de apartamentos crudos recopilados por el Agente Investigador, "
        "analizarlos con absoluto rigor matemático y estructurar el reporte final.\n"
        "\n"
        "Debes seguir estos pasos obligatorios:\n"
        "1. Validar los datos recopilados: elimina cualquier propiedad sospechosa o que no sea de Lechería, Venezuela.\n"
        "2. Realizar los cálculos: calcula el precio promedio general del mercado y el costo promedio por metro cuadrado (USD/m²).\n"
        "3. Identificar los 'MVPs' (Most Valuable Properties): aquellas propiedades que presentan la mejor relación "
        "calidad-precio o una clara oportunidad de inversión (ej. precios por debajo del promedio del área con excelente metraje).\n"
        "4. Redactar el informe estructurado final en Markdown con las siguientes secciones:\n"
        "   - # INFORME DE INVERSIÓN: OPORTUNIDADES MVP EN LECHERIA, VENEZUELA\n"
        "   - ## RESUMEN EJECUTIVO DE OPORTUNIDADES\n"
        "   - ## TABLA COMPARATIVA Y METRICAS CLAVE (Zonas, precio promedio y precio estimado por m²)\n"
        "   - ## PROPIEDADES 'MVP' SELECCIONADAS (Detalle de las 3-5 mejores opciones costo-beneficio para invertir, con justificación analítica)\n"
        "   - ## ANÁLISIS DE FACTIBILIDAD Y TEMPERATURA DE INVERSIÓN\n"
        "\n"
        "IMPORTANTE: Entrega una redacción premium, profesional y sin emojis para garantizar compatibilidad con terminales."
    )
)

def main():
    print("=" * 60)
    print("SISTEMA REACT MULTI-AGENTE INMOBILIARIO (LANGCHAIN 1.X + DEEPSEEK)")
    print("=" * 60)
    
    # 1. Ejecutar el Agente Investigador ReAct
    print("\n[Agente 1 ReAct] Iniciando investigación de ofertas con Firecrawl...")
    query_investigacion = "Busca listados de apartamentos en venta en Lecheria, Anzoategui, Venezuela con precios en USD, metros cuadrados y ubicaciones."
    
    try:
        inputs_inv = {"messages": [{"role": "user", "content": query_investigacion}]}
        res_inv = investigator_agent.invoke(inputs_inv)
        
        messages_inv = res_inv.get("messages", [])
        if not messages_inv:
            print("Error: El Agente Investigador no devolvió resultados.")
            return
            
        raw_data = messages_inv[-1].content
        print("\n[Exito] Agente Investigador ReAct recopiló datos del mercado.")
        
        # 2. Ejecutar el Agente Validador / Analista ReAct
        print("\n[Agente 2 ReAct] Transfiriendo datos para análisis financiero y selección MVP...")
        query_val = (
            f"Por favor, valida, calcula y genera el informe enfocado en oportunidades de inversión MVP "
            f"con base en los siguientes datos crudos recopilados por el investigador:\n\n{raw_data}"
        )
        
        inputs_val = {"messages": [{"role": "user", "content": query_val}]}
        res_val = validator_agent.invoke(inputs_val)
        
        messages_val = res_val.get("messages", [])
        if not messages_val:
            print("Error: El Agente Validador no devolvió resultados.")
            return
            
        final_report = messages_val[-1].content
        
        # Escribir el informe a informe_mercado_lecheria.md en el workspace
        filename = "informe_mercado.md"
        filepath = os.path.join(r"c:\Users\armon\DEV\react-search-agent", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_report)
            
        print(f"\n[Exito] ¡El informe MVP ha sido generado y guardado en: {filename}!")
        print("\n" + "=" * 60)
        print("CONTENIDO DEL INFORME MVP GENERADO:")
        print("=" * 60)
        print(final_report)
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\nOcurrió un error inesperado durante el análisis: {str(e)}\n")

if __name__ == "__main__":
    main()
