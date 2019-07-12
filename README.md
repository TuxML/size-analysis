# Analysis of 125+ Linux configurations (this time for predicting/understanding kernel sizes) 

 * pre-requisite: http://37.187.140.181/tuxml_dataset/dataset_encoded_all_size.csv `MD5 (dataset_encoded_all_size.csv) = a701f11bb6f2d655707cce14b45934d7` 
 * size_analysis.ipynb 
 


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


