from tkinter import *
from tkinter import font
from tkinter.font import BOLD, nametofont
from tkinter import filedialog
from tkinter import messagebox
import sounddevice as sound
from scipy.io.wavfile import write
import wavio as wv
import time
#import tkinter as tk
from tkinter.filedialog import askopenfilename
from PyPDF2 import PdfFileMerger, PdfFileReader
from pathlib import Path

def back():
    page_Notes.pack_forget()
    page_start.pack()

def back2():
    page_Recorder.pack_forget()
    page_start.pack()
    page_Recorder.itemconfig(timer,text='')

def back3():
    page_MergePDF.pack_forget()
    page_start.pack()
    page_MergePDF.itemconfig(lbl_items,text='')

def TakingNote(): 
    page_start.pack_forget()
   
    def save_file():
        open_file = filedialog.asksaveasfile(mode='w',defaultextension='.txt')
        if open_file is None:
            return
        text = str(entry.get(1.0,END))
        open_file.write(text)
        open_file.close()
    
    def open_file():
        file = filedialog.askopenfile(mode='r',filetype=[('text files','*.txt')])
        if file is not None:
            content = file.read()
        entry.insert(INSERT,content)

    label = Frame(root)
    label.pack(fill = BOTH, expand = True)
    entry =Text(label,height=29,width =46,wrap=NONE,bg='#F8F8F8')
    entry.pack(side = LEFT, fill = BOTH, expand = True)
    scroll = Scrollbar(label, orient = VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)
    scroll.config(command = entry.yview)
    entry.config(yscrollcommand = scroll.set)
    b1 =Button(page_Notes,text='Save File',borderwidth = 0,fg='#4B3F91',bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=save_file)
    page_Notes.create_window(120,25, window=b1)
    b2 = Button(page_Notes,text='Open File',borderwidth = 0,fg='#4B3F91',bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=open_file)
    page_Notes.create_window(285,25, window=b2)
    
    b3 = Button(page_Notes,text='Back',borderwidth = 0,bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=back)
    page_Notes.create_window(200,555, window=b3)
    page_Notes.pack()
    page_Notes.create_window(7,45, window = label, anchor = NW)
  
def VoiceRecord():
    global timer
    page_start.pack_forget()
    page_Recorder.pack()
 
    def Record():
        freq = 44100
        dur =int(duration.get()) 
        recording = sound.rec(dur*freq,samplerate=freq,channels=2)
        try:
            temp = int(duration.get())
        except:
            print('Please enter the right value')
        while temp>0:
            page_Recorder.update()
            time.sleep(1)
            temp-=1
            if(temp==0):
                messagebox.showinfo('Time Countdown','Times up')
            page_Recorder.itemconfig(timer,text=f"{str(temp)}",font=("Courier",16, "italic",BOLD))
        sound.wait()
        write('recording.wav',freq,recording)  
    L1 = page_Recorder.create_text(200,268,text='Press the button to start',fill='#62799B',font=("Courier",13, "italic",BOLD))
    L2 = page_Recorder.create_text(200,165,font=("Courier",13, "italic",BOLD),fill='#62799B',justify = CENTER, text='The record duration:\n (in second)')
    duration = StringVar()
    E1 = Entry(page_Recorder,textvariable=duration)
    page_Recorder.create_window(200,200, anchor='center', window=E1)
    b_r1 = Button(page_Recorder,text='Start',bg='#FCDF24',borderwidth = 0,relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),fg='#4B3F91',command=Record)
    page_Recorder.create_window(200,310, anchor='center', window=b_r1)
    b_r2 = Button(page_Recorder,text='Back',borderwidth = 0,bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=back2)
    page_Recorder.create_window(200,555, anchor='center', window=b_r2)
    timer = page_Recorder.create_text(200,370,font=("Courier",13, "italic",BOLD),fill='#B62154', text='Timer')

def MergePDF():
    global lbl_items
    page_start.pack_forget()
    page_MergePDF.pack()
    filelist = []
    merger = PdfFileMerger()
    def open_file(files):
        filepath = askopenfilename(
            filetypes=[("PDF Files","*.pdf"), ("All Files", "*.*")])
        if not(filepath and Path(filepath).exists()):
            return
        files.append(filepath)
        # list out all filenames
        page_MergePDF.itemconfig(lbl_items,text='\n'.join(str(f) for f in files))
        if len(files) >= 2 and btn_merge['state'] == "disabled":
            btn_merge["state"] = "normal"
    def merge_pdfs(files):
        for f in files:
            merger.append(PdfFileReader(open(f, "rb")))
    
        output_filename = ent_output_name.get()

        if not output_filename:
            output_filename = "Untitled.pdf"
        elif ".pdf" not in output_filename:
            output_filename += ".pdf"
        merger.write(output_filename)
    
    lbl_open = page_MergePDF.create_text(200,165,fill='#62799B',justify = CENTER,font=("Courier", 13, "italic",BOLD), text='Please choose PDFs to join: \n(2 and above)')
    
    btn_open = Button(page_MergePDF,text='Open files',fg='#4B3F91',borderwidth = 0,bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=lambda: open_file(filelist))
    page_MergePDF.create_window(200,209, window=btn_open)
    
    lbl_items = page_MergePDF.create_text(200,250,fill='#F8F8F8',font=("Courier",8, "italic"),justify = CENTER, text='')
    
    lbl_to_merge = page_MergePDF.create_text(200,325,font=("Courier", 13, "italic",BOLD),fill='#62799B', text='Merged file name:')
 
    ent_output_name =Entry(page_MergePDF,width=15)
    page_MergePDF.create_window(200,350, anchor='center', window=ent_output_name)
    
    btn_merge =Button(page_MergePDF,text='Merge PDF',fg='#4B3F91',borderwidth = 0,bg='#FCDF24',relief='flat',activebackground='#FCDF24',state='disabled',font=("Courier", 10, "italic",BOLD),command=lambda: merge_pdfs(filelist))
    page_MergePDF.create_window(200,385, anchor='center', window=btn_merge)
  
    b_M2 = Button(page_MergePDF,text='Back',borderwidth = 0,bg='#FCDF24',relief='flat',activebackground='#FCDF24',font=("Courier", 10, "italic",BOLD),command=back3)
    page_MergePDF.create_window(200,555, anchor='center', window=b_M2)
  
# init
root = Tk()
root.title('Study With Me')
root.geometry('400x600')
root.resizable(0,0)
root.iconbitmap('logo3.ico')

page_start = Canvas(root, width=400, height=600, bd=0, highlightthickness=0)
page_Notes = Canvas(root, width=400, height=600, bd=0, highlightthickness=0,scrollregion=(0,0,1000,1000))
page_Recorder =Canvas(root, width=400, height=600, bd=0, highlightthickness=0) 
page_MergePDF= Canvas(root, width=400, height=600, bd=0, highlightthickness=0)

button1 = Button(root,text='Note Pad',borderwidth = 2,activeforeground='#9ED3FF',activebackground='#F8F8F8',relief='ridge',bg='#F8F8F8',font=("Arial",12,BOLD),fg='#B9D8F2',width=15, height=2,command=TakingNote)
button2 = Button(root,text='Voice Recorder',borderwidth = 2,activeforeground='#9ED3FF',activebackground='#F8F8F8',relief='ridge',bg='#F8F8F8',font=("Arial",12,BOLD),fg='#B9D8F2',width=15, height=2,command=VoiceRecord)
button3 = Button(root,text='PDF Merger',borderwidth = 2,activeforeground='#9ED3FF',activebackground='#F8F8F8',relief='ridge',bg='#F8F8F8',font=("Arial",12,BOLD),fg='#B9D8F2',width=15, height=2,command=MergePDF)

page_start.create_window(200,300, anchor='center', window=button1)
page_start.create_window(200,355, anchor='center', window=button2)
page_start.create_window(200,410, anchor='center', window=button3)
page_start.pack(fill='both', expand=True)

MyImage1 = PhotoImage(file='Study With Me.png')
MyImage2 = PhotoImage(file='Study With22.png')
MyImage3 = PhotoImage(file='Study With2.png')
MyImage4 = PhotoImage(file='Study With4.png')
CanvasImage = page_start.create_image(0,0,image= MyImage1, anchor='nw')
CanvasImage = page_MergePDF.create_image(0,0,image= MyImage2, anchor='nw')
CanvasImage = page_Notes.create_image(0,0,image= MyImage3, anchor='nw')
CanvasImage = page_Recorder.create_image(0,0,image= MyImage4, anchor='nw')
root.mainloop()