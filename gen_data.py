# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 00:23:06 2022

@author: sayori

只需调用access函数，如果表单存在则自动返回数据，若不存在则根据传入数据自动生成数据，typ=0生成学生数据，typ=1生成教师数据，
code_add传入学号/职工号偏移量，否则在新建表时会发生编号重复

"""

import numpy as np
import json
import pickle
import pandas as pd
from PIL import Image
import os

STU_NUM_START=206001000
PRO_NUM_START=100000000
#################################################
#以下程序生成个人信息表

def prefix(x):
    if len(x)==1:
        return '0'+x
    else:
        return x
    
def get_check_code(s):
    cof=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    ret=['1','0','X','9','8','7','6','5','4','3','2']
    sum=0
    for i in range(len(s)):
        sum+=int(s[i])*cof[i]
    return ret[sum%11]      
        

def utf8():
    return chr(np.random.randint(0x4e00,0x9faf))
def name():
    name_=['王','李','张','刘','陈','杨','黄','赵','周','吴']
    if np.random.rand()<0.2:
        return np.random.choice(name_)+utf8()
    else:return np.random.choice(name_)+utf8()+utf8()
    
def ID(DOB):
    try:
        with open('raw_data/area.json','rb') as f:
            data=json.load(f)
            area_code=np.random.choice(list(data.keys()))
            date=(str(np.random.randint(DOB[0],DOB[1])),prefix(str(np.random.randint(1,13))),prefix(str(np.random.randint(1,29))))
            code=area_code+''.join(date)
            
            gender=round(np.random.rand()) #1 represents male
            sqe_code=str(2*np.random.randint(5)+gender)
            code=code+str(np.random.randint(10))+sqe_code
            code=code+get_check_code(code)
            return code,'-'.join(date),gender,data[area_code]
    except IOError:
        print("地理信息缺失！")

def major_load():#内部调用
    majors=[]
    m=pd.read_csv('raw_data/major.csv','r',header=0)
    for i in range(702):
        majors.append(m.iloc[i][0])
    with open('raw_data/major.json','w') as f:
        json.dump(majors,f)
    print("专业数据已加载！")
    return majors

def major():
    if not os.path.exists('raw_data/major.json'):
        print("专业数据缺失！")
        major_load()
    with open('raw_data/major.json','rb') as f:
        data=json.load(f)
    return np.random.choice(data)

def pic():
    try:
        im=Image.open('raw_data/img_align_celeba/img_align_celeba/{}.jpg'.format(str(np.random.randint(100000,200000))))
    except IOError:
        print("no picture access!")     
    return im

def gen_single(DOB):
    sex=['女','男']
    name_=name()
    code,date,gender,area=ID(DOB)
    gender=sex[gender]
    majo=list(major().split(','))
    return {'姓名':name_,'身份证':code,'性别':gender,'出生年月':date,'地区':area,'专业':majo}

def gen_form1(cnt=1000,add_pic=True,code_dif=0):
    data=[]
    for i in range(cnt):
        a=gen_single((2000,2003))
        if add_pic:
            a['学号']=STU_NUM_START+i+code_dif
            a['图片']=pic()
            a['码']='学号'
        data.append(a)
    return data
###############################################################
#以下程序输出老师信息
def gen_form2(cnt=100,add_pic=True,code_dif=0):
    data=[]
    univ=['清华大学','北京大学','浙江大学','复旦大学','上海交通大学','电子科技大学','中国科学技术大学','哈尔滨工业大学','MIT','CMU','UCLA']
    degree=['硕士','博士']
    pos=['讲师','副教授','教授','研究员']
    for i in range(cnt):
        a=gen_single((1950,1980))
        if add_pic:
            a['职工号']=PRO_NUM_START+i+code_dif
            a['图片']=pic()
            a['专业']=a['专业'][0]
            a['毕业院校']=np.random.choice(univ)
            a['学历']=np.random.choice(degree)
            a['职位']=np.random.choice(pos)
            a['码']='职工号'
        data.append(a)
    return data

def access(filename='db.pkl',data_num=100,pic=True,typ=0,code_add=0):
    fun_list=[gen_form1,gen_form2]#函数列表，简化写法
    if os.path.exists(filename):
        with open(filename,'rb') as f:
            a=pickle.load(f)
        return a
    else:
        print("创建新数据！")
        a=fun_list[typ](cnt=data_num,add_pic=pic,code_dif=code_add)
        with open(filename,'wb') as f:
            pickle.dump(a,f)
        print("数据已写入！")
        return a



        

    


    
    
