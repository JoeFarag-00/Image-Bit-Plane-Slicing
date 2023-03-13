from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import os

class BitPlaneSlicing:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1375x860")
        self.root.title("Bit-Plane Slicing")
        self.image_path = None
        
        title = Label(self.root, text="Bit-Plane Slicing", font=('Arial', 30, 'bold'), pady=2, bd=12, bg="#8A8A8A", fg="Black", relief=GROOVE)
        title.pack(fill=X)
        
        self.LoadImg_Frame = LabelFrame(self.root, text="Load Image", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.LoadImg_Frame.place(x=0, y=75, width=625, height=705)
        
        self.Option_Frame = LabelFrame(self.LoadImg_Frame, text="Options", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.Option_Frame.place(x=0, y=570, width=605, height=100)
        
        self.load_button = Button(self.Option_Frame, text="Load Image", command=self.load_image,bg="#13B10F", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        self.load_button.pack(side=LEFT,padx=4)
        
        self.slice_button = Button(self.Option_Frame, text="Slice Image", command=self.slice_image, state=DISABLED, bg="red", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        self.slice_button.pack(side=LEFT, padx=4)
        
        self.reconstruct_button = Button(self.Option_Frame, text="Reconstruct Image", command=self.reconstruct_image, state=DISABLED,  bg="red", bd=2, fg="black", pady=15, width=20, font='arial 13 bold')
        self.reconstruct_button.pack(side=LEFT,padx=4)
        
        self.Generated_Frame = LabelFrame(self.root, text="Output", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.Generated_Frame.place(x=625, y=75, width=750, height=705)
    
        self.plane_checkboxes = []
        self.plane_images = []
        
        self.Bit_Frame = LabelFrame(self.root, text="Choose Bits", font=('arial', 14, 'bold'), bd=10, bg="grey")
        self.Bit_Frame.place(x=0, y=780, relwidth=1, height=80)
        
        for i in range(8):
            select = BooleanVar()
            select.set(True)
            self.plane_checkboxes.append(Checkbutton(self.Bit_Frame, text="Bit {}".format(i), variable=select, bg="grey", fg="black", pady=40, padx=5, width=5))
            self.plane_checkboxes[i].var = select
            self.plane_images.append(Label(self.Generated_Frame))
        
        self.reset = Button(self.Bit_Frame, text="Reset", command=self.ResetWindow,  bg="red", bd=2, fg="black", width=10, font='arial 13 bold')
        self.reset.pack(side=RIGHT,padx=60)
        
        for checkbox in self.plane_checkboxes:
            checkbox.pack(side=LEFT)
        self.reconstruct_button.pack()
    
    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        
        if self.image_path:
            self.Original_image = Image.open(self.image_path).convert("L")
            self.Original_image = self.Original_image.resize((550, 550))
            self.photo = ImageTk.PhotoImage(self.Original_image)
            self.image_display = Label(self.LoadImg_Frame)
            self.image_display.pack()
            self.image_display.config(image=self.photo)
            self.slice_button.config(state=NORMAL)
    
    def slice_image(self):
        self.Bit_List = np.array(self.Original_image)
        self.Bit_Planes_List = []
        self.Bit_Recon_List = []
        for i in range(8):
            self.plane = np.bitwise_and(self.Bit_List, 2**i)
            self.plane = self.plane.astype(np.uint8)
            # print("Plane",i,":\n",self.plane)
            self.Bit_Recon_List.append(self.plane) 
            self.Bit_Planes_List.append(Image.fromarray(self.plane)) 
        
        drive_me = 7
        for i in range(2):
            for c in range(4):
                if self.plane_checkboxes[drive_me].var.get():
                    self.Bit_Planes_List[drive_me] = self.Bit_Planes_List[drive_me].resize((350, 150))
                    photo = ImageTk.PhotoImage(self.Bit_Planes_List[drive_me])
                    self.plane_images[drive_me].config(image=photo)
                    self.plane_images[drive_me].image = photo
                    self.plane_images[drive_me].grid(row = c, column = i , padx = 5, pady=5)
                else:
                    self.plane_images[drive_me].pack_forget()
                drive_me-=1
            self.reconstruct_button.config(state=NORMAL)

    def reconstruct_image(self):
        
        ReConst_List = []
        for i in range(8):
            if self.plane_checkboxes[i].var.get():
                ReConst_List.append(i)
        
        if(len(ReConst_List)>0):       
            shingshong = np.copy(self.Bit_Recon_List[ReConst_List[0]])
            for i in range(1,len(ReConst_List)):
                shingshong+=np.copy(self.Bit_Recon_List[ReConst_List[i]])
            resimg = Image.fromarray(shingshong)
            resimg = resimg.resize((550,550))
            photo = ImageTk.PhotoImage(resimg)
            self.image_display.image = photo
            self.image_display.config(image=photo)
            
        
    
    def ResetWindow(self):
        root.destroy()
        os.system('main.py')

    
if __name__ == "__main__":
    root = Tk()
    app = BitPlaneSlicing(root)
    root.mainloop()
