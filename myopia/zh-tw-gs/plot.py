from js import sex, age, y1, y2, records, suggestion, localStorage, report , language_type
if 'ale' in sex:
    sex = {'Male': '男', 'Female': '女'}[sex]
#print(language_type)
import pandas as pd
import numpy as np
import pickle
from scipy.interpolate import make_interp_spline
with open('data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area , data_al= pickle.load(f)[report]

from datetime import datetime
now = datetime.now()
formatted_time = now.strftime('%Y%m%d_%H%M')
#with open('data_to_plot_20231013.pkl', 'rb') as f:
    #db_version , slope_groupby , results_groupby , stacked_area , constant_ci_groupby , coef_ci_025_groupby , coef_ci_975_groupby = pickle.load(f)[report]
display(f'{formatted_time}', target='copyrightid')
#with open('LFC_data_to_plot_20231227.pkl', 'rb') as f:
    #data_al = pickle.load(f)
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

def moving_average_cal(data):
  moving_average = []
  window_sum = 0
  window_count=0
  length= len(data)
  #print(data)
  for index in range(0,length):
    window_count = 0
    window_sum = 0
    if index - 2 >= 0:
       window_sum += data.iloc[index - 2]
       window_count+=1
    if index - 1 >= 0:
       window_sum += data.iloc[index - 1]
       window_count+=1
    window_sum += data.iloc[index]
    window_count+=1
    #print(data.iloc[index])
    if index + 1 < length:
       window_sum += data.iloc[index + 1]
       window_count+=1
    if index + 2 < length:
       window_sum += data.iloc[index + 2]
       window_count+=1
    moving_average.append(window_sum/window_count)
  #print(moving_average)
  return moving_average

def plot(sex, report):
    area = stacked_area.loc[sex].loc[3:16]
    MorF = {'男': 'Male', '女': 'Female'}[sex]
    if report == '軸長':
        #area_index_smooth = np.linspace(area.index.min(), area.index.max(), 100)
        #splP100 = make_interp_spline(area.index, area['P100'], k=3)
        #splP90 = make_interp_spline(area.index, area['P90'], k=3)
        #splP75 = make_interp_spline(area.index, area['P75'], k=3)
        #splP50 = make_interp_spline(area.index, area['P50'], k=3)
        #area_100_smooth = splP100(area_index_smooth)
        #area_90_smooth = splP90(area_index_smooth)
        #area_75_smooth = splP75(area_index_smooth)
        #area_50_smooth = splP50(area_index_smooth)
        area_100_smooth = moving_average_cal(area['P100'])
        area_90_smooth = moving_average_cal(area['P90'])
        area_75_smooth = moving_average_cal(area['P75'])
        area_50_smooth = moving_average_cal(area['P50'])
        plt.fill_between(area.index, area_100_smooth, area_90_smooth, color='red', alpha=0.2, label='High Risk')
        plt.fill_between(area.index, area_90_smooth, area_75_smooth, color='yellow', alpha=0.2, label='Medium Risk')#orange
        plt.fill_between(area.index, area_75_smooth, area_50_smooth, color='lightgreen', alpha=0.2, label='Low Risk')#yellow
        #plt.fill_between(area_index_smooth, area_50_smooth, 19.5, color='lightgreen', alpha=0.2, label='0~50%')
    else :
        #area_index_smooth = np.linspace(area.index.min(), area.index.max(), 100)
        #splP50 = make_interp_spline(area.index, area['P50'], k=3)
        #splP25 = make_interp_spline(area.index, area['P25'], k=3)
        #splP10 = make_interp_spline(area.index, area['P10'], k=3)
        #area_50_smooth = splP50(area_index_smooth)
        #area_25_smooth = splP25(area_index_smooth)
        #area_10_smooth = splP10(area_index_smooth)
        #plt.fill_between(area_index_smooth, area_50_smooth, 5, color='lightgreen', alpha=0.2, label='50~100%')
        #plt.fill_between(area_index_smooth, area_25_smooth, area_50_smooth, color='yellow', alpha=0.2, label='25~50%')
        #plt.fill_between(area_index_smooth, area_10_smooth, area_25_smooth, color='orange', alpha=0.2, label='10~25%')
        #plt.fill_between(area_index_smooth, -9, area_10_smooth, color='red', alpha=0.2, label='0~10%')
        area_100_smooth = moving_average_cal(area['P100'])
        area['P100']=moving_average_cal(area['P100'])
        area_50_smooth = moving_average_cal(area['P50'])
        area['P50']=moving_average_cal(area['P50'])
        area_25_smooth = moving_average_cal(area['P25'])
        area['P25']=moving_average_cal(area['P25'])
        area_10_smooth = moving_average_cal(area['P10'])
        area['P10']=moving_average_cal(area['P10'])
        area_0_smooth = moving_average_cal(area['P0'])
        area['P0']=moving_average_cal(area['P0'])
        plt.fill_between(area.index, area_50_smooth, area_100_smooth, color='lightgreen', alpha=0.2, label='50~100%')
        plt.fill_between(area.index, area_25_smooth, area_50_smooth, color='yellow', alpha=0.2, label='25~50%')
        plt.fill_between(area.index, area_10_smooth, area_25_smooth, color='orange', alpha=0.2, label='10~25%')
        plt.fill_between(area.index, area_0_smooth, area_10_smooth, color='red', alpha=0.2, label='0~10%')
    #plt.title(f"Trend of {MorF} Children in Taiwan  {db_version}", fontsize=12)
    if language_type== 0 :
        if report == '軸長':
            plt.title(f"{sex}童軸長成長趨勢", fontproperties=custom_font, fontsize=16)
        if report == '球面度數':
            plt.title(f"{sex}童球面度數成長趨勢", fontproperties=custom_font, fontsize=16)
    elif language_type== 1:
        if report == '軸長':
            plt.title(f"Trend in axial length of {MorF} children", fontsize=16)
        if report == '球面度數':
            plt.title(f"Trend in spherical diopter of {MorF}children", fontsize=16)
    elif language_type== 2:
        if report == '軸長':
            plt.title(f"{sex}童轴长成长趋势", fontproperties=custom_font, fontsize=16)
        if report == '球面度數':
            plt.title(f"{sex}童球面度数成长趋势", fontproperties=custom_font, fontsize=16)
    else :
        if report == '軸長':
            plt.title(f"Trend in axial length of {MorF} children", fontsize=16)
        if report == '球面度數':
            plt.title(f"Trend in spherical diopter of {MorF} children", fontsize=16)

risk = [...] * 4
eye_word = [...] * 2
#x_label=[ "ortho-k" ,"glasses" ,"multiple treatment" ,"no treatment", "atropine" ]
sdl_coef=[ -0.54 ,-0.357 ,-0.392 , -0.696 , -0.424 ]
sdl_coef_d=[ 0.944 ,0.968 ,0.694 , 1.007 , 0.73 ]
sdr_coef=[ -0.685 ,-0.282 ,-0.617 , -0.419 , -0.436 ]
sdr_coef_d=[ 1.178 , 0.658 , 0.617 , 0.84 , 0.817 ]
all_coef=[ 0.092 , 0.14 , 0.13 , 0.141 , 0.253 ]
all_coef_d=[ 0.169 , 0.331 , 0.17 , 0.203 , 1.178 ]
alr_coef=[ 0.097 , 0.1 , 0.156 , 0.124 , 0.116 ]
alr_coef_d=[ 0.213 , 0.185 , 0.236 , 0.18 , 0.173 ]

if language_type== 0 :
    if report == '軸長':
        eye_word[0]= '右眼軸長'
        eye_word[1]= '左眼軸長'
    if report == '球面度數':
        eye_word[0]= '右眼球面度數'
        eye_word[1]= '左眼球面度數'
    risk[0] = f'低'#","- 生活方式與用眼習慣","戶外活動：每天至少1小時戶外活動，增加自然光暴露","視力休息：每20分鐘遠眺6公尺外的物體至少20秒","- 飲食與營養品","均衡飲食：確保足夠的維他命A、C和E，有助於眼睛健康","營養品：考慮補充Omega-3脂肪酸","- 定期回診時間","定期檢查：每年至少進行一次視力檢查"]
    risk[1] = f'中'#","- 生活方式與用眼習慣","戶外活動：每天至少1小時戶外活動，增加自然光暴露","視力休息：每20分鐘遠眺6公尺外的物體至少20秒","長時間休息：每使用電子設備1小時後，進行5-10分鐘的較長時間休息","視力保健：使用防藍光眼鏡","- 飲食與營養品","均衡飲食：增加富含抗氧化劑的食物，如藍莓、胡蘿蔔、菠菜","營養品：補充葉黃素和玉米黃質，以及Omega-3脂肪酸","- 定期回診時間\n 定期檢查：每6到12個月至少進行一次視力檢查"]
    risk[2] = f'高'#","- 生活方式與用眼習慣","戶外活動：每天至少1小時戶外活動，增加自然光暴露","視力休息：每使用20分鐘後，遠眺6公尺外的物體至少20秒","長時間休息：每使用電子設備1小時後，進行10-15分鐘的較長時間休息","視力保健：減少電子設備的使用時間，考慮使用角膜塑形鏡片","- 飲食與營養品","均衡飲食：攝取富含維他命A、C、E和鋅的食物","營養品：補充高劑量的葉黃素、玉米黃質和Omega-3脂肪酸","- 定期回診時間","定期檢查：每3到6個月進行一次視力檢查"]
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
        eye_word[0]= '右眼球面度数'
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

#plt.figure(figsize=(7.5, 7.5))
plot(sex, report)

import re
def x(age):
    m = re.match('(\d+)歲(\d+)', age)
    return int(m.group(1)) + int(m.group(2)) / 12

if round(x(age)) in range(3, 17):
    if report == '軸長' and language_type!=0:
        p0, p50, p75, p90, p100 = stacked_area.loc[sex].loc[round(x(age))]
        for y, eye , ODOS in (y1, eye_word[0],'OD'), (y2, eye_word[1],'OS'):
            if y < p50:
                if language_type== 1:
                    display(f'{eye}{risk[0]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y < p75:
                if language_type== 1:
                    display(f'{eye}{risk[1]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y < p90:
                if language_type== 1:
                    display(f'{eye}{risk[2]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                if language_type== 1:
                    display(f'{eye}{risk[3]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[3]}', target='advice')
                localStorage.setItem(eye, 3)

    if report == '軸長' and language_type == 0:
            p0, p50, p75, p90, p100 = stacked_area.loc[sex].loc[round(x(age))]
            eye="ODOS"
            if y1 < p50 or y2 < p50:
                display(f'{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y1 < p75 or y2 < p75:
                display(f'{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y1 < p90 or y2 < p90:
                display(f'{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                display(f'{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)

    if report == '球面度數'  and language_type!=0:
        p100, p50, p25, p10, p0 = stacked_area.loc[sex].loc[round(x(age))]
        for y, eye , ODOS in (y1, eye_word[0],'OD'), (y2, eye_word[1],'OS'):
            if y > p50:
                if  language_type== 1:
                    display(f'{eye}{risk[0]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y > p25:
                if language_type== 1:
                    display(f'{eye}{risk[1]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y > p10:
                if language_type== 1:
                    display(f'{eye}{risk[2]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                if language_type== 1:
                    display(f'{eye}{risk[3]}', target=f'advice{ODOS}')
                else :
                    display(f'{eye}{risk[3]}', target='advice')
                localStorage.setItem(eye, 3)
                
    if report == '球面度數' and language_type == 0:
            p100, p50, p25, p10, p0 = stacked_area.loc[sex].loc[round(x(age))]
            eye="ODOS"
            print(f'{y1} {type(y1)}')
            if y1 > p50 or y2 > p50:
                display(f'{risk[0]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y1 > p25 or y2 > p25:
                display(f'{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            elif y1 > p10 or y2 > p10:
                display(f'{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)
            else:
                display(f'{risk[2]}', target='advice')
                localStorage.setItem(eye, 2)

else:
    if language_type== 1 :
        display(samples_not_enought, target='adviceOD')
        display(samples_not_enought, target='adviceOS')
    else :
        display(samples_not_enought, target='advice')
    localStorage.setItem('右眼', '')
    localStorage.setItem('左眼', '')

if suggestion == None :
    suggestion='不處置'
if suggestion == '不處置' :
    label_index = 3
elif suggestion == '低散瞳劑' or suggestion == '中散瞳劑' or suggestion == '高散瞳劑' :
    label_index = 4
elif suggestion == '一般眼鏡' :
    label_index = 1
elif suggestion == '一般眼鏡＋中散瞳劑' :
    label_index = 2
elif suggestion == '一般眼鏡散瞳劑' :
    label_index = 2
else :
    label_index = 0
agecounter = int(16-x(age))+2
if agecounter <= 0:
    agecounter = 1
x_age_series=[0]*agecounter#this is for initial
x_stdu_value_series=[0]*agecounter#this is for initial
x_stdd_value_series=[0]*agecounter#this is for initial
x_age_series[0]=x(age)
odp_first=True
osp_first=True

for age_index in range(1,agecounter):
    x_age_series[age_index] = x_age_series[age_index-1] + 1
def C_I_cal(nowvalue):  
    #print("In draw  constant_ci_groupby : "+str(constant_ci_groupby[sex][suggestion])+ "----coef_ci_025_groupby is "+ str(coef_ci_025_groupby[sex][suggestion])+ "----coef_ci_975_groupby is "+ str(coef_ci_975_groupby[sex][suggestion]))
    constant_025=nowvalue-constant_ci_groupby[sex][suggestion]
    constant_975=nowvalue+constant_ci_groupby[sex][suggestion]
    max_value = constant_025 +  coef_ci_025_groupby[sex][suggestion]

    min_value = constant_025 +  coef_ci_975_groupby[sex][suggestion]
    if  constant_975 +  coef_ci_025_groupby[sex][suggestion]  > max_value :
        max_value = constant_975 +  coef_ci_025_groupby[sex][suggestion]
    if  constant_975 +  coef_ci_025_groupby[sex][suggestion]  < min_value :
        min_value = constant_975 +  coef_ci_025_groupby[sex][suggestion]

    if  constant_975 + coef_ci_975_groupby[sex][suggestion]  > max_value :
        max_value = constant_975 + coef_ci_975_groupby[sex][suggestion]
    if  constant_975 + coef_ci_975_groupby[sex][suggestion]  < min_value :
        min_value = constant_975 + coef_ci_975_groupby[sex][suggestion]   

    return max_value,min_value
def logarithm_calculate_high_low(nowvalue , age_index , age_origin): 
    difference_high = np.exp(data_al[report][sex][suggestion]["con_975"]+np.log(age_index)*data_al[report][sex][suggestion]["x_975"]) - np.exp(data_al[report][sex][suggestion]["con_975"]+np.log(age_origin)*data_al[report][sex][suggestion]["x_975"])
    difference_low = np.exp(data_al[report][sex][suggestion]["con_025"]+np.log(age_index)*data_al[report][sex][suggestion]["x_025"]) - np.exp(data_al[report][sex][suggestion]["con_025"]+np.log(age_origin)*data_al[report][sex][suggestion]["x_025"])
    return nowvalue + difference_high  , nowvalue + difference_low
def logarithm_calculate_middle(nowvalue , age_index , age_origin):
    difference = np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_index)*data_al[report][sex][suggestion]["b1"]) - np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_origin)*data_al[report][sex][suggestion]["b1"])
    return nowvalue + difference
if y1 != "":
    if y1 == 0 and report == '軸長':
        y1 = 19.5
    plt.scatter(x(age), y1, color='red', label='OD now' , marker='D', zorder=9)
    #print("od is : " + str(y1 ))
if y2 != "":
    if y2 == 0 and report == '軸長':
        y2 = 19.5
    plt.scatter(x(age), y2, color='blue', label='OS now' , marker='D', zorder=9)
    #print("os is : " + str(y2))
if y1 != "" and slope_groupby[sex].get(suggestion):
    x_stdu_value_series[0] = y1
    x_stdd_value_series[0] = y1
    for age_index in range(1,agecounter):
        #x_stdu_value_series[age_index],x_stdd_value_series[age_index] = C_I_cal(y1 + slope_groupby[sex][suggestion] * (age_index-1))
        x_stdu_value_series[age_index],x_stdd_value_series[age_index] = logarithm_calculate_high_low(y1 , x_age_series[age_index], x_age_series[0])
        if odp_first :
            #plt.scatter(x_age_series[age_index], y1 + slope_groupby[sex][suggestion] * age_index, color='red', alpha=0.5, label='OD in 1 yr', marker='*')
            plt.scatter(x_age_series[age_index], logarithm_calculate_middle(y1 , x_age_series[age_index], x_age_series[0]), color='red', alpha=0.7, label='OD in 1 yr', marker='*')
            odp_first=False
        else :
            #plt.scatter(x_age_series[age_index], y1 + slope_groupby[sex][suggestion] * age_index, color='red', alpha=0.5, marker='*')
            plt.scatter(x_age_series[age_index],logarithm_calculate_middle(y1 , x_age_series[age_index], x_age_series[0]), color='red', alpha=0.7, marker='*')
    plt.fill_between(x_age_series, x_stdu_value_series, x_stdd_value_series, color='#E84F6B', alpha=0.6, label='OD in future')##AC92EB
    #plt.scatter(x(age) + 1, y1 + slope_groupby[sex][suggestion], color='red', label='OD in 1 yr', marker='*')
if y2 != "" and slope_groupby[sex].get(suggestion):
    x_stdu_value_series[0] = y2
    x_stdd_value_series[0] = y2
    for age_index in range(1,agecounter):
        #x_stdu_value_series[age_index],x_stdd_value_series[age_index] = C_I_cal(y2 + slope_groupby[sex][suggestion] * (age_index-1))
        x_stdu_value_series[age_index],x_stdd_value_series[age_index] = logarithm_calculate_high_low(y2 , x_age_series[age_index], x_age_series[0])
        if osp_first :
            #plt.scatter(x_age_series[age_index], y2 + slope_groupby[sex][suggestion] * age_index, color='blue', alpha=0.5, label='OS in 1 yr', marker='*')
            plt.scatter(x_age_series[age_index],logarithm_calculate_middle(y2 , x_age_series[age_index], x_age_series[0]), color='blue', alpha=0.7, label='OS in 1 yr', marker='*')
            osp_first=False
        else :
            #plt.scatter(x_age_series[age_index], y2 + slope_groupby[sex][suggestion] * age_index, color='blue', alpha=0.5, marker='*')
            plt.scatter(x_age_series[age_index],logarithm_calculate_middle(y2 , x_age_series[age_index], x_age_series[0]), color='blue', alpha=0.7, marker='*')
    plt.fill_between(x_age_series, x_stdu_value_series, x_stdd_value_series, color='#4FC1E8', alpha=0.6, label='OS in future')
    #plt.scatter(x(age) + 1, y2 + slope_groupby[sex][suggestion], color='blue', label='OS in 1 yr', marker='*')


if report=="軸長":
    suggestion ="不處置"
else :
    suggestion ="一般眼鏡"
if y1 != "" and slope_groupby[sex].get(suggestion):
    x_stdu_value_series[0] = y1
    x_stdd_value_series[0] = y1
    for age_index in range(1,agecounter):
        x_stdu_value_series[age_index],x_stdd_value_series[age_index] = logarithm_calculate_high_low(y1 , x_age_series[age_index], x_age_series[0])
    if report=="軸長":#軸長#球面度數
        if x_stdu_value_series[1]>=x_stdd_value_series[1]:
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
        else :
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
    else :
        if x_stdu_value_series[1]<=x_stdd_value_series[1]:
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
        else :
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
if y2 != "" and slope_groupby[sex].get(suggestion):
    x_stdu_value_series[0] = y2
    x_stdd_value_series[0] = y2
    for age_index in range(1,agecounter):
        x_stdu_value_series[age_index],x_stdd_value_series[age_index] = logarithm_calculate_high_low(y2 , x_age_series[age_index], x_age_series[0])
    if report=="軸長":#軸長#球面度數
        if x_stdu_value_series[1]>=x_stdd_value_series[1]:
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
        else :
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
    else :
        if x_stdu_value_series[1]<=x_stdd_value_series[1]:
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
        else :
            plt.plot(x_age_series, x_stdu_value_series, color='0.3', linewidth=0.7, label='No treatment')#, alpha=0.2
import json
records = json.loads(records)
od, os = (18, 24) if report == '軸長' else (15, 21)
odp_first=True
osp_first=True
x_age_record=[]
y_od_record=[]
y_os_record=[]
x_age_record.append(x(age))
y_od_record.append(y1)
y_os_record.append(y2)
for record in records:
    if record[od] != "":
        if odp_first :
            plt.scatter(x(record[11]), record[od], color='red', marker='.' , label='OD in past')
            odp_first=False
        else :
            plt.scatter(x(record[11]), record[od], color='red', marker='.')
        x_age_record.append(x(record[11]))
        y_od_record.append(record[od])
        #print("od is : " + str(record[od]) )
    if record[os] != "":
        if osp_first :
            plt.scatter(x(record[11]), record[os], color='blue', marker='.', label='OS in past')
            osp_first=False
        else :
            plt.scatter(x(record[11]), record[os], color='blue', marker='.')
        y_os_record.append(record[os])
        #print("os is : " + str(record[os]))
        
plt.plot(x_age_record, y_od_record, color='red')
plt.plot(x_age_record, y_os_record, color='blue')
plt.plot(3, 19.5 , linestyle='none' , marker='None', alpha=0, label=db_version)
if report == '軸長':
    plt.legend(loc='center right' , bbox_to_anchor=(1.21, 0.25),fontsize=8)
if report == '球面度數':
    plt.legend(loc='center right' , bbox_to_anchor=(1.21, 0.25),fontsize=8)
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
plt.subplots_adjust(left=0.1, right=0.84, bottom=0.1, top=0.9, wspace=0.8, hspace=0.2)
if report == '軸長':
    plt.ylim(21, 29)
    plt.xlim(3, 16)
    plt.text(16 if x(age) + 1 < 16 else x(age) + 1, 18.8 if sex=='女' else 19.2, f'', horizontalalignment='right', fontsize=8)
if report == '球面度數':
    if language_type== 0 or language_type == 1:
        plt.ylim(2, -8)
    else:
        plt.ylim(-8, 2)
    plt.xlim(3, 16)
    plt.text(16 if x(age) + 1 < 16 else x(age) + 1, -10.5 if sex=='女' else -10.5, f'', horizontalalignment='right', fontsize=8)
plt.grid(alpha=0.2)
ax = plt.gca()
if report == '軸長':
    ax.set_aspect(aspect=1.25)
else :
    ax.set_aspect(aspect='auto')
display(plt, target='plot')