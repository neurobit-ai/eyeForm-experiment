from js import sex, age, y1, y2, records, report , language_type, suggestion
if 'ale' in sex:
    sex = {'Male': '男', 'Female': '女'}[sex]
import re
import pickle
with open('data_to_plot.pkl', 'rb') as f:
    db_version, slope_groupby, stacked_area = pickle.load(f)[report]
with open('LFC_data_to_plot_20231227.pkl', 'rb') as f:
    data_al = pickle.load(f)
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
        return f'&nbsp{space01}{m_y}歲{space02}{m.group(2)}個月{sign}'
    elif language_type== 2:
        return f'&nbsp{space01}{m_y}岁{space02}{m.group(2)}个月{sign}'
    else:
        return f'&nbsp{space01}{m_y}y{space02}{m.group(2)}m{sign}'
    
#print(language_type)
table = {}
sign='⯁'
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

def logarithm_calculate_middle(age_index , age_origin): 
    difference = np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_index)*data_al[report][sex][suggestion]["b1"]) - np.exp(data_al[report][sex][suggestion]["bo"]+np.log(age_origin)*data_al[report][sex][suggestion]["b1"])
    return difference
now_age = x(age)
agecounter = int(16-x(age))+1
if agecounter <= 0:
    agecounter = 2
OD_new=y1
OS_new=y2
sign='★'
for age_index in range(1,agecounter):
    table['Age　'].append(f'{_y_m(age,age_index,sign)}')
    OD_new += logarithm_calculate_middle(now_age + age_index,now_age + age_index - 1 )#slope_groupby[sex][suggestion]
    OS_new += logarithm_calculate_middle(now_age + age_index,now_age + age_index - 1)#slope_groupby[sex][suggestion]
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

            if record[os] == -9 :
                table['OS'].insert(0, f'<-9')
            elif record[os] == 5 :
                table['OS'].insert(0, f'>5')
            else :
                table['OS'].insert(0, f'{record[os]:.2f}')
import pandas as pd
df = pd.DataFrame(table)
if report == '軸長':
    new_column_names = {'OD': 'OD(mm)　', 'OS': 'OS(mm)　'}
elif language_type == 0 or language_type == 2:
    new_column_names = {'OD': 'OD(度)　', 'OS': 'OS(度)　'}
else :
    new_column_names = {'OD': 'OD(degrees)　', 'OS': 'OS(degrees)　'}
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
styled_df = df.style.hide(axis="columns")
styled_df = styled_df.set_properties(**{
'background-color': 'white', 
'color': 'black',
'text-align': 'center',
'border': 'solid',
'border-width': '2px',
'padding': '2px'
})

display(styled_df, target='table')