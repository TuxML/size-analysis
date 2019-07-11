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

see docker/Dockerfile (it can take a while)
then:
 * apk add git 
 * git clone https://github.com/TuxML/size-analysis
 * cd size-analysis
 * wget http://37.187.140.181/tuxml_dataset/dataset_encoded_size.csv
 * python feature_frequency.py 
note: I will improve many parts, and you need to set the space/swap of Docker ;) 

