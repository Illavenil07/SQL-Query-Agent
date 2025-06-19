# SQL Query Agent

A natural language to SQL query agent that uses LLMs to generate and execute SQL queries based on natural language input.

## Features

- Natural language to SQL query conversion
- MS SQL Server database integration
- Vector store for schema embeddings
- Streamlit web interface
- Query logging and history
- Schema caching

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sql-query-agent
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
# Database Configuration
DB_SERVER=your_server
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Open your browser and navigate to the provided URL (usually http://localhost:8501)

3. Enter your natural language query in the text area and click "Generate Query"

4. View the generated SQL query and results

## Project Structure

```
llm_sql_query_agent/
├── .env                    # API keys & DB credentials
├── requirements.txt        # Project dependencies
├── README.md              # Project overview and setup instructions
│
├── data/
│   └── schema_cache.json   # Optional: schema snapshot
│
├── src/
│   ├── config.py          # Configuration loader
│   ├── db_connector.py    # MS SQL connection + schema extraction
│   ├── embedder.py        # Embedding generation
│   ├── query_agent.py     # LLM prompt construction and API calls
│   ├── vector_store.py    # Chroma DB setup and retrieval
│   └── app.py             # Streamlit frontend
│
└── logs/
    └── query_logs.txt     # Query history
```
