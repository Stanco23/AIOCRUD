from db_methods import postgres
class CRUDFactory:
    """
    Make sure you have these envirement varables set in the .env file.\n
    ("DB_NAME"),\n
    ("DB_USER"),\n
    ("DB_PASSWORD"),\n
    ("DB_HOST"),\n
    ("DB_PORT")\n
    """
    @staticmethod
    def create_crud(database_type):
        if database_type == "postgresql":
            return postgres.PostgreSQLCRUD()
        # Add more cases for other database types
    
        raise ValueError("Unsupported database type")
