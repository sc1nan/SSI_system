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
import psutil

ctk.set_appearance_mode('light')
IP_Address: dict = json.load(open("Resources\\network_settings.json"))


class ip_setup(ctk.CTk):
    global IP_Address
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.check_ethernet_port()

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
        
        title_name = "J.Z. Angeles Veterinary Clinic Network Setup"
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

        self.own_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.own_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.own_frame.pack_propagate(0)
        ctk.CTkLabel(self.own_frame, text = 'Computer IP', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.own_address = cctk.ip_entry(self.own_frame, width, height * .15,  font=('DMMono-Medium', 24))
        self.own_address.pack(padx = (width * .004), pady = (width * .005))

        self.reception_ip = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.reception_ip.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.reception_ip.pack_propagate(0)
        ctk.CTkLabel(self.reception_ip, text = 'Reception IP', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.reception_address = cctk.ip_entry(self.reception_ip, width, height * .15,  font=('DMMono-Medium', 24))
        self.reception_address.pack(padx = (width * .004), pady = (width * .005))

        self.cashier_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.cashier_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.cashier_frame.pack_propagate(0)
        ctk.CTkLabel(self.cashier_frame, text = 'Cashier IP', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.cashier_address = cctk.ip_entry(self.cashier_frame, width, height * .15,  font=('DMMono-Medium', 24))
        self.cashier_address.pack(padx = (width * .004), pady = (width * .005))
        
        self.admin_frame = ctk.CTkFrame(self, height = height * .15, corner_radius= 2)
        self.admin_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.admin_frame.pack_propagate(0)
        ctk.CTkLabel(self.admin_frame, text = 'Admin IP', font=('DMMono-Medium', 24)).pack(padx = (width * .005), anchor = 'w')
        self.admin_address = cctk.ip_entry(self.admin_frame, width, height * .15,  font=('DMMono-Medium', 24))
        self.admin_address.pack(padx = (width * .004), pady = (width * .005))

        self.set_as_local_frame = ctk.CTkFrame(self, height = height * .07, corner_radius= 2)
        self.set_as_local_frame.pack(padx = (height * .01), pady = (height * .01, 0), fill = 'x')
        self.set_as_local_frame.pack_propagate(0)
        self.default_settings = ctk.CTkCheckBox(self.set_as_local_frame, text='Use localhost', command= self.set_default)
        self.default_settings.pack(anchor = 'w', padx = (width * .02), pady = (width * .005))

        self.btn = ctk.CTkButton(self, width * .4, height * .1, text='Set IP', font=('DMMono-Medium', 24), command= self.set_ips)
        self.btn.pack(pady = (height * .15, 0))
        self.set_save()

    def set_save(self):
        self.own_address.setIP(IP_Address['MY_NETWORK_IP'])
        self.reception_address.setIP(IP_Address['RECEPTIONIST_IP'])
        self.cashier_address.setIP(IP_Address['CASHIER_IP'])
        self.admin_address.setIP(IP_Address['ADMIN_IP'])

    def set_default(self):
        if self.default_settings.get() == 1:
            self.own_address.setIP('127.0.0.1')
            self.reception_address.setIP('127.0.0.1')
            self.cashier_address.setIP('127.0.0.1')
            self.admin_address.setIP('127.0.0.1')
            self.own_address.configure(state = 'readonly')
            self.reception_address.configure(state = 'readonly')
            self.cashier_address.configure(state = 'readonly')
            self.admin_address.configure(state = 'readonly')
        else:
            self.own_address.configure(state = ctk.NORMAL)
            self.reception_address.configure(state = ctk.NORMAL)
            self.cashier_address.configure(state = ctk.NORMAL)
            self.admin_address.configure(state = ctk.NORMAL)
            self.set_save()

    def set_ips(self):
        self.modify_json('MY_NETWORK_IP', self.own_address.getIP())
        self.modify_json('RECEPTIONIST_IP', self.reception_address.getIP())
        self.modify_json('CASHIER_IP', self.cashier_address.getIP())
        self.modify_json('ADMIN_IP', self.admin_address.getIP())

        messagebox.showinfo("Success", "IP Change, proceed to login\nIf there's an error, proceed to DB settings", parent = self)
        self.destroy()
    
    def modify_json(self, key, new_value):
        try:
            with open('Resources\\network_settings.json', 'r') as file:
                data = json.load(file)

            data[key] = new_value

            with open('Resources\\network_settings.json', 'w') as file:
                json.dump(data, file, indent=2) 
        finally:
             pass
        
    def check_ethernet_port(self):
        ethernet_prescence: bool = False
        interfaces = psutil.net_if_addrs()

        for interface, t in interfaces.items():
            if 'ethernet' in interface.lower():
                ethernet_prescence = True
            print(interface, t[0].family, t[0].address)

        if not ethernet_prescence:
            messagebox.showerror("Unable to proceed", "Your ethernet port is disabled\n(System will not work for networks)\ngo to network settings and enable it", parent = self)

if __name__ == '__main__':
    app = ip_setup()
    app.mainloop()