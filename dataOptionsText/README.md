Each calc contains the manual analysis of a given keyword (the name of the calc).

In red: false positive.

In orange: maybe false positive.

Otherwise: clear true positive.

The file `helpMsgs.csv` is the output results of the script `analyse_kconfig_help_msg`. It contains all the help messages.

Commands that produced the results:

`cat helpMsgs.csv | grep -Poi ".*(big)+.*" > big.csv`
`cat helpMsgs.csv | grep -Poi ".*(bloat)+.*" > bloat.csv`
`cat helpMsgs.csv | grep -Poi ".*(enlarge)+.*" > enlarge.csv`
`cat helpMsgs.csv | grep -Poi ".*(huge)+.*" > huge.csv`
`cat helpMsgs.csv | grep -Poi ".*(increase)+.*" > increase.csv`
`cat helpMsgs.csv | grep -Poi ".*(inlin)+.*" > inlin.csv`
`cat helpMsgs.csv | grep -Poi ".*(larger)+.*" > larger.csv`
`cat helpMsgs.csv | grep -Poi ".*(little)+.*" > little.csv`
`cat helpMsgs.csv | grep -Poi ".*(optim)+.*" > optim.csv`
`cat helpMsgs.csv | grep -Poi ".*(overhead)+.*" > overhead.csv`
`cat helpMsgs.csv | grep -Poi ".*(reduce)+.*" > reduce.csv`
`cat helpMsgs.csv | grep -Poi ".*(small)+.*" > small.csv`
`cat helpMsgs.csv | grep -Poi ".*(smaller)+.*" > smaller.csv`
`cat helpMsgs.csv | grep -Poi ".*(space)+.*" | grep -vi "userspace" | grep -vi "user space" | grep -vi "user-space" | grep -vi "namespace" > space.csv`
`cat helpMsgs.csv | grep -Poi ".*(trim)+.*" > trim.csv`
