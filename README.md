# React Search Agent: Multi-Agente Inmobiliario (Lechería, Venezuela)

Este repositorio contiene un sistema automatizado de inteligencia inmobiliaria basado en una **Cadena Secuencial de Multi-Agentes de Inteligencia Artificial**. El sistema realiza búsquedas en tiempo real en la web mediante **Firecrawl** para recopilar ofertas de apartamentos en venta en **Lechería, Estado Anzoátegui, Venezuela**, calcula métricas de mercado clave y genera de forma automática un **Informe de Oportunidades de Inversión MVP**.

##  Características de la Arquitectura

El proyecto ha sido rediseñado utilizando lo último en ingeniería de agentes y telemetría:

1. **Cadena Secuencial Multi-Agente (ReAct Nativo)**:
   * **Agente Investigador (`investigator_agent`)**: Implementado de forma nativa con el compilador de agentes `create_agent` de **LangChain 1.x** (basado en arquitecturas de grafos). Utiliza una herramienta personalizada de **Firecrawl** para recopilar de manera exhaustiva ofertas reales de propiedades (precios en USD, metros cuadrados, conjuntos residenciales, habitaciones y URLs).
   * **Agente Validador / Analista Financiero (`validator_agent`)**: Recibe la información del investigador, realiza una limpieza rigurosa eliminando duplicados o datos incompletos y aplica matemáticas analíticas para calcular el precio promedio del mercado y el costo por metro cuadrado de cada propiedad. Finalmente, selecciona las **propiedades MVP** ( Most Valuable Properties) de mayor oportunidad de inversión.

2. **Búsqueda Web Avanzada**:
   * Implementación de una herramienta personalizada (`web_search`) sobre el SDK `firecrawl-py` (`app.search`) que consulta portales inmobiliarios clave (como RE/MAX, Century 21 y MercadoLibre Venezuela) para recopilar datos de mercado frescos.

3. **Telemetría e Integración con LangSmith**:
   * El sistema incluye un cargador y saneador de variables de entorno robusto diseñado específicamente para Windows. Limpia los prefijos `export ` y comillas de tu archivo `.env` garantizando que **LangSmith** capture, trace e ilustre cada paso de la cadena en tiempo real en la nube.

4. **Automatización "Move-Forward"**:
   * Diseñado para ejecutarse de un solo tirón y sin fricciones humanas. Al ejecutar el comando, realiza el scraping, analiza, clasifica los MVPs y exporta directamente el reporte listo en formato Markdown a **`informe_mercado_lecheria.md`**, imprimiendo el resultado en consola.

---

##  Estructura del Proyecto

* **[main.py](file:///c:/Users/armon/DEV/react-search-agent/main.py)**: Archivo principal de ejecución que define los agentes, la herramienta de búsqueda de Firecrawl, limpia el entorno de Windows y ejecuta la secuencia del reporte de inversión.
* **[informe_mercado_lecheria.md](file:///c:/Users/armon/DEV/react-search-agent/informe_mercado_lecheria.md)**: El reporte final de inversión en Lechería generado de forma automatizada.
* **[pyproject.toml](file:///c:/Users/armon/DEV/react-search-agent/pyproject.toml)**: Gestión de dependencias modernas utilizando `uv` (incluyendo `langchainhub` para soporte de agentes).
* **[.env](file:///c:/Users/armon/DEV/react-search-agent/.env)**: Archivo de claves de API de DashScope, Firecrawl y variables de telemetría de LangSmith.

---

## 🚀 Cómo Ejecutar

Asegúrate de contar con tus llaves en tu archivo `.env` y ejecuta el comando de automatización:

```powershell
uv run python main.py
```

El script se encargará de realizar todo el flujo en segundo plano y verás el informe desplegado en tu pantalla al instante, con su respectivo archivo `.md` listo para ser consultado o compartido.
