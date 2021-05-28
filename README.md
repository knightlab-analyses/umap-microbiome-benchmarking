# umap-microbiome-benchmarking

## Installation
These notebooks' dependencies are listed in the `requirements.yml` file.

Additionally, using the notebooks will require Jupyter.

```bash
ENV_NAME=umap-benchmarking
conda create -n ${ENV_NAME}
conda activate ${ENV_NAME}
conda env update --file requirements.yml
jupyter notebook
```

## Figures

```bash
cd notebooks
mkdir results
jupyter notebook
```

Then these notebooks contain the analyses:
* `real-data-keyboard-benchmark.ipynb`
* `real-data-soil-benchmark.ipynb`
* `technical-effects-hmpv13v35.ipynb`

