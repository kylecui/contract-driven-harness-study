I'll create a no-overwrite academic research project scaffold. Let me start by examining the existing workspace structure to understand what's already present.

```python
import os
import json
from pathlib import Path

# First, let's examine the current directory structure
def list_directory_contents(path="."):
    """List files and directories in the given path."""
    contents = []
    for root, dirs, files in os.walk(path):
        # Skip .git directory contents for brevity
        if '.git' in root:
            continue
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        contents.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            contents.append(f"{subindent}{file}")
    return contents

# Check current directory
print("Current directory structure:")
for item in list_directory_contents():
    print(item)

# Check specific mentioned files
print("\nChecking specific mentioned files:")
important_files = ["AGENTS.md", ".agents/installed-packs.json", ".git"]
for file in important_files:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} does not exist")
```

Now I'll create the academic research project scaffold. Based on the task requirements and typical academic research workflows, I'll create a standard structure while respecting the no-overwrite constraint.

```python
# Define the academic research project structure
# Based on evidence: project profile is academic research (fixture-pi-e02)
research_structure = {
    "directories": [
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
        "experiments",
        "results"
    ],
    "files": {
        "README.md": "# Academic Research Project\n\n## Project Overview\n\nBrief description of the research project.\n\n## Repository Structure\n\n- `data/`: Research data (raw, processed, external)\n- `notebooks/`: Jupyter notebooks for exploration and analysis\n- `src/`: Source code modules\n- `reports/`: Generated reports and visualizations\n- `paper/`: Manuscript preparation\n- `literature/`: Literature review materials\n- `experiments/`: Experimental protocols and logs\n- `results/`: Final results and outputs\n\n## Getting Started\n\nInstructions for setting up the research environment.\n",
        "requirements.txt": "# Research project dependencies\n\n# Core scientific computing\nnumpy\npandas\nscipy\n\n# Machine learning\nscikit-learn\n\n# Visualization\nmatplotlib\nseaborn\n\n# Jupyter\njupyter\n\n# Documentation\nsphinx\n",
        "environment.yml": "name: research-project\nchannels:\n  - defaults\ndependencies:\n  - python=3.9\n  - numpy\n  - pandas\n  - scipy\n  - scikit-learn\n  - matplotlib\n  - seaborn\n  - jupyter\n  - pip\n  - pip:\n    - -e .\n",
        "setup.py": "from setuptools import setup, find_packages\n\nsetup(\n    name='research_project',\n    version='0.1.0',\n    packages=find_packages(where='src'),\n    package_dir={'': 'src'},\n    install_requires=[\n        'numpy>=1.21.0',\n        'pandas>=1.3.0',\n        'scipy>=1.7.0',\n        'scikit-learn>=1.0.0',\n        'matplotlib>=3.4.0',\n        'seaborn>=0.11.0',\n    ],\n    python_requires='>=3.8',\n)\n",
        ".gitignore": "# Python\n__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n\n# IPython\nprofile_default/\nipython_config.py\n\n# Jupyter Notebook\n.ipynb_checkpoints\n\n# pyenv\n.python-version\n\n# Environments\n.env\n.venv\nenv/\nvenv/\nENV/\nenv.bak/\nvenv.bak/\n\n# Data files\n*.csv\n*.json\n*.parquet\n*.feather\n*.h5\n*.hdf5\n\n# OS\n.DS_Store\n.DS_Store?\n._*\n.Spotlight-V100\n.Trashes\nehthumbs.db\nThumbs.db\n\n# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n*~\n",
        "research_plan.md": "# Research Plan\n\n## Research Questions\n\n1. \n\n## Hypotheses\n\n1. \n\n## Methodology\n\n### Data Collection\n\n### Analysis Methods\n\n### Validation Approach\n\n## Timeline\n\n- [ ] Literature review\n- [ ] Data collection\n- [ ] Exploratory analysis\n- [ ] Model development\n- [ ] Validation\n- [ ] Paper writing\n",
        "src/__init__.py": "# Research project source code\n",
        "src/data/__init__.py": "# Data processing modules\n",
        "src/data/make_dataset.py": "import pandas as pd\nimport numpy as np\nfrom pathlib import Path\n\n\ndef load_raw_data(data_path):\n    \"\"\"Load raw data from the data/raw directory.\"\"\"\n    raw_path = Path(data_path) / 'raw'\n    # Implementation depends on data format\n    pass\n\n\ndef process_data(raw_data):\n    \"\"\"Process raw data into clean format.\"\"\"\n    # Data cleaning and preprocessing logic\n    pass\n\n\ndef save_processed_data(processed_data, output_path):\n    \"\"\"Save processed data to data/processed directory.\"\"\"\n    output_path = Path(output_path) / 'processed'\n    # Save implementation\n    pass\n",
        "src/features/__init__.py": "# Feature engineering modules\n",
        "src/features/build_features.py": "import pandas as pd\nimport numpy as np\n\n\ndef create_features(data):\n    \"\"\"Create features from processed data.\"\"\"\n    # Feature engineering logic\n    pass\n\n\ndef select_features(feature_data, method='correlation'):\n    \"\"\"Select important features for modeling.\"\"\"\n    # Feature selection logic\n    pass\n",
        "src/models/__init__.py": "# Model development modules\n",
        "src/models/train_model.py": "from sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score, precision_score, recall_score\nimport pickle\n\n\ndef train_model(X, y, model_type='logistic'):\n    \"\"\"Train a machine learning model.\"\"\"\n    # Model training logic\n    pass\n\n\ndef evaluate_model(model, X_test, y_test):\n    \"\"\"Evaluate model performance.\"\"\"\n    # Model evaluation logic\n    pass\n\n\ndef save_model(model, model_path):\n    \"\"\"Save trained model to disk.\"\"\"\n    with open(model_path, 'wb') as f:\n        pickle.dump(model, f)\n",
        "src/visualization/__init__.py": "# Visualization modules\n",
        "src/visualization/visualize.py": "import matplotlib.pyplot as plt\nimport seaborn as sns\n\n\ndef plot_distributions(data, columns=None):\n    \"\"\"Plot distributions of selected columns.\"\"\"\n    # Distribution plotting logic\n    pass\n\n\ndef plot_correlations(data):\n    \"\"\"Plot correlation matrix.\"\"\"\n    # Correlation plotting logic\n    pass\n\n\ndef save_figure(fig, filename, dpi=300):\n    \"\"\"Save figure to reports/figures directory.\"\"\"\n    fig.savefig(f'../reports/figures/{filename}', dpi=dpi, bbox_inches='tight')\n",
        "notebooks/exploratory/01_data_exploration.ipynb": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": [\n