import pandas as pd
import os
import datetime
import re
import numpy

currentPath = os.getcwd()

# If no LTE Black folder, create one
if not os.path.exists('98B-500-0007R-LTE_1B.B-99B-500-0006R'):
    print('create LTE Black folder ')
    os.mkdir('98B-500-0007R-LTE_1B.B-99B-500-0006R')

# If no LTE Grey folder, create one
if not os.path.exists('98B-500-0010R-LTE_1B.G-99B-501-0006R'):
    print('create LTE Grey folder ')
    os.mkdir('98B-500-0010R-LTE_1B.G-99B-501-0006R')


# If no WIFI Black folder, create one
if not os.path.exists('98B-500-0011R-WIFI_1A.B-99B-501-0005R'):
    print('create WIFI Black dir')
    os.mkdir('98B-500-0011R-WIFI_1A.B-99B-501-0005R')


# If no WIFI Grey folder, create one
if not os.path.exists('98B-500-0012R-WIFI_1A.G-99B-500-0005R'):
    print('create WIFI Grey dir')
    os.mkdir('98B-500-0012R-WIFI_1A.G-99B-500-0005R')

# If no SN table, create one
if not os.path.exists('SN_table'):
    os.mkdir('SN_table')

lteBlack = {'path': currentPath + '/98B-500-0007R-LTE_1B.B-99B-500-0006R/', 'name': 'LTE-Black'}
lteGrey = {'path': currentPath + '/98B-500-0010R-LTE_1B.G-99B-501-0006R/', 'name': 'LTE-Grey'}
wifiBlack = {'path': currentPath + '/98B-500-0011R-WIFI_1A.B-99B-501-0005R/', 'name': 'WIFI-Black'}
wifiGrey = {'path': currentPath + '/98B-500-0011R-WIFI_1A.B-99B-501-0005R/', 'name': 'WIFI-Grey'}

snDir = currentPath + '/SN_table/'
snTables = os.listdir(snDir)

serialTable = None
for snTable in snTables:
    df = pd.read_csv(snDir + '/' + snTable, header=None)
    try:
        if serialTable == None:
            serialTable = df
        else:
            pass
    except Exception as e:
        newTable = pd.concat([serialTable, df])
        serialTable = newTable

products = [lteBlack, lteGrey, wifiBlack, wifiGrey]


for product in products:
    print('\n' * 3 + '-' * 50 + '\n{product} section start\n'.format(product=product['name']) + '-' * 50 + '\n' * 3)
    allFiles= os.listdir(product['path'])
    # seperate function test files and final test files to different array
    funcLogNames = []
    logNames = []

    for file in allFiles:
        try:
            mac, subFix = file.split('_')
            if subFix[0] == 'F':
                funcLogNames.append(file)
            # print('file "{product}" has symbol "_F" --> for [function] test : line 70'.format(product=file))
        except:
            # print('file "{product}" does not have symbol "_F" --> for [final] test : line 70'.format(product=file))
            logNames.append(file)

    print('\nfunction test log files:')
    print(funcLogNames)
    print('\nfinal test log files:')
    print(logNames)

    #Final test data fields, and generate final test report
    print('*' * 50 + '\nStart generating "{product}" final test rerport. \n'.format(product=product['name']) + '*' * 50)


    # LTEinfo = {}
    data = {
        'Application Version': [],
        'Test Time': [],
        'DUT SN': [],
        'DUT MAC': [],
        'Detect device and comport': [],
        'BLE firmware': [],
        'FW Version': [],
        'FW Final Check': [],
        'Check LTE Information': [],
        'WIFI function': [],
    }

    try:
        for logName in logNames:

            if not re.findall(r"\.", logName):
                logName=logName + '.'

            preFix, proFix = logName.split(".")

            fwVersion = ''
            try:
                log = pd.read_csv(product['path']+logName, header=None, delimiter=':')
                dfKeys = log[0].values

                for key in data.keys():
                    # # set value generally as ''
                    value = ''

                    # If key in the log, retrieve it as value (application version/ MAC )
                    if key =='Application Version':
                        value = str(log[log[0] == key][1].values[0]).replace(' ', '')

                    if key =='Test Time':
                        value = str(log[log[0] == key][1].values[0]).replace(' ', '')

                    # If key is serial number, get the original mac and map to find sn#
                    if key == 'DUT SN':
                        macNum = str(log[log[0] == key][1].values[0]).replace(' ', '')
                        try:
                            serialNumber = serialTable[serialTable[0] == macNum][1].values[0]
                            value = serialNumber
                        except Exception as e:
                            value = 'No Matching data in the SN table'

                    if key == 'DUT MAC':
                        value = str(log[log[0] == key][1].values[0]).replace(' ', '')

                    # if Detect device and comport show on log, pass
                    if key == 'Detect device and comport':
                        try:
                            detail = log[log[0].str.startswith('Detected device comport')]
                            value = 'PASS'
                        except:
                            value = 'FAIL'

                    # Retreving BLE FW version
                    if key == 'BLE firmware' :
                        detail = log[log[0].str.startswith('ble bicmd2')].values[0][0].split(' ')[2]
                        if re.findall(r'^072b', detail):
                            value = 'PASS'

                    # Retrieving FW version
                    if key == 'FW Version':
                        major = log[log[0].str.startswith('Major')].values[0][1]
                        minor = log[log[0].str.startswith('Minor')].values[0][1]
                        patch = log[log[0].str.startswith('Patch')].values[0][1]
                        value = major + '.' + minor + '.' + patch
                    # Final FW check
                    if key == 'FW Final Check':
                        try:
                            detail = log[log[0].str.startswith('Test Check Firmware PASS')].values[0][0].split(' ')
                            value = detail[3]
                        except:
                            value = 'FAIL'

                    # For LTE version: check LTE
                    if key == 'Check LTE Information':
                        try:
                            iccid = log[log[0].str.startswith('SIM ICCID')].values[0][1]
                            imsi = log[log[0].str.startswith('SIM IMSI')].values[0][1]
                            lteModule = log[log[0].str.startswith('LTE MODULE')].values[0][1]
                            value = 'PASS'
                        except:
                            try:
                                log[log[0].str.startswith('Test Set WiFi Information PASS')].values[0][0].split(' ')
                                value = 'N/A'
                            except:
                                value = 'FAIL'

                    # For WIFI version: Test Set WiFi Information PASS
                    if key == 'WIFI function':
                        try:
                            detail = log[log[0].str.startswith('Test Set WiFi Information PASS')].values[0][0].split(' ')
                            value = detail[4]
                        except:
                            try:
                                log[log[0].str.startswith('SIM ICCID')].values[0][1]
                                value = 'N/A'
                            except:
                                value = 'FAIL'
                    data[key] += [value]
                print('file "{product}" succeeded to generate "final test" report.'.format(product=file))

            except Exception as e:
                print(logName + ' fail: Read file fail')
                print(e)
    except:
        print('file "{product}" fail to generate "final test" report.'.format(product=file))

    targetDir = "finalTestReport"
    fileName = "finalTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['name'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    pd.DataFrame.from_dict(data, orient='index').T.to_excel(os.path.join(targetDir, fileName))

    # #Function test data fields, and generate function test report
    print('*'*50 + '\nstart generating {product} function test rerport\n'.format(product=product['name']) + '*'*50)

    funcData = {
        'Application Version': [],
        'Test Time': [],
        'DUT SN': [],
        'DUT MAC': [],
        'Detect device and comport': [],
        'BLE firmware': [],
        'FW Version': [],
        'FW Final Check': [],
        'Check LTE Information': [],
        'WIFI function': [],
    }

    try:
        for funcLogName in funcLogNames:
            print(funcLogName)
    except:
        print('file "{product}" fail to generate "function test" report.'.format(product=file))



    print('\n' * 3 + '-' * 50 + '\n{product} section done\n'.format(product=product['name'])+ '-' * 50 + '\n' * 10)