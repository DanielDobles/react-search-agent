# React Search Agent: Multi-Agente Inmobiliario con LCEL (Lechería, Venezuela)

Este repositorio contiene un sistema automatizado de inteligencia inmobiliaria basado en una **Cadena de Multi-Agentes de Inteligencia Artificial** encadenados de forma elegante mediante **LCEL (LangChain Expression Language)**. El sistema realiza búsquedas en tiempo real mediante **Firecrawl** para recopilar ofertas de apartamentos en venta en **Lechería, Estado Anzoátegui, Venezuela**, calcula métricas de mercado clave y genera de forma automática un **Informe de Oportunidades de Inversión MVP**.

## 🏗️ Arquitectura del Sistema

El proyecto implementa una de las arquitecturas más modernas y recomendadas de LangChain:

1. **Cadena Multi-Agente con LCEL (LangChain Expression Language)**:
   Los agentes y transformaciones de datos se encadenan de forma puramente declarativa utilizando la clase **`RunnableLambda`** y el operador de tuberías **`|`**:
   ```python
   lcel_multiagent_chain = (
       run_investigator 
       | extract_raw_data 
       | format_validator_input 
       | run_validator 
       | extract_final_report
   )
   ```
   * **Agente Investigador (`investigator_agent`)**: Implementado nativamente con el compilador de agentes `create_agent` de **LangChain 1.x**. Utiliza la herramienta de **Firecrawl** para extraer listados reales (precios en USD, metros cuadrados, habitaciones y ubicaciones).
   * **Agente Validador / Analista Financiero (`validator_agent`)**: Valida los datos crudos recolectados por el Investigador, calcula promedios y el valor por metro cuadrado individual de cada inmueble. Finalmente, destaca las propiedades **MVP (Most Valuable Properties)** de mayor beneficio costo-metraje.

2. **Búsqueda Web Avanzada**:
   * Implementación de una herramienta personalizada (`web_search`) sobre el SDK `firecrawl-py` (`app.search`) que consulta portales inmobiliarios clave (como RE/MAX, Century 21 y MercadoLibre Venezuela) para recopilar datos de mercado frescos.

3. **Telemetría e Integración con LangSmith**:
   * El sistema incluye un cargador y saneador de variables de entorno robusto diseñado específicamente para Windows. Limpia los prefijos `export ` y comillas de tu archivo `.env` garantizando que **LangSmith** capture, trace e ilustre cada paso de la cadena en tiempo real en la nube.

4. **Automatización "Move-Forward"**:
   * Diseñado para ejecutarse de un solo tirón y sin fricciones humanas. Al ejecutar el comando, realiza el scraping, analiza, clasifica los MVPs y exporta directamente el reporte listo en formato Markdown a **`informe_mercado_lecheria.md`**, imprimiendo el resultado en consola.

---

## 📁 Estructura del Proyecto

* **[main.py](file:///c:/Users/armon/DEV/react-search-agent/main.py)**: Archivo principal de ejecución que define los agentes, la herramienta de búsqueda de Firecrawl, limpia el entorno de Windows y ejecuta la secuencia del reporte de inversión.
* **[informe_mercado_lecheria.md](file:///c:/Users/armon/DEV/react-search-agent/informe_mercado_lecheria.md)**: El reporte final de inversión en Lechería generado de forma automatizada.
* **[pyproject.toml](file:///c:/Users/armon/DEV/react-search-agent/pyproject.toml)**: Gestión de dependencias modernas utilizando `uv`.
* **[requirements.txt](file:///c:/Users/armon/DEV/react-search-agent/requirements.txt)**: Lista de paquetes requeridos del proyecto para instalaciones clásicas.
* **[.env](file:///c:/Users/armon/DEV/react-search-agent/.env)**: Archivo de claves de API de DashScope, Firecrawl y variables de telemetría de LangSmith.

---

## 🚀 Cómo Ejecutar e Instalar

Asegúrate de contar con tus llaves en tu archivo `.env`.

### 1. Instalación de paquetes
Sincroniza y descarga todas las dependencias de forma automatizada con UV ejecutando:
```powershell
uv sync
```
*(O de forma clásica con `uv pip install -r requirements.txt`)*

### 2. Ejecutar la cadena LCEL
Para iniciar el flujo y generar tu reporte, simplemente ejecuta:
```powershell
uv run python main.py
```

El script se encargará de realizar todo el flujo de agentes en segundo plano y verás el informe desplegado en tu pantalla al instante, con su respectivo archivo `.md` listo para ser consultado.
