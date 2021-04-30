# Production Test Log Classifier

Input the Production test logs, output the certain format csv file:

![format](https://photos.google.com/share/AF1QipO2DWxrrEWus_wLdlHrRVvQcSCzqnr_Tj-berR-cJFLoKWeeBTPWcQmnp0a0ODhrg/photo/AF1QipNPeecT2saVuv92xLc7CdKc8Cp3j_tRhvB55Hgv?key=cUgxY2puWjVMZElPV3RnalBDcC04cFh4YXFDb1pR)


## Setup python environemnt:

```
pip install requirements.txt
```

### How to Use

* Generate related folders

    1. Exectue logClassify.py. SN_table and other 4 empty folders with product P/N.
    ```
    $ python logClassify.py
    ```
    2. Put the respective test log files into files

* Gerate report
```
$ python logClassify.py
```
The reports will be generated and put into "combinedReport and "shippingSNReport" folder
