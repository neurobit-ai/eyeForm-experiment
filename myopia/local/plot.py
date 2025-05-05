from js import sex, age, y1, y2, records, suggestion, localStorage, report , language_type
# import os as os_e
from pyscript import display
from pyodide.ffi import JsProxy
# from pyscript import display
# current_dir = os_e.getcwd()
# print(f' plot.py at {current_dir}')
# items = os_e.listdir(current_dir)
# for item in items:
#     print(f'plot.py同資料夾內的文件{item}')

#local端的py檔案無法與html共用localStorage，所以大部分變數要先在此宣告
sex='男'
report="球面度數"#球面度數#軸長
age="18歲7個月"
# age="17歲1個月"
suggestion = "角膜塑型片"
if 'ale' in sex and sex !="":
    sex = {'Male': '男', 'Female': '女'}[sex]
# y1 = -0.5
# y2 = 0.5
y1 = -2.5
y2 = -3.25
# y1 = -4
# y2 = -4
# y1 = -1.25
# y2 = -1.5
# y1 = 25.08
# y2 = 25.47

#根據VHBI設定的衰退曲線係數
growth_base   = [ -0.246, -0.164, -0.082, 0,  0.082,0.184, 0.239,0.323, 0.378,0.434, 0.471,0.508, 0.527,0.536]
growth_interval = [-0.018,-0.014,-0.01,-0.006,-0.0022,0.0014,0.0028,0.0092,0.0143,0.0172,0.0228,0.0257,0.0307,0.0335]
attu_base =    [ -0.12,-0.08,-0.04, 0,  0.04, 0.133, 0.136,0.269, 0.3, 0.378, 0.439, 0.596,0.7, 0.77]
attu_interval =  [0.039,0.033,0.044,0.039,0.033, 0.044,0.056, 0.056,0.042, 0.053, 0.04, 0.098,0.17, 0.23]

import pandas as pd
import numpy as np
import pickle
with open('../data_to_plot_20240507.pkl', 'rb') as f:
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

#邏輯回歸的係數設定，目前已經沒有使用
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

"""#age with logarithmic calculations
data_al = [
    ["性別", "目標", "處置方式", "bo", "b1", "con_025", "con_975", "x_025", "x_975"],
    ["男", "軸長", "一般眼鏡", 2.9481, 0.1034, 2.923, 2.973, 0.091,0.116],
    ["男", "軸長", "角膜塑型片", 3.0351, 0.0716, 2.9, 3.17, 0.017, 0.126],
    ["男", "軸長", "不處置", 2.983, 0.0818, 2.972, 2.993, 0.076, 0.087],
    ["男", "軸長", "散瞳劑", 3.0975, 0.0443, 3.08, 3.115, 0.036, 0.052],
    ["男", "軸長", "一般眼鏡散瞳劑", 3.0647, 0.0673, 3.035, 3.094, 0.054, 0.081],

    ["女", "軸長", "一般眼鏡", 2.9752, 0.0708, 2.950, 3, 0.058, 0.084],
    ["女", "軸長", "角膜塑型片", 3.2655, -0.0198, 3.144, 3.387, -0.068, 0.029],
    ["女", "軸長", "不處置", 2.9600, 0.0847, 2.949, 2.971, 0.079, 0.09],
    ["女", "軸長", "散瞳劑", 3.0568, 0.0517, 3.024, 3.09, 0.037, 0.066],
    ["女", "軸長", "一般眼鏡散瞳劑", 3.0482, 0.0622, 3.01, 3.086, 0.045, 0.079],

    ["男", "球面度數", "一般眼鏡", 3.3251, -0.3325, 3.454, 3.196, -0.271, -0.394],
    ["男", "球面度數", "角膜塑型片", 3.0864, -0.1941, 3.407, 2.766, -0.330, -0.058],
    ["男", "球面度數", "不處置", 2.877, -0.1109, 2.907, 2.848, -0.096, -0.126],
    ["男", "球面度數", "散瞳劑", 2.8545, -0.1321, 2.948, 2.761, -0.090, -0.174],
    ["男", "球面度數", "一般眼鏡散瞳劑", 2.6366, -0.1012, 2.802, 2.471, -0.028, -0.175],

    ["女", "球面度數", "一般眼鏡", 2.9953, -0.1713, 3.097, 2.894, -0.121, -0.221],
    ["女", "球面度數", "角膜塑型片", 3.7620, -0.5258, 4.172, 3.352, -0.352, -0.7],
    ["女", "球面度數", "不處置", 2.91, -0.1201, 2.937, 2.883, -0.107, -0.134],
    ["女", "球面度數", "散瞳劑", 2.4921, 0.0354, 2.635, 2.35, 0.100, -0.029],
    ["女", "球面度數", "一般眼鏡散瞳劑", 2.6968, -0.1122, 2.861, 2.533, -0.041, -0.183]
]
"""
# suggestion = "散瞳劑"
if suggestion == '低散瞳劑' or suggestion == '中散瞳劑' or suggestion == '高散瞳劑' :
    indices = [index for index, row in enumerate(data_al) if row[0] == sex and row[1] == report and row[2] == "散瞳劑"]
    # print(hi)
else :
    indices = [index for index, row in enumerate(data_al) if row[0] == sex and row[1] == report and row[2] == suggestion]
#target_index = data_al[indices[0]]

#y1 = np.exp(target_index[3]+np.log(age_index)*target_index[4])
#y2 = np.exp(target_index[3]+np.log(age_index)*target_index[4])
#y1 = 0.8
#y1 = 25.08
#y2 = 0.8
#y2 = 25.31
#y1 = -2.5
#y2 = -2.75
#由於local端的py檔案無法與html共用localStorage，所以改成用變數傳遞的方式，無須再給json讀取
#避免json發生無法讀取的狀態
#import json
#records = json.loads(records)

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
OD_zero = False
OS_zero = False


for age_index in range(1,agecounter):
    x_age_series[age_index] = x_age_series[age_index-1] + 1


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
display(plt, target='plot')