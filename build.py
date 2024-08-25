import os

# Create project directory structure
directories = [
    'backend',
    'backend/app',
    'backend/app/pipelines',
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create necessary backend files
backend_files = {
    'backend/app/__init__.py': '',
    'backend/app/routes.py': '',
    'backend/app/pipelines/__init__.py': '',
    'backend/app/pipelines/dummy_pipelines.py': '',
    'backend/run.py': '',
}

for file_path, content in backend_files.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("Backend structure created successfully!")