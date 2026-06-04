import os
import re

tests_dir = "tests"
for file in os.listdir(tests_dir):
    if file.startswith("test_") and file != "test_01_auth.py" and file.endswith(".py"):
        filepath = os.path.join(tests_dir, file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Normal strings
        content = re.sub(r'client\.(get|post|put|delete|patch)\(\s*"/', r'client.\1("/api/v1/', content)
        # f-strings
        content = re.sub(r'client\.(get|post|put|delete|patch)\(\s*f"/', r'client.\1(f"/api/v1/', content)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {file}")
