from app.core.database import execute_query
import json

def check_schema():
    tables = ['drivers', 'students', 'buses']
    schema_info = {}
    
    for table in tables:
        try:
            # For MySQL
            results = execute_query(f"SHOW COLUMNS FROM {table}", fetch_all=True)
            schema_info[table] = [row['Field'] for row in results]
        except Exception as e:
            schema_info[table] = f"Error: {str(e)}"
            
    print(json.dumps(schema_info, indent=2))

if __name__ == "__main__":
    check_schema()
