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

installerversion = "v0.2-alpha"

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

def inputquestion(text,desc=""):
    run("clear")
    print(f"{Back.WHITE}{Fore.BLACK}{text}{Fore.RESET}{Back.RESET}")
    print()
    print(desc)
    return input(">> ")

def menu(text,options,desc="",returnitemname=False):
    select = 0
    if settings["color"] == 1:
        colord = Back.RESET
    elif settings["color"] == 2:
        colord = Back.BLACK
    elif settings["color"] == 3:
        colord = Back.RED
    elif settings["color"] == 4:
        colord = Back.BLUE
    elif settings["color"] == 5:
        colord = Back.GREEN
    elif settings["color"] == 6:
        colord = Back.CYAN
    elif settings["color"] == 7:
        colord = Back.MAGENTA
    elif settings["color"] == 8:
        colord = Back.YELLOW
    elif settings["color"] == 9:
        colord = Back.WHITE
    while True:
        run("clear")
        maxlen = len(options)
        print(f"{colord}{Fore.BLACK}{text}{Fore.RESET}{Back.RESET}".center(20,"#"))
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

def startserver(showserver=False):
    if showserver:
        cmd = Popen(f"sh start.sh",shell=True)
    else:
        cmd = Popen(f"sh start.sh",shell=True,stdout=PIPE)
    output, err = cmd.communicate()
    return [output.decode(),err]

def check_for_updates():
    info("Requesting https://apt.github.com/")
    try:
        data = requests.get("https://api.github.com/repos/mas6y6/PyMC-Server/releases",timeout=10)
    except requests.exceptions.Timeout:
        error("Server failed to respond. Please check your network. Failure_name: TIMEOUT")
        data = None
        return data
    except requests.exceptions.ConnectionError as err:
        error(f"Unable to connect to github. Check your network connection. full error below:\n{err}")
        data = None
        return data

    try:
        returndata = list(json.loads(data.text))
    except:
        error("Failed to compile versions")
        data = None
        return data

    try:
        data = returndata[len(returndata) - 1]["tag_name"]
    except:
        error("Github REST API request limit has been reached unable to get updates")
        data = None
        return data

    return data

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
    servername = inputquestion("What the name of your NEW minecraft server")
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
    q = inputquestion("Description",desc="Leave blank for server name")
    if q == "":
        motd = servername
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
        lines[32] = f"motd={motd}\n"
        f.writelines(lines)
        f.truncate()
    ok("Success")
    ok("The server setup has been completed")
    warning("Just to let you know if you delete the settings.json file the installer will forget all of the changes that you made\nTo continue press enter")
    input()
    info("Please wait writing settings.json")
    f = open("settings.json","w")
    settingsdata = {"servername":servername,"color":1,"directory":directory}
    json.dump(settingsdata,f,indent=4)
    f.close()
    ok("Success")
    ok("The Setup process has been completed")
    questionnogui("Are you sure that you want to start server now or head to main menu (Y/n)")
    if pyinputplus.inputYesNo() == "yes":
        info("Starting server...")
        startserver(showserver=True)
        sys.exit(0)
    else:
        info("Starting main menu...")
        startmenu()

def finderrors():
    pass

def startmenu():
    d = menu(settings["servername"],desc="Use arrow keys to navagate",["Start Server","Server settings","Installer settings","exit"])
    if d == 1:
        output = startserver()
        finderrors(output)
    elif d == 2:
        serversettings()
    elif d == 3:
        sys.exit()
    else:
        pass

def serversettings():

def unpack_settings():
    f = open("settings.json","r")
    return json.load(f)

def update_settings():
    f = open("")

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
        else:
            info("Unpacking settings.json")
            settings = unpack_settings()
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