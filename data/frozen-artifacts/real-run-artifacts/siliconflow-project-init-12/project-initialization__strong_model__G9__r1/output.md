I'll create a no-overwrite academic research project scaffold based on the task requirements. Let me start by examining the existing workspace structure.

```python
# First, let's examine the current directory structure to understand what exists
import os
from pathlib import Path

def list_directory_contents(path="."):
    """List all files and directories in the given path."""
    contents = []
    for root, dirs, files in os.walk(path):
        # Skip .git directory contents
        if '.git' in root:
            continue
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        contents.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            contents.append(f"{subindent}{file}")
    return contents

current_contents = list_directory_contents()
print("Current directory structure:")
for item in current_contents:
    print(item)
```

```python
# Check for specific files mentioned in the evidence bundle
existing_files = []
important_files = ["AGENTS.md", ".agents/installed-packs.json", ".git/"]

for file_path in important_files:
    if os.path.exists(file_path):
        existing_files.append(file_path)
        print(f"✓ Found: {file_path}")
    else:
        print(f"✗ Missing: {file_path}")

print(f"\nTotal existing important files: {len(existing_files)}")
```

```python
# Now, let's create the academic research project scaffold
# Based on evidence: "The project profile is academic research." (fixture-pi-e02)
# And constraint: "Use research workflow directories."

research_directories = [
    "data/raw",
    "data/processed",
    "data/external",
    "notebooks/exploratory",
    "notebooks/analysis",
    "src/data",
    "src/features",
    "src/models",
    "src/visualization",
    "reports/figures",
    "reports/tables",
    "paper/sections",
    "paper/figures",
    "paper/tables",
    "literature",
    "experiments/configs",
    "experiments/results",
    "docs"
]

research_files = [
    "README.md",
    "requirements.txt",
    "environment.yml",
    "setup.py",
    "src/__init__.py",
    "notebooks/README.md",
    "data/README.md",
    ".gitignore",
    "paper/README.md",
    "literature/README.md",
    "experiments/README.md"
]

# Create directories first
created_dirs = []
for directory in research_directories:
    try:
        os.makedirs(directory, exist_ok=True)
        created_dirs.append(directory)
        print(f"Created directory: {directory}")
    except Exception as e:
        print(f"Error creating {directory}: {e}")

print(f"\nCreated {len(created_dirs)} directories")
```

```python
# Create files only if they don't exist (no-overwrite)
created_files = []
skipped_files = []

for file_path in research_files:
    if os.path.exists(file_path):
        skipped_files.append(file_path)
        print(f"Skipped (exists): {file_path}")
    else:
        try:
            # Create file with appropriate content based on file type
            if file_path == "README.md":
                content = """# Academic Research Project

## Project Overview
Brief description of the research project.

## Repository Structure
```
project/
├── data/           # Data storage
│   ├── raw/        # Raw, immutable data
│   ├── processed/  # Cleaned data
│   └── external/   # External data sources
├── notebooks/      # Jupyter notebooks
│   ├── exploratory/ # Exploratory data analysis
│   └── analysis/   # Analysis notebooks
├── src/           # Source code
│   ├── data/      # Data processing scripts
│   ├── features/  # Feature engineering
│   ├── models/    # Modeling code
│   └── visualization/ # Visualization code
├── paper/         # Manuscript
│   ├── sections/  # Paper sections
│   ├── figures/   # Paper figures
│   └── tables/    # Paper tables
├── literature/    # Literature review materials
├── experiments/   # Experimental configurations and results
├── reports/       # Generated reports
└── docs/          # Documentation
```

## Getting Started
1. Set up environment: `conda env create -f environment.yml`
2. Install dependencies: `pip install -r requirements.txt`
3. Run exploratory analysis: See notebooks/exploratory/

## Citation
If you use this work, please cite: [Citation information]
"""
            elif file_path == "requirements.txt":
                content = """# Research project dependencies
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
ipykernel>=6.0.0
black>=21.0.0
flake8>=4.0.0
pytest>=6.0.0
"""
            elif file_path == "environment.yml":
                content = """name: research-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pip
  - pip:
    - -r requirements.txt
"""
            elif file_path == "setup.py":
                content = """from setuptools import setup, find_packages

setup(
    name="research_project",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
    ],
)
"""
            elif file_path == ".gitignore":
                content = """# Data
data/raw/
data/external/
data/processed/*.csv
data/processed/*.parquet

# Notebooks
notebooks/*.ipynb_checkpoints/

# Experiments
experiments/results/

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyTest
.pytest_cache/
.coverage
htmlcov/
.tox/

# Jupyter
.ipynb_checkpoints
"""
            elif "README.md" in file_path:
                # Generic README for subdirectories
                dir_name = os.path.dirname(file_path)
                content = f"""# {os.path.basename(dir_name).title()} Directory

This directory contains {' '.join(os.path.basename(dir_name).split('_'))} materials.

## Contents
- [Add description of contents]

## Usage
[Add usage instructions]
"""
            elif file_path == "src/__init__.py":
                content = """# Research project source code package
__version__ = "0.1.0"
"""
            else:
                content = "# Placeholder file\n\nAdd content here."
            
            with open(file_path, 'w') as f:
                f.write(content)
            created_files.append(file_path)
            print(f"Created: {file_path}")
        except Exception as e:
            print(f"Error creating {file_path}: {e}")
            skipped_files.append(file_path)

print(f"\nCreated {len(created_files)} files")
print(f"Skipped {len(skipped_files)} files")
```

```python
# Verify AGENTS.md was not overwritten (evidence: fixture-pi-e01)
if os.path.exists("AGENTS.md"):
    with open("AGENTS.md", 'r') as f:
        agents_content = f.read()
    print(f"\nAGENTS.md preserved (not overwritten). Size: {len(agents_content)} characters")
else:
    print("\nAGENTS.md not found (should exist per evidence)")

# Check .agents/installed-packs.json
if os.path.exists(".agents/installed-packs.json"):
    print(".agents/installed-packs.json preserved")
```

```python
# Final verification of created structure
def count_files_and_dirs():
    total_dirs = 0
    total_files = 0
    for root, dirs, files in os.walk("."):
        if '.git' in root:
            continue
        total_dirs += len(dirs)
        total_files += len(files)
    return total_dirs, total_files

final_dirs, final_files