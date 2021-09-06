import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import messagebox
import random
import tkinter.ttk as ttk
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import filedialog
import base64
import os
import webbrowser

pagenum = 1
win = Tk()
win.minsize(300,200)
win.title("B Mail")
win.iconbitmap('pics/Mail.ico')
bg = PhotoImage(file="pics/Mail.png")
myfont=font.Font(family="alternate sans",size="10",weight="bold")

global username, password
username = ""
password = ""

filenamelist = []
atno=1
attlist=[]

def logout():
        global pagenum
        if os.path.exists("username.txt"):
                os.remove("username.txt")
        if os.path.exists("password.txt"):
                os.remove("password.txt")
        else:
                messagebox.showinfo("Bmail", "Unable to delete saved data. restart the app.")
        pagenum=1
        changepage()

def filebox():
	global attlist, filenamelist, atlist
	def dellist():
		for i in lbox.curselection():
			a = filenamelist.pop(i)
			b= attlist.pop(i)
			c= lbox.delete(i)
			z=str(len(attlist))+" files"
			tlabel.config(text=z)
			atlist.config(text=z)
	
	lb=Toplevel(win)
	lb.config(bg="white")
	myfont45 = font.Font(family="alternate sans",size="8",weight="bold")
	a=0
	g = Frame(lb)
	g.pack()
	lbox = Listbox(g, height=5, width=30,bg="#3897f1",fg="white", font=myfont45)
	lbox.pack(side=LEFT, fill=BOTH)
	scrollbar = Scrollbar(g)
	
	scrollbar.pack(side = RIGHT, fill = BOTH)
	
	lbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command = lbox.yview)
	
	scrollbar2 = Scrollbar(g)
	scrollbar2.pack(side = BOTTOM)
	lbox.config(xscrollcommand=scrollbar2.set)
	
	scrollbar2.config(command = lbox.xview)
	
	tlabel=Label(lb, text="", bg="white", fg="#3897f1")
	tlabel.pack(side= LEFT)
	
	deletebtn=Button(lb, text="Delete",command=dellist ,bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",font=myfont45)
	deletebtn.pack()
	for i in attlist:
		if len(i)>2:
			lbox.insert(a, i)
			z=str(len(attlist))+" files"
			tlabel.config(text=z)
			atlist.config(text=z)
			a+=1

def fileopen():
   global filenamelist, atno, atlist
   try:
   		input = filedialog.askopenfilename(initialdir="/storage/emulated/0/")
   except:
   		input = filedialog.askopenfilename(initialdir="/")
   try:
   	if input[-1]!="/":
   		filenamelist.append(str(input))
   		fn=str(input).split("/")
   		attlist.append(fn[-1])
   		atno+=1
   		z=str(len(attlist))+" files"
   		atlist.config(text=z)
   except:
   	print("no file selected")

def mail_send():
	global attlist, tomail, sub, ebody
	fromad = username
	pwd = password
	to = tomail.get()
	subject = sub.get()
	
	msg = MIMEMultipart()
	
	msg['From'] = fromad
	msg['To'] = to
	msg['Subject'] = subject
	
	body = ebody.get("1.0", END) + "\n This Email was Sent By Bmail tkinter(python gui) app"
	if var.get()==2:
		msg.attach(MIMEText(body, 'html'))
	else:
		msg.attach(MIMEText(body, 'plain'))
	number=0
	for filename in filenamelist:
		if filename!="":
			attachment = open(filename, "rb")
			p = MIMEBase('application', 'octet-stream')
			p.set_payload((attachment).read())
			encoders.encode_base64(p)
			p.add_header('Content-Disposition', 'attachment; filename=%s'%attlist[number])
			msg.attach(p)
			number+=1
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(fromad, pwd)
		text = msg.as_string()
		server.send_message(msg)
		messagebox.showinfo("Bmail", "Email sent.\nTell your sender\nto check his Inbox.")
		server.quit()
	except:
		messagebox.showerror("Bmail", "Message not Sent.\nUnknown Error.")
	
	
	
chkvar=True



def checking():
	if chkvar==True:
		chk.config(text="Login Success",bg="#00FF00", fg="dark green")
	elif chkvar==False:
		chk.config(text="Invalid Credentials",bg="#ffcccb", fg="red")


def login_chk():
	global username, password, chkvar
	checking()
	usr = userentry.get()
	
	pwd = passwordtxt.get()
	if len(usr)<1:
		usr="your_email@gmail.com"
		pwd="your_password"
		messagebox.showinfo("B Mail", "Shortcut Used.\nUsing default Email\n(pythonguitkinter@gmail.com).")
		username=usr
		password=pwd
		loginstore = open("username.txt", "w")
		loginstore.write(username)
		loginstore.close()
		pwdstore = open("password.txt", "w")
		pwdstore.write(password)
		pwdstore.close()
		cpg2()
	else:
		username = usr
		password = pwd
		server=smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		try:
			server.login(usr,pwd)
			check = True
			chkvar=True
			checking()
		except:
			check = False
			print("password incorrect")
			chkvar=False
			checking()
		server.quit()
		if check==True:
			messagebox.showinfo("B Mail", "Login Successful.")
			loginstore = open("username.txt", "w")
			loginstore.write(username)
			loginstore.close()
			pwdstore = open("password.txt", "w")
			pwdstore.write(password)
			pwdstore.close()
			cpg2()
		else:
			messagebox.showerror("B Mail", "Login Unsuccessful.")
			

def cpg1():
	global pagenum
	pagenum=1
	changepage()

def cpg2():
	global pagenum
	pagenum=2
	changepage()

on=1
def showp():
	global  showb, pentry, on
	if on==1:
		pentry.config(show="")
		showb.config(text="Hide")
		on=0
	else:
		pentry.config(show="★")
		showb.config(text="Show")
		on=1
	
def callback():
    webbrowser.open("https://myaccount.google.com/lesssecureapps", new=1)

def page1(win):
	global userentry, passwordtxt, chk, showb, pentry
	myfont= font.Font(family="magic",size="15", weight="bold")
	myfontog= font.Font(family="magic",size="8", weight="bold")
	myfont1= font.Font(family="alternate sans",size="8",weight="bold")
	myfont2= font.Font(family="alternate sans",size="7")
	myfont3 = font.Font(family="alternate sans",size="7",weight="bold")
	myfont45 = font.Font(family="alternate sans",size="8",weight="bold")
	Label(win,text="", bg="#ffffff",width=41, height=35).grid(row=0,column=0,rowspan=30)

	Tcc=Label(win,text="", font=myfont, bg="white")
	Tcc.grid(row=1, column=0)
	#Tcc=Label(win,text="", font=myfont, bg="white")
	#Tcc.grid(row=2, column=0)
	Tcc=Label(win,text="", image=bg, font=myfont, bg="white")
	Tcc.grid(row=2, column=0)
	Tcc=Label(win,text="Bmail", font=myfont, bg="white")
	Tcc.grid(row=3, column=0)
	

	Tcc=Label(win,text="", font=myfont, bg="white")
	Tcc.grid(row=4, column=0)

	userid = Label(win, text="Login ID", font=myfont1, bg="white")
	userid.grid(row=6, column=0, sticky="sw",padx=16)
	userentry= Entry(win, width=42, font=myfontog, bg="#fafafa")
	userentry.grid(row=7,column=0, ipady=10)
	password = Label(win, text="Password", font=myfont1, bg="white")
	password.grid(row=8, column=0, sticky="sw", padx=16)
	passwordtxt = StringVar()
	pentry = Entry(win,textvariable=passwordtxt,show="★", font=myfontog,width=32, bg="#fafafa")
	pentry.grid(row=9,column=0,sticky="w", padx=20, ipady=10)
	showb=Button(win,text="Show", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",font=myfont45,width=6, height=2, command=showp)
	showb.grid(row=9,column=0,sticky="e", padx=20)
	Tcc=Label(win,text="", font=myfont, bg="white")
	Tcc.grid(row=10, column=0)
	Lb=Button(win,text="Log In", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",font=myfont1,width=35, height=2, command=login_chk)
	Lb.grid(row=11,column=0)
	chk = Label(win, text="", font=myfont1, bg="white")
	chk.grid(row=12, column=0)
	Help = Label(win, text="Tip:-\nKeep username blank and \nclick Login To use default Email.", font=myfont1, bg="white")
	Help.grid(row=13, column=0)
	Help = Label(win, text="Enable less Secure app access.\nbefore proceeding.", font=myfont1, bg="white")
	Help.grid(row=14, column=0)
#	Help = Label(win, text="Click here for less secure app access", font=myfont1, bg="white")
#	Help.grid(row=14, column=0)
	link1 = Label(win, text="Click here for less secure app access", bg='white', fg="blue", cursor="hand2")
	link1.grid(row=15, column=0)
	link1.bind("<Button-1>", lambda e: callback())
	
def page2(win):
	global userentrys, tomail, sub, ebody, username, var, atlist
	myfont= font.Font(family="alternate sans",size="18", weight="bold")
	myfont1= font.Font(family="alternate sans",size="11",weight="bold")
	myfont2= font.Font(family="alternate sans",size="7")
	myfont3 = font.Font(family="alternate sans",size="8",weight="bold")
	myfontog= font.Font(family="magic",size="9", weight="bold")
	Label(win,text="", bg="#ffffff", width=41, height=40).grid(row=0,column=0,rowspan=30)
	
	Tcc=Label(win,text="", font=myfont, bg="white")
	Tcc.grid(row=1, column=0)
	Tcc=Label(win,text="Bmail", font=myfont, bg="white")
	Tcc.grid(row=2, column=0)
	
	msg1=Label(win,text="Send Email\n ", font=myfont1, bg="white", fg="grey")
	msg1.grid(row=3, column=0)
	Lb=Button(win,text="Log Out.", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",font=myfont3,width=35, height=2, command=logout)
	Lb.grid(row=4, column=0,pady=10)
	Frgt= Label(win,text="————————————OR————————————",font=myfont3, bg="white", fg="grey")
	Frgt.grid(row=5,column=0)
	userid = Label(win, text="From", font=myfont3, bg="white")
	userid.grid(row=6, column=0, sticky="sw",padx=16)
	userentrys = Entry(win, width=36, font=myfontog, bg="#fafafa")
	userentrys.grid(row=7, column=0, ipady=10)
	userid = Label(win, text="To", font=myfont3, bg="white")
	userid.grid(row=8, column=0, sticky="sw",padx=16)
	tomail= Entry(win, width=36, font=myfontog, bg="#fafafa")
	tomail.grid(row=9, column=0, ipady=10)
	userid = Label(win, text="Subject", font=myfont3, bg="white")
	userid.grid(row=10, column=0, sticky="sw",padx=16)
	sub= Entry(win, width=36, font=myfontog, bg="#fafafa")
	sub.grid(row=11, column=0, ipady=10)
	userid = Label(win, text="Compose Email", font=myfont3, bg="white")
	userid.grid(row=12, column=0, sticky="sw",padx=16)
	ebody= Text(win, height=6, width=36, font=myfontog, bg="#fafafa")
	ebody.grid(row=13, column=0, ipady=10)
	x = Button(win, text ="Attach",bg="#3897f1",fg="white", activebackground="white",font=myfont3, activeforeground="#3897f1", command = lambda:fileopen())
	x.grid(row=14,column=0,sticky="e",padx=20)
	var = IntVar()
	R1 = Radiobutton(win, text="Text", variable=var, value=1,bg="white",font=myfont3)
	R1.grid(row=14,column=0,sticky="w",padx=20)
	R2 = Radiobutton(win, text="HTML", variable=var, value=2,font=myfont3, bg="white")
	R2.grid(row=14,column=0,sticky="w",padx=80)
	atlist = Button(win, text="0 files",bg="#3897f1",fg="white",font=myfont3,  activebackground="white",activeforeground="#3897f1", command=filebox)
	atlist.grid(row=14,column=0,sticky="e",padx=80)
	Lb=Button(win,text="Send", bg="#3897f1",fg="white", activebackground="white",activeforeground="#3897f1",font=myfont3,width=35, height=2,command=mail_send)
	Lb.grid(row=15, column=0)
	userentrys.insert(0, username)

	
	
def changepage():
    global pagenum, win
    for widget in win.winfo_children():
        widget.destroy()
    if pagenum == 1:
        page1(win)
    elif pagenum==2:
        page2(win)

try:
        print("Checking for saved Credentials.....")
        fileu =open("username.txt", "r")
        username = fileu.read()
        
        filep =open("password.txt", "r")
        password = filep.read()
        fileu.close()
        filep.close()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, password)
        page2(win)
except:
        try:
                os.remove("username.txt")
                os.remove("password.txt")
        except:
                print("No Credentials found.")
        page1(win)
win.mainloop()
