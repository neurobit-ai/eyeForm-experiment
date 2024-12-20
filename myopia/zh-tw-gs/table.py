from js import sex, age, y1, y2, records, report , language_type, suggestion
if 'ale' in sex:
    sex = {'Male': '男', 'Female': '女'}[sex]
import re
import pickle
with open('../data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area , data_al= pickle.load(f)[report]
#with open('LFC_data_to_plot_20231227.pkl', 'rb') as f:
    #data_al = pickle.load(f)
def x(age):
    m = re.match('(\d+)歲(\d+)', age)
    return int(m.group(1)) + int(m.group(2)) / 12

def _y_m(age,year,sign):
    m = re.match('(\d+)歲(\d+)', age)
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
    
#print(language_type)
table = {}
sign='R/L'
table['Age　'] = [f'{_y_m(age,0,sign)}']
if y1 == 19.5 :
    table['OD'] = [f'<20']
elif y1== 30.5 :
    table['OD'] = [f'>30']
else :
    table['OD'] = [f'{y1:.2f}']

if y2 == 19.5 :
    table['OS'] = [f'<20']
elif y2 == 30.5 :
    table['OS'] = [f'>30']
else :
    table['OS'] = [f'{y2:.2f}']

table['OD_m'] = ['-']
table['OS_m'] = ['-']

def logarithm_calculate_middle(age_index , age_origin): 
    difference = np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_index)*data_al[report][sex][suggestion]["b1"]) - np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_origin)*data_al[report][sex][suggestion]["b1"])
    return difference
now_age = x(age)
agecounter = int(16-x(age))+1
if agecounter <= 0:
    agecounter = 2
OD_new=y1
OS_new=y2
sign=' '

OD_no_management_data=[0]*agecounter#this is for initial
OS_no_management_data=[0]*agecounter#this is for initial
OD_no_management_data[0] = y1
OS_no_management_data[0] = y2

OD_control_data=[0]*agecounter#this is for initial
OS_control_data=[0]*agecounter#this is for initial
OD_control_data[0] = y1
OS_control_data[0] = y2
if  round(x(age)) in range(3,17):
    if report == '球面度數':
        OD_no_management_data = curve_calculation(OD_no_management_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age)),0)
        OS_no_management_data = curve_calculation(OS_no_management_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age)),0)
    else:
        OD_no_management_data = curve_calculation_AL(OD_no_management_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age)),0)
        OS_no_management_data = curve_calculation_AL(OS_no_management_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age)),0)     
    OD_control_data = curve_calculation(OD_control_data,current_slope_rate_OD,current_slope_attu_OD,int(x(age)),control_rate)
    OS_control_data = curve_calculation(OS_control_data,current_slope_rate_OS,current_slope_attu_OS,int(x(age)),control_rate)
    
    for age_index in range(1,agecounter):
        table['Age　'].append(f'{_y_m(age,age_index,sign)}')
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
#print("*********************")
#print(type(records))

#print(type(records))

import json
records = json.loads(records)
sign='●'
od, os = (18, 24) if report == '軸長' else (15, 21)
for record in records:
    if record[od] or record[os]:
        table['Age　'].insert(0, f'{_y_m(record[11],0,sign)}')
        if report == '軸長':
            if record[od] == 19.5 :
                table['OD'].insert(0, f'<20')
            elif record[od] == 30.5 :
                table['OD'].insert(0, f'>30')
            else :
                table['OD'].insert(0, f'{record[od]:.2f}')

            if record[os] == 19.5 :
                table['OS'].insert(0, f'<20')
            elif record[os] == 30.5 :
                table['OS'].insert(0, f'>30')
            else :
                table['OS'].insert(0, f'{record[os]:.2f}')
        else:
            if record[od] == -9 :
                table['OD'].insert(0, f'<-9')
            elif record[od] == 5 :
                table['OD'].insert(0, f'>5')
            else :
                table['OD'].insert(0, f'{record[od]:.2f}')
            table['OD_m'].insert(0,'-')
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