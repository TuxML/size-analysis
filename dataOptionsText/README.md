Each calc contains the manual analysis of a given keyword (the name of the calc).

In red: false positive.

In orange: maybe false positive.

Otherwise: clear true positive.

The file `helpMsgs.csv` is the output results of the script `analyse_kconfig_help_msg`. It contains all the help messages.

Commands that produced the results:

`cat helpMsgs.csv | grep -Po ".*(larger)+.*" > larger.csv`
`cat helpMsgs.csv | grep -Po ".*(smaller)+.*" > smaller.csv`
`cat helpMsgs.csv | grep -Po ".*(increase)+.*" > increase.csv`
`cat helpMsgs.csv | grep -Po ".*(reduce)+.*" > reduce.csv`
`cat helpMsgs.csv | grep -Po ".*(large)+.*" > large.csv`
`cat helpMsgs.csv | grep -Po ".*(small)+.*" > small.csv`
`cat helpMsgs.csv | grep -Po ".*(big)+.*" > big.csv`
`cat helpMsgs.csv | grep -Po ".*(overhead)+.*" > overhead.csv`
`cat helpMsgs.csv | grep -Po ".*(optim)+.*" > optim.csv`
`cat helpMsgs.csv | grep -Po ".*(optim)+.*" > optim.csv`
`cat helpMsgs.csv | grep -Po ".*(trim)+.*" > trim.csv`
`cat helpMsgs.csv | grep -Po ".*(slice)+.*" > slice.csv`
`cat helpMsgs.csv | grep -Po ".*(little)+.*" > little.csv`
`cat helpMsgs.csv | grep -Po ".*(space)+.*" | grep -v "userspace" | grep -v "user space" | grep -v "user-space" | grep -v "Userspace" | grep -v "namespace" > space.csv`
