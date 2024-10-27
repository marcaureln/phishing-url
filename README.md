# Phishing URL detection using NLP techniques

## Getting Started

### Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) (recommended). Visual Studio Code will prompt you to install the recommended extensions when you open the project.
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html). If you already have the full Anaconda distribution installed, you don't need to install Miniconda.
- [Make](https://www.gnu.org/software/make/) (optional). Make is commonly pre-installed on Unix-based operating systems. If you're using Windows, you can install Make with [Chocolatey](https://chocolatey.org/): `choco install make`.

### Setting Up the Environment

Create a new Conda environment and install the required packages:

```bash
make install
```

Every time you want to work on the project, activate the Conda environment:

```bash
conda activate phishing-url
```

If you are using Visual Studio Code, make sure to select the Python interpreter. Open the Command Palette (Ctrl+Shift+P) and search for `Python: Select Interpreter`. Choose the `phishing-url` environment.

Start the Jupyter Lab server:

```bash
jupyter lab --no-browser --NotebookApp.token='' --NotebookApp.disable_check_xsrf=True
```

We remove the token requirement so that you can access Jupyter Lab with this URL: <http://localhost:8888/lab> without having to copy and paste the token every time.

When you're done, you can deactivate the environment with:

```bash
conda deactivate
```

## Collaboration

This project uses [Git](https://git-scm.com/doc) for version control.

### Prerequisites

- [Git](https://git-scm.com/doc)
- [pipx](https://github.com/pypa/pipx)

### Setting Up the Repository

To manage Jupyter Notebooks, we use [nb-clean](https://github.com/srstevenson/nb-clean) to clean up the notebooks before committing them to the repository. Follow these steps to set up `nb-clean`:

1. **Install `nb-clean` globally**:
    ```bash
    pipx install nb-clean
    ```

2. **Add `nb-clean` as a Git filter**:
    ```bash
    nb-clean add-filter --remove-empty-cells --preserve-cell-outputs
    ```

By following these steps, you ensure that your Jupyter Notebooks are properly cleaned before being committed to the repository.
