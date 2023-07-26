#This code was made by @mas6y6 on github
#
#
#
#
#
#
#
# Its NOT recommended to edit this code

from subprocess import run, Popen, PIPE
import os
import time
import json
import sys

#Package prep

try:
    import colorama
    import progressbar
    import getkey
    import pyinputplus
    import requests
except:
    print("Python Warning the packages that are required to run the server installer is not installed\n The program will install them now")
    time.sleep(3)
    run("pip install progressbar2",shell=True)
    run("pip install colorama",shell=True)
    run("pip install getkey",shell=True)
    run("pip install PyInputPlus",shell=True)
    run("pip install requests",shell=True)
    print("The packages have been installed")
    print("The mcserver installer will now start")

#main program

installerversion = "0.1B"

from colorama import Fore, Style, Back
import progressbar
import urllib.request
import getkey
from requests import get

widgets = [Fore.CYAN,Style.BRIGHT," ",progressbar.Percentage(),progressbar.Bar('#'),Style.NORMAL,progressbar.ETA(format_NA="ETA: Unknown", format_not_started="ETA: --:--:-- ",format="ETA: %(eta)s ",format_finished="ETA: 0:00:00 "),progressbar.Timer(format="TIME: %(elapsed)s")]
pbar = None
def _show_loading(num,block_size,total_size):
    global pbar
    if pbar == None:
        pbar = progressbar.ProgressBar(widgets=widgets,maxval=total_size)
        pbar.start()
    downloaded = num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def download(url,tofile):
    urllib.request.urlretrieve(url,tofile,_show_loading)

#download("https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/95/downloads/paper-1.20.1-95.jar")

def fatul(text):
    print(f"{Fore.RESET}{Style.NORMAL}{Style.DIM}{Fore.RED}[X] {text}{Fore.RESET}{Style.NORMAL}")

def warning(text):
    print(f"{Fore.RESET}{Style.NORMAL}{Style.BRIGHT}{Fore.YELLOW}[!] {text}{Fore.RESET}{Style.NORMAL}")

def info(text):
    print(f"{Fore.RESET}{Style.NORMAL}[i] {text}{Fore.RESET}{Style.NORMAL}")

def error(text):
    print(f"{Fore.RESET}{Style.NORMAL}{Style.BRIGHT}{Fore.RED}[x] {text}{Fore.RESET}{Style.NORMAL}")

def ok(text):
    print(f"{Fore.RESET}{Style.NORMAL}{Style.BRIGHT}{Fore.GREEN}[*] {text}{Fore.RESET}{Style.NORMAL}")

def questionnogui(text):
    print(f"{Fore.RESET}{Style.NORMAL}{Style.BRIGHT}{Fore.MAGENTA}[?] {text}{Fore.RESET}{Style.NORMAL}")

def question(text,options,desc="",returnitemname=False):
    select = 0
    while True:
        maxlen = len(options)
        run("clear")
        print(f"{Back.WHITE}{Fore.BLACK}{text}{Fore.RESET}{Back.RESET}")
        print()
        print(desc)
        print()
        for i in range(maxlen):
            if select == i:
                print(">>",options[i])
            else:
                print(options[i])
        key = getkey.getkey()
        if key == getkey.keys.ENTER:
            break
        elif key == getkey.keys.UP:
            if not select == 0:
                select -= 1
        elif key == getkey.keys.DOWN:
            if not select == maxlen - 1:
                select += 1
    run("clear")
    if returnitemname == False:
        return select
    elif returnitemname == True:
        return options[select]
    else:
        raise TypeError("returnitemname accepts Boolean values")

def inputquestion(text,desc):
    run("clear")
    print(f"{Back.WHITE}{Fore.BLACK}{text}{Fore.RESET}{Back.RESET}".center(os.get_terminal_size[1]))
    print()
    print(desc)
    return input(">> ")

def menu(text,options,desc="",returnitemname=False):
    select = 0
    while True:
        run("clear")
        maxlen = len(options)
        print(f"{Back.CYAN}{Fore.BLACK}{text}{Fore.RESET}{Back.RESET}".center(20,"#"))
        print()
        print(desc)
        print()
        for i in range(maxlen):
            if select == i:
                print(">>",options[i])
            else:
                print(options[i])
        key = getkey.getkey()
        if key == getkey.keys.ENTER:
            break
        elif key == getkey.keys.UP:
            if not select == 0:
                select -= 1
        elif key == getkey.keys.DOWN:
            if not select == maxlen - 1:
                select += 1
    run("clear")
    if returnitemname == False:
        return select
    elif returnitemname == True:
        return options[select]
    else:
        raise TypeError("returnitemname accepts Boolean values")

def startmenu():
    pass

def loading():
    lu = progressbar.ProgressBar(widgets=[Fore.RESET,progressbar.AnimatedMarker()])
    while True:
        lu.update(0)

def startserver():
    cmd = Popen(f"sh start.sh",shell=True,stdout=PIPE)
    output, err = cmd.communicate()
    return [output.decode(),err]

def setup():
    dirs = [item for item in os.listdir() if not item.startswith(".")]
    dirs.append(".")
    dirs.append("+ Create a new directory")
    info("Placing settings.json")
    try:
        os.remove("settings.json")
    except:
        pass
    with open("settings.json","w") as f:
        f.close()
    ok("Success")
    time.sleep(0.5)
    while True:
        directory = ""
        q = question("Where do you want to install your Minecraft server",dirs,desc="Use arrow keys to navigate",returnitemname=True)
        if q == "+ Create a new directory":
            info("Creating new directory")
            os.mkdir("mcserver")
            os.chdir("mcserver")
            directory = os.getcwd()
            info(f"The server will be placed on {directory}")
            ok("Directory Created")
            break
        else:
            if q == ".":
                directory = os.getcwd()
                info(f"The server will be placed on {directory}")
                ok("Using current directory")
                break
            else:
                if os.path.isdir(q):
                    if not os.listdir(q):
                        info(f"The directory {q} was selected")
                        os.chdir(q)
                        directory = os.getcwd()
                        info(f"The server will be placed on {directory}")
                        ok("Directory Selected")
                        break
                    else:
                        error("That is not a vaild directory\nThe directory needs to be empty")
                else:
                    error("That is not a vaild directory")
    time.sleep(1)
    info("Requesting PaperMC for server versions")
    returndata = get("https://api.papermc.io/v2/projects/paper/").content.decode(encoding='utf-8')
    versions = json.loads(returndata)["versions"]
    questionnogui('Do you want the Latest version of papermc (Y/n)')
    anwser = pyinputplus.inputYesNo()
    found = False
    if anwser == "no":
        while True:
            print(versions)
            questionnogui('What version of papermc that you want to install\nPlease pick one of the following versions above')
            anwser = input()
            for i in range(len(versions)):
                if versions[i - 1] == str(anwser):
                    minecraftserverver = versions[i - 1]
                    found = True
            if found == True:
                ok("Selected")
                break
            else:
                error("That version was not found on PaperMC")
    else:
        minecraftserverver = versions[len(versions) - 1]
    
    info("The server version has been saved")
    info(f"Requesting PaperMC for server {minecraftserverver} builds")
    returndata = get(f"https://api.papermc.io/v2/projects/paper/versions/{str(minecraftserverver)}").content.decode(encoding='utf-8')
    builds = json.loads(returndata)["builds"]
    questionnogui('Do you want the Latest build of papermc (Y/n)')
    anwser = pyinputplus.inputYesNo()
    found = False
    if anwser == "no":
        while True:
            print(builds)
            questionnogui('What version of papermc that you want to install\nPlease pick one of the following builds above')
            anwser = input()
            for i in range(len(builds)):
                if builds[i - 1] == int(anwser):
                    minecraftserverbuild = builds[i - 1]
                    found = True
            if found == True:
                ok("Selected")
                break
            else:
                error("That version was not found on PaperMC")
    else:
        minecraftserverbuild = builds[len(builds) - 1]
    
    info(f"Selected the Paper:\nVersion:{minecraftserverver}\nBuild:{minecraftserverbuild}")
    info(f"Downloading the following file paper-{minecraftserverver}-{minecraftserverbuild}.jar to your {os.getcwd()}...")
    download(f"https://api.papermc.io/v2/projects/paper/versions/{minecraftserverver}/builds/{minecraftserverbuild}/downloads/paper-{minecraftserverver}-{minecraftserverbuild}.jar","paper.jar")
    ok("Download Success")
    questionnogui("Do custom ram value (Y/n)\nThe default ram is 1024M")
    anwser = pyinputplus.inputYesNo()
    if anwser == "yes":
        questionnogui("How much ram do you want for the server")
        ram = pyinputplus.inputNum()
    else:
        ram = "1024"
    ok(f"The selected ram {ram}")
    with open("start.sh","w") as f:
        f.write(f"java -Xmx{ram}M -Xms{ram}M -jar {os.getcwd()}/paper.jar nogui")
        f.close()
    
    info("Unpacking Jar file...")
    warning("The Jar file will crash because the eula check has not been completed")
    output = startserver()
    if "Failed to load eula.txt" in output[0]:
        error("Eula check failed")
    ok("Jar file unpacked Successfully")
    questionnogui("Do you agree to the Minecraft server eula *Required to start server* (Y/n)\nLearn more here https://www.minecraft.net/en-us/eula")
    if pyinputplus.inputYesNo() == "yes":
        eula = True
        ok("Eula accepted")
    else:
        eula = False
        error("Eula refused")
        error("The server need the eula to be accepted")
        fatul("Process killed please delete the folder that contants the server info")
        sys.exit()
    info("Updateing Eula file...")
    with open("eula.txt","r+") as f:
        lines = f.readlines()
        f.seek(0)
        lines[2] = "eula=true\n"
        f.writelines(lines)
        f.truncate()
    ok("Success")
    q = question("Gamemode",["Survial","Creative"],returnitemname=True)
    if q == "Survial":
        Gamemode = "normal"
    elif q == "Creative":
        Gamemode = "easy"
    else:
        pass
    q = question("Difficulty",["Normal","Easy","Hard","Hardcore"],returnitemname=True)
    if q == "Normal":
        Difficulty = "normal"
        Hardcore = "false"
    elif q == "Easy":
        Difficulty = "easy"
        Hardcore = "false"
    elif q == "Hard":
        Difficulty = "hard"
        Hardcore = "false"
    elif q == "Hardcore":
        Difficulty = "Normal"
        Hardcore = "true"
    else:
        pass
    q = inputquestion("Seed",desc="Leave blank for random seed number")
    if q == "":
        seed = ""
    else:
        seed = q
    q = inputquestion("Description",desc="")
    if q == "":
        motd = ""
    else:
        motd = q
    info("Rewriteing Server Properties")
    with open("server.properties","r+") as f:
        lines = f.readlines()
        f.seek(0)
        lines[7] = f"difficulty={Difficulty}\n"
        lines[18] = f"gamemode={Gamemode}\n"
        lines[21] = f"hardcore={Hardcore}\n"
        lines[26] = f"level-seed={seed}\n"
        f.writelines(lines)
        f.truncate()
    ok("Success")
    ok("The server setup has been completed")







if __name__ == "__main__":
    info("This Minecraft server installer is made my @mas6y6 on github")
    time.sleep(0.5)
    info("Finding the settings file")
    time.sleep(0.25)
    if os.path.isfile("settings.json"):
        ok("Found starting menu")
        time.sleep(0.25)
        info("Starting server main menu")
        if os.path.getsize("settings.json") == 0:
            error("It seams that the settings.json file is empty (This happens when the setup process is tnterrupted)")
            questionnogui("do you want do run the setup process (Y/n)")
            if pyinputplus.inputYesNo() == 'yes':
                setup()
            else:
                fatul("Process stopped")
                sys.exit()
        startmenu()
            
    else:
        error("The settings.json file was not found")
        questionnogui("do you want do run the setup process (Y/n)")
        if pyinputplus.inputYesNo() == 'yes':
            setup()
        else:
            fatul("Process stopped")
            sys.exit()
else:
    fatul('The following process has been killed because this is not a module its is a script and needs to be runned by using the shell command "python3 main.py"')
    sys.exit()