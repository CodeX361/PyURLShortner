# Importing Required Modules
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import json
import logging
import webbrowser
import pyperclip
import threading

# Settings Up Logging Module For Dumping Errors
logging.basicConfig(filename="logs/Application_Logs.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

# Geting The URL List From The Apps DataBase
DataFile=open("data/MetaData.PYUS","r+")
data=json.load(DataFile)
DataFile.close()

# App Configurations 
AppName="PyURLShortner"
AppDeveloper="Shadow"
AppVersion="5.0.1"

# Function To Use RGB Colors In The GUI
def color(rgb):
   return "#%02x%02x%02x" % rgb

# App GUI Configurations
root=Tk()
root.title(f"{AppName} By {AppDeveloper} Version {AppVersion}")
root.geometry("900x600")
root.resizable(0,0)
root.config(bg=color((22,22,22)))

# App Variables
url=StringVar()
nickname=StringVar()

# App GUI Heading And Sub Heading
app_title=Label(root,text="PyURLocker",font=("forte",40,"bold"),bg=color((22,22,22)),fg="aqua").pack()
app_sub_heading=Label(root,text="An Easy To Use URL Storing App",font=("berlin sans fb demi",12,"bold"),bg=color((22,22,22)),fg="aqua").pack()

# App List Box
list_box=Listbox(root,bg=color((21,21,21)),width=95,height=20,font=("berlin sans fb demi",11,"bold"),fg="white",selectmode=SINGLE)
list_box.place(x=20,y=160)

# Function To Add Items To List From Dictionary (Database)
def addListItems():
   for Item in data:
      list_box.insert(END,Item)

addListItems()

# Function To Shorten Links And To Store In DataBase
def addURL():
   site_url=url.get()
   site_name=nickname.get()

   if (site_url!="") and (site_name!=""):
      new_shorten_url={
         f"{site_name}" : f"{site_url}" }
      with open("data\MetaData.PYUS","r+") as file:
         BaseFile=json.load(file)
         BaseFile.update(new_shorten_url)
         file.seek(0)
         json.dump(BaseFile,file)
         list_box.insert(END,f"{site_name}")
   elif (site_url=="") or (site_name==""):
      messagebox.showerror("Error","Please Enter Something In URL/URL Name Field!")

# Function To Remove Selected Item From List And DataBase
def removeItem():
   try:
      current_selection=list_box.curselection()
      current_selection=list_box.get(current_selection)
      #print(data[current_selection])

      list_box.delete(ANCHOR)

      with open("data\MetaData.PYUS","r+") as mainfile:
         data=json.load(mainfile)
         print(data)
         del data[current_selection]
         print(data)
         with open("data\MetaData.PYUS","r+") as cls:
            cls.truncate(0)
            cls.write(json.dumps(data))

   except Exception as e:
      print(e)
      logging.info(e)
      messagebox.showerror("Item Removal Error","Selected Item Cannot Be Removed!")

# Function To Open The URL Directly
def openURL():
   current_selection=list_box.curselection()
   current_selection=list_box.get(current_selection)
   item=data[current_selection]
   print(item)
   webbrowser.open(item)


# Function To Remove All Items From Database And List
def removeAll():
   try:
      list_box.delete(0,END)
      with open("data\MetaData.PYUS","r+") as mainfile:
         mainfile.truncate(0)
         mainfile.write("{}")
         mainfile.close()
   except Exception as e:
      logging.info(e)
      messagebox.showerror("Error!",f"{e}")

# Function To Copy The Link Of The URL
def copyLink():
   current_selection=list_box.curselection()
   current_selection=list_box.get(current_selection)
   item=data[current_selection]
   pyperclip.copy(item)      

# App GUI Labels
enter_url=Label(root,text="Enter The URL",font=("ubuntu",9,"bold"),bg=color((22,22,22)),fg="white")
enter_url.place(x=20,y=100)
url_nickname=Label(root,text="Enter A Name For The URL",font=("ubuntu",9,"bold"),bg=color((22,22,22)),fg="white")
url_nickname.place(x=440,y=100)

# App GUI URL Entry Box
add_url=Entry(root,textvar=url,font=("berlin sans fb demi",12,"bold"),width=40)
add_url.place(x=20,y=125)
url_name=Entry(root,textvar=nickname,font=("berlin sans fb demi",12,"bold"),width=27)
url_name.place(x=440,y=125)

# App GUI Button
add_url_button=Button(root,text="Shorten",font=("berlin sans fb demi",10,"bold"),bg=color((0,255,0)),fg="white",width=20,bd=4,command=addURL)
add_url_button.place(x=730,y=121)
open_url_button=Button(root,text="Open Link",font=("berlin sans fb demi",10,"bold"),bg=color((0,255,0)),fg="white",width=23,bd=4,command=openURL)
open_url_button.place(x=20,y=553)
remove_item_button=Button(root,text="Remove Item",font=("berlin sans fb demi",10,"bold"),bg=color((0,255,0)),fg="white",width=23,bd=4,command=removeItem)
remove_item_button.place(x=240,y=553)
remove_all_items=Button(root,text="Remove All Items",font=("berlin sans fb demi",10,"bold"),bg=color((0,255,0)),fg="white",width=23,bd=4,command=removeAll)
remove_all_items.place(x=480,y=553)
copy_link=Button(root,text="Copy Link",font=("berlin sans fb demi",10,"bold"),bg=color((0,255,0)),fg="white",width=23,bd=4,command=copyLink)
copy_link.place(x=705,y=553)

# App GUI Mainloop
root.mainloop()
