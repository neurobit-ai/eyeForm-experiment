from js import sex, age, y1, y2, records, report , language_type, suggestion
from pyscript import display
from pyodide.ffi import JsProxy
import numpy as np
import re
import pickle
with open('../data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area , data_al = pickle.load(f)[report]

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
        return f'&nbsp{space01}{m_y}歲{space02}　<br>{m.group(2)}個月{sign}'
    elif language_type== 2:
        return f'&nbsp{space01}{m_y}岁{space02}{m.group(2)}个月{sign}'
    else:
        return f'&nbsp{space01}{m_y}y{space02}{m.group(2)}m{sign}'
    
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
def curve_calculation_AL(curve_point,slope,attu,age,control_rate):
    # print(current_slope_rate)
    current_slope_rate = slope * (1 - attu ) * (1 - control_rate)
    for i in range(1,len(curve_point)):#(let i = 1; i < age_growth.length; i++) {
        curve_point[i] = curve_point[i-1] + current_slope_rate
        current_slope_rate = current_slope_rate * (1 - attu ) * (1 - control_rate)
        age = age + 1
    return curve_point  

def slope_calculate(age,slope,start_point):
    age_index = age - 3
    sd_count = ((-0.5) - start_point) / 0.5
    sd_now = 1 - ( growth_base[age_index] + ( sd_count * growth_interval[age_index]))
    slope = slope * sd_now
    return slope

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

def attu_calculate_AL(attu,start_point):
    attu = attu + ((start_point - 25) * (-0.003))
    return attu
import json
records = json.loads(records)
if isinstance(records, JsProxy):
    records_py = records.to_py()
else:
    records_py = records.copy()
od, os = (18, 24) if report == '軸長' else (15, 21)
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
        
growth_base   = [ -0.246, -0.164, -0.082, 0,  0.082,0.184, 0.239,0.323, 0.378,0.434, 0.471,0.508, 0.527,0.536]
growth_interval = [-0.018,-0.014,-0.01,-0.006,-0.0022,0.0014,0.0028,0.0092,0.0143,0.0172,0.0228,0.0257,0.0307,0.0335]
attu_base =    [ -0.12,-0.08,-0.04, 0,  0.04, 0.133, 0.136,0.269, 0.3, 0.378, 0.439, 0.596,0.7, 0.77]
attu_interval =  [0.039,0.033,0.044,0.039,0.033, 0.044,0.056, 0.056,0.042, 0.053, 0.04, 0.098,0.17, 0.23]

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

#print(language_type)
if 'ale' in sex:
    sex = {'Male': '男', 'Female': '女'}[sex]

OD_zero = False
OS_zero = False
age_new = records_py[0][11]
OD_new = records_py[0][od]
OS_new = records_py[0][os]
agecounter = int(16-x(age_new))+1
if agecounter <= 0:
    agecounter = 2
growth_without_control_rate=[0]*agecounter#this is for initial
growth_with_control_rate=[0]*agecounter#this is for initial
table = {}
sign='R/L'
table['Age　'] = [f'{_y_m(age_new,0,sign)}']
if OD_new == 19.5 :
    table['OD'] = [f'<20']
elif OD_new== 30.5 :
    table['OD'] = [f'>30']
else :
    table['OD'] = [f'{OD_new:.2f}']

if OS_new == 19.5 :
    table['OS'] = [f'<20']
elif OS_new == 30.5 :
    table['OS'] = [f'>30']
else :
    table['OS'] = [f'{OS_new:.2f}']

table['OD_m'] = ['-']
table['OS_m'] = ['-']


sign=' '

OD_no_management_data=[0]*agecounter#this is for initial
OS_no_management_data=[0]*agecounter#this is for initial
OD_no_management_data[0] = OD_new
OS_no_management_data[0] = OS_new

OD_control_data=[0]*agecounter#this is for initial
OS_control_data=[0]*agecounter#this is for initial
OD_control_data[0] = OD_new
OS_control_data[0] = OS_new

current_slope_rate_OD = 0
current_slope_rate_OS = 0
if len(records_py)!=0 and round(x(age_new)) in range(3,17):
    for index,record in enumerate(records_py):
        if record[od] != "" and record[os] != "":
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

if  round(x(age_new)) in range(3,17):
    if report == '球面度數':
        OD_no_management_data = curve_calculation(OD_no_management_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0)
        OS_no_management_data = curve_calculation(OS_no_management_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0)
    else:
        OD_no_management_data = curve_calculation_AL(OD_no_management_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),0)
        OS_no_management_data = curve_calculation_AL(OS_no_management_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),0)     
    OD_control_data = curve_calculation(OD_control_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age_new)),control_rate)
    OS_control_data = curve_calculation(OS_control_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age_new)),control_rate)
    
    for age_index in range(1,agecounter):
        table['Age　'].append(f'{_y_m(age_new,age_index,sign)}')
        OD_new=OD_no_management_data[age_index]
        OS_new=OS_no_management_data[age_index]
        OD_new_control=OD_control_data[age_index]
        OS_new_control=OS_control_data[age_index]
        if report == '軸長':
            if OD_new <= 19.5 :
                table['OD'].append(f'<20')
            elif OD_new >= 30.5 :
                table['OD'].append(f'>30')
            else :
                table['OD'].append(f'{OD_new:.2f}')

            if OS_new <= 19.5 :
                table['OS'].append(f'<20')
            elif OS_new >= 30.5 :
                table['OS'].append(f'>30')
            else :
                table['OS'].append(f'{OS_new:.2f}')
        else:
            if OD_new <= -9:
                table['OD'].append(f'<-9')
            elif OD_new >= 5 :
                table['OD'].append(f'>5')
            else :
                table['OD'].append(f'{OD_new:.2f}')

            if OS_new <= -9 :
                table['OS'].append(f'<-9')
            elif OS_new >= 5 :
                table['OS'].append(f'>5')
            else :
                table['OS'].append(f'{OS_new:.2f}')
                
            if OD_new_control <= -9:
                table['OD_m'].append(f'<-9')
            elif OD_new >= 5 :
                table['OD_m'].append(f'>5')
            else :
                table['OD_m'].append(f'{OD_new_control:.2f}')

            if OS_new_control <= -9 :
                table['OS_m'].append(f'<-9')
            elif OS_new >= 5 :
                table['OS_m'].append(f'>5')
            else :
                table['OS_m'].append(f'{OS_new_control:.2f}') 

sign='●'
for record in records_py[1:]:
    if record[od] != "" and record[os] != "":
        table['Age　'].insert(0, f'{_y_m(record[11],0,sign)}')
        if report == '軸長':
            if record[od] !="":
                if record[od] == 19.5 :
                    table['OD'].insert(0, f'<20')
                elif record[od] == 30.5 :
                    table['OD'].insert(0, f'>30')
                else :
                    table['OD'].insert(0, f'{record[od]:.2f}')

            if record[os] !="":
                if record[os] == 19.5 :
                    table['OS'].insert(0, f'<20')
                elif record[os] == 30.5 :
                    table['OS'].insert(0, f'>30')
                else :
                    table['OS'].insert(0, f'{record[os]:.2f}')
        else:
            if record[od] !="":
                if record[od] == -9 :
                    table['OD'].insert(0, f'<-9')
                elif record[od] == 5 :
                    table['OD'].insert(0, f'>5')
                else :
                    table['OD'].insert(0, f'{record[od]:.2f}')
                table['OD_m'].insert(0,'-')
            if record[os] !="":
                if record[os] == -9 :
                    table['OS'].insert(0, f'<-9')
                elif record[os] == 5 :
                    table['OS'].insert(0, f'>5')
                else :
                    table['OS'].insert(0, f'{record[os]:.2f}')
                table['OS_m'].insert(0,'-')
import pandas as pd
df = pd.DataFrame(table)
if report == '軸長':
    new_column_names = {'OD': 'OD(mm)　', 'OS': 'OS(mm)　'}
elif language_type == 0 or language_type == 2:
    new_column_names = {'OD': '右眼(D)　<br>無控制', 'OS': '左眼(D)　<br>無控制','OD_m':'右眼(D)　<br>有控制','OS_m':'左眼(D)　<br>有控制'}
else :
    new_column_names = {'OD': 'OD(D)　<br>No Treatment', 'OS': 'OS(D)　<br>No Treatment','OD_m':'OD(D)　<br>Control','OS_m':'OS(D)　<br>Control'}
df.rename(columns=new_column_names, inplace=True)

df = df.T
#print(df.index)

if language_type == 0 :
    new_index_names  = {'Age　': '年齡　'}
    df.rename(index=new_index_names, inplace=True)
    df.columns = df.loc['年齡　']
    #df = df.drop(index='年齡　')
elif  language_type == 2:
    new_index_names  = {'Age　': '年龄　'}
    df.rename(index=new_index_names, inplace=True)
    df.columns = df.loc['年龄　']
    #df = df.drop(index='年龄　')
else:
    df.columns = df.loc['Age　']
    #df = df.drop(index='Age　')

left_top_element = df.iloc[0, 0]
#print(left_top_element)
#print(df.index)
duplicated_columns = df.columns[df.columns.duplicated()]
if not duplicated_columns.empty:
    renamed_columns  = df.columns
    for col_name  in duplicated_columns:
        count = 1
        while col_name  in renamed_columns:
            renamed_columns = renamed_columns.to_list()
            renamed_columns[renamed_columns.index(col_name)] = f"{col_name}_v{count}"
            renamed_columns = pd.Index(renamed_columns)
            count += 1
    df.columns = renamed_columns

#print(df.index)
"""
def hide_border(val):
    if val == '　':  # 當值為單空格時隱藏左方和下方框線
        return 'border-left: none; border-right: none; border-bottom: none;'
    elif val == '　　':  # 當值為雙空格時隱藏左方和下方框線
        return 'border-left: none; border-right: none; border-bottom: none; border-top: none;'
    else:
        return ''
"""
styled_df = df.style.hide(axis="columns")
styled_df = styled_df.set_properties(**{
'background-color': 'white', 
'color': 'black',
'text-align': 'center',
'border': 'solid',
'border-width': '2px',
'padding': '2px'
})
# styled_df = styled_df.applymap(hide_border)
display(styled_df, target='table')