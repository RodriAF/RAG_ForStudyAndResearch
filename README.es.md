# RAG Local para Estudio e Investigación

> **Asistente de estudio personal 100% privado y local**

Sistema de preguntas y respuestas sobre documentos PDF usando Retrieval Augmented Generation (RAG) con modelos de IA ejecutados completamente en local. Diseñado para estudiantes, investigadores y profesionales que necesitan analizar documentos de forma privada y segura.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama)
![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
---

## ¿Qué es este proyecto?

Es un agente personal disponible 24/7 que ha leído todos tus apuntes, papers, y documentos de estudio. Este proyecto convierte PDFs en una base de conocimiento conversacional donde puedes hacer preguntas específicas y obtener respuestas precisas citando las fuentes exactas del documento.

**Lo mejor:** Todo funciona en tu ordenador. Tus documentos jamás salen de tu máquina.

### Caso de Uso Principal: Estudio e Investigación

Este sistema fue diseñado específicamente para:

#### **Estudiantes**
- Sube tus apuntes de clase, libros de texto o material de estudio
- Pregunta conceptos específicos sin tener que releer todo
- Prepara exámenes haciendo preguntas sobre el contenido
- Obtén explicaciones basadas en TUS propios materiales de estudio

**Ejemplo:**
```
PDF: "Apuntes de Cálculo II - Integración"
Pregunta: "¿Cuál es el método de integración por partes y cuándo se usa?"
Respuesta: Basada en tus apuntes específicos, no en definiciones genéricas de internet
```

#### **Investigadores y Doctorandos**
- Analiza papers académicos de tu campo de investigación
- Sube documentación técnica de tu tesis o investigación
- Haz preguntas complejas sobre metodologías, resultados o conclusiones
- Compara información entre diferentes papers (próximamente)
- **100% privado:** Tu investigación no se comparte con servicios externos

**Ejemplo:**
```
PDF: "Paper sobre Redes Neuronales Convolucionales - 2024"
Pregunta: "¿Qué arquitectura de CNN proponen los autores y qué resultados obtuvieron?"
Respuesta: Extracción precisa de la metodología y resultados del paper
```

#### **Profesionales**
- Analiza manuales técnicos, normativas o especificaciones
- Consulta documentación interna de proyectos
- Extrae información de contratos, informes o procedimientos
- Mantén la confidencialidad empresarial (datos locales)

---

## Características Principales

### Privacidad Total
- **100% Local** - Ningún dato sale de tu ordenador
- **Sin APIs externas** - No se envía información a servicios cloud
- **Cero telemetría** - No hay registro de tu actividad
- **Sin cuentas** - No necesitas registrarte en ningún servicio

### Tecnología
- **RAG (Retrieval Augmented Generation)** - Respuestas basadas en evidencia
- **Embeddings semánticos** - Búsqueda inteligente de información relevante
- **Base de datos vectorial** - Recuperación eficiente de contexto
- **LLM local con Ollama** - Modelos Llama 3.2, Mistral, Phi-3, etc.

### Fácil de Usar
- **Interfaz web intuitiva** - Diseño limpio y moderno
- **Drag & drop** de PDFs
- **Respuestas con fuentes** - Ve exactamente de dónde viene cada respuesta
- **Múltiples documentos** - Gestiona varios PDFs simultáneamente

### Eficiente
- **Procesamiento rápido** - Fragmentación optimizada de documentos
- **Respuestas contextuales** - Usa solo la información relevante
- **Ajustable** - Controla cuántos fragmentos usar por consulta
- **Modelos ligeros disponibles** - Funciona incluso en laptops modestas

---
## Instalación Rápida

### Prerequisitos
- Python 3.11+
- 4GB RAM mínimo (8GB recomendado)
- 10GB espacio en disco

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/RodriAF/RAG_ForStudyAndResearch.git
cd pdf-rag-study

# 2. Ejecutar script de instalación
chmod +x setup.sh
./setup.sh

# 3. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 4. Descargar modelo
ollama pull llama3.2

# 5. Iniciar sistema
# Terminal 1: ollama serve
# Terminal 2: cd backend && source venv/bin/activate && uvicorn app.main:app --reload
# Terminal 3: cd frontend && python -m http.server 8080

# 6. Abrir navegador en http://localhost:8080
```

Ver [documentación completa de instalación](docs/INSTALL.es.md) para más detalles.

---

## Casos de Uso Detallados

### 1. Preparación de Exámenes
**Escenario:** Tienes un examen de Derecho Constitucional en 2 semanas.

**Flujo de trabajo:**
1. Subes tus apuntes de las últimas 10 clases (PDF)
2. Subes el capítulo del libro de texto (PDF)
3. Preguntas conceptos específicos: "¿Qué establece el artículo 14 sobre igualdad?"
4. El sistema te responde citando tus apuntes y el libro
5. Haces preguntas de seguimiento para profundizar

**Ventaja:** Estudias con tus materiales, no con resúmenes genéricos de internet.

### 2. Análisis de Papers Académicos
**Escenario:** Estás haciendo tu tesis doctoral sobre Machine Learning.

**Flujo de trabajo:**
1. Subes un paper de 40 páginas sobre Transformers
2. Preguntas: "¿Qué mejoras propone este paper respecto a BERT?"
3. El sistema extrae la información específica del paper
4. Preguntas: "¿Cuáles fueron los datasets usados en la evaluación?"
5. Obtienes las tablas y resultados exactos

**Ventaja:** Análisis rápido sin leer todo el paper, ideal para revisión bibliográfica.

### 3. Revisión de Normativas y Regulaciones
**Escenario:** Necesitas verificar compliance con GDPR para tu empresa.

**Flujo de trabajo:**
1. Subes la normativa GDPR completa (PDF de 100+ páginas)
2. Preguntas: "¿Qué obligaciones tengo respecto al consentimiento del usuario?"
3. El sistema te muestra los artículos relevantes
4. Preguntas: "¿Cuáles son las multas por incumplimiento?"
5. Obtienes información precisa citando los artículos exactos

**Ventaja:** Búsqueda específica en documentos largos sin leer todo.

### 4. Aprendizaje de Nuevas Tecnologías
**Escenario:** Estás aprendiendo un nuevo framework de programación.

**Flujo de trabajo:**
1. Subes la documentación oficial (PDF)
2. Preguntas: "¿Cómo se implementa autenticación JWT?"
3. El sistema te da ejemplos de la documentación
4. Preguntas: "¿Qué middleware necesito instalar?"
5. Obtienes pasos específicos del manual

**Ventaja:** Consulta interactiva de documentación técnica.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (HTML/JS)                │
│              Interfaz Web Intuitiva                 │
└────────────────────┬────────────────────────────────┘
                     │ HTTP API
                     ▼
┌─────────────────────────────────────────────────────┐
│              BACKEND (FastAPI)                      │
│  • Gestión de uploads                               │
│  • Procesamiento de PDFs                            │
│  • Orquestación de servicios                        │
└─────┬──────────┬──────────┬────────────────────────┘
      │          │          │
      ▼          ▼          ▼
┌──────────┐ ┌─────────┐ ┌──────────────┐
│ PyMuPDF  │ │Sentence │ │  ChromaDB    │
│  (PDF)   │ │Transform│ │ (Vector DB)  │
│          │ │(Embed.) │ │              │
└──────────┘ └─────────┘ └──────────────┘
                              │
                              ▼
                         ┌──────────┐
                         │  Ollama  │
                         │ (LLM     │
                         │  Local)  │
                         └──────────┘
```

### Flujo de Procesamiento

**1. Upload de PDF:**
```
PDF → PyMuPDF → Texto Extraído → Chunking (fragmentos de 1000 chars)
```

**2. Creación de Embeddings:**
```
Fragmentos → Sentence Transformers → Vectores (384 dimensiones)
```

**3. Almacenamiento:**
```
Vectores + Fragmentos → ChromaDB → Base de Datos Vectorial Local
```

**4. Consulta:**
```
Pregunta → Embedding → Búsqueda por similitud → Top 5 fragmentos relevantes
         → LLM (Ollama) + Contexto → Respuesta fundamentada
```

---

## Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Python 3.11+** - Lenguaje principal
- **PyMuPDF (fitz)** - Extracción de texto de PDFs
- **Sentence Transformers** - Generación de embeddings semánticos
- **ChromaDB** - Base de datos vectorial para búsqueda eficiente
- **Ollama** - Servidor local de LLMs

### Frontend
- **HTML5/CSS3** - Interfaz responsiva
- **JavaScript Vanilla** - Sin frameworks, máxima velocidad
- **Fetch API** - Comunicación con backend

### Modelos de IA
- **Llama 3.2** (3B) - Rápido, 2GB RAM
- **Llama 3.1** (8B) - Balance, 4.7GB RAM
- **Mistral** (7B) - Optimizado para RAG, 4.1GB RAM
- **Phi-3** (3.8B) - Eficiente, 2.3GB RAM

---

## Guía de Uso

### 1. Subir un Documento
- Haz clic en "Choose File"
- Elige tu archivo (apuntes, paper, manual, etc.)
- Espera 10-30 segundos mientras se procesa
- Se agregará a "Documents" el documento agregado

### 2. Hacer Preguntas
- Selecciona el documento de la lista
- Escribe tu pregunta en lenguaje natural
- Ajusta cuántos fragmentos usar (3-10)
- Haz clic en "Get Answer"
- Espera 5-20 segundos (depende de tu hardware)

### 3. Revisar Respuesta
- Lee la respuesta generada
- Verifica las fuentes exactas del documento en "Sources"
- Haz preguntas de seguimiento si necesitas más detalle

### 4. Gestionar Documentos
- Todos tus documentos en la barra lateral
- Selecciona uno para hacer consultas
- Elimina documentos que ya no necesites

---

## Privacidad y Seguridad

### Garantías de Privacidad

**Este sistema fue diseñado con privacidad desde el principio:**

1. **Procesamiento Local**
   - Todos los cálculos se realizan en tu ordenador
   - Los PDFs nunca se envían a servidores externos
   - Los modelos de IA corren 100% en local

2. **Sin Telemetría**
   - No hay analytics ni tracking
   - No se registra tu actividad
   - No hay cookies de terceros

3. **Sin Cuentas Externas**
   - No necesitas API keys de OpenAI, Groq, etc.
   - No hay registro de usuarios en servicios cloud
   - Tus datos no están en servidores de terceros

4. **Datos Locales**
   - Los PDFs se guardan en `data/uploads/` (tu disco)
   - Los embeddings se guardan en `data/chroma_db/` (tu disco)
   - Puedes eliminar todo en cualquier momento

### Ideal Para

- **Investigación confidencial** (tesis doctorales, papers pre-publicación)
- **Documentos empresariales** (contratos, informes internos)
- **Información sensible** (datos médicos, legales)
- **Cumplimiento normativo** (GDPR, HIPAA)
- **Educación** (sin compartir material protegido por copyright)

### Limitaciones Actuales

- **Sin autenticación** - Cualquiera con acceso al ordenador puede ver los documentos
- **Sin encriptación** - Los archivos se almacenan en texto plano (mejora futura)
- **Un solo usuario** - No hay separación de documentos por usuario (mejora v2.0)

---
## Mejoras Futuras y Roadmap

### Corto Plazo (v1.1)

#### Experiencia de Usuario
- [X] **Drag & Drop** para subir PDFs
- [ ] **Historial de conversaciones** por documento
- [ ] **Exportar respuestas** a PDF/TXT/Markdown

#### Funcionalidad
- [ ] **Resúmenes automáticos** de documentos completos
- [ ] **Preguntas sugeridas** basadas en el contenido
- [ ] **Destacado de texto** en fragmentos relevantes
- [ ] **Modo examen** (genera preguntas del documento)
- [ ] **Flashcards interactivas** generadas por IA

#### Multi-documento
- [ ] **Comparación entre documentos y busqueda transversal** ("¿En qué se diferencian estos dos papers?")
- [ ] **Etiquetas y categorías** para organizar documentos
- [ ] **Colecciones de documentos** (ej: "Matemáticas Semestre 1")

#### Formatos Adicionales
- [ ] **Soporte para DOCX, TXT, HTML** (Word)
- [ ] **OCR para PDFs escaneados**

### Largo Plazo (v2.0)

#### IA Avanzada
- [ ] **Fine-tuning de modelos** específicos por dominio
- [ ] **Resúmenes automáticos** por capítulo/sección
- [ ] **Mapas conceptuales** generados automáticamente

#### Integraciones
- [ ] **App móvil** (iOS/Android)

### Enterprise

- [ ] **Autenticación de usuarios** (JWT)
- [ ] **Roles y permisos**
- [ ] **Auditoría y logs**
- [ ] **Backup automático**
- [ ] **Deployment en Docker**

## Licencia
Este proyecto está bajo la MIT License - consulta el archivo [LICENSE](LICENSE) para más detalles.