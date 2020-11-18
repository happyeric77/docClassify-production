import pandas as pd
import os
import datetime
import re
import numpy as np
import tkinter as tk
from tkinter import messagebox


class Report:
    def __init__(self, product: dict, data: dict):
        self.data = data
        self.product = product

    def get_mask_value(self, condition, log):
        mask = log[0].str.startswith(condition)
        if len(log[mask].values) > 1:
            outputValue = log[mask].values[-1]
        else:
            outputValue = log[mask].values[0]
        return outputValue

    def retrieve_value(self,condition, log, contentToFill=''):
        try:
            detail = self.get_mask_value(condition, log)[0]
            _, version = detail.split(':')
            try:
                value = version.replace(' ', '')
                # if it is ICCID, retrieve only 19 digits
                try:
                    value = re.findall(r'\d{19}', value)[0]
                except:
                    pass
            except:
                value = version
                # if it is ICCID, retrieve only 19 digits
                try:
                    value = re.findall(r'\d{19}', value)[0]
                except:
                    pass

            if contentToFill != '':
                self.data[contentToFill] += [str(value)]
            return str(value)
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
        df = pd.DataFrame.from_dict(self.data, orient='index').T

        return pd.DataFrame.from_dict(self.data, orient='index').T

    def combine_df(self, dfToCombine, on, suffixSelf, suffixTocombine, sortBy=None):
        currentDf = self.generate_df()
        dfToCombine = dfToCombine
        df_combine = pd.merge(currentDf, dfToCombine, on=on, how='outer',
                              suffixes=[suffixSelf, suffixTocombine])

        try:
            if sortBy:
                df_combine = df_combine.sort_values(sortBy)
                df_combine.index = np.arange(1, len(df_combine) + 1)
        except Exception as e:
            print('sort combined report dataframe fail, detail: ' + str(e))
            df_combine.index = np.arrange(1, len(df_combine) + 1)

        try:
            df_combine = df_combine.drop(columns=['DUT SN' + suffixTocombine])
        except Exception as e:
            print('Fail to drop unneeded field in combine_df class. Detail: ' + str(e))
        return df_combine

    def generate_report(self, product, targetDir, fileName, fileType='xlsx', sortBy=None):
        targetDir = targetDir
        fileName = "{fileName}_{product}_{date}.{fileType}".format(
            date=datetime.datetime.now().strftime('%Y%m%d%H'),
            product=product['bitkeyPN'],
            fileName=fileName,
            fileType=fileType
        )
        if not os.path.exists(targetDir):
            os.mkdir(targetDir)
        try:
            if sortBy:
                df = self.generate_df().sort_values(sortBy)
                df.index = np.arange(1, len(df) + 1)
            else:
                df = self.generate_df()
                df.index = np.arange(1, len(df) + 1)
        except Exception as e:
            df = self.generate_df()
            df.index = np.arange( 1, len(df) + 1)
            print('sort report dataframe fail, detail: ' + str(e))

        if fileType == 'csv':
            df.to_csv(os.path.join(targetDir, fileName))
        else:
            df.to_excel(os.path.join(targetDir, fileName))

    def remove_unmatched(self, df_remove, column, content, targetDir, fileName):
        root = tk.Tk()
        root.geometry('300x200')
        def yes():
            try:
                print(df_remove)
                mask = ~ df_remove[column].str.contains(content).fillna(False)
                print(mask)
                df = df_remove[mask]
                print(df)
                df.to_csv(os.path.join(targetDir, fileName))
            except:
                pass
            root.destroy()

        def no():
            root.destroy()
            pass

        label = tk.Label(root, text='Do you want to delete unmatched SN data')
        label.pack()
        buttonYes = tk.Button(root, text='Yes', command=yes)
        buttonYes.pack()
        buttonYes.pack()
        buttonNo = tk.Button(root, text='No', command=no)
        buttonNo.pack()
        root.mainloop()

