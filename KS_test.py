import random
from numpy.lib.shape_base import split
from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

print('請選擇讀取資料的方式: (1)手動輸入 (2)從檔案讀取')
input_desicion = input()

ideal_data = []
real_data = []
total_average_people_in_one_hour = []
str = []
days_result = []

if input_desicion == '1':
    print('選擇手動輸入......')
    print('請輸入KS-test的時間範圍: (1)一個月 (2)一天')
    time_scale = input()
    if time_scale == '1':
        print("請輸入天數:")
        days = int(input())
        print("請開始輸入每天的結果(用換行的方式輸入，1代表過勞，0代表沒有過勞):")
        for i in range(days):
            result = int(input())
            days_result.append(result)
        averahe_result = statistics.mean(days_result)
        if averahe_result >= 0.5 :
            print("該月份的結果為 過勞")
        else :
            print("該月份的結果為 沒有過勞")
    elif time_scale == '2':
        print("請輸入當天日期(yyyy/mm/dd):")
        date = input()
        print("請選擇要寫入結果的檔案:")
        f_write = open(input(),'a')
        print("請選擇是否考慮人數的權重: (1)是 (2)否")
        weight_desicion = input()
        if weight_desicion == '1':
            print('請輸入有多少筆資料:')
            number = int(input())
            print('請開始輸入資料(資料請以換行的方式輸入):')
            for i in range(number):
                single_data = float(input())
                real_data.append(single_data)
            print('請輸入理想狀況的時間:')
            ideal_times = float(input())
            print('請輸入理想狀況的標準差:')
            ideal_sigma = float(input())
            print('請輸入alpha值:')
            alpha = float(input())
            print('請輸入理想狀況的人數:')
            ideal_person = int(input())
            for i in range(number):
                x = random.gauss(mu=ideal_person*ideal_times, sigma=ideal_sigma)
                ideal_data.append(x)
            statistic,pvalue=ks_2samp(real_data, ideal_data)
            #print('p-value的值為: {0}'.format(pvalue))
            if pvalue < alpha :
                print('p-value 為 {0} 小於 alpha {1}，結果為 過勞'.format(round(pvalue,2),alpha))
                if_overwork = 1
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            elif pvalue >= alpha :
                print('p-value 為 {0} 不小於 alpha {1}，結果為 沒有過勞'.format(round(pvalue,2),alpha))
                if_overwork = 0
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            plt.figure(figsize=(8,4),dpi=100)
            sns.distplot(real_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightcoral", "lw":1.5, 'linestyle':'--'},
            rug_kws={'color':'lightcoral','alpha':1, 'lw':2,}, label='real data distribution')
            sns.distplot(ideal_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightseagreen", "lw":1.5, 'linestyle':'-'},
            rug_kws={'color':'lightseagreen','alpha':1, 'lw':2,}, label='ideal data distribution')
            plt.title(("Fishmen Working Times Distribution"))
            plt.ylabel("Probability Density") # y label
            plt.xlabel("Weighted Working Times per Hour") # x label
            plt.show()
        elif weight_desicion == '2':
            print('請輸入有多少筆資料:')
            number = int(input())
            print('請開始輸入資料(資料請以換行的方式輸入):')
            for i in range(number):
                single_data = float(input())
                real_data.append(single_data)
            print('請輸入理想狀況的時間:')
            ideal_times = float(input())
            print('請輸入理想狀況的標準差:')
            ideal_sigma = float(input())
            print('請輸入alpha值:')
            alpha = float(input())
            for i in range(number):
                x = random.gauss(mu=ideal_times, sigma=ideal_sigma)
                ideal_data.append(x)
            statistic,pvalue=ks_2samp(real_data, ideal_data)
            #print('p-value的值為: {0}'.format(pvalue))
            if pvalue < alpha :
                print('p-value 為 {0} 小於 alpha {1}，結果為 過勞'.format(round(pvalue,2),alpha))
                if_overwork = 1
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            elif pvalue >= alpha :
                print('p-value 為 {0} 不小於 alpha {1}，結果為 沒有過勞'.format(round(pvalue,2),alpha))
                if_overwork = 0
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            plt.figure(figsize=(8,4),dpi=100)
            sns.distplot(real_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightcoral", "lw":1.5, 'linestyle':'--'},
            rug_kws={'color':'lightcoral','alpha':1, 'lw':2,}, label='real data distribution')
            sns.distplot(ideal_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightseagreen", "lw":1.5, 'linestyle':'-'},
            rug_kws={'color':'lightseagreen','alpha':1, 'lw':2,}, label='ideal data distribution')
            plt.title(("Fishmen Working Times Distribution"))
            plt.ylabel("Probability Density") # y label
            plt.xlabel("Working Times per Hour") # x label
            plt.show()
    
elif input_desicion == '2':
    number = 0
    print('選擇從檔案讀取......')
    print('請輸入欲讀取的檔案名稱:')
    path_name = input()
    f = open(path_name,"r")

    print('請輸入KS-test的時間範圍: (1)一個月 (2)一天')
    time_scale = input()
    if time_scale == '2':
        print("請輸入當天日期(yyyy/mm/dd):")
        date = input()
        print("請選擇要寫入結果的檔案:")
        f_write = open(input(),'a')
        print("請選擇是否考慮人數的權重: (1)是 (2)否")
        weight_desicion = input()
        if weight_desicion == '1':
            for line in f.readlines():
                if "Weighted times in one hour" in line :
                    str = line.split(' ')
                    real_data.append(float(str[6]))
                    number = number + 1
                elif "Average people in one hour" in line :
                    str = line.split(' ')
                    total_average_people_in_one_hour.append(int(str[6]))
            #print("number : {0}".format(number))
            #print(real_data)
            ideal_person = statistics.mean(total_average_people_in_one_hour)
            print('請輸入理想狀況的時間:')
            ideal_times = float(input())
            print('請輸入理想狀況的標準差:')
            ideal_sigma = float(input())
            print('請輸入alpha值:')
            alpha = float(input())
            for i in range(number):
                x = random.gauss(mu=ideal_person*ideal_times, sigma=ideal_sigma)
                ideal_data.append(x)
            #print(ideal_data)
            statistic,pvalue=ks_2samp(real_data, ideal_data)
            #print('p-value的值為: {0}'.format(pvalue))
            if pvalue < alpha :
                print('p-value 為 {0} 小於 alpha {1}，結果為 過勞'.format(round(pvalue,2),alpha))
                if_overwork = 1
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            elif pvalue >= alpha :
                print('p-value 為 {0} 不小於 alpha {1}，結果為 沒有過勞'.format(round(pvalue,2),alpha))
                if_overwork = 0
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            plt.figure(figsize=(8,4),dpi=100)
            sns.distplot(real_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightcoral", "lw":1.5, 'linestyle':'--'},
            rug_kws={'color':'lightcoral','alpha':1, 'lw':2,}, label='real data distribution')
            sns.distplot(ideal_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightseagreen", "lw":1.5, 'linestyle':'-'},
            rug_kws={'color':'lightseagreen','alpha':1, 'lw':2,}, label='ideal data distribution')
            plt.title(("Fishmen Working Times Distribution"))
            plt.ylabel("Probability Density") # y label
            plt.xlabel("Weighted Working Times per Hour") # x label
            plt.show()
        elif weight_desicion == '2':
            for line in f.readlines():
                if "Total people appears in times during one hours" in line :
                    str = line.split(' ')
                    real_data.append(float(str[9]))
                    number = number + 1
            #print("number : {0}".format(number))
            #print(real_data)
            ideal_person = 1
            print('請輸入理想狀況的時間:')
            ideal_times = float(input())
            print('請輸入理想狀況的標準差:')
            ideal_sigma = float(input())
            print('請輸入alpha值:')
            alpha = float(input())
            for i in range(number):
                x = random.gauss(mu=ideal_person*ideal_times, sigma=ideal_sigma)
                ideal_data.append(x)
            #print(ideal_data)
            statistic,pvalue=ks_2samp(real_data, ideal_data)
            #print('p-value的值為: {0}'.format(pvalue))
            if pvalue < alpha :
                print('p-value 為 {0} 小於 alpha {1}，結果為 過勞'.format(round(pvalue,2),alpha))
                if_overwork = 1
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            elif pvalue >= alpha :
                print('p-value 為 {0} 不小於 alpha {1}，結果為 沒有過勞'.format(round(pvalue,2),alpha))
                if_overwork = 0
                f_write.write("{0} : {1}\n".format(date,if_overwork))
            plt.figure(figsize=(8,4),dpi=100)
            sns.distplot(real_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightcoral", "lw":1.5, 'linestyle':'--'},
            rug_kws={'color':'lightcoral','alpha':1, 'lw':2,}, label='real data distribution')
            sns.distplot(ideal_data, hist=False, kde=True, rug=True,
            kde_kws={"color":"lightseagreen", "lw":1.5, 'linestyle':'-'},
            rug_kws={'color':'lightseagreen','alpha':1, 'lw':2,}, label='ideal data distribution')
            plt.title(("Fishmen Working Times Distribution"))
            plt.ylabel("Probability Density") # y label
            plt.xlabel("Working Times per Hour") # x label
            plt.show()
    elif time_scale == '1':
        for line in f.readlines():
            str = line.split(' ')
            days_result.append(int(str[2]))
        averahe_result = statistics.mean(days_result)
        if averahe_result >= 0.5 :
            print("該月份的結果為 過勞")
        else :
            print("該月份的結果為 沒有過勞")