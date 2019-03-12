# nrpe_plugins
Nagios based NRPE plugins developed by me.


## check_generic_process.py
Using this plugin, We can check for any process in linux. 
For example:- 
./check_generic_process.py -w a:b -c e:f -p chromium
let number of process be L
if L < a OR L>b, It will be a warning.
if L < e OR L>f, It will be a critical state.

So, Using this you can set threshold value on it. You can also replace chromium with any other name. Though using this have some security risks involved. Will be writing on it and posting it here soon.
