# Workflow

This directory contains the data cleaning pipeline implemented with
[Snakemake](https://snakemake.readthedocs.io/). Each rule invokes a Python
script using `uv run` so that the locked dependencies are honored.

Run the full pipeline from the repository root with:

```bash
snakemake -s workflow/Snakefile --cores 1
```

Intermediate files are written to `data/intermediate_files` and the final
dataset is placed in `data/output`.

