from js import sex, age, y1, y2

import pandas as pd

import pickle
with open('data_to_plot.pkl', 'rb') as f:
    data_to_plot = pickle.load(f)

import matplotlib.pyplot as plt
def plot(sex):
    morf = data_to_plot.loc[sex].loc[3:16]
    MorF = {'男': 'Male', '女': 'Female'}[sex]
    plt.fill_between(morf.index, morf['<lambda_4>'], morf['<lambda_3>'], color='red', alpha=0.6, label='90~100%')
    plt.fill_between(morf.index, morf['<lambda_3>'], morf['<lambda_2>'], color='orange', alpha=0.6, label='75~90%')
    plt.fill_between(morf.index, morf['<lambda_2>'], morf['<lambda_1>'], color='yellow', alpha=0.6, label='50~75%')
    plt.fill_between(morf.index, morf['<lambda_1>'], morf['<lambda_0>'], color='lightgreen', alpha=0.6, label='0~50%')
    plt.title(f'Axial Length Growth in {MorF} Taiwanese Children', fontsize=14)

risk = [...] * 4
risk[0] = '軸長在年齡正常範圍內，屬無/少風險，建議一年定期檢查，無潛在近視發展狀況。'
risk[1] = '軸長稍長於年齡正常範圍，屬低風險，建議一年定期檢查，需改變生活型態及減少外在環境影響。'
risk[2] = '軸長長於年齡正常範圍，屬中風險，建議半年回診檢查，需改變生活型態及減少外在環境影響（例：電腦及手機使用時間需要注意並適度休息、戶外活動需要配戴太陽眼鏡防藍光、UV），並搭配葉黃素或魚油服用。'
risk[3] = '軸長甚長於年齡正常範圍，屬高風險，有極高近視惡化發展可能，建議3個月回診檢查，需改變生活型態及減少外在環境影響（例：電腦及手機使用時間需要注意並適度休息、避免坐姿不正，戶外活動需要配戴太陽眼鏡防藍光、UV），搭配葉黃素或魚油服用，並搭配積極治療控制。'

import re
m = re.match('(\d+)歲(\d+)', age)
x = int(m.group(1)) + int(m.group(2)) / 12

if round(x) in range(3, 17):
    p0, p50, p75, p90, p100 = data_to_plot.loc[sex].loc[round(x)]
    y = max(y1, y2)
    if y < p50:
        print(risk[0])
    elif y < p75:
        print(risk[1])
    elif y < p90:
        print(risk[2])
    else:
        print(risk[3])
else:
    print('該年齡收案不足，無法提供具有統計意義之危險度分級。')

plot(sex)
if y1:
    plt.scatter(x, y1, color='red', label='OD')
if y2:
    plt.scatter(x, y2, color='blue', label='OS')
plt.legend(loc='lower right')
plt.xticks(range(3, 17))
plt.yticks(range(20, 30))
plt.xlabel('Age', fontsize=14)
plt.ylabel('Axial Length', fontsize=14)
plt