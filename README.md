# Phishing URL detection using NLP techniques and the PhiUSIIL dataset

## Getting Started

### Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) (recommended). Visual Studio Code will prompt you to install the recommended extensions when you open the project.
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html). If you already have the full Anaconda distribution installed, you don't need to install Miniconda.

### Setting up the environment

Create a new Conda environment (you only need to do this once):

```bash
conda create -n phishing-url python=3.12 pandas numpy matplotlib scikit-learn jupyterlab
```

Every time you want to work on the project, activate the Conda environment and start Jupyter Lab:

```bash
conda activate phishing-url
jupyter lab --no-browser
```

You'll see a URL with a token that you can copy and paste into your browser or your IDE to access Jupyter Lab. It should look something like this: `http://localhost:8888/lab?token=...`

When you're done, you can deactivate the environment with:

```bash
conda deactivate
```
