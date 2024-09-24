# pylis

The `pylis` library contains helpful functions for pre- and postprocessing for the NASA Land Information System in Python (e.g., reading in data, visualization, CDF matching, ...).

## How to use

Clone the repository from KUL-RSDA (or use your own fork if you want to make personal changes to the code):
```
cd your/path/to/scripts
git clone https://github.com/KUL-RSDA/pylis
```

When you are working on a Python script or notebook in which you want to use `pylis` functionalities, add these lines to the top:
```python 
# enable loading in the necessary scripts
# use here the parent directory where the pylis folder is located

import sys
sys.path.append("your/path/to/scripts")
```

You can then use `pylis` as if it is a library you have installed, e.g.,
```python
from pylis import readers
from pylis import visualization as vis
from pylis.help import root_zone

dc_sm = readers.lis_cube(...)
vis.map_imshow(root_zone(dc_sm).mean(dim = "time"))
```

For use cases on how to use the different functionalities, you can consult the notebooks under the `tutorials` folder.


%%% my branch %%%

## Installing dependencies

To install the environment with all its dependencies, you can use the environment file `requirements_pylis_env.yaml`. If you've never used such an installation procedure, see the [conda guide](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file). The name of the environment will be `pylis_env`.

Alternatively, you can use the script `setup_conda_env.sh` to do it automatically for you. This is a folder-wise installation of an environment, meaning that the environment will be stored in the `conda` folder and you will have to export the PATH by running `source ./conda/pylis_env_settings` every time you want to activate the environment. If this sounds odd to you, just stick to the first way of doing the installation of the environment.
If you install the conda environment with this folder-wise procedure, you will have to follow the next section "Installing the jupyter kernel on VSC..." to use the environment in jupyter lab.

### Installing the jupyter kernel on VSC or any other HPC

To run jupyter lab with a kernel that "sees" your pylis_env environment, you will have to install a kernel. To do this, follow these steps.

1. Activate your environment, either by running `conda activate pylis_env` or `source pylis_env_settings`.
2. Install the kernel:

```bash
python -m ipykernel install --user --env PYTHONPATH "" --name <name kernel or environment> --display-name <name kernel>
```
3. Since PYTHONPATH is “”, you will have the kernel installed in the default location:
```
${VSC_DATA}/.local/share/jupyter/kernels/
```
If you want to change the default location or export the path in another way, or in any other case you would need some clarification on the kernel installation, follow the [official VSC guide](https://docs.vscentrum.be/leuven/services/openondemand.html#jupyterlab).


## Running a python script with a slurm job
Prepare your `.slurm` file as usual, and be careful to load all the necessary modules, exporting the necessary paths and activate your environment before running your python file. The end of your `.slurm` script should look like this:

- if you performed the folder-wise installation:
```
module load cluster/<name of cluster>/batch
source $PYLIS_DIR/conda/pylis_env_settings
python script.py
```
- if you performed a normal installation:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DATA/miniconda3/envs/pylis_env/lib
conda activate pylis_env
python script.py
```