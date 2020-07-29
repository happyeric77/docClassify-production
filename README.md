# Production Document Classifying Tool

Following the step below to start:

## 1. install python in your Win or Mac

##  2. install depandencies by pip in your terminal :
* pandas
```
pip install pandas
```
* numpy
```
pip install numpy
```
## 3. Start generating report by production test log file

1. generate the needed folder on the working directory
```
python logClassify.py
```
folloiwng 7 folders will shows on the working directory
- 98B-500-0007R-LTE_1B.B-99B-500-0006R
- 98B-500-0010R-LTE_1B.G-99B-501-0006R
- 98B-500-0011R-WIFI_1A.B-99B-501-0005R
- 98B-500-0012R-WIFI_1A.G-99B-500-0005R
- finalTestReport
- functionTestReport
- SN_table

2. put the log files and S/N table into corrosponding folder:

log format:
- <12digMacNumber>.log --> product final test log
-  <12digMacNumber>_F.log --> PCBA function test log

3. run "logClassify.py" script again
```
python logClassify.py
```

4. excel reports will be generated into "finalTestReport" and "functionTestReport" folder


