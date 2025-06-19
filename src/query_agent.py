from services.schema_service import SchemaService
from services.embedding_service import EmbeddingService
from services.vector_search_service import VectorSearchService
from services.gemini_service import GeminiService
from repositories.mssql_repository import MSSQLRepository
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class QueryAgent:
    def __init__(self, schema_service: SchemaService,
                 embedding_service: EmbeddingService,
                 vector_search_service: VectorSearchService,
                 gemini_service: GeminiService,
                 sql_executor: MSSQLRepository):
        self.schema_service = schema_service
        self.embedding_service = embedding_service
        self.vector_search_service = vector_search_service
        self.gemini_service = gemini_service
        self.sql_executor = sql_executor
        logger.info("QueryAgent initialized with all required services")

    def full_query_workflow(self, user_query: str, database_name: str, execute_sql: bool = False):
        """
        Executes the full workflow from schema embedding to SQL execution.

        Args:
            user_query (str): Natural language user question
            database_name (str): Database name for schema context
            execute_sql (bool): Whether to execute the SQL query

        Returns:
            dict: {
                'sql_query': str,
                'query_result': any,
                'similar_schemas': list,
            }
        """
        try:
            # 1. Get schema text
            logger.info("Step 1: Fetching schema text...")
            schema_text = self.schema_service.get_schema_text()
            logger.info(f"Schema text retrieved successfully. Length: {len(schema_text)} characters")

            # 2. Generate schema embedding
            logger.info("Step 2: Generating schema embedding...")
            schema_embedding = self.embedding_service.generate_embedding(schema_text)
            logger.info("Schema embedding generated successfully")

            # 3. Store or update in vector DB
            logger.info("Step 3: Storing schema in vector database...")
            self.vector_search_service.add_schema_embedding(
                doc_id=database_name, 
                schema_text=schema_text, 
                embedding_vector=schema_embedding
            )
            logger.info(f"Schema stored in vector database with ID: {database_name}")

            # 4. Generate user input SQL query embedding
            logger.info("Step 4: Generating embedding for user query...")
            query_embedding = self.embedding_service.generate_embedding(user_query)
            logger.info("User query embedding generated successfully")

            # 5. Retrieve similar schemas
            logger.info("Step 5: Retrieving similar schemas...")
            similar_schemas = self.vector_search_service.search_similar_schemas(query_embedding, top_k=1)
            logger.info(f"Found {len(similar_schemas)} similar schemas")

            # 6. Build LLM prompt
            logger.info("Step 6: Building LLM prompt...")
            # For context, pick the top similar schema text or fallback to full schema_text
            if similar_schemas and similar_schemas.get('documents') and len(similar_schemas['documents']) > 0:
                context = similar_schemas['documents'][0]
                logger.info("Using top similar schema for context")
            else:
                context = schema_text
                logger.info("Using full schema text for context")

            prompt = self.gemini_service.build_prompt(schema_context=context, user_query=user_query)
            logger.info(f"LLM prompt built successfully: {prompt}")

            # 7. Generate SQL
            logger.info("Step 7: Generating SQL query...")
            sql_query = self.gemini_service.generate_sql_query(prompt)
            logger.info(f"SQL query generated: {sql_query}")

            result = {
                "sql_query": sql_query,
                "query_result": None,
                "similar_schemas": similar_schemas
            }

            if execute_sql:
                # 8. Execute SQL
                logger.info("Step 8: Executing SQL query...")
                query_result = self.sql_executor.execute_query(sql_query)
                logger.info("SQL query executed successfully")
                result["query_result"] = query_result

            return result

        except Exception as e:
            logger.error(f"Error in query workflow: {str(e)}", exc_info=True)
            raise
