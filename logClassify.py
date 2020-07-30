import pandas as pd
import os
import datetime
import re

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
wifiGrey = {'path': currentPath + '/98B-500-0012R-WIFI_1A.G-99B-500-0005R/', 'name': 'WIFI-Grey'}

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
        func=len(funcLogNames)) + '\nEnter any key to go on ...')

    # Final test data fields, and generate final test report
    print('*' * 50 + '\nStart generating "{product}" final test rerport. \n'.format(product=product['name']) + '*' * 50)

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

            def get_mask_value(condition):
                mask =log[0].str.startswith(condition)
                return log[mask].values[0]

            def check_function(logContent, contentToFill):
                try:
                    duc = get_mask_value(logContent)[0]
                    if duc and duc != '':
                        data[contentToFill] += ['PASS']
                    else:
                        if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Check LTE Information')) or ((len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')):
                            data[contentToFill] += ['N/A']
                        else:
                            data[contentToFill] += ['FAIL']
                except:
                    if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Check LTE Information')) or ((len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')):
                        data[contentToFill] += ['N/A']
                    else:
                        data[contentToFill] += ['FAIL']

            def retrieve_value(condition, contentToFill=''):
                try:
                    detail = get_mask_value(condition)[0]
                    _, version = detail.split(':')
                    value = version.replace(' ', '')
                    if contentToFill != '':
                        data[contentToFill] += [value]
                    return value
                except Exception as e:
                    if contentToFill != '':
                        data[contentToFill] += ['UNKNOWN']
                    return e

            try:
                log = pd.read_csv(product['path']+logName, header=None)
                # Retrieve Application version
                retrieve_value('Application Version:', 'Application Version')

                # Test Time
                retrieve_value('Test Time:', 'Test Time')

                # MAC#
                macValue = retrieve_value('DUT MAC:', 'DUT MAC')

                # SN
                try:
                    mask = serialTable[0] == macValue
                    serialValue = serialTable[mask][1].values[0]
                    data['DUT SN'] += [serialValue]
                except:
                    data['DUT SN'] += ['No Match on Serial Table']

                # Retrieve Detected device comport
                try:
                    detail = get_mask_value('Detected device comport=COM')
                    if len(detail[0]) > 0:
                        data['Detect device and comport'] += ['PASS']
                    else:
                        data['Detect device and comport'] += ['FAIL']
                except:
                    data['Detect device and comport'] += ['FAIL']

                # BLE firmware
                check_function('ble bicmd2 072b', 'BLE firmware')

                # Firmware version
                try:
                    major = retrieve_value('Major:')
                    minor = retrieve_value('Minor:')
                    patch = retrieve_value('Patch:')
                    fwVersion = str(major) + '.' + str(minor) + '.' + patch
                    data['FW Version'] += [fwVersion]
                except:
                    data['FW Version'] += ['UNKNOWN']
                # FW final check
                check_function('Test Check Firmware PASS', 'FW Final Check')
                # Check LTE Information
                check_function('Test Check LTE Information PASS', 'Check LTE Information')
                # Check WIFI function
                check_function('Test Set WiFi Information PASS', 'WIFI function')

                print('file "{product}" succeeded to generate "final test" report.'.format(product=logName))

            except Exception as e:
                print(logName + ' fail: Read file fail')
                print(e)
    except:
        print('file "{product}" fail to generate "final test" report.'.format(product=file))

    targetDir = "finalTestReport"
    fileName = "finalTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['name'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    df_final = pd.DataFrame.from_dict(data, orient='index').T
    df_final.to_excel(os.path.join(targetDir, fileName))

    # Function test data fields, and generate function test report
    print('*'*50 + '\nstart generating {product} function test rerport\n'.format(product=product['name']) + '*'*2)

    funcData = {
        'Application Version': [],
        'DUT SN': [],
        'DUT MAC': [],
        'Detect device and comport': [],
        'Burn BLE': [],
        'SOC version': [],
        'BLE version': [],
        'Test Check Firmware': [],
        'Test LTE Connection': [],
        'Test WIFI connection': [],
        'Test BLE': [],
        'Test LED': [],
        'Test Button': [],
        'Format': [],
    }

    try:
        for funcLogName in funcLogNames:

            if not re.findall(r"\.", funcLogName):
                funcLogName=funcLogName + '.'

            preFix, proFix = funcLogName.split(".")

            def get_mask_value(condition):
                mask = funcLog[0].str.startswith(condition)
                return funcLog[mask].values[0]

            def check_function(logContent, contentToFill):
                try:
                    duc = get_mask_value(logContent)[0]
                    if duc and duc != '':
                        funcData[contentToFill] += ['PASS']
                    else:
                        if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Test LTE Connection')) or ((len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                            funcData[contentToFill] += ['N/A']
                        else:
                            funcData[contentToFill] += ['FAIL']
                except:
                    if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Test LTE Connection')) or ((len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                        funcData[contentToFill] += ['N/A']
                    else:
                        funcData[contentToFill] += ['FAIL']

            try:
                funcLog = pd.read_csv(product['path']+funcLogName, header=None)
                # Retrieve Application version
                try:
                    detail = get_mask_value('Application Version:')[0]
                    _, version = detail.split(':')
                    value = version.replace(' ', '')
                    funcData['Application Version'] += [value]
                except:
                    funcData['Application Version'] += ['Unknown']

                # Retrieve Detected device comport
                try:
                    detail = get_mask_value('Detected device comport=COM')
                    if len(detail[0])>0:
                        funcData['Detect device and comport'] += ['PASS']
                    else:
                        funcData['Detect device and comport'] += ['FAIL']
                except:
                    funcData['Detect device and comport'] += ['FAIL']

                # Check BLE burn
                check_function('[Burn BLE]', 'Burn BLE')

                # Retrieve SOC version and check if it matches production version
                try:
                    detail = get_mask_value('SOC version')[0]
                    vut, productionVersion = re.findall(r"v\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}", detail)
                    if vut == productionVersion:
                        funcData['SOC version'] += [vut]
                    else:
                        funcData['SOC version'] += ['FAIL']
                except:
                    funcData['SOC version'] += ['FAIL']

                # Retrieve BLE version and check if it matches production version
                try:
                    detail = get_mask_value('BLE version')[0]
                    vut, productionVersion = re.findall(r"v\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}", detail)
                    if vut == productionVersion:
                        funcData['BLE version'] += [vut]
                    else:
                        funcData['BLE version'] += ['FAIL']
                except:
                    funcData['BLE version'] += ['FAIL']

                # Test check firmware
                check_function('Test Check Firmware PASS', 'Test Check Firmware')

                # Test LTE connection
                check_function('Test LTE Connection: PASS', 'Test LTE Connection')

                # 'Test WIFI connection'
                check_function('Test WiFi Connection: PASS', 'Test WIFI connection')

                # Test BLE
                check_function('Test BLE Echo: PASS', 'Test BLE')

                # 'Test LED'
                check_function('TEST LED PASS', 'Test LED')

                # 'Test Button'
                check_function('Test Button: PASS', 'Test Button')

                # 'Format'
                check_function('formating...', 'Format')

                # MAC# & SN
                try:
                    detail = get_mask_value('Create BD Address file with')[0].split(' ')
                    macValue = detail[-1]
                    mask = serialTable[0]==macValue
                    serialValue = serialTable[mask][1].values[0]
                    funcData['DUT SN'] += [serialValue]
                    funcData['DUT MAC'] += [macValue]
                except:
                    funcData['DUT MAC'] += ['UNKNOWN']
                    funcData['DUT SN'] += ['No Match on Serial Table']


                print('file "{product}" succeeded to generate "Function test" report.'.format(product=funcLogName))

            except Exception as e:
                print(funcLogName + ' fail: Read file fail')
                print(e)

    except Exception as e:
        print('file "{product}" fail to generate "function test" report.'.format(product=file))

    print('\n' * 3 + '-' * 50 + '\n{product} section done\n'.format(product=product['name'])+ '-' * 50 + '\n' * 2)

    targetDir = "functionTestReport"
    fileName = "functionTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['name'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    df_function = pd.DataFrame.from_dict(funcData, orient='index').T
    df_function.to_excel(os.path.join(targetDir, fileName))

    # Combine function test and final test as combinedReport and save to combinedReport dir
    print('\n' * 3 + '-' * 50 + '\nStart combining {product} "final test" and "function test" Report ...\n'.format(product=product['name']) + '-' * 50)
    df_combine = pd.merge(df_final, df_function, how='outer', suffixes=['_final', '_function'])
    targetDir = "combinedReport"
    fileName = "combinedTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'),
                                                                 product=product['name'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    df_combine.to_excel(os.path.join(targetDir, fileName))
    print('\n' * 3 + '===' * 50 + '\n{product} combinedReport(final + function) generated\n'.format(product=product['name']) + '====' * 50)

    input('***'*20 + "\nFollowing {product}'s reports have been generated".format(product=product['name']) + '\nFinal Test report: {final}'.format(final=len(data['DUT MAC'])) + '\nFunction Test report: {func}'.format(func=len(funcData['DUT MAC'])) + '\nEnter any key to go on ...')



