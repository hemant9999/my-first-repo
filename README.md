# Policy RAG Assistant

End-to-end local RAG project for policy PDFs using LangChain, Google Cloud Vertex AI Gemini, Vertex AI embeddings, and a persistent local Chroma database.

## What This Includes

- PDF ingestion pipeline with metadata enrichment and deterministic chunk IDs
- Local persistent Chroma vector store
- Gemini chatbot through Vertex AI
- FastAPI service for chat and ingestion
- CLI ingestion and chat tools
- Retrieval and answer validation pipeline
- Golden-question evaluation dataset scaffold

## Project Structure

```text
app/
  api/             FastAPI app and routes
  chatbot/         Gemini RAG prompt and answer chain
  core/            config, schemas, logging
  ingestion/       PDF loading, cleaning, chunking, embedding, indexing
  retrieval/       Chroma retriever and citation formatting
  validation/      golden dataset loading, retrieval eval, answer eval
data/
  raw_pdfs/        put policy PDFs here
  chroma/          local persistent Chroma DB
  eval/            golden questions and reports
scripts/
  ingest.py        CLI ingestion
  chat_cli.py      terminal chatbot
  validate.py      RAG validation
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ui]"
cp .env.example .env
```

Set these in `.env`:

```env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json
```

Your Google Cloud identity must have Vertex AI access.

## Ingest Policy PDFs

Put PDFs in `data/raw_pdfs/`, then run:

```bash
python scripts/ingest.py
```

Or ingest a specific file/directory:

```bash
python scripts/ingest.py /path/to/policies
python scripts/ingest.py /path/to/policy.pdf
```

Ingestion replaces existing chunks for the same source path, so reruns are safe.

## Chat Locally

```bash
python scripts/chat_cli.py
```

## Streamlit Chat UI

```bash
streamlit run app/ui/streamlit_app.py
```

## Run API

```bash
uvicorn app.api.main:app --reload
```

Useful endpoints:

```text
GET  /health
POST /ingest
POST /chat
```

Example chat request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the policy say about sick leave?"}'
```

## Validate Retrieval

The default validation dataset is tailored to `Pearl Stay_Guest Guide.pdf`:

```bash
python scripts/validate.py --mode retrieval
python scripts/validate.py --mode answer
python scripts/validate.py --mode all
```

Retrieval validation reports both `source_recall_at_k` and `page_recall_at_k`, so it checks
whether the right PDF and the right page were retrieved.

To create another evaluation set, copy `data/eval/pearl_stay_guest_guide.yaml` and edit cases:

```yaml
- id: pearl_smoking_fine
  question: "Is smoking allowed inside Pearl Stay, and what fine applies if this rule is broken?"
  expected_answer_contains:
    - "not allowed"
    - "10,000"
  expected_sources:
    - file: "Pearl Stay_Guest Guide.pdf"
      pages: [4, 5]
```

Use a custom dataset with:

```bash
python scripts/validate.py data/eval/my_questions.yaml --mode retrieval
```

Reports are written to `data/eval/reports/`.

## Notes

- Default generation model: `gemini-2.5-flash`
- Default embedding model: `text-embedding-005`
- Default retriever: MMR with `top_k=6`
- The assistant is prompted to answer only from retrieved policy context and cite source pages.
