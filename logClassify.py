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
    print('create sn table')
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

print(serialTable)

products = [lteBlack, lteGrey, wifiBlack, wifiGrey]


for product in products:

    logNames = os.listdir(product['path'])

    LTEinfo = {}
    data = {}

    try:
        for logName in logNames:

            if not re.findall(r"\.", logName):
                logName=logName + '.'

            preFix, proFix = logName.split(".")


            fwVersion = ''
            try:
                log = pd.read_csv(product['path']+logName, header=None, delimiter=':')
                keys = log[0].values

                if len(re.findall(r"WIFI", product['name']))>0:
                    print(re.findall(r"WIFI", product['name']))
                    keys = numpy.append(keys, ['SIM ICCID','SIM IMSI','LTE MODULE','Test Check LTE Information PASS'])
                    # print(keys)

                else:
                    print(re.findall(r"LTE", product['name']))



                for key in keys:

                    # Application version
                    if key == 'Application Version':
                        value = log[log[0] == key][1].values[0]

                    # test time
                    elif key == 'Test Time':
                        value = log[log[0] == key][1].values[0]

                    # SN#
                    elif key == 'DUT SN':
                        # get original MAC number
                        value = log[log[0] == key][1].values[0].replace(' ', '')
                        # search SN number Table for matching SN number, if not exist, show No Matching error
                        try:
                            serialNumber = serialTable[serialTable[0] == value][1].values[0]
                            value = serialNumber
                        except Exception as e:
                            value = 'No Matching data in the SN table'

                    # MAC
                    elif key == 'DUT MAC':
                        value = log[log[0] == key][1].values[0]

                    # Detect device and comport
                    elif key =='Detect device and comport':
                        value = 'Pass'

                    elif len(re.findall(r"^Detected device comport", key))>0:
                        value = 'Detected'
                        key = 'Detected device comport'

                    # Check Firmware version
                    elif len(re.findall(r"072b", key))>0:
                        value = 'FW checked'
                        key = 'BLE firmware'
                    # Get fw Major version
                    elif key == 'Major':
                        fwVersion += str(log[log[0] == key][1].values[0])
                        key = 'Na'
                    # Get fw Minor version
                    elif key == 'Minor':
                        fwVersion += str(log[log[0] == key][1].values[0])
                        key = 'Na'
                    # Get fw patch version
                    elif key == 'Patch':
                        fwVersion += str(log[log[0] == key][1].values[0])
                        fwVersion = fwVersion.replace(' ' , '.')
                        if fwVersion == '.1.0.15':
                            value = fwVersion
                            key = 'FW Version'
                    # Test Check Firmware PASS
                    elif key == 'Test Check Firmware PASS' and fwVersion == '.1.0.15':
                        value = 'Pass'
                        key = 'FW Final Check'

                    # below test items are different according to WIFI or LTE device

                    #LTE functions
                    # Retrieving SIM ICCID
                    elif key == 'SIM ICCID':
                        ICCID = str(log[log[0] == key][1].values[0]).replace(' ','')
                        if len(ICCID) == 20:
                            LTEinfo['SIM ICCID'] = ICCID
                        key = 'Na'

                    # Retrieving SIM IMSI
                    elif key == 'SIM IMSI':
                        IMSI = str(log[log[0] == key][1].values[0]).replace(' ','')
                        if IMSI and len(IMSI) == 15:
                            LTEinfo['SIM IMSI'] = IMSI
                        key = 'Na'

                    # Retrieving LTE MODULE#
                    elif key == 'LTE MODULE':
                        LTE = str(log[log[0] == key][1].values[0]).replace(' ','')
                        if LTE and len(LTE) == 15:
                            LTEinfo['LTE MODULE'] = LTE
                        key = 'Na'

                    # Check LTE Information
                    elif key == 'Test Check LTE Information PASS' and LTEinfo['LTE MODULE'] and LTEinfo['SIM IMSI'] and LTEinfo['SIM ICCID']:
                        value = 'Pass'
                        key = 'Check LTE Information'


                    else:
                        key = 'Na'
                        value = None

                    # add into current list
                    try:
                        preData = [i for i in data[key]]
                        newData = preData + [value]
                        data[key] = newData
                    except:
                        data[key] = [value]
            except Exception as e:
                print(logName + ' fail: Read file fail')
                print(e)
    except:
        print('fail')

    del data['Na']

    targetDir = "modifiedFile"
    fileName = "finalTestReport_{product}_{date}.xlsx".format(date=datetime.datetime.now().strftime('%Y%m%d%H'), product=product['name'])
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    pd.DataFrame.from_dict(data).to_excel(os.path.join(targetDir, fileName))