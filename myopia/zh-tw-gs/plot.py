from js import sex, age, y1, y2, records, suggestion, localStorage, report , language_type
from pyscript import display
from pyodide.ffi import JsProxy
if 'ale' in sex and sex !="":
    sex = {'Male': '男', 'Female': '女'}[sex]
#print(language_type)
#根據VHBI設定的衰退曲線係數
growth_base   = [ -0.246, -0.164, -0.082, 0,  0.082,0.184, 0.239,0.323, 0.378,0.434, 0.471,0.508, 0.527,0.536]
growth_interval = [-0.018,-0.014,-0.01,-0.006,-0.0022,0.0014,0.0028,0.0092,0.0143,0.0172,0.0228,0.0257,0.0307,0.0335]
attu_base =    [ -0.12,-0.08,-0.04, 0,  0.04, 0.133, 0.136,0.269, 0.3, 0.378, 0.439, 0.596,0.7, 0.77]
attu_interval =  [0.039,0.033,0.044,0.039,0.033, 0.044,0.056, 0.056,0.042, 0.053, 0.04, 0.098,0.17, 0.23]

import pandas as pd
import numpy as np
import pickle
with open('../data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area , data_al= pickle.load(f)[report]

from datetime import datetime
now = datetime.now()
formatted_time = now.strftime('%Y%m%d_%H%M')
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

#對高中低風險的曲線做平滑化
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

#把中高低風險的分布畫在背景中
def plot(sex, report):
    area = stacked_area.loc[sex].loc[3:16]
    MorF = {'男': 'Male', '女': 'Female'}[sex]
    if report == '軸長':
        area_100_smooth = moving_average_cal(area['P100'])
        area_90_smooth = moving_average_cal(area['P90'])
        area_75_smooth = moving_average_cal(area['P75'])
        area_50_smooth = moving_average_cal(area['P50'])
        if language_type == 1:
            plt.fill_between(area.index, area_100_smooth, area_90_smooth, color='red', alpha=0.2, label='High Risk')
            plt.fill_between(area.index, area_90_smooth, area_75_smooth, color='yellow', alpha=0.2, label='Medium Risk')#orange
            plt.fill_between(area.index, area_75_smooth, area_50_smooth, color='lightgreen', alpha=0.2, label='Low Risk')#yellow
        else:
            plt.fill_between(area.index, area_100_smooth, area_90_smooth, color='red', alpha=0.2, label='高風險')
            plt.fill_between(area.index, area_90_smooth, area_75_smooth, color='yellow', alpha=0.2, label='中風險')#orange
            plt.fill_between(area.index, area_75_smooth, area_50_smooth, color='lightgreen', alpha=0.2, label='低風險')#yellow
    else :
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
        if language_type == 1:
            plt.fill_between(area.index, area_50_smooth, 10, color='lightgreen', alpha=0.2, label='Low Risk')
            plt.fill_between(area.index, area_25_smooth, area_50_smooth, color='yellow', alpha=0.2, label='Medium Risk')
            plt.fill_between(area.index, -10, area_25_smooth, color='red', alpha=0.2, label='High Risk')
        else:
            plt.fill_between(area.index, area_50_smooth, 10, color='lightgreen', alpha=0.2, label='低風險')
            plt.fill_between(area.index, area_25_smooth, area_50_smooth, color='yellow', alpha=0.2, label='中風險')
            plt.fill_between(area.index, -10, area_25_smooth, color='red', alpha=0.2, label='高風險')
    #plt.title(f"Trend of {MorF} Children in Taiwan  {db_version}", fontsize=12)
    if language_type== 0 :
        if report == '軸長':
            plt.title(f"{sex}童軸長成長趨勢", fontproperties=custom_font, fontsize=16)
        if report == '球面度數':
            plt.title(f"{sex}童球面度數成長趨勢-使用{suggestion}控制-", fontproperties=custom_font, fontsize=16)
    elif language_type== 1:
        if report == '軸長':
            plt.title(f"Trend in axial length of {MorF} children", fontsize=16)
        if report == '球面度數':
            if suggestion == '一般眼鏡':
                suggestion_tr = 'regular glasses'
            elif suggestion == '漸進多焦點眼鏡':
                suggestion_tr = 'progressive addition spectacles'
            elif suggestion == '雙焦眼鏡':
                suggestion_tr = 'executive bifocals'
            elif suggestion == '周邊離焦鏡片' or suggestion == '周邊離焦(近視控制)鏡片':
                suggestion_tr = 'peripheral defocus spectacles'
            elif suggestion == '軟式隱形眼鏡' or suggestion == '近視控制隱形眼鏡':
                suggestion_tr = 'soft contact lens for myopia control'
            else:
                suggestion_tr = 'regular glasses'
            plt.title(f"Trend in spherical diopter of {MorF}children \n with {suggestion_tr}", fontsize=16)
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
    return area


risk = [...] * 4
eye_word = [...] * 2
#邏輯回歸的係數設定，目前已經沒有使用
#x_label=[ "ortho-k" ,"glasses" ,"multiple treatment" ,"no treatment", "atropine" ]
sdl_coef=[ -0.54 ,-0.357 ,-0.392 , -0.696 , -0.424 ]
sdl_coef_d=[ 0.944 ,0.968 ,0.694 , 1.007 , 0.73 ]
sdr_coef=[ -0.685 ,-0.282 ,-0.617 , -0.419 , -0.436 ]
sdr_coef_d=[ 1.178 , 0.658 , 0.617 , 0.84 , 0.817 ]
all_coef=[ 0.092 , 0.14 , 0.13 , 0.141 , 0.253 ]
all_coef_d=[ 0.169 , 0.331 , 0.17 , 0.203 , 1.178 ]
alr_coef=[ 0.097 , 0.1 , 0.156 , 0.124 , 0.116 ]
alr_coef_d=[ 0.213 , 0.185 , 0.236 , 0.18 , 0.173 ]

#根據當下的資料決定要回傳哪一種建議的內容設定
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
    risk[0] = f'Low'#' within the normal age range, it is considered low risk. Regular annual check-ups are recommended, and there is no indication of potential nearsightedness development.'
    risk[1] = f'Medium'#' slightly beyond the normal age range, it is considered moderate risk. Regular annual check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences.'
    risk[2] = f'High'#' beyond the normal age range, it is considered high risk. Biannual follow-up check-ups are recommended, along with the need to adjust lifestyle and minimize external environmental influences (e.g., being mindful of screen time for computers and phones and taking breaks, wearing sunglasses to protect against blue light and UV rays during outdoor activities). Additionally, consider supplementing with lutein or fish oil.'
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
area = plot(sex, report)

import re
def x(age):
    m = re.match(r'(\d+)歲(\d+)', age)
    return int(m.group(1)) + int(m.group(2)) / 12

def _y_m(age,year,sign):
    m = re.match(r'(\d+)歲(\d+)', age)
    if int(m.group(1))+year > 9:
        space01=''
    else :
        space01='&nbsp'
    if int(m.group(2)) > 9:
        space02=''
    else :
        space02='&nbsp'
    m_y=str(int(m.group(1))+year)
    if language_type== 0 :
        return f'{m_y}歲{m.group(2)}個月{sign}'
    elif language_type== 2:
        return f'{m_y}岁{m.group(2)}个月{sign}'
    else:
        return f'{m_y}y{m.group(2)}m{sign}'

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

import json
records = json.loads(records)

#使用改版後的pyscripts時會需要用到以下設定
od, os = (18, 24) if report == '軸長' else (15, 21)
if isinstance(records, JsProxy):
    records_py = records.to_py()
else:
    records_py = records.copy()

#依據是否有歷史資料判斷要怎麼做前處理
already_exist=False
if len(records_py)!=0:
    if y1 != "" and y2 != "" and age != "":
        for record in records_py:
            if x(record[11]) == x(age) and record[od] == y1 and record[os] == y2:
                already_exist = True
                break
        if not already_exist:
            new_record = [""] * len(records_py[-1])
            new_record[11]=age
            new_record[od]=y1
            new_record[os]=y2
            # new_record[0]="Latest_Input"
            records_py.append(new_record)

    for index_i in range(0,len(records_py)-1):
        for index_j in range(index_i+1,len(records_py)):
            if x(records_py[index_i][11]) < x(records_py[index_j][11]):
                records_py[index_i], records_py[index_j] = records_py[index_j], records_py[index_i]
else:
    if y1 != "" and y2 != "" and age != "":
        new_record = [""] * 25
        new_record[11]=age
        new_record[od]=y1
        new_record[os]=y2
        # new_record[0]="Latest_Input"
        records_py=[]
        records_py.append(new_record)
x_age_record=[]
x_age_record_text =[]
y_od_record=[]
y_os_record=[]
# print('OD ',records_py[0][od] , ' OS ',records_py[0][os] ,' age ',records_py[0][11])
age_new = records_py[0][11]
OD_new = records_py[0][od]
OS_new = records_py[0][os]

agecounter = int(16-x(age_new))+2
# print('counter is ' , agecounter)
if agecounter <= 0:
    agecounter = 1
x_age_series=[0]*agecounter#this is for initial
x_stdu_value_series=[0]*agecounter#this is for initial
x_stdd_value_series=[0]*agecounter#this is for initial
x_age_series[0]=x(age_new)
x_age_series_text=[]
x_age_series_text.append(_y_m(records_py[0][11],0,'○'))#age_new,age_index,sign
OD_zero = False
OS_zero = False


for age_index in range(1,agecounter):
    x_age_series[age_index] = x_age_series[age_index-1] + 1
    x_age_series_text.append(_y_m(records_py[0][11],age_index,''))

# if 
# x_age_record.append(x(age))
# y_od_record.append(y1)
# y_os_record.append(y2)

#依據目前落點的區域決定要顯示低中高風險的處置建議
if round(x(age_new)) in range(3, 17):
    if report == '軸長' and language_type == 2:
        p0, p50, p75, p90, p100 = area.loc[round(x(age_new))]
        for y, eye , ODOS in (y1, eye_word[0],'OD'), (y2, eye_word[1],'OS'):
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

    if report == '軸長' and language_type != 2:
        p0, p50, p75, p90, p100 = area.loc[round(x(age_new))]
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

    if report == '球面度數'  and language_type == 2:
        p100, p50, p25, p10, p0 = area.loc[round(x(age_new))]
        for y, eye , ODOS in (y1, eye_word[0],'OD'), (y2, eye_word[1],'OS'):
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
                
    if report == '球面度數' and language_type != 2:
            p100, p50, p25, p10, p0 = area.loc[round(x(age_new))]
            eye="ODOS"
            if y1 < p25 or y2 < p25:
                display(f'{risk[2]}', target='advice')
                localStorage.setItem(eye, 0)
            elif y1 < p50 or y2 < p50:
                display(f'{risk[1]}', target='advice')
                localStorage.setItem(eye, 1)
            else:
                display(f'{risk[0]}', target='advice')
                localStorage.setItem(eye, 2)

else:
    display(samples_not_enought, target='advice')
    localStorage.setItem('右眼', '')
    localStorage.setItem('左眼', '')

#計算成長斜率
def slope_calculate(age,slope,start_point):
    age_index = age - 3
    sd_count = ((-0.5) - start_point) / 0.5
    sd_now = 1 - ( growth_base[age_index] + ( sd_count * growth_interval[age_index]))
    slope = slope * sd_now
    return slope

#計算球面度數衰減率
def attu_calculate(age,slope,start_point):
    if age - 3 < 14 and age - 3 >= 0:
        age_index = age - 3
    elif age - 3 < 0: 
        age_index = 0
    else:
        age_index = 13
    sd_count = ((-0.5) - start_point) / 0.5
    sd_now = 1 - ( growth_base[age_index] + ( sd_count * growth_interval[age_index]))
    attu = (slope /  sd_now) *0.0962
    return -attu

#計算軸長衰減率
def attu_calculate_AL(attu,start_point):
    attu = attu + ((start_point - 25) * (-0.003))
    return attu
current_slope_rate_OD = 0
current_slope_rate_OS = 0

#把當下以及歷史資料組合並且加上label
if len(records_py)!=0 :#and round(x(age_new)) in range(3,17)
    for index,record in enumerate(records_py):
        if record[od] != "" and record[os] != "":
            if index ==0 :
                if language_type !=0:
                    label_show_OD = 'Latest OD'
                    label_show_OS = 'Latest OS'
                else:
                    label_show_OD = '右眼最新\n紀錄'
                    label_show_OS = '左眼最新\n紀錄'
                marker_show_OD = '$R$'
                marker_show_OS = '$L$'
            elif index == 1:
                if language_type !=0:
                    label_show_OD = 'OD in past'
                    label_show_OS = 'OS in past'
                else:
                    label_show_OD = '右眼歷史\n紀錄'
                    label_show_OS = '左眼歷史\n紀錄'
                marker_show_OD = '.'
                marker_show_OS = '.'
            else:
                label_show_OD=''
                label_show_OS=''
                marker_show_OD = '.'
                marker_show_OS = '.'
            plt.scatter(x(record[11]), record[od], color='red', marker=marker_show_OD , label=label_show_OD)
            plt.scatter(x(record[11]), record[os], color='blue', marker=marker_show_OS , label=label_show_OS)
            if index == 1 :
                if x(age_new)-x(record[11]) == 0:
                    current_slope_rate_OD=0
                    OD_zero=True
                    current_slope_rate_OS=0
                    OS_zero=True
                else:
                    current_slope_rate_OD = (OD_new - record[od]) / (x(age_new)-x(record[11]))
                    current_slope_rate_OS = (OS_new - record[os]) / (x(age_new)-x(record[11]))
                    current_slope_attu_OD = attu_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)
                    current_slope_attu_OS = attu_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
            else :
                if OD_zero ==True and x(age_new)-x(record[11]) > 0:
                    current_slope_rate_OD = (OD_new - record[od]) / (x(age_new)-x(record[11]))
                    current_slope_attu_OD = attu_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)
                    OD_zero = False
                    current_slope_rate_OS = (OS_new - record[os]) / (x(age_new)-x(record[11]))
                    current_slope_attu_OS = attu_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
                    OS_zero=False
            x_age_record.append(x(record[11]))
            x_age_record_text.append(_y_m(record[11],0,'●'))
            y_od_record.append(record[od])
            y_os_record.append(record[os])
    if report =='球面度數':
        if current_slope_rate_OD >= 0 or current_slope_rate_OD < -3:
            current_slope_rate_OD=-1.078
            current_slope_attu_OD=0.1038
            if  round(x(age_new)) in range(3,17):
                current_slope_rate_OD = slope_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)
                current_slope_attu_OD = attu_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)

        if current_slope_rate_OS >= 0 or current_slope_rate_OS < -3:
            current_slope_rate_OS=-1.078
            current_slope_attu_OS=0.1038
            if  round(x(age_new)) in range(3,17):
                current_slope_rate_OS = slope_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
                current_slope_attu_OS = attu_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
    
    else:
        current_slope_attu_OD=0.15
        current_slope_attu_OS=0.15
        if current_slope_rate_OD <= 0 :
            current_slope_rate_OD=1.326#1.127
            current_slope_attu_OD=0.15
            for i in range(round(x(age_new))-3):
                current_slope_rate_OD = current_slope_rate_OD * ( 1 - current_slope_attu_OD)
            current_slope_attu_OD = attu_calculate_AL(current_slope_attu_OD,OD_new)

        current_slope_attu_OD = attu_calculate_AL(current_slope_attu_OD,OD_new)
        if current_slope_rate_OS <= 0 :
            current_slope_rate_OS=1.326
            current_slope_attu_OS=0.15
            for i in range(round(x(age_new))-3):
                current_slope_rate_OS = current_slope_rate_OS * ( 1 - current_slope_attu_OS)
            current_slope_attu_OS = attu_calculate_AL(current_slope_attu_OS,OS_new)

        current_slope_attu_OS = attu_calculate_AL(current_slope_attu_OS,OS_new)
        # print('計算完得到的衰減率',current_slope_attu_OD,current_slope_attu_OS,round(x(age)))
    # print(f'Last age :{x_age_record[1]}  OD : {y_od_record[1]} OS : {y_os_record[1]} slope {current_slope_rate_OD}')
    # print(f'Now age :{x_age_record[0]}  OD : {y_od_record[0]} OS : {y_os_record[0]} slope {current_slope_rate_OS}')
    plt.plot(x_age_record, y_od_record, color='red', alpha=0.2)
    plt.plot(x_age_record, y_os_record, color='blue', alpha=0.2)
else : 
    if report =='球面度數':
        current_slope_rate_OD=-1.078
        current_slope_rate_OS=-1.078
        current_slope_attu_OD=0.1038
        current_slope_attu_OS=0.1038
        if  round(x(age_new)) in range(3,17):
            current_slope_rate_OD = slope_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)
            current_slope_rate_OS = slope_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
            current_slope_attu_OD = attu_calculate(int(x(age_new)),current_slope_rate_OD,OD_new)
            current_slope_attu_OS = attu_calculate(int(x(age_new)),current_slope_rate_OS,OS_new)
    else:
        current_slope_rate_OD=1.326#1.127
        current_slope_rate_OS=1.326#1.127
        current_slope_attu_OD=0.15
        current_slope_attu_OS=0.15
        for i in range(round(x(age_new))-3):
            current_slope_rate_OD = current_slope_rate_OD * ( 1 - current_slope_attu_OD)
        current_slope_rate_OS = current_slope_rate_OD
        current_slope_attu_OD = attu_calculate_AL(current_slope_attu_OD,OD_new)
        current_slope_attu_OS = attu_calculate_AL(current_slope_attu_OS,OS_new)
################################## 
################################## 
# if y1 != "":
#     if y1 == 0 and report == '軸長':
#         y1 = 19.5
#     if language_type == 1 :
#         plt.scatter(x(age), y1, color='red', label='OD now' , marker='$R$', zorder=9) 
#     else :
#         plt.scatter(x(age), y1, color='red', label='右眼當前\n資料' , marker='$R$', zorder=9) 
#     #print("od is : " + str(y1 ))
# if y2 != "":
#     if y2 == 0 and report == '軸長':
#         y2 = 19.5
#     if language_type == 1 :
#         plt.scatter(x(age), y2, color='blue', label='OS now' , marker='$L$', zorder=9)
#     else :
#         plt.scatter(x(age), y2, color='blue', label='左眼當前\n資料' , marker='$L$', zorder=9)
    #print("os is : " + str(y2))
# print(f'OD is {y1} OS is {y2} Age is {int(x(age))} record length {len(records_py)} suggestion {suggestion}')

#依照得到的斜率與衰減率計算未來球面度數的成長數據
def curve_calculation(curve_point,current_slope_rate,current_slope_attu,age,control_rate):
    age_index = age - 3
    sd_count = ((-0.5) - curve_point[0]) / 0.5
    attu_age_base = attu_base[age_index]
    attu_age_interval =  attu_interval[age_index]
    # print(current_slope_rate)
    current_slope_rate = current_slope_rate * (1-control_rate)
    for i in range(1,len(curve_point)):#(let i = 1; i < age_growth.length; i++) {
        # curve_point[i] = curve_point[i-1] + current_slope_rate
        if (current_slope_rate < -0.1) :
            current_slope_rate += current_slope_attu * (1-control_rate) * ( 1 + (attu_age_interval*sd_count) )* (1 - attu_age_base)
        else :
            current_slope_rate += current_slope_attu * (1-control_rate) * ( 1 + (attu_age_interval*sd_count) )* (1 - attu_age_base) * 0.2
        if (current_slope_rate > -0.01) :
            current_slope_rate = 0
        curve_point[i] = curve_point[i-1] + current_slope_rate
    return curve_point

#依照得到的斜率與衰減率計算未來軸長的成長數據
def curve_calculation_AL(curve_point,slope,attu,age,control_rate):
    # print(current_slope_rate)
    current_slope_rate = slope * (1 - attu ) * (1 - control_rate)
    for i in range(1,len(curve_point)):#(let i = 1; i < age_growth.length; i++) {
        curve_point[i] = curve_point[i-1] + current_slope_rate
        current_slope_rate = current_slope_rate * (1 - attu ) * (1 - control_rate)
        age = age + 1
    return curve_point
##################################
growth_without_control_rate=[0]*agecounter#this is for initial
growth_with_control_rate=[0]*agecounter#this is for initial
if suggestion == "一般眼鏡":
    control_rate = 0.13
elif suggestion == "軟式隱形眼鏡" or suggestion == '近視控制隱形眼鏡':
    control_rate = 0.43
elif suggestion == "周邊離焦鏡片" or suggestion == '周邊離焦(近視控制)鏡片':
    control_rate = 0.19
elif suggestion == "雙焦眼鏡":
    control_rate = 0.50
elif suggestion == "漸進多焦點眼鏡":
    control_rate = 0.10
elif suggestion == "角膜塑型片":
    control_rate = 0.44
else :
    control_rate = 0.13

#把過去、現在與未來的資料畫在圖上
if OD_new != "" and round(x(age_new)) in range(3,17) and report == '球面度數':#and slope_groupby[sex].get(suggestion)
    growth_without_control_rate[0] = OD_new
    growth_with_control_rate[0] = OD_new
    growth_without_control_rate = curve_calculation(growth_without_control_rate,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0)
    growth_with_control_rate = curve_calculation(growth_with_control_rate,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),control_rate)
    if language_type != 0: 
        plt.plot(x_age_series, growth_without_control_rate, color='red', linewidth=0.7, label='OD \nNo treatment')#, alpha=0.7
        plt.plot(x_age_series, growth_with_control_rate, color='#e34fe8', linestyle='--', linewidth=0.9, label='OD Control')#, alpha=0.7
    else:
        plt.plot(x_age_series, growth_without_control_rate, color='red', linewidth=0.7, label='右眼無控制\n成長趨勢')#, alpha=0.7
        plt.plot(x_age_series, growth_with_control_rate, color='#e34fe8', linestyle='--', linewidth=0.9, label='右眼有控制\n成長趨勢')#, alpha=0.7
if OS_new != "" and round(x(age_new)) in range(3,17) and report == '球面度數':#and slope_groupby[sex].get(suggestion)
    growth_without_control_rate[0] = OS_new
    growth_with_control_rate[0] = OS_new
    growth_without_control_rate = curve_calculation(growth_without_control_rate,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0)
    growth_with_control_rate = curve_calculation(growth_with_control_rate,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),control_rate) 
    if language_type != 0: 
        plt.plot(x_age_series, growth_without_control_rate, color='blue', linewidth=0.7, label='OS \nNo treatment')#, alpha=0.7
        plt.plot(x_age_series, growth_with_control_rate, color='#4FC1E8', linestyle='--', linewidth=0.9, label='OS Control')#, alpha=0.7
    else:
        plt.plot(x_age_series, growth_without_control_rate, color='blue', linewidth=0.7, label='左眼無控制\n成長趨勢')#, alpha=0.7
        plt.plot(x_age_series, growth_with_control_rate, color='#4FC1E8', linestyle='--', linewidth=0.9, label='左眼有控制\n成長趨勢')#, alpha=0.7  
if OD_new != "" and round(x(age_new)) in range(3,17) and report == '軸長':
    growth_without_control_rate[0] = OD_new
    # print('OD slope is ',current_slope_rate_OD,y1)
    growth_without_control_rate = curve_calculation_AL(growth_without_control_rate,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0)
    if language_type != 0: 
        plt.plot(x_age_series, growth_without_control_rate, color='red', linewidth=0.7, label='OD No treatment')#, alpha=0.7
    else:
        plt.plot(x_age_series, growth_without_control_rate, color='red', linewidth=0.7, label='右眼無控制\n成長趨勢')#, alpha=0.7
if OS_new != "" and round(x(age_new)) in range(3,17) and report == '軸長':
    growth_without_control_rate[0] = OS_new
    # print('OS slope is ',current_slope_rate_OS,y2)
    growth_without_control_rate = curve_calculation_AL(growth_without_control_rate,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0)
    if language_type != 0: 
        plt.plot(x_age_series, growth_without_control_rate, color='blue', linewidth=0.7, label='OD No treatment')#, alpha=0.7
    else:
        plt.plot(x_age_series, growth_without_control_rate, color='blue', linewidth=0.7, label='右眼無控制\n成長趨勢')#, alpha=0.7
##################################
# plt.plot(3, 19.5 , linestyle='none' , marker='None', alpha=0, label=db_version)

#設定x軸y軸的單位與範圍
if report == '軸長':
    if language_type == 1:
        plt.legend(loc='center right' , bbox_to_anchor=(1.22, 0.35),fontsize=8)
    else:
        plt.legend(loc='center right' , bbox_to_anchor=(1.22, 0.35),fontsize=8,prop=custom_font)
if report == '球面度數':
    if language_type == 1:
        plt.legend(loc='center right' , bbox_to_anchor=(1.22, 0.55),fontsize=8)
    else:
        plt.legend(loc='center right' , bbox_to_anchor=(1.22, 0.55),fontsize=8,prop=custom_font)
plt.xticks(range(3, 17 if x(age_new) + 1 <= 16 else int(x(age_new)) + 2))
plt.yticks(range(20, 30) if report == '軸長' else range(-8, 7))

#根據語言設定繪圖的標題
if language_type== 0 :
    plt.xlabel("年齡 (歲)", fontproperties=custom_font_s, fontsize=12)
elif language_type== 2:
    plt.xlabel("年龄 (岁)", fontproperties=custom_font_s, fontsize=12)
else :
    plt.xlabel("Age (years)", fontsize=12)
#plt.xlabel('Age', fontsize=12)
if language_type== 0 :
    plt.ylabel('軸長 (mm)' if report == '軸長' else '球面度數 (D)', fontproperties=custom_font_s, fontsize=12)
elif language_type== 2:
    plt.ylabel('轴长 (mm)' if report == '軸長' else '球面度数 (D)', fontproperties=custom_font_s, fontsize=12)
else :
    plt.ylabel('Axial Length (mm)' if report == '軸長' else 'SPH (degrees)', fontsize=12)
#plt.ylabel('Axial Length' if report == '軸長' else 'SPH', fontsize=12)
plt.margins(0)
plt.subplots_adjust(left=0.1, right=0.84, bottom=0.1, top=0.9, wspace=0.8, hspace=0.2)
if report == '軸長':
    plt.ylim(21, 29)
    plt.xlim(3, 16)
    # plt.text(16 if x(age) + 1 < 16 else x(age) + 1, 18.8 if sex=='女' else 19.2, f'', horizontalalignment='right', fontsize=8)
if report == '球面度數':
    if language_type== 0 or language_type == 1:
        plt.ylim(2, -8)
    else:
        plt.ylim(-8, 2)
    plt.xlim(3, 16)
    # plt.text(16 if x(age) + 1 < 16 else x(age) + 1, -10.5 if sex=='女' else -10.5, f'', horizontalalignment='right', fontsize=8)
plt.grid(alpha=0.2)

#設定放大的效果
ax = plt.gca()
if report == '軸長':
    ax.set_aspect(aspect=1.25)
else :
    ax.set_aspect(aspect='auto')

#把圖放在html中
# display(plt, target='plot')

import json
from js import Bokeh, JSON
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, TableColumn, NumberFormatter, CheckboxGroup, CustomJS, Legend, PanTool, Range1d
from bokeh.layouts import column, row

#############右眼部分
# 繪圖區域設定與工具設定
if report == '球面度數':
    y_range = Range1d(start=2, end=-8)
    y_range.max_interval = 10 
    x_range = Range1d(start=3, end=16)
    x_range.max_interval = 10 
    p = figure(width=650, height=650,x_range=x_range,y_range=y_range,title=f"{sex}童右眼球面度數成長趨勢",x_axis_label="年紀(歲)",y_axis_label="度 (D)",)
else:
    y_range = Range1d(start=21, end=29)
    y_range.max_interval = 10 
    p = figure(width=650, height=650,x_range=(3, 16),y_range=(21, 29),title=f"{sex}童右眼軸長成長趨勢",x_axis_label="年紀(歲)",y_axis_label="軸長 (mm)")

p.title.text_font_size = "16pt"
p.title.align = "center"
original_pan = p.select_one(PanTool)
p.tools.remove(original_pan)
pan_y = PanTool(dimensions="height")
p.add_tools(pan_y)
p.toolbar.active_drag = pan_y

# 根據讀取進來的資料設定低中高風險的位置與畫出歷史資料的紀錄
area = stacked_area.loc[sex].loc[3:16]
area_25_smooth = moving_average_cal(area['P25'])
area_50_smooth = moving_average_cal(area['P50'])
varea_low_OD = p.varea(x=area.index, y1=area_50_smooth, y2=10, fill_color="lightgreen", fill_alpha=0.2)#,legend_label='低風險'
varea_medium_OD = p.varea(x=area.index, y1=area_25_smooth, y2=area_50_smooth, fill_color="yellow", fill_alpha=0.2)#,legend_label='中風險'
varea_high_OD = p.varea(x=area.index, y1=-10, y2=area_25_smooth, fill_color="red", fill_alpha=0.2)#,legend_label='高風險'
if len(y_od_record)>1:
    line_history_OD = p.line(x_age_record, y_od_record, line_width=1, color="red")#,  legend_label="右眼歷史紀錄"
    p.circle(x_age_record[1:], y_od_record[1:], size=8, color="firebrick")
p.circle(x_age_record[0], y_od_record[0], line_color="firebrick", fill_color = '#e34fe8', line_width=2, size=8)

# 做不同處置方式的初始設定
growth_without_control_rate_OD=[0]*agecounter#this is for initial
# growth_with_control_rate_OD=[0]*agecounter#this is for initial
growth_with_RG_control_rate_OD=[0]*agecounter#一般眼鏡 Regular glasses
growth_with_PAS_control_rate_OD=[0]*agecounter#漸進多焦點眼鏡 Progressive addition spectacles
growth_with_EB_control_rate_OD=[0]*agecounter#雙焦眼鏡 Executive bifocals
growth_with_PDS_control_rate_OD=[0]*agecounter#周邊離焦鏡片 Peripheral defocus spectacles
growth_with_SCLFMC_control_rate_OD=[0]*agecounter#軟式隱形眼鏡 Soft contact lens for myopia control
growth_with_OKL_control_rate_OD=[0]*agecounter#角膜塑型片 Ortho_K_lenses

# 計算不同處置方式的未來發展趨勢並畫在圖上
if OD_new != "" and round(x(age_new)) in range(3,17) and report == '球面度數':#and slope_groupby[sex].get(suggestion)
    growth_without_control_rate_OD[0] = OD_new
    growth_with_RG_control_rate_OD[0] = growth_with_PAS_control_rate_OD[0] = growth_with_EB_control_rate_OD[0] = growth_with_PDS_control_rate_OD[0] = growth_with_SCLFMC_control_rate_OD[0] = growth_with_OKL_control_rate_OD[0] = OD_new
    growth_without_control_rate_OD = curve_calculation(growth_without_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0)
    growth_with_RG_control_rate_OD = curve_calculation(growth_with_RG_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.13)
    growth_with_PAS_control_rate_OD = curve_calculation(growth_with_PAS_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.43)
    growth_with_EB_control_rate_OD = curve_calculation(growth_with_EB_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.19)
    growth_with_PDS_control_rate_OD = curve_calculation(growth_with_PDS_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.50)
    growth_with_SCLFMC_control_rate_OD = curve_calculation(growth_with_SCLFMC_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.10)
    growth_with_OKL_control_rate_OD = curve_calculation(growth_with_OKL_control_rate_OD,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0.44)

    line_without_control_OD = p.line(x_age_series, growth_without_control_rate_OD, line_width=1.5, color="red", line_dash="dotted")#, alpha=0.7,  legend_label="無控制"
    line_RG_OD = p.line(x_age_series, growth_with_RG_control_rate_OD, line_width=1.5, color="#1f77b4", line_dash="dashed")#, alpha=0.7, legend_label="一般眼鏡"
    line_PAS_OD = p.line(x_age_series, growth_with_PAS_control_rate_OD, line_width=1.5, color="#d62728", line_dash="dotdash")#, alpha=0.7, legend_label="漸進多焦點眼鏡"
    line_EB_OD = p.line(x_age_series, growth_with_EB_control_rate_OD, line_width=1.5, color="#2ca02c", line_dash="dotted")#, alpha=0.7, legend_label="雙焦眼鏡"
    line_PDS_OD = p.line(x_age_series, growth_with_PDS_control_rate_OD, line_width=1.5, color="#9467bd", line_dash="dotted")#, alpha=0.7, legend_label="周邊離焦鏡片"
    line_SCLFMC_OD = p.line(x_age_series, growth_with_SCLFMC_control_rate_OD, line_width=1.5, color="#8c564b", line_dash="dotdash")#, alpha=0.7, legend_label="軟式隱形眼鏡"
    line_OKL_OD = p.line(x_age_series, growth_with_OKL_control_rate_OD, line_width=1.5, color="#7f7f7f", line_dash="dashdot")#, alpha=0.7, legend_label="角膜塑型片"
    
    line_RG_OD.visible = line_PAS_OD.visible = line_EB_OD.visible = line_PDS_OD.visible = line_SCLFMC_OD.visible = line_OKL_OD.visible = False

# 做標籤的設定
legend_items_line1 = []
legend_items_line1.append(("低風險", [varea_low_OD]))
legend_items_line1.append(("中風險", [varea_medium_OD]))
legend_items_line1.append(("高風險", [varea_high_OD]))
if len(y_od_record)>1:
    legend_items_line1.append(("右眼歷史紀錄", [line_history_OD]))
legend_items_line1.append(("無控制", [line_without_control_OD]))
legend_items_line2 = []
legend_items_line2.append(("一般眼鏡", [line_RG_OD]))
legend_items_line2.append(("漸進多焦點眼鏡", [line_PAS_OD]))
legend_items_line2.append(("雙焦眼鏡", [line_EB_OD]))
legend_items_line2.append(("周邊離焦鏡片", [line_PDS_OD]))
legend_items_line2.append(("軟式隱形眼鏡", [line_SCLFMC_OD]))
legend_items_line2.append(("角膜塑型片", [line_OKL_OD]))

# 從這邊設定要不要顯示指定的處置方式發展趨勢
checkbox_OD = CheckboxGroup(labels=[ "一般眼鏡","漸進多焦點眼鏡","雙焦眼鏡","周邊離焦鏡片","軟式隱形眼鏡","角膜塑型片"], active=[])
checkbox_OD.js_on_change("active", CustomJS(args=dict(l_RG_OD=line_RG_OD, l_PAS_OD=line_PAS_OD, l_EB_OD=line_EB_OD, l_PDS_OD=line_PDS_OD, l_SCLFMC_OD=line_SCLFMC_OD, l_OKL_OD=line_OKL_OD), code="""
    l_RG_OD.visible = cb_obj.active.includes(0);
    l_PAS_OD.visible = cb_obj.active.includes(1);
    l_EB_OD.visible = cb_obj.active.includes(2);
    l_PDS_OD.visible = cb_obj.active.includes(3);
    l_SCLFMC_OD.visible = cb_obj.active.includes(4);
    l_OKL_OD.visible = cb_obj.active.includes(5);                                     
"""))
if len(y_od_record)>1:
    df = pd.DataFrame({
        # '年紀': x_age_record[::-1] + x_age_series[1:-1],
        '年紀': x_age_record_text[:0:-1] + x_age_series_text[:-1],
        '無控制': y_od_record[:0:-1] + growth_without_control_rate_OD[:-1],
        '一般眼鏡': y_od_record[:0:-1] + growth_with_RG_control_rate_OD[:-1],
        '漸進多焦點眼鏡': y_od_record[:0:-1] + growth_with_PAS_control_rate_OD[:-1],
        '雙焦眼鏡': y_od_record[:0:-1] + growth_with_EB_control_rate_OD[:-1],
        '一般周邊離焦鏡片眼鏡': y_od_record[:0:-1] + growth_with_PDS_control_rate_OD[:-1],
        '軟式隱形眼鏡': y_od_record[:0:-1] + growth_with_SCLFMC_control_rate_OD[:-1],
        '角膜塑型片': y_od_record[:0:-1] + growth_with_OKL_control_rate_OD[:-1]
    })
else:
    df = pd.DataFrame({
        # '年紀': x_age_record[::-1] + x_age_series[1:-1],
        '年紀': x_age_record_text+ x_age_series_text[:-1],
        '無控制': y_od_record + growth_without_control_rate_OD[:-1],
        '一般眼鏡': y_od_record + growth_with_RG_control_rate_OD[:-1],
        '漸進多焦點眼鏡': y_od_record + growth_with_PAS_control_rate_OD[:-1],
        '雙焦眼鏡': y_od_record + growth_with_EB_control_rate_OD[:-1],
        '一般周邊離焦鏡片眼鏡': y_od_record + growth_with_PDS_control_rate_OD[:-1],
        '軟式隱形眼鏡': y_od_record + growth_with_SCLFMC_control_rate_OD[:-1],
        '角膜塑型片': y_od_record + growth_with_OKL_control_rate_OD[:-1]
    })

# 建立一個table並把全部的數據放進去
columns = [
    TableColumn(field="年紀", title="年紀"),
    TableColumn(field="無控制", title="無控制", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="一般眼鏡", title="一般眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="漸進多焦點眼鏡", title="漸進多焦點眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="雙焦眼鏡", title="雙焦眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="一般周邊離焦鏡片眼鏡", title="一般周邊離焦鏡片眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="軟式隱形眼鏡", title="軟式隱形眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="角膜塑型片", title="角膜塑型片一般眼鏡", formatter=NumberFormatter(format="0.00"))
]
source = ColumnDataSource(df)
data_table = DataTable(source=source, columns=columns, width=550, height=600, index_position=None)
legend_1 = Legend(items=legend_items_line1, location="bottom_center", orientation="horizontal")
legend_2 = Legend(items=legend_items_line2, location="bottom_center", orientation="horizontal")

# 最後整理排版並輸出結果
p.add_layout(legend_1, 'below')
p.add_layout(legend_2, 'below')
layout = row(column(p , checkbox_OD), data_table)
p_json = json.dumps(json_item(layout, "plot"))

Bokeh.embed.embed_item(JSON.parse(p_json))

#############左眼部分
# 繪圖區域設定與工具設定
if report == '球面度數':
    y_range = Range1d(start=2, end=-8)
    y_range.max_interval = 10 
    x_range = Range1d(start=3, end=16)
    x_range.max_interval = 10 
    p = figure(width=650, height=650,x_range=(3, 16),y_range=(2, -8),title=f"{sex}童左眼球面度數成長趨勢",x_axis_label="年紀(歲)",y_axis_label="度 (D)")
else:
    y_range = Range1d(start=21, end=29)
    y_range.max_interval = 10 
    x_range = Range1d(start=3, end=16)
    x_range.max_interval = 10 
    p = figure(width=650, height=650,x_range=(3, 16),y_range=(21, 29),title=f"{sex}童左眼軸長成長趨勢",x_axis_label="年紀(歲)",y_axis_label="軸長 (mm)")

p.title.text_font_size = "16pt"
p.title.align = "center"
original_pan = p.select_one(PanTool)
p.tools.remove(original_pan)
pan_y = PanTool(dimensions="height")
p.add_tools(pan_y)
p.toolbar.active_drag = pan_y

# 根據讀取進來的資料設定低中高風險的位置與畫出歷史資料的紀錄
area = stacked_area.loc[sex].loc[3:16]
area_25_smooth = moving_average_cal(area['P25'])
area_50_smooth = moving_average_cal(area['P50'])
varea_low_OS = p.varea(x=area.index, y1=area_50_smooth, y2=10, fill_color="lightgreen", fill_alpha=0.2)#,legend_label='低風險'
varea_medium_OS = p.varea(x=area.index, y1=area_25_smooth, y2=area_50_smooth, fill_color="yellow", fill_alpha=0.2)#,legend_label='中風險'
varea_high_OS = p.varea(x=area.index, y1=-10, y2=area_25_smooth, fill_color="red", fill_alpha=0.2)#,legend_label='高風險'
if len(y_os_record)>1:
    line_history_OS = p.line(x_age_record, y_os_record, line_width=1, color="blue")#, legend_label="左眼歷史紀錄"
    p.circle(x_age_record[1:], y_os_record[1:], size=8, color="navy")
p.circle(x_age_record[0], y_os_record[0], line_color="navy", fill_color = '#4FC1E8', line_width=2,  size=8)

# 做不同處置方式的初始設定
growth_without_control_rate_OS=[0]*agecounter#this is for initial
# growth_with_control_rate_OS=[0]*agecounter#this is for initial
growth_with_RG_control_rate_OS=[0]*agecounter#一般眼鏡 Regular glasses
growth_with_PAS_control_rate_OS=[0]*agecounter#漸進多焦點眼鏡 Progressive addition spectacles
growth_with_EB_control_rate_OS=[0]*agecounter#雙焦眼鏡 Executive bifocals
growth_with_PDS_control_rate_OS=[0]*agecounter#周邊離焦鏡片 Peripheral defocus spectacles
growth_with_SCLFMC_control_rate_OS=[0]*agecounter#軟式隱形眼鏡 Soft contact lens for myopia control
growth_with_OKL_control_rate_OS=[0]*agecounter#角膜塑型片 Ortho_K_lenses

# 計算不同處置方式的未來發展趨勢並畫在圖上
if OS_new != "" and round(x(age_new)) in range(3,17) and report == '球面度數':#and slope_groupby[sex].get(suggestion)
    growth_without_control_rate_OS[0] = OS_new
    growth_with_RG_control_rate_OS[0] = growth_with_PAS_control_rate_OS[0] = growth_with_EB_control_rate_OS[0] = growth_with_PDS_control_rate_OS[0] = growth_with_SCLFMC_control_rate_OS[0] = growth_with_OKL_control_rate_OS[0] = OS_new
    growth_without_control_rate_OS = curve_calculation(growth_without_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0)
    growth_with_RG_control_rate_OS = curve_calculation(growth_with_RG_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.13)
    growth_with_PAS_control_rate_OS = curve_calculation(growth_with_PAS_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.43)
    growth_with_EB_control_rate_OS = curve_calculation(growth_with_EB_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.19)
    growth_with_PDS_control_rate_OS = curve_calculation(growth_with_PDS_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.50)
    growth_with_SCLFMC_control_rate_OS = curve_calculation(growth_with_SCLFMC_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.10)
    growth_with_OKL_control_rate_OS = curve_calculation(growth_with_OKL_control_rate_OS,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0.44)
    
    line_without_control_OS = p.line(x_age_series, growth_without_control_rate_OS, line_width=1.5, color="blue", line_dash="dotted")#, alpha=0.7,  legend_label="無控制"
    line_RG_OS = p.line(x_age_series, growth_with_RG_control_rate_OS, line_width=1.5, color="#1f77b4", line_dash="dashed")#, alpha=0.7, legend_label="一般眼鏡"
    line_PAS_OS = p.line(x_age_series, growth_with_PAS_control_rate_OS, line_width=1.5, color="#d62728", line_dash="dotdash")#, alpha=0.7, legend_label="漸進多焦點眼鏡"
    line_EB_OS = p.line(x_age_series, growth_with_EB_control_rate_OS, line_width=1.5, color="#2ca02c", line_dash="dotted")#, alpha=0.7, legend_label="雙焦眼鏡"
    line_PDS_OS = p.line(x_age_series, growth_with_PDS_control_rate_OS, line_width=1.5, color="#9467bd", line_dash="dotted")#, alpha=0.7, legend_label="周邊離焦鏡片"
    line_SCLFMC_OS = p.line(x_age_series, growth_with_SCLFMC_control_rate_OS, line_width=1.5, color="#8c564b", line_dash="dotdash")#, alpha=0.7, legend_label="軟式隱形眼鏡"
    line_OKL_OS = p.line(x_age_series, growth_with_OKL_control_rate_OS, line_width=1.5, color="#7f7f7f", line_dash="dashdot")#, alpha=0.7, legend_label="角膜塑型片"
    
    line_RG_OS.visible = line_PAS_OS.visible = line_EB_OS.visible = line_PDS_OS.visible = line_SCLFMC_OS.visible = line_OKL_OS.visible = False

# 做標籤的設定
legend_items_line1 = []
legend_items_line1.append(("低風險", [varea_low_OS]))
legend_items_line1.append(("中風險", [varea_medium_OS]))
legend_items_line1.append(("高風險", [varea_high_OS]))
if len(y_os_record)>1:
    legend_items_line1.append(("右眼歷史紀錄", [line_history_OS]))
legend_items_line1.append(("無控制", [line_without_control_OS]))
legend_items_line2 = []
legend_items_line2.append(("一般眼鏡", [line_RG_OS]))
legend_items_line2.append(("漸進多焦點眼鏡", [line_PAS_OS]))
legend_items_line2.append(("雙焦眼鏡", [line_EB_OS]))
legend_items_line2.append(("周邊離焦鏡片", [line_PDS_OS]))
legend_items_line2.append(("軟式隱形眼鏡", [line_SCLFMC_OS]))
legend_items_line2.append(("角膜塑型片", [line_OKL_OS]))

# 從這邊設定要不要顯示指定的處置方式發展趨勢
checkbox_OS = CheckboxGroup(labels=[ "一般眼鏡","漸進多焦點眼鏡","雙焦眼鏡","周邊離焦鏡片","軟式隱形眼鏡","角膜塑型片"], active=[])
checkbox_OS.js_on_change("active", CustomJS(args=dict(l_RG_OS=line_RG_OS, l_PAS_OS=line_PAS_OS, l_EB_OS=line_EB_OS, l_PDS_OS=line_PDS_OS, l_SCLFMC_OS=line_SCLFMC_OS, l_OKL_OS=line_OKL_OS), code="""
    l_RG_OS.visible = cb_obj.active.includes(0);
    l_PAS_OS.visible = cb_obj.active.includes(1);
    l_EB_OS.visible = cb_obj.active.includes(2);
    l_PDS_OS.visible = cb_obj.active.includes(3);
    l_SCLFMC_OS.visible = cb_obj.active.includes(4);
    l_OKL_OS.visible = cb_obj.active.includes(5);                                     
"""))
if len(y_os_record)>1:
    df = pd.DataFrame({
        # '年紀': x_age_record[::-1] + x_age_series[1:-1],
        '年紀': x_age_record_text[:0:-1] + x_age_series_text[:-1],
        '無控制': y_os_record[:0:-1] + growth_without_control_rate_OS[:-1],
        '一般眼鏡': y_os_record[:0:-1] + growth_with_RG_control_rate_OS[:-1],
        '漸進多焦點眼鏡': y_os_record[:0:-1] + growth_with_PAS_control_rate_OS[:-1],
        '雙焦眼鏡': y_os_record[:0:-1] + growth_with_EB_control_rate_OS[:-1],
        '一般周邊離焦鏡片眼鏡': y_os_record[:0:-1] + growth_with_PDS_control_rate_OS[:-1],
        '軟式隱形眼鏡': y_os_record[:0:-1] + growth_with_SCLFMC_control_rate_OS[:-1],
        '角膜塑型片': y_os_record[:0:-1] + growth_with_OKL_control_rate_OS[:-1]
    })
else:
    df = pd.DataFrame({
        # '年紀': x_age_record[::-1] + x_age_series[1:-1],
        '年紀': x_age_record_text + x_age_series_text[:-1],
        '無控制': y_os_record + growth_without_control_rate_OS[:-1],
        '一般眼鏡': y_os_record + growth_with_RG_control_rate_OS[:-1],
        '漸進多焦點眼鏡': y_os_record + growth_with_PAS_control_rate_OS[:-1],
        '雙焦眼鏡': y_os_record + growth_with_EB_control_rate_OS[:-1],
        '一般周邊離焦鏡片眼鏡': y_os_record + growth_with_PDS_control_rate_OS[:-1],
        '軟式隱形眼鏡': y_os_record + growth_with_SCLFMC_control_rate_OS[:-1],
        '角膜塑型片': y_os_record + growth_with_OKL_control_rate_OS[:-1]
    })

# 建立一個table並把全部的數據放進去
columns = [
    TableColumn(field="年紀", title="年紀"),
    TableColumn(field="無控制", title="無控制", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="一般眼鏡", title="一般眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="漸進多焦點眼鏡", title="漸進多焦點眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="雙焦眼鏡", title="雙焦眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="一般周邊離焦鏡片眼鏡", title="一般周邊離焦鏡片眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="軟式隱形眼鏡", title="軟式隱形眼鏡", formatter=NumberFormatter(format="0.00")),
    TableColumn(field="角膜塑型片", title="角膜塑型片一般眼鏡", formatter=NumberFormatter(format="0.00"))
]


source = ColumnDataSource(df)
data_table = DataTable(source=source, columns=columns, width=550, height=600, index_position=None)
legend_1 = Legend(items=legend_items_line1, location="bottom_center", orientation="horizontal")
legend_2 = Legend(items=legend_items_line2, location="bottom_center", orientation="horizontal")
p.add_layout(legend_1, 'below')
p.add_layout(legend_2, 'below')

# 最後整理排版並輸出結果
layout = row(column(p , checkbox_OS), data_table)
p_json = json.dumps(json_item(layout, "table"))
Bokeh.embed.embed_item(JSON.parse(p_json))