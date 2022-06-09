# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:29:40 2022

@author: ivers
"""

import numpy as np
import pandas as pd
nf=pd.read_csv('netflix_titles.csv',encoding='utf8')
nf.info()#資料概要

#================================================= 
#處理缺失值
nf.isna().sum()
nf.iloc[:,3] = nf.iloc[:,3].fillna('0')
nf.iloc[:,4] = nf.iloc[:,4].fillna('0')
nf.iloc[:,5] = nf.iloc[:,5].fillna('0')
nf.iloc[:,6] = nf.iloc[:,6].fillna('00, 00, 0000')
nf.iloc[:,9] = nf.iloc[:,9].fillna('0 min')

#=================================================
#將影片名稱都換成大寫，便於進行查詢
for i in range(0,len(nf)):
    nf.iloc[i,2]=nf.iloc[i,2].upper()

#=================================================
nf_movie = nf.loc[(nf['type'] == 'Movie')]
nf_TV_Show=nf.loc[nf['type'] == 'TV Show']
#全部電影的種類
nf_movie_listed_in=[]
for j in range(0,len(nf_movie)):
    for i in range(0,len(nf_movie.iloc[j,10].split(', '))):
        nf_movie_listed_in.append(nf_movie.iloc[j,10].split(', ')[i])
len(pd.unique(nf_movie_listed_in))
#dict to dataframe
nf_movie_listed_in_1=dict.fromkeys (nf_movie_listed_in, 0)
nf_movie_listed_in_1
for x in nf_movie_listed_in:
    nf_movie_listed_in_1[x] += 1
df_nf_movie_listed_in_1=pd.DataFrame(list(nf_movie_listed_in_1.items()),columns=['movie_type', 'value'])
df_nf_movie_listed_in_1.sort_values(by=['value'],ascending=False).head(5)#標籤出現次數最多的前五名
df_nf_movie_listed_in_5=df_nf_movie_listed_in_1.sort_values(by=['value'],ascending=False).head(5)

for i in range(0,5):
    print('{0:.2f}'.format(df_nf_movie_listed_in_1.sort_values(by=['value'],ascending=False).head(5).iloc[i,1]/8581)  )

#=================================================
#全部影集的種類
nf_TV_Show_listed_in=[]
for j in range(0,len(nf_TV_Show)):
    for i in range(0,len(nf_TV_Show.iloc[j,10].split(', '))):
        nf_TV_Show_listed_in.append(nf_TV_Show.iloc[j,10].split(', ')[i])
len(pd.unique(nf_TV_Show_listed_in))
#dict to dataframe
nf_TV_Show_listed_in_1=dict.fromkeys (nf_TV_Show_listed_in, 0)
nf_TV_Show_listed_in_1
for x in nf_TV_Show_listed_in:
    nf_TV_Show_listed_in_1[x] += 1
df_nf_TV_Show_listed_in_1=pd.DataFrame(list(nf_TV_Show_listed_in_1.items()),columns=['TV_Show_type', 'value'])
df_nf_TV_Show_listed_in_1.sort_values(by=['value'],ascending=False).head(5)#標籤出現次數最多的前五名
df_nf_TV_Show_listed_in_5=df_nf_TV_Show_listed_in_1.sort_values(by=['value'],ascending=False).head(5)

#=================================================
#進行分析與推薦
user_list=nf.iloc[1:20,:]

movie_name=input('請輸入電影或影集名稱 (兩部或以上請用","隔開):').upper().split(',')
while movie_name[0]!='STOP':
    for i in range(0,len(nf)):
        if nf.iloc[i,2] in movie_name:
            user_list=user_list.append(nf.iloc[i,:])
            user_nf_movie = user_list.loc[(user_list['type'] == 'Movie')]
            user_nf_TV_Show_=user_list.loc[user_list['type'] == 'TV Show']
    #計算電影資料
    nf_movie_listed_in=[]
    for j in range(0,len(user_nf_movie)):
        for i in range(0,len(user_nf_movie.iloc[j,10].split(', '))):
            nf_movie_listed_in.append(user_nf_movie.iloc[j,10].split(', ')[i])   
    #dict to dataframe
    nf_movie_listed_in_1=dict.fromkeys (nf_movie_listed_in, 0)
    for x in nf_movie_listed_in:
        nf_movie_listed_in_1[x] += 1
    #標籤出現次數最多的前五名
    df_nf_movie_listed_in_first_5=pd.DataFrame(list(nf_movie_listed_in_1.items()),columns=['movie_type', 'value']).sort_values(by=['value'],ascending=False).head(5)
    #計算每層抽樣數量
    movie_value=0
    for i in range(5):
        movie_value+=df_nf_movie_listed_in_first_5.iloc[i,1]
    movie_first_1 = int(round(df_nf_movie_listed_in_first_5.iloc[0,1]/movie_value,1)*10)
    movie_first_2 = int(round(df_nf_movie_listed_in_first_5.iloc[1,1]/movie_value,1)*10)
    movie_first_3 = int(round(df_nf_movie_listed_in_first_5.iloc[2,1]/movie_value,1)*10)
    movie_first_4 = int(round(df_nf_movie_listed_in_first_5.iloc[3,1]/movie_value,1)*10)
    movie_first_5 = int(round(df_nf_movie_listed_in_first_5.iloc[4,1]/movie_value,1)*10)
    #抓出每層的全部內容
    nf_movie_condition_1=[]
    nf_movie_condition_2=[]
    nf_movie_condition_3=[]
    nf_movie_condition_4=[]
    nf_movie_condition_5=[]
    for i in range(0,len(user_nf_movie)):
        if '%s' %df_nf_movie_listed_in_first_5.iloc[0,0] in user_nf_movie.iloc[i,10]:
            nf_movie_condition_1.append(user_nf_movie.iloc[i,:])
        if '%s' %df_nf_movie_listed_in_first_5.iloc[1,0] in user_nf_movie.iloc[i,10]:
            nf_movie_condition_2.append(user_nf_movie.iloc[i,:])
        if '%s' %df_nf_movie_listed_in_first_5.iloc[2,0] in user_nf_movie.iloc[i,10]:
            nf_movie_condition_3.append(user_nf_movie.iloc[i,:])
        if '%s' %df_nf_movie_listed_in_first_5.iloc[3,0] in user_nf_movie.iloc[i,10]:
            nf_movie_condition_4.append(user_nf_movie.iloc[i,:])
        if '%s' %df_nf_movie_listed_in_first_5.iloc[4,0] in user_nf_movie.iloc[i,10]:
            nf_movie_condition_5.append(user_nf_movie.iloc[i,:])
    #轉換成DataFrame
    nf_movie_condition_1=pd.DataFrame(nf_movie_condition_1)
    nf_movie_condition_2=pd.DataFrame(nf_movie_condition_2)
    nf_movie_condition_3=pd.DataFrame(nf_movie_condition_3)
    nf_movie_condition_4=pd.DataFrame(nf_movie_condition_4)
    nf_movie_condition_5=pd.DataFrame(nf_movie_condition_5)
    #抓出各層的抽樣對象
    nf_movie_condition_1_sample=nf_movie_condition_1.sample(n=movie_first_1)
    nf_movie_condition_2_sample=nf_movie_condition_2.sample(n=movie_first_2)
    nf_movie_condition_3_sample=nf_movie_condition_3.sample(n=movie_first_3)
    nf_movie_condition_4_sample=nf_movie_condition_4.sample(n=movie_first_4)
    nf_movie_condition_5_sample=nf_movie_condition_5.sample(n=movie_first_5)
    #合併成一個DataFrame
    movie=pd.concat([nf_movie_condition_1_sample,nf_movie_condition_2_sample,nf_movie_condition_3_sample,
                  nf_movie_condition_4_sample,nf_movie_condition_5_sample])
    #列出推薦電影
    print('\n電影推薦名單:\n',movie.iloc[:,2])
    print('電影各層標籤比例:')
    print('1.%s' %df_nf_movie_listed_in_first_5.iloc[0,0],'  {:.0%}'.format(round(df_nf_movie_listed_in_first_5.iloc[0,1]/movie_value,2)))
    print('2.%s' %df_nf_movie_listed_in_first_5.iloc[1,0],'  {:.0%}'.format(round(df_nf_movie_listed_in_first_5.iloc[1,1]/movie_value,2)))
    print('3.%s' %df_nf_movie_listed_in_first_5.iloc[2,0],'  {:.0%}'.format(round(df_nf_movie_listed_in_first_5.iloc[2,1]/movie_value,2)))
    print('4.%s' %df_nf_movie_listed_in_first_5.iloc[3,0],'  {:.0%}'.format(round(df_nf_movie_listed_in_first_5.iloc[3,1]/movie_value,2)))
    print('5.%s' %df_nf_movie_listed_in_first_5.iloc[4,0],'  {:.0%}'.format(1-(round(df_nf_movie_listed_in_first_5.iloc[0,1]/movie_value,2)+
     round(df_nf_movie_listed_in_first_5.iloc[1,1]/movie_value,2)+
     round(df_nf_movie_listed_in_first_5.iloc[2,1]/movie_value,2)+
     round(df_nf_movie_listed_in_first_5.iloc[3,1]/movie_value,2))))
    #=================================================
    #計算影集資料
    nf_TV_Show_listed_in=[]
    for j in range(0,len(user_nf_TV_Show_)):
        for i in range(0,len(user_nf_TV_Show_.iloc[j,10].split(', '))):
            nf_TV_Show_listed_in.append(user_nf_TV_Show_.iloc[j,10].split(', ')[i])
    #dict to dataframe
    nf_TV_Show_listed_in_1=dict.fromkeys (nf_TV_Show_listed_in, 0)
    for x in nf_TV_Show_listed_in:
        nf_TV_Show_listed_in_1[x] += 1
    #標籤出現次數最多的前五名
    df_nf_TV_Show_listed_in_first_5=pd.DataFrame(list(nf_TV_Show_listed_in_1.items()),columns=['TV_Show_type', 'value']).sort_values(by=['value'],ascending=False).head(5)
    #計算每層抽樣數量
    TV_Show_value=0
    for i in range(5):
        TV_Show_value+=df_nf_TV_Show_listed_in_first_5.iloc[i,1]
    TV_Show_first_1 = int(round(df_nf_TV_Show_listed_in_first_5.iloc[0,1]/TV_Show_value,1)*10)
    TV_Show_first_2 = int(round(df_nf_TV_Show_listed_in_first_5.iloc[1,1]/TV_Show_value,1)*10)
    TV_Show_first_3 = int(round(df_nf_TV_Show_listed_in_first_5.iloc[2,1]/TV_Show_value,1)*10)
    TV_Show_first_4 = int(round(df_nf_TV_Show_listed_in_first_5.iloc[3,1]/TV_Show_value,1)*10)
    TV_Show_first_5 = int(round(df_nf_TV_Show_listed_in_first_5.iloc[4,1]/TV_Show_value,1)*10)
    #抓出每層的全部內容
    nf_TV_Show_condition_1=[]
    nf_TV_Show_condition_2=[]
    nf_TV_Show_condition_3=[]
    nf_TV_Show_condition_4=[]
    nf_TV_Show_condition_5=[]
    for i in range(0,len(user_nf_TV_Show_)):
        if '%s' %df_nf_TV_Show_listed_in_first_5.iloc[0,0] in user_nf_TV_Show_.iloc[i,10]:
            nf_TV_Show_condition_1.append(user_nf_TV_Show_.iloc[i,:])
        if '%s' %df_nf_TV_Show_listed_in_first_5.iloc[1,0] in user_nf_TV_Show_.iloc[i,10]:
            nf_TV_Show_condition_2.append(user_nf_TV_Show_.iloc[i,:])
        if '%s' %df_nf_TV_Show_listed_in_first_5.iloc[2,0] in user_nf_TV_Show_.iloc[i,10]:
            nf_TV_Show_condition_3.append(user_nf_TV_Show_.iloc[i,:])
        if '%s' %df_nf_TV_Show_listed_in_first_5.iloc[3,0] in user_nf_TV_Show_.iloc[i,10]:
            nf_TV_Show_condition_4.append(user_nf_TV_Show_.iloc[i,:])
        if '%s' %df_nf_TV_Show_listed_in_first_5.iloc[4,0] in user_nf_TV_Show_.iloc[i,10]:
            nf_TV_Show_condition_5.append(user_nf_TV_Show_.iloc[i,:])
    #轉換成DataFrame   
    nf_TV_Show_condition_1=pd.DataFrame(nf_TV_Show_condition_1)
    nf_TV_Show_condition_2=pd.DataFrame(nf_TV_Show_condition_2)
    nf_TV_Show_condition_3=pd.DataFrame(nf_TV_Show_condition_3)
    nf_TV_Show_condition_4=pd.DataFrame(nf_TV_Show_condition_4)
    nf_TV_Show_condition_5=pd.DataFrame(nf_TV_Show_condition_5)
    #抓出各層的抽樣對象
    nf_TV_Show_condition_1_sample=nf_TV_Show_condition_1.sample(n=TV_Show_first_1)
    nf_TV_Show_condition_2_sample=nf_TV_Show_condition_2.sample(n=TV_Show_first_2)
    nf_TV_Show_condition_3_sample=nf_TV_Show_condition_3.sample(n=TV_Show_first_3)
    nf_TV_Show_condition_4_sample=nf_TV_Show_condition_4.sample(n=TV_Show_first_4)
    nf_TV_Show_condition_5_sample=nf_TV_Show_condition_5.sample(n=TV_Show_first_5)
    #合併成一個DataFrame
    TV_Show=pd.concat([nf_TV_Show_condition_1_sample,nf_TV_Show_condition_2_sample,nf_TV_Show_condition_3_sample,
                  nf_TV_Show_condition_4_sample,nf_TV_Show_condition_5_sample])
    #列出推薦影集
    print('影集推薦名單:\n',TV_Show.iloc[:,2])
    print('\n影集各層標籤比例:')
    print('1.%s' %df_nf_TV_Show_listed_in_first_5.iloc[0,0],'  {:.0%}'.format(round(df_nf_TV_Show_listed_in_first_5.iloc[0,1]/TV_Show_value,2)))
    print('2.%s' %df_nf_TV_Show_listed_in_first_5.iloc[1,0],'  {:.0%}'.format(round(df_nf_TV_Show_listed_in_first_5.iloc[1,1]/TV_Show_value,2)))
    print('3.%s' %df_nf_TV_Show_listed_in_first_5.iloc[2,0],'  {:.0%}'.format(round(df_nf_TV_Show_listed_in_first_5.iloc[2,1]/TV_Show_value,2)))
    print('4.%s' %df_nf_TV_Show_listed_in_first_5.iloc[3,0],'  {:.0%}'.format(round(df_nf_TV_Show_listed_in_first_5.iloc[3,1]/TV_Show_value,2)))
    print('5.%s' %df_nf_TV_Show_listed_in_first_5.iloc[4,0],'  {:.0%}'.format(1-(round(df_nf_TV_Show_listed_in_first_5.iloc[0,1]/TV_Show_value,2)+
     round(df_nf_TV_Show_listed_in_first_5.iloc[1,1]/TV_Show_value,2)+
     round(df_nf_TV_Show_listed_in_first_5.iloc[2,1]/TV_Show_value,2)+
     round(df_nf_TV_Show_listed_in_first_5.iloc[3,1]/TV_Show_value,2))))
    print('\n若想離開請輸入stop')
    movie_name=input('請輸入電影或影集名稱 (兩部或以上請用","隔開):').upper().split(',')
    
