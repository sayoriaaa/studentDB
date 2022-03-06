# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 16:10:51 2022

@author: sayori
"""

import numpy as np
import json
import pickle
import pandas as pd
from PIL import Image

import gen_data as ga

def dic_cmp(a,b):
    for i in a.items():
        try:
            if not b[i[0]]==i[1]:
                return False
        except KeyError:
            return False
    return True

def dic_merge(a,b):
    ret={}
    for i in a.items():
        ret[i[0]]=i[1]
    for i in b.items():
        ret[i[0]]=i[1]
    return ret

def CREATE_FORM(name,key,**args):
    ret=[]
    ent={'码':key}
    for i in args:
        ent[i]=None
    ret.append(ent)
    with open(name+'.pkl','wb') as f:
        pickle.dump(a,f)
    return ret
    
    

def simple_search(a,key=None,value=None):
    print(key,value)
    ret=[]
    if value==None:
        for i in a:
            try:
                ret.append({i['码']:i[i['码']],key:i[key]})
            except KeyError:
                print("无此属性！")         
    elif key==None:
        for i in a:
            for j in i.items():
                if j[1]==value:
                    ret.append(i)
                if type(j[1])==list:
                    for k in j[1]:
                        if k==value:
                            ret.append(i)
    else:
        try:
            for i in a:
                if i[key]==value:
                    ret.append(i)
                if type(i[key])==list:
                    for k in i[key]:
                        if k==value:
                            ret.append(i)
        except KeyError:
            print("无此属性！")
    if len(ret)==0:
        print("无此查询值！")
    return ret

def delete(a,del_list):
    for i in a:
        for k in del_list:      
            if dic_cmp(i,k):
                a.remove(i)
    return 

def add_entity(a,**kwargs):
    new_=a[0].copy()
    for i in new_.keys():
        new_[i]=None
    for i in kwargs:
        new_[i[0]]=i[1]
    a.append(a)
    
def DIFF(a,b):
    ret=[]
    for i in a:
        ret.append(i)
        for k in b:      
            if dic_cmp(i,k):
                ret.remove(i)
    return ret

def ADD(a,b):
    ret=[]
    for i in a:
        ret.append(i)
        for k in b:      
            if not dic_cmp(i,k):
                ret.append(k)
    return ret

def INTERSECT(a,b,*args):
    ret=[]
    for i in a:
        for j in b:
            for key in args:
                try:
                    if i[key]==j[key]:
                        ret.append(i)
                except KeyError:
                    continue
    return ret

def CARTESIAN(a,b):
    ret=[]
    for i in a:
        for j in b:
            ret.append(dic_merge(i,j))
    return ret

def PROJECTION(a,*args):
    ret=[]
    for i in a:
        ent={}
        for k in i.keys():
            if k in args:
                continue
            else:
                ent[k]=i[k]
        ret.append(ent)
    return ret

def SELECT(a,*args):
    tmp=a
    for i in args:
        tmp=simple_search(tmp,key=i[0],value=i[1])
    return tmp    
    
def update(a,filename):
    with open(filename,'wb') as f:
        pickle.dump(a,f)
        
        
        
    
    


if __name__=='__main__':  
    a=ga.access('db1.pkl',data_num=10,typ=0)
    b=ga.access('db2.pkl',code_add=50,typ=1)
    print(a)
    
    s=simple_search(a,value='医学')
    print(s)
    delete(a,s)
    print(len(a))
    
    '''         
    print(simple_search(a,key='学号',value=206001005))
    print(simple_search(a,value='计算机类')) 
    print(simple_search(a,key='专业',value='工学'))
    '''
            
    

    