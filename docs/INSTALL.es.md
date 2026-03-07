# Instalación

### Prerequisitos

- **Python 3.11+**
- **4GB RAM mínimo** (8GB recomendado)
- **10GB espacio en disco** (para los modelos)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/RodriAF/RAG_ForStudyAndResearch.git
cd pdf-rag-app
```

### Paso 2: Instalar Ollama

Ollama es necesario para ejecutar los modelos de IA en local.

#### En Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### En macOS:
```bash
# Opción 1: Descargar desde
open https://ollama.com/download/mac

# Opción 2: Con Homebrew
brew install ollama
```

#### En Windows:
```bash
# Descargar e instalar desde
start https://ollama.com/download/windows
```

**Verificar instalación:**
```bash
ollama --version
```

### Paso 3: Descargar un modelo de IA

Elige uno según tu hardware:

```bash
# Recomendado para empezar (2GB - Rápido)
ollama pull llama3.2

# Más potente pero más lento (4.7GB)
ollama pull llama3.1

# Alternativa optimizada para RAG (4.1GB)
ollama pull mistral

# Muy ligero y eficiente (2.3GB)
ollama pull phi3
```

**Verificar que se descargó:**
```bash
ollama list
```

### Paso 4: Crear estructura del proyecto

```bash
# Crear archivos __init__.py necesarios
touch backend/app/__init__.py
touch backend/app/services/__init__.py

# En Windows, usa estos comandos:
# type nul > backend\app\__init__.py
# type nul > backend\app\services\__init__.py

# Crear directorios de datos
mkdir -p data/uploads data/chroma_db

# En Windows:
# mkdir data\uploads
# mkdir data\chroma_db
```

### Paso 5: Configurar entorno virtual

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 6: Instalar dependencias de Python

```bash
# Asegúrate de estar en backend/ con venv activado
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: La primera vez descargará el modelo de embeddings (~90MB). Esto es normal.

### Paso 7: Configurar variables de entorno

Crea el archivo `backend/.env`:

```bash
# Crear archivo .env
touch backend/.env  # En Windows: type nul > backend\.env
```

Edita `backend/.env` y añade:

```env
# Ollama Configuration (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Embeddings Model (Local)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# PDF Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Storage Paths
CHROMA_DB_PATH=./data/chroma_db
UPLOAD_DIR=./data/uploads
```

---

## Ejecución

### Opción A: Ejecución Manual (3 terminales)

#### Terminal 1: Iniciar Ollama

```bash
ollama serve
```

**Nota**: En Mac/Windows, Ollama suele ejecutarse automáticamente como servicio. Si ya está corriendo, este paso no es necesario.

#### Terminal 2: Iniciar Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Terminal 3: Iniciar Frontend

```bash
cd frontend
python -m http.server 8080
```

Luego abre tu navegador en: **http://localhost:8080**

### Opción B: Abrir Frontend directamente

Si prefieres no usar servidor HTTP:

1. Ve a la carpeta `frontend/`
2. Doble clic en `index.html`
3. Se abrirá en tu navegador predeterminado

---

##  Verificación

### 1. Verificar que Ollama está corriendo

Abre en tu navegador:
```
http://localhost:11434
```

Deberías ver: `Ollama is running`

### 2. Verificar el Backend

Abre en tu navegador:
```
http://localhost:8000/health
```

Deberías ver:
```json
{
  "api": "✅ OK",
  "ollama": "✅ Conectado",
  "model": "llama3.2",
  "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
  "vector_db": "ChromaDB"
}
```

### 3. Probar la aplicación

1. **Abre el frontend** en `http://localhost:8080` o abriendo `index.html`
2. **Sube un PDF** usando el botón "Selecciona un PDF"
3. **Espera** a que se procese (verás "✅ PDF procesado: X fragmentos")
4. **Haz una pregunta** en el área de texto
5. **Obtén respuesta** generada por IA local

---

## Uso

### Subir un documento

1. Haz clic en **"Choose File"**
2. Elige tu archivo PDF
3. Haz clic en **"Process PDF"**
4. Espera a que se procese (puede tardar 10-30 segundos dependiendo del tamaño)

### Hacer preguntas

1. Selecciona un documento de la lista
2. Escribe tu pregunta en el área de texto
3. (Opcional) Ajusta el número de fragmentos a usar (1-10)
4. Haz clic en **"Get Answer"**
5. Espera la respuesta (puede tardar 5-20 segundos dependiendo de tu hardware)

### Ver fragmentos relevantes

Después de obtener una respuesta, puedes expandir la sección "📄 Ver fragmentos relevantes" para ver qué partes del documento utilizó la IA para generar la respuesta.

---

## Solución de Problemas

### Error: "Ollama no está corriendo"

**Solución:**
```bash
# Verificar estado
ollama list

# Iniciar Ollama
ollama serve
```

### Error: "Model not found: llama3.2"

**Solución:**
```bash
ollama pull llama3.2
```

### Error: "No module named 'app'"

**Solución:**
```bash
# Asegúrate de tener los archivos __init__.py
touch backend/app/__init__.py
touch backend/app/services/__init__.py
```

### Error: "CORS policy blocked"

**Solución:**
- Verifica que el backend esté corriendo
- Asegúrate de que en `backend/app/main.py` existe la configuración CORS
- Intenta acceder al frontend desde `http://localhost:8080` en lugar de `file://`

### El procesamiento es muy lento

**Soluciones:**
- Usa un modelo más ligero: `ollama pull llama3.2` o `phi3`
- Reduce el número de fragmentos en las consultas (usa 3 en lugar de 5)
- Cierra otras aplicaciones para liberar RAM
- Reduce `CHUNK_SIZE` en `.env` a `500`

### Error de memoria / RAM insuficiente

**Soluciones:**
- Usa el modelo más ligero: `phi3` (2.3GB)
- Cierra otras aplicaciones
- Reduce `n_results` a 3 en las consultas
- Si tienes menos de 4GB RAM, considera usar Groq API (gratis) en lugar de local

---

## 📁 Estructura del Proyecto

```
pdf-rag-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # API endpoints
│   │   ├── config.py            # Configuración
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── pdf_processor.py # Extracción de texto
│   │       ├── embeddings.py    # Generación de embeddings
│   │       ├── vector_store.py  # ChromaDB
│   │       └── ollama_service.py # Integración con Ollama
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── index.html               # Interfaz web
├── data/
│   ├── uploads/                 # PDFs subidos
│   └── chroma_db/              # Base de datos vectorial
└── README.md
```

---

## ⚙️ Configuración Avanzada

### Cambiar el modelo de IA

1. **Descargar nuevo modelo:**
```bash
ollama pull mistral  # o llama3.1, phi3, etc.
```

2. **Actualizar `.env`:**
```env
OLLAMA_MODEL=mistral
```

3. **Reiniciar backend**

### Ajustar tamaño de chunks

En `.env`, modifica:
```env
CHUNK_SIZE=500        # Más pequeño = más precisión, más lento
CHUNK_OVERLAP=100     # Overlap entre chunks
```

### Cambiar modelo de embeddings

En `.env`:
```env
# Más pequeño (más rápido)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Mejor calidad (más lento)
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

---

## Requisitos de Hardware

| Modelo | RAM Mínima | RAM Recomendada | Velocidad |
|--------|------------|-----------------|-----------|
| phi3 | 3GB | 4GB | ⚡⚡⚡⚡⚡ |
| llama3.2 | 4GB | 6GB | ⚡⚡⚡⚡ |
| mistral | 6GB | 8GB | ⚡⚡⚡ |
| llama3.1 | 8GB | 12GB | ⚡⚡ |

---

