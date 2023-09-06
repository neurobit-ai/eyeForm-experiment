from js import sex, age, y1, y2, records, suggestion, localStorage, report , language_type
if 'ale' in sex:
    sex = {'Male': '男', 'Female': '女'}[sex]
#print(language_type)
import pandas as pd

import pickle
with open('data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area = pickle.load(f)[report]
display(f'{db_version}', target='copyrightid')

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#font_path = 'TaipeiSansTCBeta-Bold.ttf'
if language_type== 0 :
    font_path = 'msjhbd.ttc'
    font_paht_s = "msjh.ttc"
elif language_type== 2:
    font_path = 'msyhbd.ttc'
    font_paht_s = "msyh.ttc"
else:
    font_path = ''
    font_paht_s = "" 
#print("PATH IS " + font_path)
custom_font = FontProperties(fname=font_path)
custom_font_s = FontProperties(fname=font_paht_s)

plt.figure(figsize=(8, 6))


def plot(sex, report):
    area = stacked_area.loc[sex].loc[3:16]
    MorF = {'男': 'Male', '女': 'Female'}[sex]
    if report == '軸長':
        plt.fill_between(area.index, area['P100'], area['P90'], color='red', alpha=0.6, label='90~100%')
        plt.fill_between(area.index, area['P90'], area['P75'], color='orange', alpha=0.6, label='75~90%')
        plt.fill_between(area.index, area['P75'], area['P50'], color='yellow', alpha=0.6, label='50~75%')
        plt.fill_between(area.index, area['P50'], area['P0'], color='lightgreen', alpha=0.6, label='0~50%')
    if report == '球面度數':
        plt.fill_between(area.index, area['P50'], area['P100'], color='lightgreen', alpha=0.6, label='50~100%')
        plt.fill_between(area.index, area['P25'], area['P50'], color='yellow', alpha=0.6, label='25~50%')
        plt.fill_between(area.index, area['P10'], area['P25'], color='orange', alpha=0.6, label='10~25%')
        plt.fill_between(area.index, area['P0'], area['P10'], color='red', alpha=0.6, label='0~10%')
    #plt.title(f"Trend of {MorF} Children in Taiwan  {db_version}", fontsize=12)
    if language_type== 0 :
        plt.title(f"台灣{sex}童趨勢", fontproperties=custom_font, fontsize=16)
    elif language_type== 1:
        plt.title(f"Trend of {MorF} Children in Taiwan", fontsize=16)
    elif language_type== 2:
        plt.title(f"台湾{sex}童趋势", fontproperties=custom_font, fontsize=16)
    else :
        plt.title(f"Trend of {MorF} Children in Taiwan", fontsize=16)


risk = [...] * 4
eye_word = [...] * 2

if language_type== 0 :
    if report == '軸長':
        eye_word[0]= '右眼軸長'
        eye_word[1]= '左眼軸長'
    if report == '球面度數':
        eye_word[0]= '右眼球面度數'
        eye_word[1]= '左眼球面度數'
    risk[0] = f'在年齡正常範圍內，屬低風險，建議一年定期檢查，無潛在近視發展狀況。'
    risk[1] = f'稍長於年齡正常範圍，屬中風險，建議一年定期檢查，需改變生活型態及減少外在環境影響。'
    risk[2] = f'長於年齡正常範圍，屬高風險，建議半年回診檢查，需改變生活型態及減少外在環境影響（例：電腦及手機使用時間需要注意並適度休息、戶外活動需要配戴太陽眼鏡防藍光、UV），並搭配葉黃素或魚油服用。'
    risk[3] = f'甚長於年齡正常範圍，屬極高風險，有極高近視惡化發展可能，建議3個月回診檢查，需改變生活型態及減少外在環境影響（例：電腦及手機使用時間需要注意並適度休息、避免坐姿不正，戶外活動需要配戴太陽眼鏡防藍光、UV），搭配葉黃素或魚油服用，並搭配積極治療控制。'
    samples_not_enought = '該年齡收案不足，無法提供具有統計意義之危險度分級。'
elif language_type== 1:
    if report == '軸長':
        eye_word[0] = 'Axial length of right eye'
        eye_word[1] = 'Axial length of left eye'
    if report == '球面度數':
        eye_word[0] = 'Spherical diopter of right eye'
        eye_word[1] = 'Spherical diopter of left eye'
    risk[0] = f' within the normal age range, it is considered low risk. Regular annual check-ups are recommended, and there is no indication of potential nearsightedness development.'
    risk[1] = f' slightly beyond the normal age range, it is considered moderate risk. Regular annual check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences.'
    risk[2] = f' beyond the normal age range, it is considered high risk. Biannual follow-up check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences (e.g., being mindful of screen time for computers and phones and taking breaks, wearing sunglasses to protect against blue light and UV rays during outdoor activities). Additionally, consider supplementing with lutein or fish oil.'
    risk[3] = f' far beyond the normal age range, it is considered extremely high risk with a significant potential for severe myopia progression. Quarterly follow-up check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences (e.g., being mindful of screen time for computers and phones and taking breaks, maintaining proper posture, wearing sunglasses to protect against blue light and UV rays during outdoor activities). Additionally, consider supplementing with lutein or fish oil, and adopting proactive treatment measures for control.'
    samples_not_enought = 'The number of cases within this age group is insufficient to provide statistically significant risk classification.'
elif language_type== 2:
    if report == '軸長':
        eye_word[0]= '右眼轴长'
        eye_word[1]= '左眼轴长'
    if report == '球面度數':
        eye_word[0]= '左眼球面度数'
        eye_word[1]= '左眼球面度数'
    risk[0] = f'在年龄正常范围内，属低风险，建议一年定期检查，无潜在近视发展状况。'
    risk[1] = f'稍长于年龄正常范围，属中风险，建议一年定期检查，需改变生活型态及减少外在环境影响。'
    risk[2] = f'长于年龄正常范围，属高风险，建议半年回诊检查，需改变生活型态及减少外在环境影响（例：电脑及手机使用时间需要注意并适度休息、户外活动需要配戴太阳眼镜防蓝光、UV ），并搭配叶黄素或鱼油服用。'
    risk[3] = f'甚长于年龄正常范围，属极高风险，有极高近视恶化发展可能，建议3个月回诊检查，需改变生活型态及减少外在环境影响（例：电脑及手机使用时间需要注意并适度休息、避免坐姿不正，户外活动需要配戴太阳眼镜防蓝光、UV），搭配叶黄素或鱼油服用，并搭配积极治疗控制。'
    samples_not_enought = '该年龄收案不足，无法提供具有统计意义之危险度分级。'
else :
    if report == '軸長':
        eye_word[0] = 'Axial length of right eye'
        eye_word[1] = 'Axial length of left eye'
    if report == '球面度數':
        eye_word[0] = 'Spherical diopter of right eye'
        eye_word[1] = 'Spherical diopter of left eye'
    risk[0] = f' within the normal age range, it is considered low risk. Regular annual check-ups are recommended, and there is no indication of potential nearsightedness development.'
    risk[1] = f' slightly beyond the normal age range, it is considered moderate risk. Regular annual check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences.'
    risk[2] = f' beyond the normal age range, it is considered high risk. Biannual follow-up check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences (e.g., being mindful of screen time for computers and phones and taking breaks, wearing sunglasses to protect against blue light and UV rays during outdoor activities). Additionally, consider supplementing with lutein or fish oil.'
    risk[3] = f' far beyond the normal age range, it is considered extremely high risk with a significant potential for severe myopia progression. Quarterly follow-up check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences (e.g., being mindful of screen time for computers and phones and taking breaks, maintaining proper posture, wearing sunglasses to protect against blue light and UV rays during outdoor activities). Additionally, consider supplementing with lutein or fish oil, and adopting proactive treatment measures for control.'
    samples_not_enought = 'The number of cases within this age group is insufficient to provide statistically significant risk classification.'
Risk = {}

import re
def x(age):
    m = re.match('(\d+)歲(\d+)', age)
    return int(m.group(1)) + int(m.group(2)) / 12

if round(x(age)) in range(3, 17):
    if report == '軸長':
        p0, p50, p75, p90, p100 = stacked_area.loc[sex].loc[round(x(age))]
        for y, eye in (y1, eye_word[0]), (y2, eye_word[1]):
            if y < p50:
                display(f'{eye}{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y < p75:
                display(f'{eye}{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y < p90:
                display(f'{eye}{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                display(f'{eye}{risk[3]}', target='advice')
                localStorage.setItem(eye, 3)
    if report == '球面度數':
        p100, p50, p25, p10, p0 = stacked_area.loc[sex].loc[round(x(age))]
        for y, eye in (y1, eye_word[0]), (y2, eye_word[1]):
            if y > p50:
                display(f'{eye}{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y > p25:
                display(f'{eye}{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y > p10:
                display(f'{eye}{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                display(f'{eye}{risk[3]}', target='advice')
                localStorage.setItem(eye, 3)
else:
    display(samples_not_enought, target='advice')
    localStorage.setItem('右眼', '')
    localStorage.setItem('左眼', '')

#plt.figure(figsize=(7.5, 7.5))
plot(sex, report)
if y1 != "":
    if y1 == 0 :
        y1 = 19.5
    plt.scatter(x(age), y1, color='red', label='OD' , marker='D')
    #print("od is : " + str(y1 ))
if y2 != "":
    if y2 == 0 :
        y2 = 19.5
    plt.scatter(x(age), y2, color='blue', label='OS' , marker='D')
    #print("os is : " + str(y2))
if y1 != "" and slope_groupby[sex].get(suggestion):
    plt.scatter(x(age) + 1, y1 + slope_groupby[sex][suggestion], color='red', label='OD in 1 yr', marker='*')
if y2 != "" and slope_groupby[sex].get(suggestion):
    plt.scatter(x(age) + 1, y2 + slope_groupby[sex][suggestion], color='blue', label='OS in 1 yr', marker='*')

import json
records = json.loads(records)
od, os = (18, 24) if report == '軸長' else (15, 21)
odp_first=True
osp_first=True
for record in records:
    if record[od] != "":
        if odp_first :
            plt.scatter(x(record[11]), record[od], color='red', marker='.' , label='OD in past')
            odp_first=False
        else :
            plt.scatter(x(record[11]), record[od], color='red', marker='.')
        #print("od is : " + str(record[od]) )
    if record[os] != "":
        if osp_first :
            plt.scatter(x(record[11]), record[os], color='blue', marker='.', label='OS in past')
            osp_first=False
        else :
            plt.scatter(x(record[11]), record[os], color='blue', marker='.')
        #print("os is : " + str(record[os]))
plt.plot(3, 19.5 , linestyle='none' , marker='None', alpha=0, label=db_version)
if report == '軸長':
    plt.legend(loc='center right' , bbox_to_anchor=(1.19, 0.25),fontsize=8)
if report == '球面度數':
    plt.legend(loc='center right' , bbox_to_anchor=(1.19, 0.25),fontsize=8)
plt.xticks(range(3, 17 if x(age) + 1 <= 16 else int(x(age)) + 2))
plt.yticks(range(20, 30) if report == '軸長' else range(-8, 7))
if language_type== 0 :
    plt.xlabel("年齡 (歲)", fontproperties=custom_font_s, fontsize=12)
elif language_type== 2:
    plt.xlabel("年龄 (岁)", fontproperties=custom_font_s, fontsize=12)
else :
    plt.xlabel("Age (years)", fontsize=12)
#plt.xlabel('Age', fontsize=12)
if language_type== 0 :
    plt.ylabel('軸長 (mm)' if report == '軸長' else '球面度數 (度)', fontproperties=custom_font_s, fontsize=12)
elif language_type== 2:
    plt.ylabel('轴长 (mm)' if report == '軸長' else '球面度数 (度)', fontproperties=custom_font_s, fontsize=12)
else :
    plt.ylabel('Axial Length (mm)' if report == '軸長' else 'SPH (degrees)', fontsize=12)
#plt.ylabel('Axial Length' if report == '軸長' else 'SPH', fontsize=12)

plt.margins(0)
plt.subplots_adjust(left=0.1, right=0.85, bottom=0.1, top=0.9, wspace=0.8, hspace=0.2)
if report == '軸長':
    plt.ylim(19.5, 30.5)
    plt.xlim(3, 16)
    plt.text(16 if x(age) + 1 < 16 else x(age) + 1, 18.8 if sex=='女' else 19.2, f'', horizontalalignment='right', fontsize=8)
if report == '球面度數':
    plt.ylim(-8.5, 7.5)
    plt.xlim(3, 16)
    plt.text(16 if x(age) + 1 < 16 else x(age) + 1, -8.5 if sex=='女' else -10.5, f'', horizontalalignment='right', fontsize=8)
display(plt, target='plot')
