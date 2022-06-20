# Analysis of 125+ Linux configurations (this time for predicting/understanding kernel sizes) 

 * git clone https://github.com/TuxML/size-analysis/ (to get `tuxml.py`)
 * git clone https://gitlab.com/FAMILIAR-project/tuxml-size-analysis-datasets/ (to get datasets)
 * then you can use `tuxml.py` to load a pre-encoded dataset (it returns a pandas dataframe): 
```
import tuxml
df = tuxml.load_dataset()
```
An example is given with `size-analysis-fast.ipynb`
Note: the datatset is loaded here: `../tuxml-size-analysis-datasets/all_size_withyes.pkl` so be careful about relative paths and your git repo locations 

## HOW TO analyse_kconfig_help_msg.py 

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
 
## Docker image 

`docker build -f docker/Dockerfile -t sklearntux .` (it can take a while)
or simply `docker pull macher/sklearntux` 

`docker run -it --rm macher/sklearntux python3 size-analysis-fast.py` should work 

Notes: 
 * there is a `all_size_withyes.pkl` pre-copied (it is a .pkl of the dataset) -- it can a CSV file as well 
 * plotting facilities are installed (matplotlib, seaborn, etc.) partly explaining the increase in size of the Docker image 


