import tkinter as tk
from io import BytesIO
from tkinter import *
from tkinter.ttk import *
import os
from PIL import Image, ImageTk
import audio_metadata
import shutil


import pygame
from pygame import mixer

mixer.init()

# import frame as frame

window = tk.Tk()
window.title("MP3 player")
window.geometry("800x650")
window.resizable(False, False)
window.configure(background='white')

window.wm_iconbitmap('C:\learning python\MP3 Player\images\logo.ico')




play_status=0


def play():

    global play_status
    if play_status==0:
        song = song_box.get(ACTIVE)
        path = "C:\learning python\MP3 Player\music\\" + song
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(0.05)

        #code of image song loader in frame
        song = song_box.get(ACTIVE)
        path = "C:\learning python\MP3 Player\music\\" + song
        # print(path)
        metadata = audio_metadata.load(path)
        artwork = metadata.pictures[0].data
        # print(metadata.pictures)
        stream = BytesIO(artwork)
        with open("images\image.png", "wb") as f:
            f.write(stream.read())
        image = Image.open('images\image.png')
        album_img = image.resize((400, 400))
        img = ImageTk.PhotoImage(album_img)
        label.configure(image=img)
        label.image = img
        bar()
    elif play_status==1:
        pygame.mixer.music.unpause()
        play_status=0




def bar():
    if progress['value'] == 400:
        progress.step(-1)

        progress.start(20)
        progress.step(1)


def pause():
    global play_status
    play_status=1

    pygame.mixer.music.pause()

def Next():
    #to get the selected song index
    next_one=song_box.curselection()
    # print(next_one)
    #to get the next song index
    next_one = next_one[0]+1

    song_box.selection_clear(0 , END)
    #activate newsong
    song_box.activate(next_one)
     #set the next song
    song_box.selection_set(next_one)
    play()


def Previous():
    #to get the selected song index
    previous_one=song_box.curselection()
    #to get the previous song index
    previous_one=previous_one[0]-1
    song_box.selection_clear(0,END)
    #activate new song
    song_box.activate(previous_one)
    #set the next song
    song_box.selection_set(previous_one)
    play()


def fav():
    song = song_box.get(ACTIVE)
    favpath = "C:\learning python\MP3 Player\\favourites\\" + song
    fav_list = fav_box.get(0,END)

    if song in fav_list:
        os.remove(favpath)

        delete_index = fav_list.index(song)
        print(delete_index)
        fav_box.delete(delete_index)
    else:
        path = "C:\learning python\MP3 Player\music\\" + song
        shutil.copyfile(path, favpath)
        fav_box.insert(END, song)



#create playlist box

song_box = Listbox(window,fg="black", height=12,width=25)
song_box.grid(row=0,column=1,padx=5)
fav_box = Listbox(window,fg="black", height=12,width=25)
fav_box.grid(row=1,column=1,padx=5)

path = "C:\learning python\MP3 Player\music"
songtracks = os.listdir(path)
for tracks in songtracks:
    song_box.insert(END, tracks)

path = "C:\learning python\MP3 Player\\favourites"
favtracks = os.listdir(path)
for tracks in favtracks:
    fav_box.insert(END, tracks)

frame2= tk.Frame(window,bg="pink",height=400,width=350)
frame3= tk.Frame(window,bg="green",height=400,width=210)

image = Image.open('images\copyright.png')
image = image.resize((212, 400))
image = ImageTk.PhotoImage(image)

label2 = Label(frame3,image=image)
label2.configure(image=image)
label2.image = image
label2.grid(row=0,column=3)

frame2.grid(row=0,column=2 ,padx=5,rowspan=2)
frame3.grid(row=0,column=3,padx=5,rowspan=2)


frame = tk.Frame(window,height=500,width=500,bg='white')
frame.grid(row=2,column=1,columnspan=3,pady=10)

image1 = Image.open('C:\learning python\MP3 Player\images\logo.jpg')
resize_image_logo = image1.resize((400, 400))
logo = ImageTk.PhotoImage(resize_image_logo)
label = Label(frame2,image=logo)
label.image=logo
label.pack()



image1 = Image.open('C:\learning python\MP3 Player\images\play.png')
resize_image1 = image1.resize((50, 50))
img1 = ImageTk.PhotoImage(resize_image1)

image2 = Image.open('C:\learning python\MP3 Player\images\prev.png')
resize_image2 = image2.resize((50, 50))
img2 = ImageTk.PhotoImage(resize_image2)

image3 = Image.open('C:\learning python\MP3 Player\images\\next.png')
resize_image3 = image3.resize((50, 50))
img3 = ImageTk.PhotoImage(resize_image3)

image4 = Image.open('C:\learning python\MP3 Player\images\\fav.png')
resize_image4 = image4.resize((50, 50))
img4 = ImageTk.PhotoImage(resize_image4)

image5 = Image.open('C:\learning python\MP3 Player\images\pause.png')
resize_image5 = image5.resize((55, 55))
img5 = ImageTk.PhotoImage(resize_image5)

prev_b = tk.Button(frame, text="prev",bg="white",height=50,width=50,command=Previous,image=img2,borderwidth=0)
play_b = tk.Button(frame, text="play",bg="white",height=50,width=50,command=play,image=img1,borderwidth=0)
next_b = tk.Button(frame, text="next",bg="white",height=50,width=50,command=Next,image=img3,borderwidth=0)
fav_b = tk.Button(frame, text="fav",bg="white",height=50,width=50,image=img4,borderwidth=0,command=fav)
pause_b = tk.Button(frame, text="pause",bg="white",height=50,width=50,image=img5,borderwidth=0,command=pause)

progress = Progressbar(window, orient="vertical", length=100, mode='determinate')
progress.grid(row=3,column=0,columnspan=3)


def song_volume(val):
    # vol = s1.get()
    volume = int(val)/100
    pygame.mixer.music.set_volume(volume)


s1 = tk.Scale( frame,from_ = 1, to = 100 , orient = "horizontal", cursor="dot", bd=5 , command=song_volume)
s1.set(25)
s1.pack(side="left",padx=20)

prev_b.pack(side="left",pady=10,padx=20)
play_b.pack(side="left",pady=10,padx=20)
pause_b.pack(side="left",pady=10,padx=20)
next_b.pack(side="left",pady=10,padx=20)
fav_b.pack(side="left",pady=10,padx=20)


window.mainloop()
