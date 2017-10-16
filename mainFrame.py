#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import time
import countFiles
import uploadService
reload(sys)
sys.setdefaultencoding('utf8')

uploadLog=file('log.log','w')

filecount=0;
currentIndex=0;
def uploadFile(event):
    console.AppendText('开始上传文件......\n')
    file= filePicker.GetPath()
    key=aliyunPath.GetValue()
    console.AppendText('文件路径:%s\n' % file )
    console.AppendText('')
    console.AppendText('默认存放路径:%s\n' % key )
    uploadService.uploadSingleFile(key,file,uploadCallBack)
    uploadLog.close()
    console.AppendText('上传成功......\n\n')

def uploadFiles(event):
    console.AppendText('开始上传文件......\n')
    folder= folderPicker.GetPath()
    console.AppendText('文件路径:%s\n' % folder )
    filecount=countFiles.fileCount(folder)
    console.AppendText('待上传文件数: %d \n\n' % filecount)

    console.AppendText('开始上传图片文件......\n')
    Imgcount=countFiles.fileCount(folder+"\image")
    console.AppendText('待上传文件数: %d \n' % Imgcount)
    uploadService.uploadImg(folder + "\image", process, Imgcount)
    console.AppendText('上传图片成功......\n\n')

    console.AppendText('开始上传PPT......\n')
    Imgcount = countFiles.fileCount(folder + "\pdf")
    console.AppendText('待上传文件数: %d \n' % Imgcount)
    uploadService.uploadPPT(folder + "\pdf", process, Imgcount)
    console.AppendText('上传PPT成功......\n\n')
    uploadLog.close()
    console.AppendText('上传结束......\n\n')



def onFileSelected(event):
    currentDate=time.strftime('%Y%m%d',time.localtime())
    filepath=str(filePicker.GetPath())
    savePath='aliyun/%s/%s' % (currentDate,filepath[filepath.rindex('\\')+1:len(filepath)])
    aliyunPath.SetValue(savePath)

def uploadCallBack(a,b):
   process.SetRange(b)
   process.SetValue(a)

def clearScreen(event):
    console.SetValue("")


app=wx.App()
win=wx.Frame(None,-1,'课件更新小工具',size=(725,500),style=wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

panel=wx.Panel(win,pos=(0,0))
#批量上传
wx.StaticText(panel,label='选择课件根目录：',pos=(5,25))
folderPicker=wx.DirPickerCtrl(panel, wx.ID_ANY,message=u"Select a folder",pos=(120,20), size=wx.Size( 450,-1 ) ,style=wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL)
flesOkBtn=wx.Button(panel,pos=(580,20),label='上传',size=(50,30))

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
clearBtn=wx.Button(panel,pos=(580,180),label='清除',size=(50,30))



okBtn.Bind(wx.EVT_BUTTON,uploadFile)
flesOkBtn.Bind(wx.EVT_BUTTON,uploadFiles)
filePicker.Bind(wx.EVT_FILEPICKER_CHANGED,onFileSelected)
clearBtn.Bind(wx.EVT_BUTTON,clearScreen)
bar=win.CreateStatusBar()
menuBar=wx.MenuBar()
label=wx.StaticText(bar,label="Author:燕为        E-mail:wei.yan@melot.cn")
win.SetMenuBar(menuBar)
win.Show()
app.MainLoop()

