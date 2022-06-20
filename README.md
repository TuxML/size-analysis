# Accurate and Interpretable Learning of Linux Kernel Configuration Sizes

This is the companion repository of the SPLC'22 40 ^th^ submission.

Further details are available in the related publication, see the [pdf file](https://github.com/TuxML/size-analysis/blob/master/SPLC_2022___Linux_Kernel_Size.pdf) in the main directory 

## In a nutshell

Our research work proposes to train interpretable performance models scaling to software systems with thousands of options. We evaluate our results on the Linux kernel. With an analysis of these models, it becomes possible to know the effect of each configuration option, and thus to decide which one should be (de)activated in order to minimize a performance property. Thanks to this work, we can answer the question : "which option should I enable to minimize the footprint of a Linux kernel?"

## Artifacts

To evaluate these artifacts, two aspects should be tested:
1. The gathering of a *dataset* of measurements on the Linux kernel. The goal is there to ensure that a-] this dataset is available b-] one can easily reproduce such a dataset thanks to our infrastructure.
2. The training of performance *models* applied on this dataset of measurements.

### Prerequisites

Install [docker](https://docs.docker.com/get-docker/). You can check that docker is working by checking its version (use the command line ```sudo docker --version```) or status (use ```sudo systemctl status docker```).

### 1. Dataset

#### a-] Availability

Our dataset of Linux measurements can be downloaded at [zenodo](https://zenodo.org/record/4943884#.YqG5cTlByV4)

Due to the large size (1.8 GB) of the dataset, the preview is not possible.

Each line of this dataset is composed of the configuration options (1 = activated, 0 = deactivated) used to compile the Linux kernel and the resulting size or footprint of the kernel.

We store this dataset of Linux compilations online.

#### b-] Reproducibility

We also maintain an infrastructure, namely [TuxML](https://github.com/TuxML/tuxml), allowing users to participate to this initiative.

In this part, we invite you to *add a line* to the existing dataset.

You will compile a Linux kernel with randomly chosen configuration options, compute the size of the resulting kernel and send it to the database. 

Please make sure python and docker are installed before executing the following command lines:

1. Download the code

`git clone https://github.com/TuxML/tuxml.git`

2. Enter the folder

`cd tuxml`

3. Run the script launching the compilation of the kernel

`python3 kernel_generator.py`

It might take few seconds or minutes to compute.

If everything is working, you'll see these lines:

![screen1](https://github.com/TuxML/size-analysis/blob/master/output-figs/screen1.png)

Thank you for contributing to TuxML!

If you are interested, additional information is available at:
[https://github.com/TuxML/tuxml/wiki/User_documentation](https://github.com/TuxML/tuxml/wiki/User_documentation)

## 2. Models

Finally, you will have to train a model on this dataset.

In our paper, we tested and compared multiple learning techniques. 

We provide you a docker container allowing to launch and test these techniques.

First, you need to pull the container, thanks to the following command line:

`sudo docker pull anonymicse2021/splc22`

Then, run the container in interactive mode:

`sudo docker run -ti anonymicse2021/splc22`

Once in the container, run the python script train.py:

`python3 train.py`

Here are some additional arguments to customize your launch:
- `--verbose` y to show detailed logs, activated by default
- `--training_size` to indicate the proportion of the dataset that should be used as training (between 0 and 1). Default 0.1
- `--ml_technique` the machine learning technique used to compute the result. `--ml_technique lr` for linear regression, `--ml_technique dt` for decision tree, `--ml_technique rf` for random forest, `--ml_technique gb` for gradient boosting. Default set to "rf".
- `--feature_selection` y if a feature selection process should be applied before the launch of the model, `--feature_selection n` otherwise. Default y.
- `--metric` the metric to compute on the test set. Default `--metric MAPE`. Alternative `--metric MAE`.

For instance, the following command will launch a gradient boosting tree, without feature selection and using 90% of the configurations as training

`python3 train.py --ml_technique gb --feature_selection n --training_size 0.9`

If everything worked, you should be able to observe the following lines:

![screen2](https://github.com/TuxML/size-analysis/blob/master/output-figs/screen2.png)

You can now exit the container and remove the image (to spare the memory of your computer) by running the following command line:

`sudo docker image rm anonymicse2021/splc22`

Thank you for testing our artifact!

## 3. Others

### HOW TO analyse_kconfig_help_msg.py 

First install Kconfiglib
`pip[3] install kconfiglib`

To realize Patch Kernel Makefile:
git clone https://github.com/ulfalizer/Kconfiglib.git
Download a Linux kernel ie in our case: https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.13.3.tar.xz
In the kernel top-directory: 
`cd linux-4.13.3`
and then `patch -p1 < ../Kconfiglib/makefile.patch`
(it will modify the Makefile of linux kernel to support some commands like `scriptconfig` see below)

Finally, you can use the script: always in the kernel directory `linux-4.13.3`, you can run:
`make ARCH=x86 scriptconfig SCRIPT=../analyse_kconfig_help_msg.py`

### Alternative to zenodo

 * git clone https://github.com/TuxML/size-analysis/ (to get `tuxml.py`)
 * git clone https://gitlab.com/FAMILIAR-project/tuxml-size-analysis-datasets/ (to get datasets)
 * then you can use `tuxml.py` to load a pre-encoded dataset (it returns a pandas dataframe): 
```
import tuxml
df = tuxml.load_dataset()
```
An example is given with `size-analysis-fast.ipynb`
Note: the datatset is loaded here: `../tuxml-size-analysis-datasets/all_size_withyes.pkl` so be careful about relative paths and your git repo locations 

### Another Docker image

`docker build -f docker/Dockerfile -t sklearntux .` (it can take a while)
or simply `docker pull macher/sklearntux` 

`docker run -it --rm macher/sklearntux python3 size-analysis-fast.py` should work 

Notes: 
 * there is a `all_size_withyes.pkl` pre-copied (it is a .pkl of the dataset) -- it can a CSV file as well 
 * plotting facilities are installed (matplotlib, seaborn, etc.) partly explaining the increase in size of the Docker image 




