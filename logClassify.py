import pandas as pd
import os
import datetime
import re
from Report import Report

toolVersion = '1.1'
releaseNote = {
    '1.1.1': ['Extract report to Report class module'],
    '1.1': [
        'Add shipping SN report',
        'Remove BLE version',
    ]
}

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

lteBlack = {'path': currentPath + '/98B-500-0007R-LTE_1B.B-99B-500-0006R/',
            'name': 'LTE-Black',
            'brcmPN': '99B-500-0006R',
            'bitkeyPN':'TW-03(BK)',
            'qtyFuncRep':'',
            'qtyFinRep': ''}
lteGrey = {'path': currentPath + '/98B-500-0010R-LTE_1B.G-99B-501-0006R/',
           'name': 'LTE-Grey',
           'brcmPN': '99B-501-0006R',
           'bitkeyPN': 'TW-03(G)',
           'qtyFuncRep':'',
           'qtyFinRep': ''}
wifiBlack = {'path': currentPath + '/98B-500-0011R-WIFI_1A.B-99B-501-0005R/',
             'name': 'WIFI-Black',
             'brcmPN': '99B-501-0005R',
             'bitkeyPN': 'TW-02(BK)',
             'qtyFuncRep': '',
             'qtyFinRep': ''}
wifiGrey = {'path': currentPath + '/98B-500-0012R-WIFI_1A.G-99B-500-0005R/',
            'name': 'WIFI-Grey',
            'brcmPN': '99B-500-0005R',
            'bitkeyPN': 'TW-02(G)',
            'qtyFuncRep': '',
            'qtyFinRep': ''}

snDir = currentPath + '/SN_table/'
snTables = os.listdir(snDir)
serialTable = None

# Import SN & MAC table from SMS
tables = []
try:
    for snTable in snTables:
        df = pd.read_csv(snDir + '/' + snTable)
        tables.append(df)
except Exception as e:
    input('***'*20+'\nSN Table folder only takes .csv type file. "{snTable}" found.\nPress enter key to finish program'.format(snTable=snTable))
    raise ValueError("SN Table folder only takes .csv type file.")

serialTable = pd.concat(tables)


products = [lteBlack, lteGrey, wifiBlack, wifiGrey]
for product in products:
    print('\n' * 3 + '===' * 50 + '\n{product} section start\n'.format(product=product['name']) + '====' * 50 + '\n' * 3)
    allFiles = os.listdir(product['path'])

    # Seperate function test files and final test files to different array
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

    input('***' * 20 + "\nFor {product}, following logs are in the log corresponding folders".format(
        product=product['name']) + '\nFinal Test log: {final}'.format(
        final=len(logNames)) + '\nFunction Test log: {func}'.format(
        func=len(funcLogNames)) + '\nPress Enter key to go on ...')

    # Create Final test data dict, and fill the data in by Final test log
    print('*' * 50 + '\nStart generating "{product}" final test rerport. \n'.format(product=product['name']) + '*' * 50)

    data = {
        'Application Version_FT2': [],
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
    finalReport = Report(product, data)

    # Create shipping serial data fields, and generate production serial data form by Final test log
    print('*' * 50 + '\nstart generating {product} Serial data shipping report\n'.format(product=product['name']) + '*' * 2)

    snData = {
        'Model': [],
        'Color': [],
        'deviceID': [],
        'SN': [],
        'ICCID': [],
        'IMSI': [],
        'IMEI': [],
        'Time': [],
        'PO No.': [],
        'Carton No.': [],
        'Estimated Time of Arrival': [],
        'Division': [],
    }
    snReport = Report(product, snData)

    try:
        # loop through each final test log in folder
        for logName in logNames:

            if not re.findall(r"\.", logName):
                logName=logName + '.'

            preFix, proFix = logName.split(".")

            try:
                # Create log DataFrame for final test log
                log = pd.read_csv(product['path']+logName, header=None)

                # Retrieve ICCID (Shipping sn report)
                snReport.retrieve_value('SIM ICCID', log, 'ICCID')

                # Retrieve, IMSI (Shipping sn report)
                snReport.retrieve_value('SIM IMSI', log, 'IMSI')

                # Retrieve IMEI (Shipping sn report)
                snReport.retrieve_value('LTE MODULE:', log, 'IMEI')

                # fill color in sn report (Shipping sn report)
                snReport.data['Color'] += [product['name'].split('-')[1]]

                # fill customer model name in sn report (Shipping sn report)
                snReport.data['Model'] += [product['bitkeyPN']]
                # fill current time in sn report (Shipping sn report)
                snReport.data['Time'] += [datetime.datetime.now().strftime('%Y%m%d%H%M%S')]

                # Test Time (final report)
                finalReport.retrieve_value('Test Time:', log, 'Test Time')

                # MAC#
                macValue = finalReport.retrieve_value('DUT MAC:', log, 'DUT MAC')

                # retrieve carton number
                try:
                    mask = serialTable['MAC'] == macValue
                    cartonNo = serialTable[mask]['Carton No'].values[0]
                    snReport.data['Carton No.'] += [cartonNo]
                except:
                    snReport.data['Carton No.'] += ['No Data Error']

                # SN
                try:
                    mask = serialTable['MAC'] == macValue
                    serialValue = serialTable[mask]['SN'].values[0]
                    finalReport.data['DUT SN'] += [serialValue]
                    snReport.data['SN'] += [serialValue]
                except:
                    finalReport.data['DUT SN'] += ['No Match on Serial Table']
                    snReport.data['SN'] += ['No Match on Serial Table, check log file: {log}'.format(log=logName)]

                # Retrieve Detected device comport
                try:
                    detail = finalReport.get_mask_value('Detected device comport=COM', log)
                    if len(detail[0]) > 0:
                        finalReport.data['Detect device and comport'] += ['PASS']
                    else:
                        finalReport.data['Detect device and comport'] += ['FAIL']
                except:
                    finalReport.data['Detect device and comport'] += ['FAIL']

                # BLE firmware
                finalReport.check_function('ble bicmd2 072b', product, log, 'BLE firmware')

                # Firmware version
                try:
                    major = finalReport.retrieve_value('Major:', log)
                    minor = finalReport.retrieve_value('Minor:', log)
                    patch = finalReport.retrieve_value('Patch:', log)
                    fwVersion = str(major) + '.' + str(minor) + '.' + patch
                    finalReport.data['FW Version'] += [fwVersion]
                except:
                    finalReport.data['FW Version'] += ['UNKNOWN']

                # Retrieve Application version (final test report)
                finalReport.retrieve_value('Application Version:', log, 'Application Version_FT2')
                # FW final check
                finalReport.check_function('Test Check Firmware PASS', product, log, 'FW Final Check')
                # Check LTE Information
                finalReport.check_function('Test Check LTE Information PASS', product, log, 'Check LTE Information')
                # Check WIFI function
                finalReport.check_function('Test Set WiFi Information PASS', product, log, 'WIFI function')

                print('file "{product}" succeeded to generate "final test" report.'.format(product=logName))

            except Exception as e:
                print(logName + ' fail: Read file fail')
                print(e)
    except:
        print('file "{product}" fail to generate "final test" report.'.format(product=file))

    # Export Final Test report
    targetDir = "finalTestReport"
    fileName = "finalTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['name'])
    finalReport.generate_report(product, targetDir, fileName)

    # Export shipping SN Report
    targetDir = "shippingSNReport"
    fileName = "serial_{product}.csv".format(product=product['bitkeyPN'])
    snReport.generate_report(product, targetDir, fileName)

    # Function test data fields, and generate function test report (funcData)
    print('*'*50 + '\nstart generating {product} function test rerport\n'.format(product=product['name']) + '*'*2)

    funcData = {
        'Application Version_FT1': [],
        'DUT SN': [],
        'DUT MAC': [],
        'Detect device and comport': [],
        'Burn BLE': [],
        'SOC version': [],
        'Test Check Firmware': [],
        'Test LTE Connection': [],
        'Test WIFI connection': [],
        'Test BLE': [],
        'Test LED': [],
        'Test Button': [],
        'Format': [],
    }

    funcReport = Report(product, funcData)

    try:
        for funcLogName in funcLogNames:
            if not re.findall(r"\.", funcLogName):
                funcLogName=funcLogName + '.'

            preFix, proFix = funcLogName.split(".")

            try:
                funcLog = pd.read_csv(product['path']+funcLogName, header=None)
                # Retrieve Application version

                try:
                    detail = funcReport.get_mask_value('Application Version:', funcLog)[0]
                    _, version = detail.split(':')
                    value = version.replace(' ', '')
                    funcReport.data['Application Version_FT1'] += [value]
                except:
                    funcReport.data['Application Version_FT1'] += ['Unknown']

                # Retrieve Detected device comport

                try:
                    detail = funcReport.get_mask_value('Detected device comport=COM', funcLog)
                    if len(detail[0])>0:
                        funcReport.data['Detect device and comport'] += ['PASS']
                    else:
                        funcReport.data['Detect device and comport'] += ['FAIL']
                except:
                    funcData['Detect device and comport'] += ['FAIL']

                # Check BLE burn
                funcReport.check_function('[Burn BLE]',product, funcLog, 'Burn BLE')

                # Retrieve SOC version and check if it matches production version
                try:
                    detail = funcReport.get_mask_value('SOC version', funcLog)[0]
                    vut, productionVersion = re.findall(r"v\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}", detail)
                    if vut == productionVersion:
                        funcReport.data['SOC version'] += [vut]
                    else:
                        funcReport.data['SOC version'] += ['FAIL']
                except:
                    funcReport.data['SOC version'] += ['FAIL']

                # Test check firmware
                funcReport.check_function('Test Check Firmware PASS',product, funcLog, 'Test Check Firmware')

                # Test LTE connection
                funcReport.check_function('Test LTE Connection: PASS',product, funcLog, 'Test LTE Connection')

                # 'Test WIFI connection'
                funcReport.check_function('Test WiFi Connection: PASS',product, funcLog, 'Test WIFI connection')

                # Test BLE
                funcReport.check_function('Test BLE Echo: PASS',product, funcLog, 'Test BLE')

                # 'Test LED'
                funcReport.check_function('TEST LED PASS',product , funcLog, 'Test LED')

                # 'Test Button'
                funcReport.check_function('Test Button: PASS', product, funcLog, 'Test Button')

                # 'Format'
                funcReport.check_function('formating...', product, funcLog, 'Format')

                # MAC & SN number

                try:
                    detail = funcReport.get_mask_value('Create BD Address file with', funcLog)[0].split(' ')
                    macValue = detail[-1]
                    funcReport.data['DUT MAC'] += [macValue]
                    try:
                        mask = serialTable['MAC'] == macValue
                        serialValue = serialTable[mask]['SN'].values[0]
                        funcReport.data['DUT SN'] += [serialValue]
                    except:
                        funcReport.data['DUT SN'] += ['No Match on Serial Table']
                except:
                    funcReport.data['DUT MAC'] += ['LogError. check log file: {logName}'.format(logName=funcLogName)]
                    funcReport.data['DUT SN'] += ['MAC# not found']

                print('file "{product}" succeeded to generate "Function test" report.'.format(product=funcLogName))

            except Exception as e:
                print(funcLogName + ' fail: Read file fail')
                print(e)

    except Exception as e:
        print('file "{product}" fail to generate "function test" report.'.format(product=file))

    print('\n' * 3 + '-' * 50 + '\n{product} section done\n'.format(product=product['name'])+ '-' * 50 + '\n' * 2)

    targetDir = "functionTestReport"
    fileName = "functionTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'),
                                                                 product=product['name'])
    funcReport.generate_report(product, targetDir, fileName)

    # Combine function test and final test as combinedReport and save to combinedReport dir
    print('\n' * 3 + '-' * 50 + '\nStart combining {product} "final test" and "function test" Report ...\n'.format(product=product['name']) + '-' * 50)
    df_combine = pd.merge(finalReport.generate_df(), funcReport.generate_df(), how='outer', suffixes=['_final', '_function'])
    targetDir = "combinedReport"
    fileName = "FTReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['bitkeyPN'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    df_combine.to_excel(os.path.join(targetDir, fileName))
    print('\n' * 3 + '===' * 50 + '\n{product} combinedReport(final + function) generated\n'.format(product=product['name']) + '====' * 50)

    input('***'*20 + "\nFollowing {product}'s reports have been generated".format(product=product['name']) + '\nFinal Test report: {final}'.format(final=len(data['DUT MAC'])) + '\nFunction Test report: {func}'.format(func=len(funcData['DUT MAC'])) + '\nPress Enter key to close this console window ...')

    product['qtyFuncRep'] = '{product} FT1: {files} logs in folder | {funcData} data in report'.format(
        files=len(funcLogNames), funcData=len(funcData['DUT MAC']), product=product['name'])
    product['qtyFinRep'] = '{product} FT2: {files} logs in folder | {data} data in report'.format(
        files=len(logNames), data=len(data['DUT MAC']), product=product['name'])

# Export result to working dir
currentTime = datetime.datetime.now().strftime('%Y%m%d%H')
fName = 'logClassifyReport_{currentTime}.txt'.format(currentTime=currentTime)

f = open(fName, 'w+')
f.write('Tool Version: {version} ({sub})\n'.format(version=toolVersion, sub=list(releaseNote.keys())[0]))
f.write('Release Note:\n{releaseNote}\n'.format(releaseNote=str(releaseNote[toolVersion]))+'='*50 +'\n')
for product in products:
    f.write(product['qtyFuncRep']+'\n')
    f.write(product['qtyFinRep']+'\n')
f.close()

