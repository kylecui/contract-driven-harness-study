I'll create a no-overwrite academic research project scaffold by examining the existing workspace and creating only missing files that follow research workflow patterns.

```python
# First, let's examine the current workspace structure
import os
import json

# Check what files and directories exist
existing_files = []
for root, dirs, files in os.walk("."):
    # Skip .git directory for now
    if ".git" in root:
        continue
    for file in files:
        path = os.path.relpath(os.path.join(root, file), ".")
        existing_files.append(path)
    for dir_name in dirs:
        if dir_name == ".git":
            continue
        path = os.path.relpath(os.path.join(root, dir_name), ".")
        existing_files.append(path + "/")

print("Existing files/directories:")
for item in sorted(existing_files):
    print(f"  - {item}")
```

```python
# Now let's define the academic research project structure
# Based on evidence: project profile is academic research (fixture-pi-e02)
# And we must not overwrite existing AGENTS.md (fixture-pi-e01)

research_structure = {
    "directories": [
        "data/",
        "data/raw/",
        "data/processed/",
        "data/external/",
        "notebooks/",
        "src/",
        "src/data/",
        "src/features/",
        "src/models/",
        "src/visualization/",
        "reports/",
        "reports/figures/",
        "paper/",
        "references/",
        "tests/",
        "tests/data/",
        "tests/src/",
        ".research/",
        ".research/workflows/",
        ".research/templates/"
    ],
    "files": [
        "README.md",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        ".research/config.yaml",
        ".research/workflows/literature_review.yaml",
        ".research/workflows/data_analysis.yaml",
        ".research/templates/experiment_report.md",
        "data/README.md",
        "notebooks/01-exploratory-analysis.ipynb",
        "notebooks/02-model-development.ipynb",
        "src/__init__.py",
        "src/data/make_dataset.py",
        "src/features/build_features.py",
        "src/models/train_model.py",
        "src/models/predict_model.py",
        "src/visualization/visualize.py",
        "paper/paper.md",
        "paper/references.bib",
        "references/literature_notes.md",
        "tests/__init__.py",
        "tests/test_data.py",
        "tests/test_features.py",
        "tests/test_models.py"
    ]
}

# Create directories first (only if they don't exist)
created_dirs = []
for directory in research_structure["directories"]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        created_dirs.append(directory)
        print(f"Created directory: {directory}")

# Create files with appropriate content (only if they don't exist)
created_files = []
skipped_files = []

for file_path in research_structure["files"]:
    if os.path.exists(file_path):
        skipped_files.append(file_path)
        continue
    
    # Create file with appropriate content based on file type
    os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
    
    if file_path == "README.md":
        content = """# Academic Research Project

## Project Overview
Brief description of the research project.

## Project Structure
```
project/
├── data/              # Data files
├── notebooks/         # Jupyter notebooks
├── src/               # Source code
├── paper/             # Manuscript files
├── references/        # Literature references
├── reports/           # Generated reports
└── tests/             # Test files
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run exploratory analysis: See notebooks/
3. Reproduce analysis: See src/

## License
[Specify license]
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
"""
    elif file_path == "setup.py":
        content = """from setuptools import setup, find_packages

setup(
    name="research_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
    ],
)
"""
    elif file_path == "pyproject.toml":
        content = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "research-project"
version = "0.1.0"
authors = [
    {name = "Research Team", email = "team@example.com"},
]
description = "Academic research project"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
]
"""
    elif file_path == ".research/config.yaml":
        content = """# Research project configuration
project:
  name: "Academic Research Project"
  version: "0.1.0"
  authors: ["Research Team"]
  
workflows:
  literature_review: ".research/workflows/literature_review.yaml"
  data_analysis: ".research/workflows/data_analysis.yaml"
  
paths:
  data_raw: "data/raw/"
  data_processed: "data/processed/"
  notebooks: "notebooks/"
  reports: "reports/"
  
reproducibility:
  seed: 42
  log_experiments: true
"""
    elif file_path == ".research/workflows/literature_review.yaml":
        content = """# Literature Review Workflow
name: "Literature Review"
description: "Workflow for conducting systematic literature review"

steps:
  - name: "Define Research Questions"
    template: "research_questions.md"
    
  - name: "Search Strategy"
    actions:
      - "Identify databases"
      - "Define search terms"
      - "Set inclusion/exclusion criteria"
    
  - name: "Screening & Selection"
    template: "screening_protocol.md"
    
  - name: "Data Extraction"
    template: "extraction_form.md"
    
  - name: "Synthesis"
    template: "synthesis_method.md"
    
outputs:
  - "references/literature_notes.md"
  - "reports/literature_review.md"
"""
    elif file_path == ".research/workflows/data_analysis.yaml":
        content = """# Data Analysis Workflow
name: "Data Analysis"
description: "Workflow for reproducible data analysis"

steps:
  - name: "Data Acquisition"
    actions:
      - "Load raw data"
      - "Document data sources"
      - "Create data dictionary"
    
  - name: "Data Cleaning"
    template: "cleaning_protocol.md"
    
  - name: "Exploratory Analysis"
    notebook: "notebooks/01-exploratory-analysis.ipynb"
    
  - name: "Model Development"
    notebook: "notebooks/02-model-development.ipynb"
    
  - name: "Validation"
    script: "src/models/validate_model.py"
    
outputs:
  - "data/processed/cleaned_data.csv"
  - "reports/exploratory_analysis.html"
  - "models/trained_model.pkl"
"""
    elif file_path == ".research/templates/experiment_report.md":
        content = """# Experiment Report: {experiment_name}

## Metadata
- **Date:** {date}
- **Researcher:** {researcher}
- **Experiment ID:** {experiment_id}

## Hypothesis
{hypothesis}

## Methods
### Data
{data_description}

### Procedure
{procedure}

## Results
{results}

## Discussion
{discussion}

## Conclusions
{conclusions}

## Files Generated
{files_generated}

## Next Steps
{next_steps}
"""
    elif file_path == "data/README.md":
        content = """# Data Directory

## Structure
- `raw/`: Original, immutable data
- `processed/`: Cleaned, transformed data
- `external/`: Third-party data sources

## Data Dictionary
[Describe your datasets here]

## Usage Notes
- Raw data should never be modified
- Processed data should be reproducible from raw data
- Document all data transformations
"""
    elif "notebooks/" in file_path and file_path.endswith(".ipynb"):
        # Create minimal Jupyter notebook
        import nbformat as nbf
        nb = nbf.v