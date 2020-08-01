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

    def retrieve_value(self,condition, log, contentToFill=''):
        try:
            detail = self.get_mask_value(condition, log)[0]
            _, version = detail.split(':')
            value = version.replace(' ', '')
            if contentToFill != '':
                self.data[contentToFill] += [value]
            return value
        except Exception as e:
            if contentToFill != '':
                self.data[contentToFill] += ['N/A']
            return e

    def check_function(self, logContent, product, log, contentToFill):
        try:
            duc = self.get_mask_value(logContent, log)[0]
            if duc and duc != '':
                self.data[contentToFill] += ['PASS']
            else:
                if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (
                        contentToFill == 'Check LTE Information')) or (
                        (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')) or (
                        (len(re.findall(r'^WIFI', product['name'])) > 0) and (
                        contentToFill == 'Test LTE Connection')) or (
                        (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                    self.data[contentToFill] += ['N/A']

                else:
                    self.data[contentToFill] += ['FAIL']
        except:
            if ((len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Check LTE Information')) or (
                    (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'WIFI function')) or (
                    (len(re.findall(r'^WIFI', product['name'])) > 0) and (contentToFill == 'Test LTE Connection')) or (
                    (len(re.findall(r'^LTE', product['name'])) > 0) and (contentToFill == 'Test WIFI connection')):
                self.data[contentToFill] += ['N/A']

            else:
                self.data[contentToFill] += ['FAIL']

    def generate_df(self):
        return pd.DataFrame.from_dict(self.data, orient='index').T

    def generate_report(self, product, targetDir, fileName ):
        targetDir = targetDir
        fileName = "{fileName}t_{product}_{date}.xlsx".format(
            date=datetime.datetime.now().strftime('%Y%m%d%H'),
            product=product['bitkeyPN'],
            fileName=fileName
        )
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)
        df = self.generate_df()
        df.to_excel(os.path.join(targetDir, fileName))

