# -*- coding: cp949 -*-
from readdata import *
from sendmail import *
from tkinter import *
from tkinter import font
import folium
import tkinter.messagebox

MyInfo = LoadAPIFromIP()
Data = LoadXMLFromFile()
Type = None    #��ü������� �ּҰ˻����� �̸��˻����� Ȯ��
Tmp_Str = None #�ӽ÷� �����ϴ� �ܾ�

window = Tk()
window.geometry("465x650+750+200")
frame = Frame(window, height = 500, width = 400)

def CreateTitleLabel():
    title = "[�����Ƿ��� �˻� ���α׷�]"
    titlefont = font.Font(window, size=23, weight='bold', family='Consolas')
    ltitle = Label(window, font=titlefont, text=title, fg='#8f1439')
    ltitle.pack()
    ltitle.place(x=5, y=10)

def CreateSearchListBox():
    global SearchListBox
    TempFont = font.Font(window, size=15,weight='bold', family = 'Consolas')
    SearchListBox = Listbox(window, font = TempFont, activestyle = 'none',
                            width = 10, height = 2, borderwidth = 8, relief = 'ridge',bg='#ffdada',fg='#c97e89')
    SearchListBox.insert(1, "�����")
    SearchListBox.insert(2, "�ּ�")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=70)

def CreateRenderText():
    global RenderText
    RenderTextScrollbarY = Scrollbar(frame)
    RenderTextScrollbarX = Scrollbar(frame, orient = HORIZONTAL)
    RenderTextScrollbarY.pack(side=RIGHT, fill=Y)
    RenderTextScrollbarX.pack(side=BOTTOM, fill=X)

    TempFont = font.Font(frame, size = 10, family = 'Consolas')
    RenderText = Listbox(frame, width = 48, height = 23, borderwidth = 8, relief = 'ridge',
                      xscrollcommand = RenderTextScrollbarX.set, yscrollcommand = RenderTextScrollbarY.set, bg='#ffdada')
    RenderText.pack()
    #RenderText.place(x=10,y=195)
    RenderTextScrollbarY.config(command=RenderText.yview)
    RenderTextScrollbarX.config(command=RenderText.xview)
    #RenderText.configure(state='disabled')

def CreateInputLabel():
    global InputLabel
    TempFont = font.Font(window, size = 15, weight = 'bold', family = 'Consolas')
    InputLabel = Entry(window, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge', bg='#ffdada')
    InputLabel.pack()
    InputLabel.place(x=10,y=140)

def CreateEmailInputLabel():
    global InputEmail
    TempFont = font.Font(window, size=15, family='Consolas')
    InputEmail = Entry(window, font=TempFont, width=25, borderwidth=6, relief='ridge',bg='#ffdada')
    TempFont = font.Font(window, size=12, weight = 'bold', family='Consolas')
    label = Label(window, text = 'E-Mail',font = TempFont)
    label.pack()
    label.place(x=10, y=610)
    InputEmail.pack()
    InputEmail.place(x=70, y=605)

def CreateSearchButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, borderwidth = 10, text = "�˻�", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=320, y=140)

def CreateInfoButton():
    TempFont = font.Font(window, size=11, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7, height = 2, borderwidth = 5, text = "�ڼ���", command=InfoButtonAction)
    SearchButton.pack()
    SearchButton.place(x=384, y=205)

def CreateMapButton():
    TempFont = font.Font(window, size=11, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7,height = 2, borderwidth = 5, text = "�������", command=MapButtonAction)
    SearchButton.pack()
    SearchButton.place(x=384, y=275)

def CreateMailButton():
    TempFont = font.Font(window, size=8, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7,height = 2, borderwidth = 5, text = "��������", command=SendMailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=368, y=600)

def CreatePrintListButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font=TempFont, borderwidth=10, text="��ü ���", command=SearchLibList )
    SearchButton.pack()
    SearchButton.place(x=150, y=80)

def SendMailButtonAction():
    global Data, RenderTextm, Type, Tmp_Str, InputEmail
    iSearchIndex = str(RenderText.curselection()) #����� ����Ʈ���� Ȯ��
    EmailID = str(InputEmail.get())
    try:
        iSearchIndex = int(iSearchIndex[1:-2]) # (����)���� ���ڸ� �̾Ƴ�
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                SendEmail(location, EmailID)
            i += 1
        elif Type == 1:
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    SendEmail(location, EmailID)
                i += 1
        elif Type == 2:
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    SendEmail(location, EmailID)
                i += 1

def MapButtonAction():
    global Data, RenderText, Type, Tmp_Str
    iSearchIndex = str(RenderText.curselection())
    try:
        iSearchIndex = int(iSearchIndex[1:-2])
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                     zoom_start=17)
                folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                              popup = location.dutyname.string,
                              icon = folium.Icon(color = 'red', icon = 'info-sign')).add_to(map_osm)
                folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                              popup='���� �� ��ġ',
                              icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                text = location.dutyname.string + ".html"
                map_osm.save(text)
            i += 1
        elif Type == 1: #�̸�
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                         zoom_start=17)
                    folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                  popup=location.dutyname.string,
                                  icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)
                    folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                                  popup='���� �� ��ġ',
                                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                    text = location.dutyname.string + ".html"
                    map_osm.save(text)
                i += 1
        elif Type == 2: #�ּ�
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                         zoom_start=17)
                    folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                  popup=location.dutyname.string,
                                  icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)
                    folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                                  popup='���� �� ��ġ',
                                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                    text = location.dutyname.string + ".html"
                    map_osm.save(text)
                i += 1

def InfoButtonAction():
    global Data, RenderText, Type, Tmp_Str
    iSearchIndex = str(RenderText.curselection())
    try:
        iSearchIndex = int(iSearchIndex[1:-2])
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                text = ""
                text = AppendDataStr(location)
                tkinter.messagebox.showinfo(location.dutyname.string, text)
            i += 1
        elif Type == 1:
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    text = ""
                    text = AppendDataStr(location)
                    tkinter.messagebox.showinfo(location.dutyname.string, text)
                i += 1
        elif Type == 2:
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    text = ""
                    text = AppendDataStr(location)
                    tkinter.messagebox.showinfo(location.dutyname.string, text)
                i += 1

def AppendDataStr(location):
    text = ""
    for i in range(0, len(location.dutyaddr.string)):
        text += location.dutyaddr.string[i]
    text += chr(10)
    for i in range(0, len(location.dutyemclsname.string)):
        text += location.dutyemclsname.string[i]
    text += chr(10)
    text += "�з��� : "
    for i in range(0, len(location.dutyemcls.string)):
        text += location.dutyemcls.string[i]
    text += chr(10)
    text += "��ǥ��ȭ : "
    for i in range(0, len(location.dutytel1.string)):
        text += location.dutytel1.string[i]
    try:
        text += chr(10)
        text += "������ȭ : "
        for i in range(0, len(location.dutytel3.string)):
            text += location.dutytel3.string[i]
    except:
        pass
    return text

def SearchButtonAction():
    global SearchListBox, InputLabel
    iSearchIndex = str(SearchListBox.curselection())
    if iSearchIndex == "()":
        pass
    elif iSearchIndex == "(0,)": #�̸��˻�
        keyword = str(InputLabel.get())
        SearchLibName(keyword)
    elif iSearchIndex == "(1,)": #�ּҰ˻�
        keyword = str(InputLabel.get())
        SearchLibAddress(keyword)

def SearchLibList():
    global Data, RenderText, Type
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        RenderText.insert(i, location.dutyname.string + " | " + location.dutyaddr.string)
        i += 1
    Type = 0

def SearchLibName(keyword):
    global Data, RenderText, Type, Tmp_Str
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        if keyword in location.dutyname.string:
            RenderText.insert(i, location.dutyname.string + " | " + location.dutyaddr.string)
            i += 1
    Type = 1
    Tmp_Str = keyword

def SearchLibAddress(keyword):
    global Data, RenderText, Type, Tmp_Str
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        if keyword in location.dutyaddr.string:
            RenderText.insert(i, location.dutyaddr.string + " | " + location.dutyname.string)
            i += 1
    Type = 2
    Tmp_Str = keyword

frame.pack()
frame.place(x = 10, y = 195)
CreateTitleLabel()
CreateEmailInputLabel()
CreateSearchListBox()
CreateInputLabel()
CreateSearchButton()
CreatePrintListButton()
CreateRenderText()
CreateInfoButton()
CreateMapButton()
CreateMailButton()

window.mainloop()# -*- coding: cp949 -*-
from readdata import *
from sendmail import *
from tkinter import *
from tkinter import font
import folium
import tkinter.messagebox

MyInfo = LoadAPIFromIP()
Data = LoadXMLFromFile()
Type = None    #��ü������� �ּҰ˻����� �̸��˻����� Ȯ��
Tmp_Str = None #�ӽ÷� �����ϴ� �ܾ�

window = Tk()
window.geometry("465x650+750+200")
frame = Frame(window, height = 500, width = 400)

def CreateTitleLabel():
    title = "[�����Ƿ��� �˻� ���α׷�]"
    titlefont = font.Font(window, size=23, weight='bold', family='Consolas')
    ltitle = Label(window, font=titlefont, text=title, fg='#8f1439')
    ltitle.pack()
    ltitle.place(x=5, y=10)

def CreateSearchListBox():
    global SearchListBox
    TempFont = font.Font(window, size=15,weight='bold', family = 'Consolas')
    SearchListBox = Listbox(window, font = TempFont, activestyle = 'none',
                            width = 10, height = 2, borderwidth = 8, relief = 'ridge',bg='#ffdada',fg='#c97e89')
    SearchListBox.insert(1, "�����")
    SearchListBox.insert(2, "�ּ�")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=70)

def CreateRenderText():
    global RenderText
    RenderTextScrollbarY = Scrollbar(frame)
    RenderTextScrollbarX = Scrollbar(frame, orient = HORIZONTAL)
    RenderTextScrollbarY.pack(side=RIGHT, fill=Y)
    RenderTextScrollbarX.pack(side=BOTTOM, fill=X)

    TempFont = font.Font(frame, size = 10, family = 'Consolas')
    RenderText = Listbox(frame, width = 48, height = 23, borderwidth = 8, relief = 'ridge',
                      xscrollcommand = RenderTextScrollbarX.set, yscrollcommand = RenderTextScrollbarY.set, bg='#ffdada')
    RenderText.pack()
    #RenderText.place(x=10,y=195)
    RenderTextScrollbarY.config(command=RenderText.yview)
    RenderTextScrollbarX.config(command=RenderText.xview)
    #RenderText.configure(state='disabled')

def CreateInputLabel():
    global InputLabel
    TempFont = font.Font(window, size = 15, weight = 'bold', family = 'Consolas')
    InputLabel = Entry(window, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge', bg='#ffdada')
    InputLabel.pack()
    InputLabel.place(x=10,y=140)

def CreateEmailInputLabel():
    global InputEmail
    TempFont = font.Font(window, size=15, family='Consolas')
    InputEmail = Entry(window, font=TempFont, width=25, borderwidth=6, relief='ridge',bg='#ffdada')
    TempFont = font.Font(window, size=12, weight = 'bold', family='Consolas')
    label = Label(window, text = 'E-Mail',font = TempFont)
    label.pack()
    label.place(x=10, y=610)
    InputEmail.pack()
    InputEmail.place(x=70, y=605)

def CreateSearchButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, borderwidth = 10, text = "�˻�", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=320, y=140)

def CreateInfoButton():
    TempFont = font.Font(window, size=11, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7, height = 2, borderwidth = 5, text = "�ڼ���", command=InfoButtonAction)
    SearchButton.pack()
    SearchButton.place(x=384, y=205)

def CreateMapButton():
    TempFont = font.Font(window, size=11, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7,height = 2, borderwidth = 5, text = "�������", command=MapButtonAction)
    SearchButton.pack()
    SearchButton.place(x=384, y=275)

def CreateMailButton():
    TempFont = font.Font(window, size=8, weight='bold', family='Consolas')
    SearchButton = Button(window, font = TempFont, width = 7,height = 2, borderwidth = 5, text = "��������", command=SendMailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=368, y=600)

def CreatePrintListButton():
    TempFont = font.Font(window, size=12, weight='bold', family='Consolas')
    SearchButton = Button(window, font=TempFont, borderwidth=10, text="��ü ���", command=SearchLibList )
    SearchButton.pack()
    SearchButton.place(x=150, y=80)

def SendMailButtonAction():
    global Data, RenderTextm, Type, Tmp_Str, InputEmail
    iSearchIndex = str(RenderText.curselection()) #����� ����Ʈ���� Ȯ��
    EmailID = str(InputEmail.get())
    try:
        iSearchIndex = int(iSearchIndex[1:-2]) # (����)���� ���ڸ� �̾Ƴ�
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                SendEmail(location, EmailID)
            i += 1
        elif Type == 1:
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    SendEmail(location, EmailID)
                i += 1
        elif Type == 2:
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    SendEmail(location, EmailID)
                i += 1

def MapButtonAction():
    global Data, RenderText, Type, Tmp_Str
    iSearchIndex = str(RenderText.curselection())
    try:
        iSearchIndex = int(iSearchIndex[1:-2])
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                     zoom_start=17)
                folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                              popup = location.dutyname.string,
                              icon = folium.Icon(color = 'red', icon = 'info-sign')).add_to(map_osm)
                folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                              popup='���� �� ��ġ',
                              icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                text = location.dutyname.string + ".html"
                map_osm.save(text)
            i += 1
        elif Type == 1: #�̸�
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                         zoom_start=17)
                    folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                  popup=location.dutyname.string,
                                  icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)
                    folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                                  popup='���� �� ��ġ',
                                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                    text = location.dutyname.string + ".html"
                    map_osm.save(text)
                i += 1
        elif Type == 2: #�ּ�
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    map_osm = folium.Map(location=[float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                         zoom_start=17)
                    folium.Marker([float(location.wgs84lat.string), float(location.wgs84lon.string)],
                                  popup=location.dutyname.string,
                                  icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)
                    folium.Marker([float(MyInfo.lat.string), float(MyInfo.lon.string)],
                                  popup='���� �� ��ġ',
                                  icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)
                    text = location.dutyname.string + ".html"
                    map_osm.save(text)
                i += 1

def InfoButtonAction():
    global Data, RenderText, Type, Tmp_Str
    iSearchIndex = str(RenderText.curselection())
    try:
        iSearchIndex = int(iSearchIndex[1:-2])
    except:
        pass
    i = 0
    for location in Data.find_all("item"):
        if Type == 0:
            if iSearchIndex == i:
                text = ""
                text = AppendDataStr(location)
                tkinter.messagebox.showinfo(location.dutyname.string, text)
            i += 1
        elif Type == 1:
            if Tmp_Str in location.dutyname.string:
                if iSearchIndex == i:
                    text = ""
                    text = AppendDataStr(location)
                    tkinter.messagebox.showinfo(location.dutyname.string, text)
                i += 1
        elif Type == 2:
            if Tmp_Str in location.dutyaddr.string:
                if iSearchIndex == i:
                    text = ""
                    text = AppendDataStr(location)
                    tkinter.messagebox.showinfo(location.dutyname.string, text)
                i += 1

def AppendDataStr(location):
    text = ""
    for i in range(0, len(location.dutyaddr.string)):
        text += location.dutyaddr.string[i]
    text += chr(10)
    for i in range(0, len(location.dutyemclsname.string)):
        text += location.dutyemclsname.string[i]
    text += chr(10)
    text += "�з��� : "
    for i in range(0, len(location.dutyemcls.string)):
        text += location.dutyemcls.string[i]
    text += chr(10)
    text += "��ǥ��ȭ : "
    for i in range(0, len(location.dutytel1.string)):
        text += location.dutytel1.string[i]
    try:
        text += chr(10)
        text += "������ȭ : "
        for i in range(0, len(location.dutytel3.string)):
            text += location.dutytel3.string[i]
    except:
        pass
    return text

def SearchButtonAction():
    global SearchListBox, InputLabel
    iSearchIndex = str(SearchListBox.curselection())
    if iSearchIndex == "()":
        pass
    elif iSearchIndex == "(0,)": #�̸��˻�
        keyword = str(InputLabel.get())
        SearchLibName(keyword)
    elif iSearchIndex == "(1,)": #�ּҰ˻�
        keyword = str(InputLabel.get())
        SearchLibAddress(keyword)

def SearchLibList():
    global Data, RenderText, Type
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        RenderText.insert(i, location.dutyname.string + " | " + location.dutyaddr.string)
        i += 1
    Type = 0

def SearchLibName(keyword):
    global Data, RenderText, Type, Tmp_Str
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        if keyword in location.dutyname.string:
            RenderText.insert(i, location.dutyname.string + " | " + location.dutyaddr.string)
            i += 1
    Type = 1
    Tmp_Str = keyword

def SearchLibAddress(keyword):
    global Data, RenderText, Type, Tmp_Str
    i=0
    RenderText.delete(0, END)
    for location in Data.find_all("item"):
        if keyword in location.dutyaddr.string:
            RenderText.insert(i, location.dutyaddr.string + " | " + location.dutyname.string)
            i += 1
    Type = 2
    Tmp_Str = keyword

frame.pack()
frame.place(x = 10, y = 195)
CreateTitleLabel()
CreateEmailInputLabel()
CreateSearchListBox()
CreateInputLabel()
CreateSearchButton()
CreatePrintListButton()
CreateRenderText()
CreateInfoButton()
CreateMapButton()
CreateMailButton()

window.mainloop()