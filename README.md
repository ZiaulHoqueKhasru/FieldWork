# 📰 AI-Based News Summarizer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

A complete end-to-end news aggregation and summarization system. This project scrapes live news data, stores it in a MySQL database, and uses a fine-tuned Large Language Model (LLM) via the Groq API to generate concise summaries, all exposed through a high-performance RESTful API.

### 🛠️ Tech Stack
* **Backend:** FastAPI, Python, SQLAlchemy
* **AI & ML:** LLM Fine-tuning, Groq API, Transformer Models
* **Database:** MySQL
* **DevOps:** Docker, Containerization
* **Data Collection:** Web Scraping

---

## 🎥 Project Demo

Watch the full system in action, including the API usage and database integration:

https://github.com/user-attachments/assets/c694f690-9c1f-4b8d-bf49-ea5fefdfabaf

---

## 🐳 Run with Docker (Recommended)

You can run the pre-built image directly from Docker Hub without installing Python dependencies manually.

```bash
docker run -p 8000:8000 \
  -e GROQ_API_KEY="your_actual_api_key_here" \
  -e DB_HOST="host.docker.internal" \
  ziaulhoquekhasru/news-app:v1