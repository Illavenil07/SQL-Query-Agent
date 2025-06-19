"""Service for managing database schema operations."""

from repositories.mssql_repository import MSSQLRepository


class SchemaService:
    """
    Service layer for extracting and formatting database schema details.
    """

    def __init__(self, db_repository: MSSQLRepository):
        """
        Initializes the SchemaService with a database repository.

        Args:
            db_repository (MSSQLRepository): Database repository instance.
        """
        self.db_repository = db_repository

    def get_schema_text(self):
        """
        Retrieves and formats the full schema details from the database.

        Returns:
            str: Formatted text containing table names and their columns.
        """
        try:
            schema_text = self.db_repository.fetch_schema_details()
            return schema_text
        except Exception as e:
            raise Exception(f"Failed to fetch schema details: {str(e)}")

    def close_connection(self):
        """
        Closes the database connection via repository.
        """
        self.db_repository.close_connection()
