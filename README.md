# Phishing URL detection using NLP techniques

## Getting Started

### Prerequisites

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

In your IDE, make sure to select the Python interpreter associated with the `phishing-url` Conda environment.

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

## Authors

- **[Dr DIAKO Doffou Jérôme](https://ci.linkedin.com/in/dr-diako-j%C3%A9r%C3%B4me-1972b485)**: Enseignant-Chercheur en Intelligence Artificielle à l'ESATIC ;
- **[Dr KEUPONDJO Armel](#)**: Coordinateur des Projets au LABTIC ;
- **[N'GUESSAN Alex Marc-Aurel](https://marcaureln.com)**: Étudiant en Master 2 en Intelligence Artificielle à l'ESATIC ;
