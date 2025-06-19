"""Repository for MS SQL database interactions."""
import pyodbc
from config import Config

class MSSQLRepository:
    """
    Handles connection and queries to the MS SQL database using Windows Authentication.
    """

    def __init__(self):
        """
        Initializes the database connection and cursor using Windows Authentication.
        """
        try:
            # Create connection string with Windows Authentication
            conn_str = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={Config.DB_SERVER};'
                f'DATABASE={Config.DB_DATABASE};'
                f'Trusted_Connection=yes;'
            )
            
            self.connection = pyodbc.connect(conn_str)
            self.cursor = self.connection.cursor()
        except pyodbc.Error as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def fetch_schema_details(self):
        """
        Fetches table names and column details from the MS SQL database.

        Returns:
            schema_info (str): Formatted text containing tables and their columns.
        """
        try:
            tables = self._get_table_names()
            schema_info = ""

            for table in tables:
                columns = self._get_columns_for_table(table)
                column_list = ", ".join(columns)
                schema_info += f"Table: {table} | Columns: {column_list}\n"

            return schema_info
        except pyodbc.Error as e:
            raise Exception(f"Failed to fetch schema details: {str(e)}")

    def execute_query(self, sql_query):
        """
        Executes a given SQL query and fetches results.

        Args:
            sql_query (str): SQL query string to execute.

        Returns:
            tuple: (columns, results) where columns is a list of column names
                  and results is a list of result rows.
        """
        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return columns, result
        except pyodbc.Error as e:
            raise Exception(f"Database query failed: {str(e)}")

    def _get_table_names(self):
        """
        Retrieves all table names in the connected database.

        Returns:
            List of table names.
        """
        try:
            self.cursor.execute(
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            )
            tables = [row[0] for row in self.cursor.fetchall()]
            return tables
        except pyodbc.Error as e:
            raise Exception(f"Failed to get table names: {str(e)}")

    def _get_columns_for_table(self, table_name):
        """
        Retrieves all column names for a given table.

        Args:
            table_name (str): Name of the table.

        Returns:
            List of column names.
        """
        try:
            self.cursor.execute(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
            )
            columns = [row[0] for row in self.cursor.fetchall()]
            return columns
        except pyodbc.Error as e:
            raise Exception(f"Failed to get columns for table {table_name}: {str(e)}")

    def close_connection(self):
        """
        Closes the database connection.
        """
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except pyodbc.Error as e:
            raise Exception(f"Failed to close database connection: {str(e)}")
