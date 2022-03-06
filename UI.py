# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 09:43:41 2022

@author: sayori

config格式：宽，高，窗体背景颜色(16进制或英文)，
"""
import json
import tkinter
from numpy import random as nrand
import cv2
from PIL import Image,ImageTk
import gen_data
import db
import os
import pickle


def load_icon():
    name=['geo','anemo','cryo','dendro','electro','hydro','pyro']
    icon=[]
    for i in name:
        icon.append(tkinter.PhotoImage(file='config/{}.png'.format(i)))
    return icon

        
class Interface():
    def __init__(self):
        self.config=[1200,900,'#33FFFF']
        self.db=None
        self.entity_num=0
        try:
            with open('config/config.json','rb') as f:
                self.config=json.load(f)
        except IOError:
            pass
        
            
        win=tkinter.Tk()
        win.minsize(self.config[0],self.config[1])
        win.maxsize(self.config[0],self.config[1])
        self.icon=load_icon()
        win.title('学生管理系统')
        win.geometry("{}x{}".format(str(self.config[0]),str(self.config[1])))       
        win.iconphoto(False,nrand.choice(self.icon))
        
        m=tkinter.Menu(win)
        m.add_command(label='加载',command=self.load_data)
        m.add_command(label='查找',command=self.cmd)
        m.add_command(label='帮助',command=self.myhelp)
        m.add_command(label='设置',command=self.setup)
        m.add_command(label='创建',command=self.gen_database)
        m.add_command(label='保存',command=self.db_save)
        m.add_command(label='插入',command=self.trivial_feature_0)
        m.add_command(label='删除',command=self.trivial_feature_1)
        m.add_command(label='排序',command=self.trivial_feature_2)
        
        win['menu']=m
        
        cv=tkinter.Canvas(win,width=self.config[0],height=self.config[1],bg=self.config[2]) 
        im=ImageTk.PhotoImage(self.set_bk_img())
        cv.create_image(self.config[0]/2,self.config[1]/2,image=im)
        
        cv.bind("<Button-1>",self.view_data_m)
        cv.bind("<Button-3>",self.view_data_p)
        cv.pack()
        self.cv=cv

        win.mainloop()
    
    def setup(self):
        win=tkinter.Toplevel()
        win.title('窗体设置')
        win.geometry("600x400") 
        win.iconphoto(False,nrand.choice(self.icon))
        
    def view_data_p(self,event):
        print("p")
        if not self.db==None and self.entity_num<len(self.db)-1:
            self.entity_num+=1
            self.refresh()
    def view_data_m(self,event):
        print("m")
        if not self.db==None and self.entity_num>0:
            self.entity_num-=1
            self.refresh()
            
            
        
        
    def refresh(self):
        self.cv.delete("inf")
        tmp=0#去掉enumerate造成的空格
        if not self.db==None:
            self.cv.create_text(self.config[0]/2,self.config[1]/10,text='当前数据库：{}  条目：{}/{}'.format(self.db_name,self.entity_num+1,len(self.db)),tag="inf")
            im=ImageTk.PhotoImage(self.db[self.entity_num]['图片'])
            self.cv.create_image(self.config[0]/2,self.config[1]/4,image=im)
            for cnt,i in enumerate(self.db[self.entity_num].items()):
                if i[0]=='码' or i[0]=='图片':
                    tmp+=1
                    continue
                self.cv.create_text(self.config[0]/2,self.config[1]/2+50*(cnt-tmp),text='{}:{}'.format(i[0],i[1]),tag="inf")
                
        self.cv.update()
        self.cv.mainloop()
        
        
        
    def load_data(self):
        '''
        在不同数据库切换时要重置数据
        '''
        def click():
            self.db_name=en1.get()
            if not os.path.exists(self.db_name+".pkl"):
                warn_inf='输入数据库名不存在，请检查或创建新数据库'
                tkinter.messagebox.showwarning('查询错误',warn_inf)
                return
            self.db=gen_data.access(filename=self.db_name+'.pkl')
            self.entity_num=0
            win.destroy()
            self.refresh()
            
        win=tkinter.Toplevel()
        win.title('加载选定数据库')
        win.geometry("400x150") 
        win.iconphoto(False,nrand.choice(self.icon)) 
        
        label1=tkinter.Label(win,text='请输入数据库名')
        label1.pack()
        en1=tkinter.Entry(win,width=30)
        en1.pack()
        bu1=tkinter.Button(win,text='确认',command=click)
        bu1.pack()
        
    def gen_database(self):
        def click():
            self.db_name=en1.get()
            if self.db_name=='':
                warn_inf='请输入数据库名'
                tkinter.messagebox.showwarning('创建错误',warn_inf)
                return
            if  os.path.exists(self.db_name+".pkl"):
                warn_inf='数据库名不存在，请检查'
                tkinter.messagebox.showwarning('创建错误',warn_inf)
                return
            if not en2.get().isdigit() or int(en2.get())<1:
                warn_inf='数据库长度错误'
                tkinter.messagebox.showwarning('创建错误',warn_inf)
                return   
            self.db=gen_data.access(filename=self.db_name+'.pkl',data_num=int(en2.get()),typ=r.get())
            win.destroy()
            self.refresh()
            
        win=tkinter.Toplevel()
        win.title('创建数据库')
        win.geometry("400x300") 
        win.iconphoto(False,nrand.choice(self.icon)) 
        
        label1=tkinter.Label(win,text='请输入数据库名')
        label1.pack()
        en1=tkinter.Entry(win,width=30)
        en1.pack()
        label2=tkinter.Label(win,text='请输入数据大小')
        label2.pack()
        en2=tkinter.Entry(win,width=30)
        en2.pack()
        
        r=tkinter.IntVar()
        label3=tkinter.Label(win,text='请选择数据类型')
        label3.pack()   
        radio=tkinter.Radiobutton(win,variable=r,value=0,text='学生')
        radio.pack()
        radio=tkinter.Radiobutton(win,variable=r,value=1,text='老师')
        radio.pack()       
        
        bu1=tkinter.Button(win,text='确认',command=click)
        bu1.pack()
        win.mainloop()   
        
        
        
    def myhelp(self):
        hel='sayori版权所有\n待完善'
        tkinter.messagebox.showinfo('帮助',hel)
        
    
    def cmd(self):
        def click():
            k=None
            v=None
            if not en1.get()=='':
                k=en1.get()
            if not en2.get()=='':
                v=en2.get()
            if v==None:
                tkinter.messagebox.showerror('警告','值不为空')
                return
            self.db=db.simple_search(self.db,key=k,value=v)
            win.destroy()
            self.refresh()
            
        win=tkinter.Toplevel()
        win.title('查找')
        win.geometry("400x150") 
        win.iconphoto(False,nrand.choice(self.icon)) 
        
        label1=tkinter.Label(win,text='请输入属性')
        label1.pack()
        en1=tkinter.Entry(win,width=30)
        en1.pack()
        label2=tkinter.Label(win,text='请输入值')
        label2.pack()
        en2=tkinter.Entry(win,width=30)
        en2.pack()
        bu1=tkinter.Button(win,text='确认',command=click)
        bu1.pack()
        
    def exe_parse(self):
        print(self.sql)
        
        
    
    def set_bk_img(self,name='bk1'):
        pic=cv2.imread("config/{}.jpg".format(name))   
        b,g,r=cv2.split(pic)
        pic=cv2.merge([r,g,b]) 
        ret=cv2.resize(pic,(self.config[0],self.config[1]))
        ret=Image.fromarray(ret)
        return ret
    
    def trivial_feature_2(self):
        def click():
            if not en1.get() in self.db[0].keys():
                tkinter.messagebox.showinfo('错误','不存在此属性') 
                return
            self.db=sorted(self.db,key=lambda x:x[en1.get()],reverse=bool(r.get()))
            tkinter.messagebox.showinfo('操作成功','排序成功')
            win.destroy()
            self.refresh()
            
        if self.db==None:
            tkinter.messagebox.showwarning('插入错误','请先加载数据库')
            return
        win=tkinter.Toplevel()
        win.title('排序')
        win.geometry("400x200") 
        win.iconphoto(False,nrand.choice(self.icon)) 
        
        label1=tkinter.Label(win,text='请输入排序属性')
        label1.pack()
        en1=tkinter.Entry(win,width=30)
        en1.pack()
        
        r=tkinter.IntVar()
        label3=tkinter.Label(win,text='请选择数据类型')
        label3.pack()   
        radio=tkinter.Radiobutton(win,variable=r,value=0,text='从小到大')
        radio.pack()
        radio=tkinter.Radiobutton(win,variable=r,value=1,text='从大到小')
        radio.pack()  
            
        bu1=tkinter.Button(win,text='确认',command=click)
        bu1.pack()
        
    def trivial_feature_1(self):
        self.db.pop(self.entity_num)
        tkinter.messagebox.showinfo('操作成功','删除成功')
        self.refresh()
        
    def trivial_feature_0(self):
        def click():
            ret={}
            for cnt,i in enumerate(self.db[0].keys()):
                if i=='图片':
                    try:
                        ret[i]=Image.open(entry_list[cnt].get())
                    except FileNotFoundError:
                        tkinter.messagebox.showerror('错误','图片文件未找到，请确保文件和后缀名输入准确')
                        return
                else:
                    ret[i]=entry_list[cnt].get()
            self.db.append(ret)
            tkinter.messagebox.showinfo('操作成功','添加成功')
            win.destroy()
            self.refresh()
            
        if self.db==None:
            tkinter.messagebox.showwarning('操作错误','请先加载数据库')
            return
        win=tkinter.Toplevel()
        win.title('创建排序')
        win.geometry("400x600") 
        win.iconphoto(False,nrand.choice(self.icon)) 
        
        label_list=[None for i in range(len(self.db[0]))]
        entry_list=[None for i in range(len(self.db[0]))]
        for cnt,i in enumerate(self.db[0].keys()):
            if i=='图片':
                label_list[cnt]=tkinter.Label(win,text='请输入图片地址')
            else:    
                label_list[cnt]=tkinter.Label(win,text=i)
            label_list[cnt].pack()
            entry_list[cnt]=tkinter.Entry(win,width=30)
            entry_list[cnt].pack()
            
        bu1=tkinter.Button(win,text='确认',command=click)
        bu1.pack()
        
    def db_save(self):
        with open('{}.pkl'.format(self.db_name),'wb') as f:
            pickle.dump(self.db,f)
        tkinter.messagebox.showinfo('操作成功','已同步至磁盘')
            
            
            
        
            
    
    

        
        
        
            
a=Interface()
        
        