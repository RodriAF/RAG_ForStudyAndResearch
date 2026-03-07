# Local RAG for Study and Research

> **100% Private and Local Personal Study Assistant**

A Q&A system for PDF documents using Retrieval Augmented Generation (RAG) with AI models running entirely locally. Designed for students, researchers, and professionals who need to analyze documents privately and securely.

![Stack](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama)

---

## What is this project?

It is a personal agent available 24/7 that has read all your notes, papers, and study documents. This project converts PDFs into a conversational knowledge base where you can ask specific questions and get precise answers citing the exact sources from the document.

**The best part:** Everything runs on your computer. Your documents never leave your machine.

### Main Use Case: Study and Research

This system was specifically designed for:

#### **Students**

* Upload your class notes, textbooks, or study material.
* Ask about specific concepts without having to reread everything.
* Prepare for exams by asking questions about the content.
* Get explanations based on YOUR own study materials.

**Example:**

```
PDF: "Calculus II Notes - Integration"
Question: "What is the integration by parts method and when is it used?"
Answer: Based on your specific notes, not on generic internet definitions.

```

#### **Researchers and PhD Students**

* Analyze academic papers in your field of research.
* Upload technical documentation for your thesis or investigation.
* Ask complex questions about methodologies, results, or conclusions.
* Compare information between different papers (coming soon).
* **100% Private:** Your research is not shared with external services.

**Example:**

```
PDF: "Paper on Convolutional Neural Networks - 2024"
Question: "What CNN architecture do the authors propose and what results did they obtain?"
Answer: Precise extraction of the methodology and results from the paper.

```

#### **Professionals**

* Analyze technical manuals, regulations, or specifications.
* Consult internal project documentation.
* Extract information from contracts, reports, or procedures.
* Maintain corporate confidentiality (local data).

---

## Key Features

### Total Privacy

* **100% Local** - No data leaves your computer.
* **No external APIs** - No information is sent to cloud services.
* **Zero telemetry** - There is no logging of your activity.
* **No accounts** - You don't need to register for any service.

### Technology

* **RAG (Retrieval Augmented Generation)** - Evidence-based answers.
* **Semantic Embeddings** - Intelligent search for relevant information.
* **Vector Database** - Efficient context retrieval.
* **Local LLM with Ollama** - Llama 3.2, Mistral, Phi-3 models, etc.

### Easy to Use

* **Intuitive Web Interface** - Clean and modern design.
* **Drag & drop** for PDFs.
* **Answers with sources** - See exactly where each answer comes from.
* **Multiple documents** - Manage several PDFs simultaneously.

### Efficient

* **Fast processing** - Optimized document chunking.
* **Contextual answers** - Uses only relevant information.
* **Adjustable** - Control how many chunks to use per query.
* **Lightweight models available** - Works even on modest laptops.

---
## Quick Installation

### Prerequisites

* Python 3.11+
* 4GB RAM minimum (8GB recommended)
* 10GB disk space

### Steps

```bash
# 1. Clone repository
git clone https://github.com/RodriAF/RAG_ForStudyAndResearch.git
cd pdf-rag-study

# 2. Run installation script
chmod +x setup.sh
./setup.sh

# 3. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 4. Download model
ollama pull llama3.2

# 5. Start system
# Terminal 1: ollama serve
# Terminal 2: cd backend && source venv/bin/activate && uvicorn app.main:app --reload
# Terminal 3: cd frontend && python -m http.server 8080

# 6. Open browser at http://localhost:8080

```

See [full installation documentation](docs/INSTALL.md) for more details.

---
## Detailed Use Cases

### 1. Exam Preparation

**Scenario:** You have a Constitutional Law exam in 2 weeks.

**Workflow:**

1. Upload your notes from the last 10 classes (PDF).
2. Upload the textbook chapter (PDF).
3. Ask specific concepts: "What does Article 14 establish regarding equality?"
4. The system answers you by citing your notes and the book.
5. Ask follow-up questions to go deeper.

**Advantage:** You study with your materials, not with generic internet summaries.

### 2. Academic Paper Analysis

**Scenario:** You are writing your doctoral thesis on Machine Learning.

**Workflow:**

1. Upload a 40-page paper on Transformers.
2. Ask: "What improvements does this paper propose compared to BERT?"
3. The system extracts specific information from the paper.
4. Ask: "What datasets were used in the evaluation?"
5. You get the exact tables and results.

**Advantage:** Fast analysis without reading the entire paper, ideal for literature reviews.

### 3. Review of Standards and Regulations

**Scenario:** You need to verify GDPR compliance for your company.

**Workflow:**

1. Upload the full GDPR regulation (100+ page PDF).
2. Ask: "What obligations do I have regarding user consent?"
3. The system shows you the relevant articles.
4. Ask: "What are the fines for non-compliance?"
5. You get precise information citing the exact articles.

**Advantage:** Specific search in long documents without reading everything.

### 4. Learning New Technologies

**Scenario:** You are learning a new programming framework.

**Workflow:**

1. Upload the official documentation (PDF).
2. Ask: "How is JWT authentication implemented?"
3. The system gives you examples from the documentation.
4. Ask: "What middleware do I need to install?"
5. You get specific steps from the manual.

**Advantage:** Interactive consultation of technical documentation.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (HTML/JS)                │
│               Intuitive Web Interface               │
└────────────────────┬────────────────────────────────┘
                     │ HTTP API
                     ▼
┌─────────────────────────────────────────────────────┐
│                BACKEND (FastAPI)                    │
│  • Upload management                                │
│  • PDF Processing                                   │
│  • Service orchestration                            │
└─────┬──────────┬──────────┬────────────────────────┘
      │          │          │
      ▼          ▼          ▼
┌──────────┐ ┌─────────┐ ┌──────────────┐
│ PyMuPDF  │ │Sentence │ │  ChromaDB    │
│  (PDF)   │ │Transform│ │ (Vector DB)  │
│          │ │(Embed.) │ │              │
└──────────┘ └─────────┘ └──────────────┘
                              │
                              ▼
                         ┌──────────┐
                         │  Ollama  │
                         │ (Local   │
                         │  LLM)    │
                         └──────────┘

```

### Processing Flow

**1. PDF Upload:**
```
PDF → PyMuPDF → Extracted Text → Chunking (1000 char fragments)
```

**2. Embedding Creation:**
```
Chunks → Sentence Transformers → Vectors (384 dimensions)
```

**3. Storage:**
```
Vectors + Chunks → ChromaDB → Local Vector Database
```

**4. Query:**
```
Question → Embedding → Similarity Search → Top 5 relevant chunks
         → LLM (Ollama) + Context → Grounded Answer
```

---

## Tech Stack

### Backend

* **FastAPI** - Modern and fast web framework.
* **Python 3.11+** - Primary language.
* **PyMuPDF (fitz)** - Text extraction from PDFs.
* **Sentence Transformers** - Semantic embedding generation.
* **ChromaDB** - Vector database for efficient searching.
* **Ollama** - Local LLM server.

### Frontend

* **HTML5/CSS3** - Responsive interface.
* **Vanilla JavaScript** - No frameworks, maximum speed.
* **Fetch API** - Communication with backend.

### AI Models

* **Llama 3.2** (3B) - Fast, 2GB RAM.
* **Llama 3.1** (8B) - Balanced, 4.7GB RAM.
* **Mistral** (7B) - Optimized for RAG, 4.1GB RAM.
* **Phi-3** (3.8B) - Efficient, 2.3GB RAM.

---

## Usage Guide

### 1. Upload a Document

* Click on "Choose File".
* Select your file (notes, paper, manual, etc.).
* Wait 10-30 seconds while it processes.
* The added document will appear in "Documents".

### 2. Ask Questions

* Select the document from the list.
* Write your question in natural language.
* Adjust how many chunks to use (3-10).
* Click on "Get Answer".
* Wait 5-20 seconds (depends on your hardware).

### 3. Review Answer

* Read the generated response.
* Verify the exact sources of the document in "Sources".
* Ask follow-up questions if you need more detail.

### 4. Manage Documents

* All your documents are in the sidebar.
* Select one to perform queries.
* Delete documents you no longer need.

---

## Privacy and Security

### Privacy Guarantees

**This system was designed with privacy from the start:**

1. **Local Processing**
 - All calculations are performed on your computer.
 - PDFs are never sent to external servers.
 - AI models run 100% locally.


2. **No Telemetry**
 - No analytics or tracking.
 - Your activity is not logged.
 - No third-party cookies.


3. **No External Accounts**
 - You don't need API keys from OpenAI, Groq, etc.
 - No user registration in cloud services.
 - Your data is not on third-party servers.


4. **Local Data**
 - PDFs are saved in `data/uploads/` (your disk).
 - Embeddings are saved in `data/chroma_db/` (your disk).
 - You can delete everything at any time.


### Ideal For

* **Confidential research** (doctoral theses, pre-publication papers).
* **Business documents** (contracts, internal reports).
* **Sensitive information** (medical, legal data).
* **Regulatory compliance** (GDPR, HIPAA).
* **Education** (without sharing copyright-protected material).

### Current Limitations

* **No authentication** - Anyone with access to the computer can see the documents.
* **No encryption** - Files are stored in plain text (future improvement).
* **Single user** - No separation of documents per user (v2.0 improvement).

---

## Future Improvements and Roadmap

### Short Term (v1.1)

#### User Experience
- [ ] **Drag & Drop** for PDF uploads
- [ ] **Conversation history** per document
- [ ] **Export answers** to PDF/TXT/Markdown

#### Functionality
- [ ] **Automatic summaries** of complete documents
- [ ] **Suggested questions** based on content
- [ ] **Text highlighting** in relevant fragments
- [ ] **Configurable token limits** per response
- [ ] **Exam mode** (generates questions from document)
- [ ] **AI-generated interactive flashcards**

#### Multi-document
- [ ] **Document comparison and Cross-document search** ("How do these two papers differ?")
- [ ] **Tags and categories** to organize documents
- [ ] **Document collections** (e.g., "Math Semester 1")

#### Additional Formats
- [ ] **DOCX, TXT, HTML support** (Word)
- [ ] **OCR for scanned PDFs**

### Long Term (v2.0)

#### Advanced AI
- [ ] **Model fine-tuning** specific to domains
- [ ] **Automatic summaries** by chapter/section
- [ ] **Auto-generated concept maps**

#### Integrations
- [ ] **Mobile app** (iOS/Android)

### Enterprise
- [ ] **User authentication** (JWT)
- [ ] **Roles and permissions**
- [ ] **Audit and logs**
- [ ] **Automatic backup**
- [ ] **Docker deployment**

---