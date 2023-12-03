from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import messagebox
from tkextrafont import Font
from PIL import Image
from tkinter import _tkinter
from Theme import Color, Icons
import re, os, json
from typing import *
from customcustomtkinter import customcustomtkinterutil as cctku
from customcustomtkinter import customcustomtkinter as cctk

ctk.set_appearance_mode('light')
IP_Address: dict = json.load(open("Resources\\network_settings.json"))
DB_SETTINGS: dict = json.load(open("Resources\\db_settings.json"))


class ip_setup(ctk.CTk):
    global IP_Address, DB_SETTINGS
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        try:
            #Transitioning to new font style
            Font(file="Font/DMSans-Bold.ttf")
            Font(file="Font/DMSans-Medium.ttf")
            Font(file='Font/DMSans-Regular.ttf')

            #Use DM Mono for numbers
            Font(file="Font/DMMono-Light.ttf")
            Font(file="Font/DMMono-Medium.ttf")
            Font(file="Font/DMMono-Regular.ttf")

        except _tkinter.TclError:
            pass
        
        title_name = "J.Z. Angeles Veterinary Clinic Database Setup"
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        
        width = 400
        height = 500
        #os_x = width/2 - root_w/2
        #pos_y = height/2 - root_h/2

        self.title(title_name)
        self.geometry(f'{width}x{height}')

        #self.admin_ip = cctk.ip_entry(self, root_w * .95, root_h * .1, font=('DMMono-Medium', 24))
        #self.admin_ip.pack()

        self.db_name_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.db_name_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.db_name_frame.pack_propagate(0)
        ctk.CTkLabel(self.db_name_frame, text = 'Database Name', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.db_name = ctk.CTkEntry(self.db_name_frame, width, height * .15,  font=('DMMono-Medium', 24))
        self.db_name.pack(padx = (width * .004), pady = (width * .005))

        self.user_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.user_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.user_frame.pack_propagate(0)
        ctk.CTkLabel(self.user_frame, text = 'User', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.db_user = ctk.CTkEntry(self.user_frame, width, height * .15,  font=('DMMono-Medium', 24))
        self.db_user.pack(padx = (width * .004), pady = (width * .005))

        self.password_frame = ctk.CTkFrame(self, height = height * .23, corner_radius= 2)
        self.password_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.password_frame.pack_propagate(0)
        ctk.CTkLabel(self.password_frame, text = 'Password', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.db_password = ctk.CTkEntry(self.password_frame, width, height * .1,  font=('DMMono-Medium', 24), show = '●')
        self.db_password.pack(padx = (width * .004), pady = (width * .005))
        self.show_pass = ctk.CTkCheckBox(self.password_frame, text='Show password')
        cmd = lambda: self.db_password.configure(show = ('●' if self.show_pass.get() == 0 else ''))
        self.show_pass.configure(command = cmd)
        self.show_pass.pack(padx = (width * .004), pady = (0, width * .005), anchor = 'w')

        self.port_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.port_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.port_frame.pack_propagate(0)
        ctk.CTkLabel(self.port_frame, text = 'Port No.', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.db_port = cctk.num_entry(self.port_frame, width, height * .15,  font=('DMMono-Medium', 24), max_val= 65535)
        self.db_port.pack(padx = (width * .004), pady = (width * .005))

        self.btn = ctk.CTkButton(self, width * .4, height * .1, text='Set Profile', font=('DMMono-Medium', 24), command= self.save)
        self.btn.pack(pady = (height * .15, 0))
        self.set_save()

    def set_save(self):
        self.db_name.delete(0, ctk.END)
        self.db_user.delete(0, ctk.END)
        self.db_password.delete(0, ctk.END)
        self.db_port.delete(0, ctk.END)

        self.db_name.insert(0, DB_SETTINGS['database'])
        self.db_user.insert(0, DB_SETTINGS['user'])
        self.db_password.insert(0, DB_SETTINGS['password'])
        self.db_port.insert(0, DB_SETTINGS['port_no'])

    def save(self):
        if self.db_name.get() == "" or self.db_password.get() == "" or self.db_port.get() == "" or self.db_user.get() == "":
            messagebox.showerror("Unable to proceed", 'fill all the entries', parent = self)
            return
        try:
            data = {
                        "database": self.db_name.get(),
                        "user": self.db_user.get(),
                        "password": self.db_password.get(),
                        "port_no": int(self.db_port.get())
                    }

            with open('Resources\\db_settings.json', 'w') as file:
                json.dump(data, file, indent=2)
        finally:
            messagebox.showinfo("Success", "Database profile change, proceed to login\nIf there's an error, proceed to Network setup", parent = self)
            self.destroy()
             

if __name__ == '__main__':
    app = ip_setup()
    app.mainloop()