# Variables
# Do not confuse them with environment variables. These are Makefile variables.
# Can be accessed using $(VAR_NAME) syntax. Whereas, environment variables are accessed using $ENV_VAR or ${ENV_VAR} syntax.
ENV_NAME = phishing-url
CONDA_ENV_FILE = environment.yml

# Phony Targets
# Prevent Make from confusing the targets with files of the same name.
.PHONY: install env save-env clean clean-all

# Targets
# Targets are commands that can be executed using `make` command.
# e.g.: `make install` will execute the `install` target.
all: env install

# Create conda environment if not exists
env: $(CONDA_ENV_FILE)
	conda env list | grep -q $(ENV_NAME) || conda env create --file $(CONDA_ENV_FILE) --name $(ENV_NAME)

# Install required packages in the conda environment.
# Warning: This will overwrite your current environment.
install:
	conda env update --name $(ENV_NAME) --file $(CONDA_ENV_FILE)

# Save the environment to a file for reproducibility.
# Remove `name` and `prefix` from the file.
save-env:
	conda env export --no-builds --name $(ENV_NAME) > $(CONDA_ENV_FILE); \
	sed -i '' '/^name: /d' $(CONDA_ENV_FILE); \
	sed -i '' '/^prefix: /d' $(CONDA_ENV_FILE)

# Remove the conda environment.
clean:
	conda remove --name $(ENV_NAME) --all -y

# Remove the environment, conda unused packages and caches.
clean-all: clean
	conda clean --all -y

# Load dataset
load-dataset:
	python src/load_dataset.py
