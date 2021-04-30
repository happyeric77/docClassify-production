# Production Test Log Classifier

Input the Production test logs, output the certain format csv file:

![format](https://lh3.googleusercontent.com/pw/ACtC-3d20T9YuhfsFvji7Oy6dJtAuvOcvxcjl3JkSb4qA3TjD-l4Hyj-6y7qD4mbripMHOL0jDDYxMuHb6Tf3hDp-BEy7-nNTB9xbdxDx9IsU90tvmFV7EFAuMEswjeauPm6EvwqZDMkTznx8gOAEIYqcJOFNA=w2338-h574-no?authuser=0)


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
