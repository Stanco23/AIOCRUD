import psycopg2
from psycopg2 import extensions
from dotenv import load_dotenv
import os
load_dotenv()

class PostgreSQLCRUD:
    """
    This is a class called "PostgreSQLCRUD" which provides methods for performing CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database.  
 
    The class has an "__init__" method that establishes a connection to the database using the provided environment variables for the database name, user, password, host, and port.  

    The "create" method allows inserting data into a specified table in the database. It takes the table name and a variable number of data tuples as arguments. The method constructs an SQL query string using the table name and data tuples, and then executes the query using a cursor.  

    The "read" method reads data from a specified table in the database. It takes the table name and an optional condition as arguments. The method constructs an SQL query string using the table name and condition, if provided, and then executes the query using a cursor. The method returns the fetched result. 

    The "update" method updates rows in a specified table in the database. It takes the table name, set values, and a condition as arguments. The method constructs an SQL query string using the table name, set values, and condition, and then executes the query using a cursor. The method commits the changes to the database. 

    The "delete" method deletes rows from a specified table in the database based on a given condition. It takes the table name and a condition as arguments. The method constructs an SQL query string using the table name and condition, and then executes the query using a cursor. The method commits the changes to the database. 

    The "close" method is used to close the database connection established by the object. It simply calls the "close" method on the connection object. 

    Overall, this class provides a convenient way to perform CRUD operations on a PostgreSQL database using Python and the psycopg2 library.
    """
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        #self.connection.set_session(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    
    def create(self, table, *data):
        """
        This is a brief description of what the method does.

        Args:
            table (string): Input a name of the table in this argument.
            *data (tuple): Here you should have a tuple of data that you want to insert.

        Returns:
            return_type: Description of the return value.

        Examples:
            employees_data = [\n
            (\n"John", "Doe", "john@example.com", "555-1234", "123 Main St", "CityA", "StateA", "12345", random.uniform(30000, 80000)\n),\n
            (\n"Jane", "Smith", "jane@example.com", "555-5678", "456 Elm St", "CityB", "StateB", "56789", random.uniform(30000, 80000)\n),\n
            
            ]\n

            for employee_data in employees_data:\n
                crud.create("employees", \n
                            ("first_name", employee_data[0]),\n
                            ("last_name", employee_data[1]),\n
                            ("email", employee_data[2]),\n
                            ("phone", employee_data[3]),\n
                            ("address", employee_data[4]),\n
                            ("city", employee_data[5]),\n
                            ("state", employee_data[6]),\n
                            ("postal_code", employee_data[7]),\n
                            ("salary", employee_data[8]))\n
        """
        columns = ", ".join([pair[0] for pair in data])
        placeholders = ", ".join(["%s" for _ in data])
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        values = [pair[1] for pair in data]
        
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)

    def read(self, table, condition=None):
        """
        This is a method that reads data from a specified table in a database. It takes two parameters: "table" which represents the name of the table to read from, and "condition" which is an optional parameter representing a condition to filter the data. 
        The method starts by constructing a SQL query string using f-string formatting. If a condition is provided, it is appended to the query using a WHERE clause.   
        """
        query = f"SELECT * FROM {table}"
        if condition!=None:
            query += f" WHERE {condition}"
        
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    
    def update(self, table, set_values, condition):
        """
        This function updates a row in a specified table in a database. It takes three parameters: "table" (the name of the table), "set_values" (the values to be updated), and "condition" (the condition that determines which row(s) to update).  
 
        The function generates an SQL query string by combining the input parameters. It then uses a cursor to execute the query and update the row(s) in the database. Finally, it commits the changes to the database. 
        """
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
        self.connection.commit()
    
    def delete(self, table, condition):
        """
        This function deletes rows from a specified table in a database based on a given condition. It takes two parameters: "table" represents the name of the table from which rows are to be deleted, and "condition" represents the condition that determines which rows should be deleted. 
 
        The function generates a SQL DELETE query using the provided table and condition. It then establishes a connection to the database and executes the query using a cursor. Finally, it commits the changes made to the database. 
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
        self.connection.commit()
    
    def close(self):
        """
        This method is used to close the connection established by the object. The "self" parameter refers to the current instance of the class that this method belongs to. By calling the "close" method, the connection is terminated and any resources associated with it are released. This is an important step to ensure that connections are properly closed and not left open, which can lead to resource leaks and potential security vulnerabilities.
        """
        self.connection.close()

# Example usage
