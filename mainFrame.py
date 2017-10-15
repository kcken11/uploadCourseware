#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import time
import aliyunConfig
reload(sys)
sys.setdefaultencoding('utf8')

uploadLog=file('log.log','w')

def uploadFile(event):
    console.AppendText('开始上传文件......\n')
    file= filePicker.GetPath()
    key=aliyunPath.GetValue()
    console.AppendText('文件路径:%s\n' % file )
    console.AppendText('默认存放路径:%s\n' % key )
    aliyunConfig.uploadFile(key,file,uploadCallBack)
    uploadLog.close()
    console.AppendText('上传成功......')

def onFileSelected(event):
    currentDate=time.strftime('%Y%m%d',time.localtime())
    filepath=str(filePicker.GetPath())
    savePath='aliyun/%s/%s' % (currentDate,filepath[filepath.rindex('\\')+1:len(filepath)])
    aliyunPath.SetValue(savePath)

def uploadCallBack(a,b):
   process.SetRange(b)
   process.SetValue(a)

app=wx.App()
win=wx.Frame(None,-1,'课件更新小工具',size=(725,500),style=wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

panel=wx.Panel(win,pos=(0,0))
#批量上传
wx.StaticText(panel,label='选择课件根目录：',pos=(5,25))
folderPicker=wx.DirPickerCtrl(panel, wx.ID_ANY,message=u"Select a folder",pos=(120,20), size=wx.Size( 450,-1 ) ,style=wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL)


#单个文件上传
wx.StaticText(panel,label='选择上传文件：',pos=(5,75))
filePicker=wx.FilePickerCtrl(panel, wx.ID_ANY,message=u"Select a folder",pos=(120,70), size=wx.Size( 450,-1 ) ,style=wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL)
wx.StaticText(panel,label='默认存放路径：',pos=(5,105))
aliyunPath=wx.TextCtrl(panel,size=(415,-1),pos=(120,100))
okBtn=wx.Button(panel,pos=(580,70),label='上传',size=(50,30))
wx.StaticText(panel,label='上传进度：',pos=(5,135))
process=wx.Gauge(panel,pos=(120,135),size=(415,25),style=wx.GA_HORIZONTAL)



tip=wx.StaticText(panel,label='控制台信息：',pos=(5,180))
tip.SetForegroundColour((255,0,0))
console=wx.TextCtrl(panel,size=(440,245),pos=(120,180),style=wx.TE_READONLY|wx.TE_MULTILINE)

okBtn.Bind(wx.EVT_BUTTON,uploadFile)
filePicker.Bind(wx.EVT_FILEPICKER_CHANGED,onFileSelected)
bar=win.CreateStatusBar()
menuBar=wx.MenuBar()
label=wx.StaticText(bar,label="Author:yanxx")
win.SetMenuBar(menuBar)
win.Show()
app.MainLoop()

