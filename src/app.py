import streamlit as st
from query_agent import QueryAgent
from services.schema_service import SchemaService
from services.embedding_service import EmbeddingService
from services.vector_search_service import VectorSearchService
from services.gemini_service import GeminiService
from repositories.mssql_repository import MSSQLRepository
from repositories.chroma_repository import ChromaRepository
from config import Config

# Initialize repositories
mssql_repo = MSSQLRepository()
chroma_repo = ChromaRepository()

# Initialize services with their dependencies
schema_service = SchemaService(db_repository=mssql_repo)
embedding_service = EmbeddingService()
vector_search_service = VectorSearchService(chroma_repo=chroma_repo)
gemini_service = GeminiService()
sql_executor = mssql_repo

# Initialize Facade Service
query_agent = QueryAgent(
    schema_service,
    embedding_service,
    vector_search_service,
    gemini_service,
    sql_executor
)

# Streamlit App UI
st.title("🦾 Natural Language to SQL Agent")

st.markdown("Convert natural language queries to executable MS SQL queries via Gemini LLM")

# User Inputs
user_query = st.text_input("🔍 Enter your Text so that I can generate a SQL query for you:")
database_name = st.text_input("💾 Enter database name:")

# Initialize session state variables
if "sql_query" not in st.session_state:
    st.session_state["sql_query"] = None
if "query_result" not in st.session_state:
    st.session_state["query_result"] = None
if "similar_schemas" not in st.session_state:
    st.session_state["similar_schemas"] = None

if st.button("📝 Generate SQL (Review Before Execution)"):
    if not user_query or not database_name:
        st.error("Please provide both the query and database name.")
    else:
        with st.spinner("Generating SQL..."):
            try:
                result = query_agent.full_query_workflow(user_query, database_name, execute_sql=False)
                st.session_state["sql_query"] = result["sql_query"]
                st.session_state["similar_schemas"] = result["similar_schemas"]
                st.session_state["query_result"] = None  # Reset previous result
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if st.session_state["sql_query"]:
    st.subheader("📝 Generated SQL Query")
    st.code(st.session_state["sql_query"], language="sql")

    if st.button("🚀 Execute SQL Query"):
        with st.spinner("Executing SQL..."):
            try:
                result = query_agent.full_query_workflow(user_query, database_name, execute_sql=True)
                st.session_state["query_result"] = result["query_result"]
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if st.session_state["query_result"] is not None:
    st.subheader("📊 Query Results")
    st.write(st.session_state["query_result"])

# Optional: Footer
st.markdown("---")
st.caption("Built with Python, Streamlit, Chroma, and Gemini API")
