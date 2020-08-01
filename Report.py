import pandas as pd
import os
import datetime
import re


class Report:

    def __init__(self, product: dict, data: dict):
        self.data = data
        self.product = product

    def get_mask_value(self, condition, log):
        mask = log[0].str.startswith(condition)
        return log[mask].values[0]

    def retrieve_value(self,condition, data, log, contentToFill=''):
        try:
            detail = self.get_mask_value(condition, log)[0]
            _, version = detail.split(':')
            value = version.replace(' ', '')
            if contentToFill != '':
                data[contentToFill] += [value]
            return value
        except Exception as e:
            if contentToFill != '':
                data[contentToFill] += ['N/A']
            return e

    def check_function(self, logContent, product, data, log, contentToFill):
        print(self, logContent, contentToFill)
        try:
            duc = self.get_mask_value(logContent, log)[0]
            print(duc)
            if duc and duc != '':
                data[contentToFill] += ['PASS']
            else:
                if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (
                        contentToFill == 'Check LTE Information')) or (
                        (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')) or (
                        (len(re.findall(r'^WIFI', product['name'])) > 0) and (
                        contentToFill == 'Test LTE Connection')) or (
                        (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                    data[contentToFill] += ['N/A']

                else:
                    data[contentToFill] += ['FAIL']
        except:
            if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Check LTE Information')) or (
                    (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')) or (
                    (len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Test LTE Connection')) or (
                    (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                data[contentToFill] += ['N/A']

            else:
                data[contentToFill] += ['FAIL']

    def generate_df(self, data):
        return pd.DataFrame.from_dict(data, orient='index').T

    def generate_report(self, product, data, targetDir, fileName ):
        targetDir = targetDir
        fileName = "{fileName}t_{product}_{date}.xlsx".format(
            date=datetime.datetime.now().strftime('%Y%m%d%H'),
            product=product['bitkeyPN'],
            fileName=fileName
        )
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)
        df = self.generate_df(data)
        df.to_excel(os.path.join(targetDir, fileName))

