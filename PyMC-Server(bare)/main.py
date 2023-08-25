from tkinter import Tk
#from tkinter import ttk
import ttkbootstrap as ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.dialog import *
import tkinter as tk
import tkinter.font as Font
import os, json
import requests
import urllib.request
from subprocess import *
from threading import Thread
import time
import git

home_directory = os.path.expanduser('~')
server_directory = None
progressbar = None
run_server_dir = None
server_settings = None
done = None
def download(url,tofile):
    urllib.request.urlretrieve(url,tofile,showloading)
    urllib.request.urlcleanup()

def _setupdirectory(exists=False):
    os.chdir(home_directory)
    if exists == False:
        os.mkdir("PyMC-Server_content")
    os.chdir("PyMC-Server_content")
    try:
        with open("settings.json","w") as f:
            json.dump({"servers":[]},f,indent=4)
    except Exception as e:
        showerror("PyMC-Server",f"An error occurred {e}")
        exit()

settings = None

def open_settings():
    global settings
    with open("settings.json","r") as f:
        settings = json.load(f)
        f.close()

def update_settings():
    global settings
    with open("settings.json","w") as f:
        json.dump(f,settings,indent=4)
        f.close()

os.chdir(home_directory)
if os.path.exists("PyMC-Server_content"):
    os.chdir(home_directory)
    os.chdir("PyMC-Server_content")
    if not os.listdir():
        _setupdirectory(exists=True)
else:
    _setupdirectory()

import editer

mainframe = None
newserver = {}

root = Tk()
root.title("PyMC-Server")
root.geometry("500x300")
root.resizable(False,False)

open_settings()

def _check_if_server_exists(button,var):
    if var.get() == "None":
        button.config(state="disabled")
    else:
        button.config(state="enabled")

def pickinstalledserver(re=False):
    global mainframe
    if re == False:
        mainframe = None
    else:
        mainframe.distroy()

    mainframe = ttk.Frame(master=root)

    l1 = ttk.Label(master=mainframe,text="Welcome to PyMC-Server",font=("",20))
    l1.pack(pady=40)

    b2 = ttk.Button(master=mainframe,text="Open server",command=open_server)
    b2.pack(side="left")

    b1 = ttk.Button(master=mainframe,text="Add server",command=add_server1)
    b1.pack(side="left",padx=10)

    item_selected = tk.StringVar()
    item_selected.set("None")

    _check_if_server_exists(b2,item_selected)

    settings["servers"].insert(0,"None")

    menu = ttk.OptionMenu(mainframe,item_selected,*settings["servers"],command=lambda:_check_if_server_exists(b2,item_selected))
    menu.pack()

    mainframe.pack()

def open_server():
    pass

def add_server1():
    global mainframe, newsettings
    newsettings = {}
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="Whats the name of this new server?",font=("",20))
    l1.pack()
    e1 = ttk.Entry(master=mainframe)
    e1.pack(side="left")
    e1.insert(0,"New Server")
    b1 = ttk.Button(master=mainframe,text="Next",command=lambda:add_server2(e1.get()))
    b1.pack(side="left",padx=10)
    
    mainframe.pack()

def add_server2(val):
    global newserver
    if val == "":
        showerror("PyMC-Server","Please put a name for your server")
        return
    newserver["name"] = val
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="Gamemode?",font=("",20))
    l1.pack()

    group = tk.StringVar()
    group.set("None")

    radio1 = ttk.Radiobutton(master=mainframe, text="Survival", value="survival", variable=group)
    radio2 = ttk.Radiobutton(master=mainframe, text="Creative", value="creative", variable=group)
    radio1.pack(side="left",padx=4)
    radio2.pack(side="left")
    b1 = ttk.Button(master=mainframe,text="Next",command=lambda:add_server3(group.get()))
    b1.pack(side="left",padx=10)
    mainframe.pack()

def add_server3(val):
    global newserver
    if val == "None":
        showerror("PyMC-Server","Please select a option")
        return
    newserver["gamemode"] = val
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="Difficulty?",font=("",20))
    l1.pack()

    group = tk.StringVar()
    group.set("None")

    radio1 = ttk.Radiobutton(master=mainframe, text="Normal", value="normal", variable=group)
    radio2 = ttk.Radiobutton(master=mainframe, text="Easy", value="easy", variable=group)
    radio3 = ttk.Radiobutton(master=mainframe, text="Hard", value="hard", variable=group)
    radio4 = ttk.Radiobutton(master=mainframe, text="Peaceful", value="peaceful", variable=group)
    radio1.pack()
    radio2.pack()
    radio3.pack()
    radio4.pack()

    b1 = ttk.Button(master=mainframe,text="Next",command=lambda:add_server4(group.get()))
    b1.pack(pady=10)
    mainframe.pack()

def _change_directory(val,l2):
    val.set(askdirectory())
    print(val.get())
    l2.config(text=val.get())

def add_server4(val):
    global newserver
    if val == "None":
        showerror("PyMC-Server","Please select a difficulty")
        return
    newserver["difficulty"] = val
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="Where do you want to place your server?",font=("",20))
    l1.pack()

    dir = tk.StringVar()
    dir.set("None")

    l2 = ttk.Label(master=mainframe,text=dir.get())
    l2.pack()

    b1 = ttk.Button(master=mainframe,text="Change directory",command=lambda:_change_directory(dir,l2))
    b1.pack()

    b2 = ttk.Button(master=mainframe,text="Next",command=lambda: add_server5(dir.get()))
    b2.pack(pady=4)
    mainframe.pack()            

def add_server5(val):
    global newserver
    if val == "None" or val=="" or val==None:
        showerror("PyMC-Server","Please select a directory")
        return
    
    try:
        re = json.loads(requests.get("https://api.papermc.io/v2/projects/paper",timeout=10).text)
    except Exception as e:
        showerror('PyMC-Server',f"An error occurred while communicating to PaperMC {e}")
        return

    newserver["dir"] = val
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="What version do you want",font=("",20))
    l1.pack()

    ver = tk.StringVar()
    ver.set("None")
    print(ver.get())

    re["versions"].insert(0,"None")
    m1 = re["versions"][len(re["versions"]) - 1] + " Latest version"
    re["versions"].insert(1,m1)

    vers = ttk.OptionMenu(mainframe,ver,*re["versions"])
    vers.pack()

    b2 = ttk.Button(master=mainframe,text="Next",command=lambda: add_server6(ver.get(),re["versions"][len(re["versions"]) - 1]))
    b2.pack(pady=4)
    mainframe.pack()

def add_server6(val,val2):
    global newserver
    if val == "None":
        showerror("PyMC-Server","Please select a version")
        return
    
    if val.find("Latest version") == -1:
        newserver["version"] = val
        ver = val
    else:
        newserver["version"] = val2
        ver = val2
    try:
        re = json.loads(requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{ver}",timeout=10).text)
    except Exception as e:
        showerror('PyMC-Server',f"An error occurred while communicating to PaperMC {e}")
        return

    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="What build do you want",font=("",20))
    l1.pack()

    build = tk.StringVar()
    build.set("None")

    re["builds"].insert(0,"None")
    m1 = str(re["builds"][len(re["builds"]) - 1]) + " Latest build"
    re["builds"].insert(1,m1)

    builds = ttk.OptionMenu(mainframe,build,*re["builds"])
    builds.pack()

    b2 = ttk.Button(master=mainframe,text="Next",command=lambda: add_server7(build.get(),str(re["builds"][len(re["builds"]) - 1])))
    b2.pack(pady=4)
    mainframe.pack()

def add_server7(val,val2):
    global newserver

    print(newserver)

    if val == "None":
        showerror("PyMC-Server","Please select a build")
        return
    
    if val.find("Latest build") == -1:
        newserver["build"] = val
    else:
        newserver["build"] = val2

    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)

    print()
    l1 = ttk.Label(master=mainframe,text="Check",font=("",20))
    l1.pack()

    l2 = ttk.Label(master=mainframe,text="Name: " + newserver["name"],font=("",15))
    l2.pack()

    l3 = ttk.Label(master=mainframe,text="Difficulty: " + newserver["difficulty"],font=("",15))
    l3.pack()

    l4 = ttk.Label(master=mainframe,text="Gamemode: " + newserver["gamemode"],font=("",15))
    l4.pack()

    l4 = ttk.Label(master=mainframe,text="Version: " + newserver["version"],font=("",15))
    l4.pack()

    l5 = ttk.Label(master=mainframe,text="Build: " + newserver["build"],font=("",15))
    l5.pack()

    l6 = ttk.Label(master=mainframe,text="Directory: " + newserver["dir"],font=("",15))
    l6.pack()

    l7 = ttk.Label(master=mainframe,text='If this is correct then click "Install" if not then click "Restart"',font=("",12))
    l7.pack()

    b1 = ttk.Button(master=mainframe,text="Install",command=lambda: goto(1))
    b1.pack(side="left",pady=9)

    b2 = ttk.Button(master=mainframe,text="Restart",command=lambda: goto(2))
    b2.pack(side="left",pady=9,padx=3)

    b2 = ttk.Button(master=mainframe,text="Go to start up page",command=lambda: goto(3))
    b2.pack(side="left",pady=9,padx=3)
    mainframe.pack()

def run_server(mem="1024M",sp=False,userun=False):
    global Done
    Done = True
    if userun:
        if sp == False:
            run("sh start.sh",cwd=run_server_dir,shell=True,)
        else:
            run("sh start.sh&",cwd=run_server_dir,shell=True)
        rund = None
    else:
        if sp == False:
            rund = Popen("nohup sh start.sh",cwd=run_server_dir,shell=True)
        else:
            rund = Popen("nohup sh start.sh&",cwd=run_server_dir,shell=True)
    Done = False
    return rund

def install():
    global mainframe, newserver, progressbar
    mainframe = ttk.Frame()
    l1 = ttk.Label(master=mainframe,text="Installing",font=("",20))
    l1.pack()
    l2 = ttk.Label(master=mainframe,text="Downloading server...",font=("",15))
    l2.pack(pady=15)
    progressbar = ttk.Progressbar(master=mainframe,length=450,bootstyle="striped",mode="determinate")
    progressbar.pack(pady=20)
    b1 = ttk.Button(master=mainframe,text="Next",command=install2,state="disabled")
    b1.pack(pady=35)
    mainframe.pack()
    dir = newserver["dir"]
    ver = newserver["version"]
    build = newserver["build"]
    download(f"https://api.papermc.io/v2/projects/paper/versions/{ver}/builds/{build}/downloads/paper-{ver}-{build}.jar",f"{dir}/paper.jar")
    print("Downloaded")
    l2.config(text="Complete")
    b1.config(state="enabled")

def install2():
    global mainframe, newserver, progressbar
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    l1 = ttk.Label(master=mainframe,text="Ram value",font=("",20))
    l1.pack()
    e1 = ttk.Entry(master=mainframe)
    e1.pack()
    e1.insert(0,"1024M")
    b1 = ttk.Button(master=mainframe,text="Next",command=lambda: install3(e1.get()))
    b1.pack(pady=4)
    mainframe.pack()


def install3(value):
    global mainframe, newserver, progressbar
    if value == "":
        showerror("Please put a ram number")
        return
    newserver["mem"] = value

    mainframe.destroy()
    mainframe = ttk.Frame()
    l1 = ttk.Label(master=mainframe,text="Unpacking",font=("",20))
    l1.pack()
    l2 = ttk.Label(master=mainframe,text="Creating Startup File...",font=("",15))
    l2.pack(pady=15)
    progressbar = ttk.Progressbar(master=mainframe,length=450,bootstyle="primary",mode="indeterminate")
    progressbar.pack(pady=20)
    b1 = ttk.Button(master=mainframe,text="Next",command=install4,state="disabled")
    b1.pack()
    mainframe.pack()
    progressbar.start()
    dir = newserver["dir"]
    mem = newserver["mem"]
    os.chdir(dir)
    with open("start.sh","w") as f:
        f.write(f"java -Xmx{mem} -Xms{mem} -jar paper.jar")
        f.close()
    l2.config(text="Unpacking server...")
    Thread(target=lambda: run_server(sp=False,userun=True)).start()
    time.sleep(0.1)
    while Done:
        mainframe.update()
    progressbar.stop()
    progressbar["value"] = 0
    b1.config(state="enabled")
    l2.config(text="Done")

def install4():
    global mainframe
    mainframe.destroy()
    mainframe = ttk.Frame(master=root)
    mainframe

def goto(page):
    global mainframe
    mainframe.destroy()
    if page == 1:
        install()
    elif page == 2:
        add_server1()
    elif page == 3:
        pickinstalledserver()
    else:
        pass

def showloading(count,downloaded,size):
    global progressbar, mainframe
    if count == 0:
        progressbar.config(maximum=size)
    else:
        progressbar.step(downloaded)
    mainframe.update()

pickinstalledserver()
root.mainloop()