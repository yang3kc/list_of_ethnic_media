# List of Ethnic Media

This repository consolidates several publicly available lists of ethnic media
outlets in the United States. Data from the CUNY Center for Community Media and
Northwestern University's Local News Initiative are cleaned and merged to create
a unified dataset of domains.

## Project structure

- `data/raw_data` – original CSV files obtained from the sources
- `data/output` – results produced by the pipeline
- `workflow` – Snakemake rules and supporting Python scripts
- `notebooks` – exploratory notebooks

## Installation

The project uses [uv](https://github.com/astral-sh/uv) for dependency
management. The locked dependencies are recorded in `uv.lock`.

Use the following command to install the dependencies:

```bash
uv sync
```

## Running the workflow

The cleaning pipeline is defined in `workflow/Snakefile`. Run it with
[Snakemake](https://snakemake.readthedocs.io/):

```bash
snakemake -s workflow/Snakefile --cores 1
```

Each rule invokes the associated script with `uv run` so that the pinned
dependencies are used. The final dataset will be written to
`data/output/final_dataset.csv`.
