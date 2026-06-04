import os
import re

tests_dir = "tests"
for file in os.listdir(tests_dir):
    if file.startswith("test_") and file != "test_01_auth.py" and file.endswith(".py"):
        filepath = os.path.join(tests_dir, file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace multiple /api/v1/ with a single /api/v1/
        content = re.sub(r'(/api/v1)+/', '/api/v1/', content)
        
        # In case some URLs were raw like client.get("/buses"), ensure they have /api/v1
        # First strip all /api/v1
        content = content.replace('"/api/v1/', '"/')
        content = content.replace('f"/api/v1/', 'f"/')
        
        # Then add /api/v1/
        content = re.sub(r'client\.(get|post|put|delete|patch)\(\s*"/', r'client.\1("/api/v1/', content)
        content = re.sub(r'client\.(get|post|put|delete|patch)\(\s*f"/', r'client.\1(f"/api/v1/', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Normalized {file}")
