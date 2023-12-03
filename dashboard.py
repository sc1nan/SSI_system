import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import datetime;
import _tkinter
import sql_commands
import numpy as np
from popup import notif_popup_entities as ntf
from tkinter import messagebox
from util import *
from functools import partial
from tkextrafont import Font
from Theme import Color, Icons
from PIL import Image
from datetime import date
from customcustomtkinter import customcustomtkinter as cctk
from customcustomtkinter import customcustomtkinterutil as cctku
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import db
from constants import action
from popup import Inventory_popup, Pet_info_popup, service_popup, transaction_popups, Sales_popup, dashboard_popup, save_as_popup, service_popup, admin_popup, customer_popup, customer_popup, mini_popup
from math import *
import random
import calendar
import acc_creation
import network_socket_util as nsu
import json

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

width = 0
height = 0
acc_info = ()
acc_cred = ()
date_logged = None
mainframes = []
IP_Address: dict = json.load(open("Resources\\network_settings.json"))
PORT_NO: dict = json.load(open("Resources\\port_no.json"))
SETTINGS_VAL : dict = json.load(open("Resources\\general_settings.json"))

ctk.set_widget_scaling(1)
ctk.set_window_scaling(1)

class dashboard(ctk.CTkToplevel):
    def __init__(self, master:ctk.CTk, entry_key: str, _date_logged: datetime):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self._master = master
        self.notifs: List[cctk.ctkButtonFrame] = []
        #self.attributes("-topmost",1)
        self._fg_color=Color.White_Platinum
        
        is_loading = 1
        rand = random.randint(1,2)
        
        #[print(screen) for screen in screeninfo.get_monitors()]
        '''Global Variables'''
        global width, height, mainframes, IP_Address, SETTINGS_VAL, PORT_NO
        width = self.winfo_screenwidth() #/ scaling
        height = self.winfo_screenheight() #/ scaling
            
        title_name = "J.Z. Angeles Veterinary Clinic"
        
        '''Fonts'''
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
        #for testing purposes, might delete after the development
        
        '''Loading Screen'''
        self.bg_img = ctk.CTkImage(light_image=Image.open("image/bg.png"),size=(1920,1080))
        gif_file = "image/cat_smaller.gif" if rand == 1 else "image/dog_smaller.gif"
        frame_count = 12
        self.pet_frames = [tk.PhotoImage(file=gif_file, format= 'gif -index %i' %(i)) for i in range(frame_count)]
        
        self.loading_frame = ctk.CTkFrame(self, fg_color=Color.Blue_Cobalt, corner_radius=0)
        self.loading_frame.place(relx =0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
        
        def update_frame(index):
            if is_loading:
                frame = self.pet_frames[index]
                index += 1
                if index == frame_count:
                    index = 0
                #print(index)
                self.cat.configure(image=frame)
                self.progress_bar.step()
                self.after(100, update_frame, index)
        
        self.content_frame = ctk.CTkFrame(self.loading_frame, fg_color="transparent")
        self.content_frame.place(relx =0.5, rely=0.5, anchor='center')
        
        ctk.CTkLabel(self.loading_frame, text='', image=Icons.get_image("python_icon", size=(50,50))).place(relx=0.995, rely=0.995, anchor='se')
        ctk.CTkLabel(self.content_frame, text=title_name, fg_color='transparent',font=("DM Sans Bold", height*0.04, 'bold'), text_color=Color.White_Lotion,).pack(pady=(height*0.05,0))
        ctk.CTkLabel(self.content_frame, text="Sales and Services System", fg_color='transparent', font=("DM Sans Medium", height*0.035), text_color=Color.White_Lotion,).pack(pady=(height*0.02,height*0.075))
        
        self.message_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.35, height=height*0.125)
        self.message_frame.pack()
        self.message_frame.grid_propagate(0)
        self.message_frame.grid_rowconfigure(0, weight=1)
        self.message_frame.grid_columnconfigure(0, weight=1)
        
        self.cat = ctk.CTkLabel(self.message_frame, text="",)
        self.cat.grid(row=0,column=0, sticky="nsew")
        
        self.loading_message = ctk.CTkLabel(self.message_frame, text="Starting...", font=("DM Sans Medium", height*0.0225), text_color=Color.White_Lotion, padx=(width*0.05))
        self.loading_message.grid(row=1,column=0, sticky='sew', padx=(10))
        
        self.progress_bar = ctk.CTkProgressBar(self.content_frame, orientation="horizontal", width=width*0.35, height=height*0.0285, border_width=3, corner_radius=10,
                                              fg_color=Color.White_Lotion, progress_color=Color.Blue_LapisLazuli_1, border_color=Color.White_Lotion,
                                              mode="indeterminate", indeterminate_speed=3)
        self.progress_bar.pack()
        self.progress_bar.set(0)
        determinate_speed = self.progress_bar._current_width/11.85
        self.progress_bar.configure(determinate_speed = determinate_speed)
        update_frame(0)
        
        global acc_info, acc_cred, date_logged, mainframes, IP_Address, PORT_NO

        """ 
        datakey = database.fetch_data(f'SELECT {db.USERNAME} from {db.ACC_CRED} where {db.acc_cred.ENTRY_OTP} = ?', (entry_key, ))
        if not datakey or entry_key == None:
            messagebox.showwarning('Warning', 'Invalid entry method\ngo to log in instead')
            self.destroy()
            return
        else:
            global acc_info, date_logged, acc_cred, mainframes
            date_logged = _date_logged
            acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (datakey[0][0], ))
            acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (datakey[0][0], ))
            database.exec_nonquery([[f'UPDATE {db.ACC_CRED} SET {db.acc_cred.ENTRY_OTP} = NULL WHERE {db.USERNAME} = ?', (datakey[0][0], )]])
            del datakey
        #for preventing security breach through python code; enable it to test it """
        #for preventing security breach through python code; enable it to test it """
        
        acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (entry_key, ))
        acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (entry_key, ))
        date_logged = _date_logged;
        #temporary for free access; disable it when testing the security breach prevention or deleting it if deploying the system

        '''Import Images'''
        self.inv_logo = ctk.CTkImage(light_image=Image.open("image/logo1.png"),size=(37,35))
        self.dashboard_icon = Icons.get_image('dashboard_icon',size=(22,22))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(26,20))
        self.inventory_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"),size=(24,25))
        self.patient_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(22,25))
        self.payment_icon  = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(25,25))
        self.report_icon = ctk.CTkImage(light_image=Image.open("image/report.png"),size=(22,22))
        self.notif_icon = ctk.CTkImage(light_image=Image.open("image/notif.png"),size=(22,25))
        self.settings_icon = Icons.get_image('settings_icon', size=(30,30))
        self.acc_icon = ctk.CTkImage(light_image=Image.open("image/acc.png"),size=(40,40))
        self.transact_icon = ctk.CTkImage(light_image=Image.open("image/transact.png"),size=(22,20))
        self.services_icon = ctk.CTkImage(light_image=Image.open("image/services.png"),size=(24,26))
        self.user_setting_icon = ctk.CTkImage(light_image=Image.open("image/usersetting.png"),size=(24,27))
        self.histlog_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"),size=(22,25))
        self.admin_icon = ctk.CTkImage(light_image=Image.open("image/admin.png"), size=(27,27))
        self.reception_icon = Icons.get_image('reception_icon', size=(30,30))
        self.payment_icon = Icons.get_image('payment_icon', size=(30,30))
        self.customer_icon = Icons.get_image('customers_logo', size=(30,30))
        '''Main Information'''
        side_frame_w = round(width * 0.175)
        self.default_menubar_width = .15
        default_menubar_height = .25
        acc_menubar_width = .2

        unselected_btn_color = Color.Blue_Yale
        selected_btn_color = Color.Blue_Steel

        #self.main_frames = [dashboard_frame(self), transaction_frame(self), services_frame(self), sales_frame(self), inventory_frame(self), patient_info_frame(self), reports_frame(self), user_setting_frame(self), histlog_frame(self)]
        temp_labels = ['Dashboard', 'Reception', 'Payment', 'Customers', 'Services', 'Sales', 'Inventory', 'Pet Information', 'Reports', 'User Settings', 'Settings', 'History']
        temp_icons = [self.dashboard_icon,  self.reception_icon, self.payment_icon,  self.customer_icon, self.services_icon, self.sales_icon, self.inventory_icon, self.patient_icon, self.report_icon, self.user_setting_icon, self.settings_icon, self.histlog_icon]
        temp_main_frames = [dashboard_frame, reception_frame, payment_frame, customer_frame, services_frame, sales_frame, inventory_frame, patient_info_frame, reports_frame, user_setting_frame,  admin_settings_frame, histlog_frame]

        temp_user_lvl_access = list(database.fetch_data('Select * from account_access_level WHERE usn = ?', (acc_info[0][0], ))[0][1:])
        self.labels = []
        self.icons = []
        self.main_frames:list = []
        for i in range(len(temp_main_frames)):
            if temp_user_lvl_access[i]:
                self.icons.append(temp_icons[i])
                self.labels.append(temp_labels[i])
                self.loading_message.configure(text=f"Loading {temp_labels[i]}...")
                self.main_frames.append(temp_main_frames[i](self))
            
        del temp_main_frames, temp_user_lvl_access, temp_labels, temp_icons
        
        self.loading_message.configure(text="Done")
        is_loading = 0
        
        self.active_win = None
        mainframes = self.main_frames
        self.active_main_frame = None

        '''setting the user level access'''
        '''user_level_access = database.fetch_data(sql_commands.get_level_acessess, (acc_info[0][2], ))[0]
        if(not user_level_access[1]):
            temp:inventory_frame = self.main_frames[4]
            temp.add_item_btn.destroy()
            del temp'''

        '''events'''
        def load_main_frame(title: str, cur_frame: int):
            self.title_label.configure(text= title.upper())
            if self.active_main_frame is not None:
                self.active_main_frame.grid_forget()
            self.active_main_frame = self.main_frames[cur_frame]
            self.active_main_frame.grid(row =1, column =1, sticky = 'nsew')
        
        
                
        self.grid_rowconfigure(1,weight=1)
        self.side_frame = ctk.CTkFrame(self, height= height, width = side_frame_w,
                                       fg_color=Color.Blue_Yale, border_color=None, corner_radius=0)
        self.side_frame.grid(rowspan=2,row = 0, column=0)
        self.side_frame.pack_propagate(False)

        '''Python Logo'''
        
        ctk.CTkLabel(self.side_frame, text='', image=Icons.get_image("python_logo", (30,30)), height=height*0.055, width=height*0.055, corner_radius=5 ).place(relx=0.025, rely=0.995, anchor='sw')
    
        '''Company Logo'''
        self.logo_frame = ctk.CTkFrame(self.side_frame, height=round(height * 0.1), width=side_frame_w,
                                       fg_color="transparent",corner_radius=0)
        self.logo_frame.pack(pady=(round(height * 0.02),round(height * 0.03)))

        self.logo_icon = ctk.CTkLabel(self.logo_frame, text="", image=self.inv_logo)
        self.logo_icon.pack(side="left",padx=(0,10))

        self.logo_label = ctk.CTkLabel(self.logo_frame, text=title_name, font=("DM Sans Medium", 16),
                                       text_color=Color.Grey_Bright, wraplength=150, justify='left')
        self.logo_label.pack(side="right",padx=(5,0))
        
        '''side buttons'''
        self.side_frame_btn: List[cctk.ctkButtonFrame] = []
        for i in range(len(self.main_frames)):
            self.side_frame_btn.append(cctk.ctkButtonFrame(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                                           fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                                           corner_radius=0, cursor="hand2",))
            self.side_frame_btn[i].configure(command=partial(load_main_frame, self.labels[i], i))
            self.side_frame_btn[i].pack()
            wbar = ctk.CTkLabel(self.side_frame_btn[i],text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
            wbar.pack(side="left")
            icon = ctk.CTkLabel(self.side_frame_btn[i],image=self.icons[i], text="")
            icon.pack(side="left", padx=(width * 0.016,width * 0.01))
            label = ctk.CTkLabel(self.side_frame_btn[i], text= self.labels[i], font=("DM Sans Medium", 16), text_color=Color.Grey_Bright,)
            label.pack(side="left")
            self.side_frame_btn[i].pack()
            self.side_frame_btn[i].update_children()

        self.sidebar_btn_mngr = cctku.button_manager(self.side_frame_btn, selected_btn_color, False, 0)
        self.sidebar_btn_mngr._state = (lambda: self.sidebar_btn_mngr.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.sidebar_btn_mngr.active.winfo_children()[0].configure(fg_color=Color.White_Ghost))
        self.sidebar_btn_mngr.click(self.sidebar_btn_mngr._default_active, None)

        '''Top Frame'''
        user_icon = {"Owner":"Owner", "Assisstant":"Assisstant","Cashier":"Cashier","Receiptionist":"Receiptionist",}
        print(user_icon.get(acc_info[0][2]) or user_icon.get("Receiptionist"))
        self.top_frame = ctk.CTkFrame(self, height=round(height * 0.1), width=round(width* 0.825),
                                      corner_radius=0,fg_color=Color.White_Lotion)
        self.top_frame.grid(row=0, column=1, sticky="nsew")
        self.top_frame.grid_propagate(False)

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.top_frame, text="", font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht)
        self.title_label.grid(row = 0, column=0,sticky='w', padx= width * 0.02)

        self.notif_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()*0.5), text= "", image= Icons.get_image('notif_none_icon', (35,32)),
                                              fg_color=Color.White_Lotion, height= round(self.top_frame.winfo_reqheight() *0.5), border_width=0, corner_radius=5,
                                              font=("DM Sans Medium", 16),hover_color=Color.White_Gray,)
        self.notif_btn.grid(row=0, column= 1, sticky='w')

        self.acc_btn = cctk.ctkButtonFrame(self.top_frame, width=round(self.top_frame.winfo_reqwidth() * .12),
                                           height=round(self.top_frame.winfo_reqheight()*.5), corner_radius=5,
                                           fg_color=Color.White_Gray,
                                           hover_color= Color.White_Platinum, cursor="hand2")

        self.acc_btn.grid(row=0, column=3, sticky='e', padx=(0,width*0.005))
        self.acc_btn.grid_rowconfigure((0,1), weight=1)
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=Icons.admin_user_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew', pady = (0,2), padx = (round(height * .005), 0))
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][1]).upper(), font=("DM Sans Bold", 14,), text_color=Color.Blue_Maastricht)
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .0025), 0), pady = (0))
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][2]).upper(), font=("DM Sans Medium", 12), text_color=Color.Blue_Maastricht)
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .0025), 0), pady = 0)
        self.acc_btn.update_children()
        self.update()

        '''menubars'''
        self.notif_menu_bar= cctk.scrollable_menubar(self, width * self.default_menubar_width * 1.5, height * .9,
                                          corner_radius= 0, fg_color=Color.White_Gray, border_width= 0, border_color=Color.Blue_Cobalt,
                                          position=(1 - self.default_menubar_width * 1.5 / 2 - .003, .55, 'c'))
        
        
        self.acc_menu_bar = cctk.menubar(self, width * acc_menubar_width, height * default_menubar_height, fg_color=Color.White_Ghost,
                                         corner_radius=0, border_width= 1, border_color=Color.White_Platinum,
                                         position= (1 - acc_menubar_width/2, self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,'c'))
        
        self.acc_menu_bar.grid_columnconfigure((0,1), weight=1)
        self.acc_menu_bar.grid_rowconfigure((3), weight = 1)
        
        ctk.CTkLabel(self.acc_menu_bar,font=("DM Sans Medium", 16), text="Name: ", width=width*0.015, fg_color="transparent").grid(row=0, column=0, sticky="nse", padx=(width*0.01,0), pady=(width*0.015,width*0.005))
        self.acc_name  = ctk.CTkLabel(self.acc_menu_bar, font=("DM Sans Medium", 16), text=acc_info[0][1], fg_color="transparent", anchor='w')
        self.acc_name.grid(row=0, column=1,sticky='nsw', padx=(0, width*0.005), pady=(width*0.015,width*0.005))   
        
        ctk.CTkLabel(self.acc_menu_bar,font=("DM Sans Medium", 16), text="Username: ", width=width*0.015, fg_color="transparent").grid(row=1, column=0, sticky="nse", padx=(width*0.01,0), pady=(0))
        self.usn_name  = ctk.CTkLabel(self.acc_menu_bar, font=("DM Sans Medium", 16), text=acc_info[0][0], fg_color="transparent", anchor='w')
        self.usn_name.grid(row=1, column=1,sticky='nsw', padx=(0, width*0.005), pady=(0))
        
        ctk.CTkLabel(self.acc_menu_bar,font=("DM Sans Medium", 16), text="Position: ", width=width*0.015, fg_color="transparent").grid(row=2, column=0, sticky="nse", padx=(width*0.01,0), pady=(width*0.005))
        self.pos_name  = ctk.CTkLabel(self.acc_menu_bar, font=("DM Sans Medium", 16), text=acc_info[0][2], fg_color="transparent", anchor='w')
        self.pos_name.grid(row=2, column=1,sticky='nsw', padx=(0, width*0.005), pady=(width*0.005))
        
        self.logout_btn = ctk.CTkButton(self.acc_menu_bar, width * acc_menubar_width * .85, height * default_menubar_height * .2, text = 'Logout', command= self.log_out, font=("DM Sans Medium", 14))
        self.logout_btn.grid(row=3, column=0, columnspan=2)

        self.top_frame_button_mngr = cctku.button_manager([self.notif_btn, self.acc_btn], Color.Platinum, True,
                                                          children=[self.notif_menu_bar, self.acc_menu_bar], active_double_click_nullified= False)

        '''setting default events'''
        load_main_frame('Dashboard', 0)
        self.loading_frame.place_forget()

        self.network_receiver = nsu.network_receiver(IP_Address['MY_NETWORK_IP'], PORT_NO['Notif_gen'], self.receiver_callback)
        self.network_receiver.start_receiving()
        self.generate_notification()
        self.protocol("WM_DELETE_WINDOW", self.log_out)
        self.mainloop()
    
    def generate_notification(self):
        '''ALL OF THE COMMENTED NTF_C VARIABLE PUT A NOTIFICATION IN INSTANCE RATHER THAN GROUP'''

        out_of_stock = [s[0] for s in database.fetch_data(sql_commands.get_out_of_stock_names)]
        ntf_c1 = [('Out of stock', f'{len(out_of_stock)} Item{"s are " if len(out_of_stock) > 1 else " is "} currently out of stock', out_of_stock)] if out_of_stock else []#  #for _ in out_of_stock]
        #ntf_c1 = [('Out sf stock', f'Item {s} is currently out of stock') for s in out_of_stock]
        
        low_stock = database.fetch_data(sql_commands.get_low_items_name)
        ntf_c2 = [('Item low stock', f'{len(low_stock)} Item{"s are" if len(low_stock) > 1 else " is"} currently low stock', low_stock)] if low_stock else []#for _ in low_stock]
        #ntf_c2 = [('Item low stock', f'Item {s[0]} is currently low stock with only {s[1]} left') for s in low_stock]

        near_expire = database.fetch_data(sql_commands.get_near_expired_items_name, (SETTINGS_VAL['Near_expiry_date_alert'], ))
        #ntf_c3 = [('About to Expire', f'Item {s[0]} is about to expire in {s[2]} day{"s" if s[2] > 1 else ""}') for s in near_expire]
        ntf_c3 = [('About to Expire', f'{len(near_expire)} Item{"s are" if len(near_expire) > 1 else " is" } about to expire', near_expire)] if near_expire else [] #for _ in near_expire]

        expired = database.fetch_data(sql_commands.get_expired_items_name)
        #ntf_c4 = [('Expired stock', f'Item {s[0]} had {s[1]} expired item{"s" if s[1] > 1 else ""}') for s in low_stock]
        ntf_c4 = [('Expired stock', f'{len(expired)} Item{"s are" if len(low_stock) > 1 else " is"} expired', expired)] if expired else []# for _ in expired]

        near_shceduled = database.fetch_data(sql_commands.get_near_scheduled_clients_names, (SETTINGS_VAL['Appointment_Alert'], SETTINGS_VAL['Appointment_Alert']))
        ntf_c5 = [('Near scheduled', f'{str(s[1]).capitalize()} is scheduled in {s[2]} day{"s" if s[2] > 1 else ""} for {s[0]}', [s]) for s in near_shceduled] if near_shceduled else []

        scheduled_today = database.fetch_data(sql_commands.get_scheduled_clients_today_names)
        ntf_c6 = [('Scheduled Today', f'{str(s[1]).capitalize()} is scheduled today for {s[0]}', [s]) for s in scheduled_today]

        past_scheduled = database.fetch_data(sql_commands.get_past_scheduled_clients_names)
        #ntf_c8 = [('Schedule Overdue', f'{str(s[1]).capitalize()} is overdue for {s[0]}') for s in past_scheduled]
        
        ntf_c7 = [('Schedule Overdue', f'{len(past_scheduled)} {"patients" if len(past_scheduled) > 1 else "patient"} overdue for an appointment', past_scheduled)] if past_scheduled else [] #for _ in past_scheduled]
        #this removes the shedule overdue when there is no overdue record, weird when it notifies 0
        
        #ntf_c8 = [('Schedule Overdue', f'{str(s[1]).capitalize()} is overdue for {s[0]}') for s in past_scheduled]
        
        ntf_c7 = [('Schedule Overdue', f'{len(past_scheduled)} {"patients" if len(past_scheduled) > 1 else "patient"} overdue for an appointment', past_scheduled)] if past_scheduled else [] #for _ in past_scheduled]
        #this removes the shedule overdue when there is no overdue record, weird when it notifies 0
        
        ntf_c = ntf_c5 + ntf_c6 + ntf_c7 + ntf_c1 + ntf_c2 + ntf_c3 + ntf_c4
        self.notif_btn.configure(image=Icons.get_image("notif_none_icon", (35,35))) if not ntf_c else self.notif_btn.configure(image=Icons.get_image("notif_alarm_icon", (35,35)))
        for _ntf in self.notifs:
            _ntf.destroy()

        self.notifs = [ntf.create_entity(self.notif_menu_bar, s[0], s[1],  width * self.default_menubar_width * 1.5 * .95, 100, Desc_lines= 3, info_cnt = (self, width, height, s[2])) for s in ntf_c]
        
    def receiver_callback(self, m):
        if m == '1':
            self.generate_notification()

    def popup_command(self,info):
        print(info)

    def log_out(self):
        b = messagebox.askyesno('Log out', 'Are you sure you want to log out?', parent = self)
        if b:
            database.exec_nonquery([[f'UPDATE {db.LOG_HIST} SET {db.log_hist.TIME_OUT} = ? WHERE {db.log_hist.DATE_LOGGED} = ? AND {db.log_hist.TIME_IN} = ?',
                                    (datetime.datetime.now().time(), date_logged.date(), date_logged.time().strftime("%H:%M:%S"))]])
            self._master.deiconify()
            self.destroy()

''' 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶 🐱 🐶'''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''main frames'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class dashboard_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        def open_sale_history(_):
            if self.sales_data_treeview.get_selected_data():
                self.sales_history.place(relx=0.5, rely=0.5, anchor="c", sales_info=self.sales_data_treeview.get_selected_data())

        def open_schedule(_):
            if self.sched_data_treeview.get_selected_data():
                self.sched_info.place(relx=0.5, rely=0.5, anchor='c', sched_info=self.sched_data_treeview.get_selected_data())
        
        self.grid_columnconfigure((0,1),weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_propagate(1)
        
        self.state = None
        self.receiving_entity = nsu.network_receiver(IP_Address["MY_NETWORK_IP"], PORT_NO['DashB_stat_ref'], self.update_receiver)
        self.canvas = None
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]

        self.date_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, corner_radius= 5,)
        self.date_frame.grid(row=0, column=1, padx = (width*0.005), pady= (width*0.005), sticky='e')
        self.date_label = ctk.CTkLabel(self.date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14))
        self.date_label.pack(anchor='c', padx = width * .015, pady = height * .01)

        '''Income summary frame'''
        self.income_summary_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Lotion, corner_radius=5)
        self.income_summary_frame.grid(row=1, column=0, padx=(width*0.005),sticky="nsew")
        self.income_summary_frame.grid_propagate(0)

        self.income_frame_width, self.income_frame_height = self.income_summary_frame.cget('width'), self.income_summary_frame.cget("height")

        '''Income summary frame contents'''
        self.income_summary_frame.grid_columnconfigure((0), weight=1)
        self.income_summary_frame.grid_rowconfigure((2,3,4), weight=1)
        self.income_summary_label = ctk.CTkLabel(self.income_summary_frame,text="Daily Income Summary",fg_color="transparent", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht,)
        self.income_summary_label.grid(row=0, column=0, sticky="ew", pady=(self.income_frame_height*0.04,0))
        self.income_summary_sub = ctk.CTkLabel(self.income_summary_frame,text=f"as of {date.today().strftime('%B %d, %Y')}", font=("DM Sans Medium", 14), text_color=Color.Grey_Davy)
        self.income_summary_sub.grid(row=1, column=0, sticky="ew")

        self.num_transactions = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.num_transactions.grid(row=2, column=0, sticky="nsew", padx=(self.income_frame_width*0.03,0), pady=(self.income_frame_height*0.05, self.income_frame_height*.015),)
        self.num_transactions.pack_propagate(0)
        ctk.CTkLabel(self.num_transactions, text="Transactions Today:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.transaction_today_count = ctk.CTkLabel(self.num_transactions, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.transaction_today_count.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Light_Green, corner_radius=5)
        self.items_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(self.income_frame_width*0.03,0), pady=(self.income_frame_height*0.015, self.income_frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.items_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Blue_Cornflower, corner_radius=5)
        self.services_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(self.income_frame_width*0.03,0),pady=( self.income_frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.services_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.15, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=5, column=0, sticky="nsew", padx=(self.income_frame_width*0.03,0),pady=(self.income_frame_height*.015, self.income_frame_height*.05))
        self.total_sales_frame.pack_propagate(0)
        ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.total_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        #Watermelon Pie
        '''Inventory Stat Frame'''
        self.inventory_stat_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.inventory_stat_frame.grid_propagate(0)
        self.inventory_stat_frame.grid(row=1, column=1, padx= (0,width*0.005), sticky='nsew')
        self.inventory_stat_frame.grid_columnconfigure(0, weight=1)
        self.inventory_stat_frame.grid_rowconfigure(1, weight=1)

        self.inventory_frame_width, self.inventory_frame_height = self.inventory_stat_frame.cget('width'), self.inventory_stat_frame.cget('height')

        #region Iventory Status
        sell_data, item_data = selling_concat_unit(database.fetch_data(sql_commands.get_selling_rate)), item_concat_unit(database.fetch_data(sql_commands.get_inventory_by_group))
        temp = [tuple(rate[0]) + (item[0], item[1], item[2]) for item in item_data for rate in sell_data  if rate[-1] == item[1]]
        self.fast = [data[1:] for data in list_filterer(reference=temp, source=['🠉'])]
        self.slow = [data[1:] for data in list_filterer(reference=temp, source=['🠋'])]
        self.order = database.fetch_data(sql_commands.get_on_order_items)
        self.partial = database.fetch_data(sql_commands.get_on_pending_items)
        self.safe = database.fetch_data(sql_commands.get_safe_state) 
        self.expired = database.fetch_data(sql_commands.get_expired_state)
        self.near_expired = database.fetch_data(sql_commands.get_near_expire_state)
        self.out_stock =  database.fetch_data(sql_commands.get_out_of_stock_state)
        self.critical =  database.fetch_data(sql_commands.get_critical_state)
        self.reorder =  database.fetch_data(sql_commands.get_reorder_state)
        
        self.inventory_stat_label = ctk.CTkLabel(self.inventory_stat_frame, text="Inventory Status", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht)
        self.inventory_stat_label.grid(row=0, column=0, sticky="w", padx=(self.inventory_frame_width*0.03,0),pady=(self.inventory_frame_height*0.045,self.inventory_frame_height*0.02))
        
        self.inventory_content_frame = ctk.CTkFrame(self.inventory_stat_frame, fg_color="transparent", corner_radius=0)
        self.inventory_content_frame.grid_propagate(0)
        self.inventory_content_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.inventory_content_frame.grid(row=1, column=0, sticky="nsew", padx=width*0.01, pady=(0,width*0.005))
        
        self.fast_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width/2,
                                                        fg_color=Color.Fast_Color, hover_color=Color.Hover_Fast_Color, display_warning=False, indicator_space=0,
                                                        text="Fast", icon_color='transparent', icon=Icons.fast_moving_icon, display_count=0,
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', processing=0,
                                                        data=self.fast, title="Fast Moving Items", color=Color.Fast_Color, count=len(self.fast)))
        self.fast_button.grid(row=0, column=0, columnspan=1, sticky="nsew", pady=(0, width*0.005), padx=(0, width*0.005))
        
        self.slow_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width/2,
                                                        fg_color=Color.Slow_Color, hover_color=Color.Hover_Slow_Color, display_warning=False, indicator_space=0,
                                                        text="Slow", icon_color='transparent', icon=Icons.slow_moving_icon, display_count=0,
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', processing=0,
                                                                                                   data=self.slow, title="Slow Moving Items", color=Color.Slow_Color, count=len(self.slow)))
        self.slow_button.grid(row=0, column=1, columnspan=1, sticky="nsew", pady=(0, width*0.005), padx=(0, width*0.005))
        
        self.on_order_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width/2,
                                                        fg_color=Color.On_Order_Color, hover_color=Color.Hover_On_Order, display_warning=False, indicator_space=0,
                                                        text="On Order", count=len(self.order), icon_color='transparent',
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', processing=0,
                                                                                                   data=self.order, title="On Order", color=Color.Slow_Color, count=len(self.order)))#window=self.show_status_popup, data=self.safe )
        self.on_order_button.grid(row=0, column=2, columnspan=1, sticky="nsew", pady=(0, width*0.005), padx=(0, width*0.005))
        
        self.partial_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width/2,
                                                        fg_color=Color.On_Partial_Color, hover_color=Color.Hover_On_Partial, display_warning=False, indicator_space=0,
                                                        text="Partial", count=len(self.partial), icon_color='transparent',
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', processing=0,
                                                                                                   data=self.partial, title="Partial Orders", color=Color.Slow_Color, count=len(self.partial)))
        self.partial_button.grid(row=0, column=3, columnspan=1, sticky="nsew", pady=(0, width*0.005), padx=(0))
        
        self.safety_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width,
                                                        fg_color=Color.Safe_color, hover_color=Color.Hover_Safe_color, display_warning=False,
                                                        text="Safe/Normal", count=len(self.safe), icon_color='transparent',
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.safe, title="Safe/Normal Level Items", color=Color.Safe_color, count=len(self.safe)))# window=self.show_status_popup, data=self.safe )
        self.safety_button.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, width*0.005), padx=(0, width*0.005))
        
        self.near_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width, 
                                                        fg_color=Color.Near_Expire_Color, hover_color=Color.Hover_Near_Expire_Color,
                                                        text="Near Expire", count=len(self.near_expired), icon_color=Color.Red_Pastel,
                                                        command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.near_expired, title="Near Expire Items", color=Color.Near_Expire_Color, count=len(self.near_expired)))
        self.near_button.grid(row=1, column=2, columnspan=2, pady=(0, width*0.005), sticky='nsew')
        
        self.reorder_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width,
                                                         fg_color=Color.Reorder_Color, hover_color=Color.Hover_Reorder_Color,
                                                        text="Reorder", count=len(self.reorder), icon_color=Color.Red_Pastel,
                                                         command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.reorder, title="Reorder Level Items", color=Color.Reorder_Color, count=len(self.reorder))) 
        self.reorder_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(0, width*0.005), pady=(0, width*0.005))
        
        self.expire_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width, 
                                                        fg_color=Color.Expire_Color, hover_color=Color.Hover_Expire_Color,
                                                        text="Expired", count=len(self.expired), icon_color=Color.Red_Pastel,
                                                         command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.expired, title="Expired Items", color=Color.Expire_Color, count=len(self.expired)))
        self.expire_button.grid(row=2, column=2, columnspan=2, sticky='nsew', pady=(0, width*0.005) )
        
        self.critical_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width,
                                                            fg_color=Color.Critical_Color, hover_color=Color.Hover_Critical_Color,
                                                        text="Critical", count=len(self.critical), icon_color=Color.Red_Pastel,
                                                         command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.critical, title="Critical Level Items", color=Color.Critical_Color, count=len(self.critical)))
        self.critical_button.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(0, width*0.005),pady=(0))
        
        self.out_stock_button = dashboard_popup.status_bar(self.inventory_content_frame, info=(), height=height*0.0725, width=self.inventory_content_frame._current_width,
                                                            fg_color=Color.Out_Stock_Color, hover_color=Color.Hover_Out_Stock_Color,
                                                        text="Out of Stock", count=len(self.out_stock), icon_color=Color.Red_Pastel,
                                                         command = lambda : self.status_popup.place(relx = .5, rely = .5, anchor = 'c', 
                                                                                                   data=self.out_stock, title="Out-of-Stock Items", color=Color.Out_Stock_Color, count=len(self.out_stock)))
        self.out_stock_button.grid(row=3, column=2, columnspan=2, sticky="nsew", pady=(0))
        
        
        self.inventory_tabs = [self.safety_button, self.reorder_button, self.critical_button, self.out_stock_button, self.near_button, self.expire_button]
        #endregion
        '''Sales History'''
        self.sales_history_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sales_history_frame.grid(row=2, column=0, padx= ((width*0.005)), pady=( width*0.005), sticky='nsew')
        self.sales_history_frame.grid_propagate(0)
        self.sales_history_frame.grid_columnconfigure(1,weight=1)
        self.sales_history_frame.grid_rowconfigure(1,weight=1)

        ctk.CTkLabel(self.sales_history_frame, text=f"Sales History", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht).grid(row=0, column=0, padx=(width*0.015,0), pady=(height*0.015, height*0.01))
        ctk.CTkLabel(self.sales_history_frame, text=f"as of {date.today().strftime('%B %Y')}", text_color="grey", font=("DM Sans Medium",14)).grid(row=0, column=1, sticky="sw", padx=(width*0.005,0), pady=(0,height*0.01))
        self.sales_data_frame = ctk.CTkFrame(self.sales_history_frame, fg_color="transparent", corner_radius=0)
        self.sales_data_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",pady=(0))

        self.sales_data_treeview = cctk.cctkTreeView(self.sales_data_frame, width=width*0.39, height=height*0.45,
                                                     column_format=f'/No:{int(width*.0325)}-#r/Day:x-tc/Total:{int(width*0.125)}-tr!30!30', 
                                                     double_click_command=open_sale_history)
        self.sales_data_treeview.pack()
        
        self.no_sales_data = ctk.CTkLabel(self.sales_data_treeview, text="No sales data yet to show.", font=("DM Sans Medium", 14))
        
        self.total_frame = ctk.CTkFrame(self.sales_history_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.225)
        self.total_frame.grid(row=2, column=1, sticky="nse", padx=width*0.01, pady=(height*0.005,height*0.015))
        self.total_frame.pack_propagate(0)
        ctk.CTkLabel(self.total_frame, text=f"Monthly Total: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side=ctk.LEFT, padx=(width*0.01))
        self.current_total = ctk.CTkLabel(self.total_frame, text="0,000.00", font=("DM Sans Medium", 14))
        self.current_total.pack(side=ctk.RIGHT, padx=(width*0.01))

        '''Schedule Appointments'''
        self.sched_client_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sched_client_frame.grid(row=2, column=1, padx= (0, width*0.005), pady=( width*0.005),sticky='nsew')
        self.sched_client_frame.grid_propagate(0)
        self.sched_client_frame.grid_columnconfigure(1,weight=1)
        self.sched_client_frame.grid_rowconfigure(1,weight=1)

        ctk.CTkLabel(self.sched_client_frame, text="Scheduled Clients Today", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht).grid(row=0, column=0, padx=(width*0.015,0), pady=(height*0.015, height*0.01))
        self.sched_data_frame = ctk.CTkFrame(self.sched_client_frame,fg_color="transparent", corner_radius=0)
        self.sched_data_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",pady=(0,width*0.01))

        self.sched_data_treeview = cctk.cctkTreeView(self.sched_data_frame, width=width*0.39, height=height*0.45, 
                                               column_format=f'/No:{int(width*.03)}-#r/ClientName:x-tl/Contact:{int(width*.125)}-tc!30!30',
                                               double_click_command = open_schedule)
        self.sched_data_treeview.pack()
        
        self.no_sched_data = ctk.CTkLabel(self.sched_data_treeview, text="No schedule data yet to show.", font=("DM Sans Medium", 14))

        self.status_popup = Inventory_popup.show_status(self, (width, height, acc_cred, acc_info))
        self.generate_DISumarry()
        self.load_saled_data_treeview()
        self.load_scheduled_service()
        self.grid_forget()
        
        self.sales_history = dashboard_popup.sales_history_popup(self, (width, height))
        self.sched_info = dashboard_popup.sched_info_popup(self, (width, height), source='dashboard')
        self.receiving_entity.start_receiving()
    
    def test_self(self):
        print(self.selector_test.get())
        
    def load_scheduled_service(self):
        data= database.fetch_data(sql_commands.get_scheduled_clients_today, None)
        self.sched_data_treeview.update_table(data)
        
        self.no_sched_data.place_forget() if len(data) != 0 else self.no_sched_data.place(relx=0.5, rely=0.5, anchor='c')

    def load_saled_data_treeview(self):
        date = datetime.datetime.now()
        data = database.fetch_data(sql_commands.get_monthly_sales_data, (date.month, date.year))
        total = sum([price_format_to_float(s[-1][1:]) for s in data])
        self.current_total.configure(text = '₱ ' + format_price(total))
        self.sales_data_treeview.update_table(data)
        self.no_sales_data.place_forget() if len(data) != 0 else self.no_sales_data.place(relx=0.5, rely=0.5, anchor='c')

    #def show_status_popup(self, name: str, data):
            #self.status_popup.status_label.configure(text = name)
            #self.status_popup.update_treeview(data)
    #        self.status_popup.place(relx = .5, rely = .5, anchor = 'c')

    def show_pie(self, data: list = None):
        if(self.canvas is not None):
            self.canvas.get_tk_widget().destroy()
        data = [self.data[0], self.data[1]] if self.data[0] + self.data[1] > 0 else [1, 0]
        
        pie_figure= Figure(figsize=(width*0.003,width*0.00285), dpi=100)
        pie_figure.set_facecolor(Color.White_Lotion)
        ax =pie_figure.add_subplot(111)
        ax.pie(data, autopct=f"{'%0.2f%%'if self.data[0] + self.data[1] > 0 else ''}", 
               startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Light_Green, Color.Blue_Cornflower] if self.data[0] + self.data[1] > 0 else [Color.White_Platinum],
                textprops={'fontsize':17, 'color': Color.White_Lotion, 'family':'monospace', 'weight':'bold' },)
        pie_figure.subplots_adjust(top=1,left=0,right=1.1, bottom=0)

        self.canvas = FigureCanvasTkAgg(pie_figure, self.income_summary_frame, )
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 6, sticky='e')

        self.no_data = ctk.CTkLabel(self.income_summary_frame,text='No transactions yet.', font=("DM Sans Medium", 14), fg_color=Color.White_Platinum)
        self.no_data.grid_forget() if self.data[0] + self.data[1] > 0 else self.no_data.grid(row = 0, column=1, rowspan = 6)

    def generate_DISumarry(self):
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0),
                    int(database.fetch_data(sql_commands.get_todays_transaction_count)[0][0] or 0)]
        self.items_sales_value.configure(text = f'₱{format_price(self.data[0])}')
        self.services_sales_value.configure(text = f'₱{format_price(self.data[1])}')
        self.total_sales_value.configure(text = f'₱{format_price(self.data[0] + self.data[1])}')
        self.transaction_today_count.configure(text = self.data[2])
        self.show_pie()

    def generate_stat_tabs(self):
        data= [database.fetch_data(sql_commands.get_safe_state),database.fetch_data(sql_commands.get_expired_state), database.fetch_data(sql_commands.get_near_expire_state),
               database.fetch_data(sql_commands.get_out_of_stock_state), database.fetch_data(sql_commands.get_critical_state),
               database.fetch_data(sql_commands.get_reorder_state),]
        #self.inventory_tabs = [self.safety_button, self.reorder_button, self.critical_button, self.out_stock_button, self.near_button, self.expire_button]
        
        [self.inventory_tabs[tabs].update_data(len(data[tabs]), data[tabs]) for tabs in range(len(self.inventory_tabs))] 

    def grid(self, **kwargs):
        self.load_scheduled_service()
        self.load_saled_data_treeview()
        self.generate_DISumarry()

        return super().grid(**kwargs)
    
    def grid_forget(self, **kwargs):
        #if self.state: [tabs.update_state('closed') for tabs in self.inventory_tabs]
        return super().grid_forget(**kwargs)

    def update_receiver(self, _):
        self.show_pie()
        self.generate_stat_tabs()
        self.generate_DISumarry()
        self.load_saled_data_treeview()
        self.load_scheduled_service()
        #minor issue: makes a lot of exception due to conflict between ui drawing engine and destroy
            
        for i in mainframes:
            if isinstance(i, reports_frame):
                temp: reports_frame = i
                temp.graphs_need_upgrade()
                temp.update_invetory_graph()
            if isinstance(i, sales_frame):
                temp: sales_frame = i
                temp.update_table()
            if isinstance(i, histlog_frame):
                temp: histlog_frame = i
                #temp.load_both()     

class reception_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master,corner_radius=0, fg_color=Color.White_Platinum)
        global width, height, acc_cred, acc_info, mainframes, IP_Address, SETTINGS_VAL
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.loaded = [False, False]

        self.sender_entity = nsu.network_sender(IP_Address["CASHIER_IP"], PORT_NO['Billing_Recieving'], IP_Address["MY_NETWORK_IP"], 252, self.post_sent_callback)
        selected_color = Color.Blue_Yale

        self.trash_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(20,20))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
        self.service_icon = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(20,20))
        self.item_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(20,20))
        self.cal_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(20,20))
        self.proceed_icon = ctk.CTkImage(light_image=Image.open("image/rightarrow.png"), size=(15,15))
        self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
        self.payment_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(22,16))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))

        '''INVOICE FRAME: START'''
        self.invoice_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.invoice_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.invoice_frame.grid_rowconfigure((1), weight=1)
        self.invoice_frame.grid_columnconfigure(0, weight=1)
        
        '''TOP FRAME'''
        self.top_con_frame = ctk.CTkFrame(self.invoice_frame,fg_color="transparent")
        self.top_con_frame.grid(row=0, column=0,sticky="new", padx=(width*0.005), pady=(height*0.01, 0))
        #invoice search button
        self.search_frame = ctk.CTkFrame(self.top_con_frame, width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.pack(side="left")
        self.search_frame.pack_propagate(0)
        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005,)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        
        self.add_item_btn = ctk.CTkButton(self.top_con_frame,width=width*0.1, height = height*0.05, text="Create Transaction ",image=self.add_icon, font=("DM Sans Medium", 14))
        self.add_item_btn.configure(command=lambda:self.show_invoice.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_item_btn.pack(side="left", padx=(width*0.005))

        self.view_schedule_btn = ctk.CTkButton(self.top_con_frame, width= width * .1, height = height*0.05, text="View Schedules",image=Icons.schedule_icon, font=("DM Sans Medium", 14),
                                               command = lambda: self.scheduled_services_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.view_schedule_btn.pack(side="left", padx=(0, width*0.005))

        self.refresh_btn = ctk.CTkButton(self.top_con_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command = lambda:self.update_invoice_treeview(True))
        self.refresh_btn.pack(side="left", padx=(0,width*0.005))
    
        self.cancel_invoice_btn = ctk.CTkButton(self.top_con_frame,text="Cancel Reception", width=width*0.065, height = height*0.05, font=("DM Sans Medium", 14), fg_color= '#ff6464', command = self.cancel_invoice)
        self.cancel_invoice_btn.pack(side="right")

        '''TAB NAV'''
        #region
        self.tab_frame = ctk.CTkFrame(self.invoice_frame, fg_color="transparent")
        self.tab_frame.grid(row=0, column=0, sticky="new" ,padx=(0), pady=(0))
        self.tab_frame.grid_columnconfigure((2,3), weight=1)
        ctk.CTkFrame(self.tab_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=6, sticky="nsew")

        self.item_tab = cctk.ctkButtonFrame(self.tab_frame, cursor="hand2", height=height*0.065, width=width*0.125,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.item_tab.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.item_tab.configure(command = lambda: self.load_tab(0))
        self.account_tab_icon = ctk.CTkLabel(self.item_tab, text="",image=Icons.get_image("inventory_icon", (24,25)))
        self.account_tab_icon.pack(side="left", padx=(width*0.01,width*0.0025))
        self.accounts_label = ctk.CTkLabel(self.item_tab, text="ITEMS QUEUE", text_color="white",font=('DM Sans Medium', 14))
        self.accounts_label.pack(side="left")
        self.item_tab.grid()
        self.item_tab.update_children()

        self.scheduling_tab = cctk.ctkButtonFrame(self.tab_frame, cursor="hand2", height=height*0.065, width=width*0.135,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.scheduling_tab.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.scheduling_tab.configure(command = lambda: self.load_tab(1))
        self.account_tab_icon = ctk.CTkLabel(self.scheduling_tab, text="",image=Icons.get_image("services_icon", (24,25)))
        self.account_tab_icon.pack(side="left", padx=(width*0.01,width*0.0035))
        self.accounts_label = ctk.CTkLabel(self.scheduling_tab, text="SERVICES QUEUE", text_color="white",font=('DM Sans Medium', 14))
        self.accounts_label.pack(side="left")
        self.scheduling_tab.grid()
        self.scheduling_tab.update_children()

        self.tab_mng = cctku.button_manager([self.item_tab, self.scheduling_tab], selected_color, False, 0)
        self.tab_mng.click(0)
        #endregion

        self.content_frame = ctk.CTkFrame(self.invoice_frame, fg_color=Color.White_Lotion, corner_radius=0)
        self.content_frame.grid(row=1, column=0, sticky='nsew')
        self.content_frame.grid_columnconfigure(0, weight=1)
        #self.content_frame.grid_rowconfigure()
        
        '''TOP FRAME'''
        self.top_con_frame = ctk.CTkFrame(self.tab_frame,fg_color="transparent")
        self.top_con_frame.grid(row=0, column= 3,sticky="nsew", padx=(0), pady=(0))
        
        self.add_item_btn = ctk.CTkButton(self.top_con_frame,width=width*0.1, height = height*0.055, text="Create Transaction ",image=self.add_icon, font=("DM Sans Medium", 14))
        self.add_item_btn.configure(command=lambda:self.show_invoice.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_item_btn.pack(side="left", padx=(width*0.005))

        self.view_schedule_btn = ctk.CTkButton(self.top_con_frame, width= width * .1, height = height*0.055, text="View Schedules",image=Icons.schedule_icon, font=("DM Sans Medium", 14),
                                               command = lambda: self.scheduled_services_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.view_schedule_btn.pack(side="left", padx=(0, width*0.005))

        self.refresh_btn = ctk.CTkButton(self.top_con_frame,text="", width=width*0.025, height = height*0.055, image=self.refresh_icon, fg_color="#83BD75", command = lambda:self.update_invoice_treeview(True))
        self.refresh_btn.pack(side="left", padx=(0,width*0.005))
    
        self.cancel_invoice_btn = ctk.CTkButton(self.top_con_frame,text="Cancel Reception", width=width*0.065, height = height*0.055, font=("DM Sans Medium", 14), fg_color= '#ff6464', command = self.cancel_invoice)
        self.cancel_invoice_btn.pack(side="right")
        
        
        '''INVOICE FRAME ITEMS'''
        self.item_treeview_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, corner_radius=0)
        self.item_treeview_frame.grid(row=0, column=0, sticky="nsew",padx=(0), pady=(width*0.005))

        self.item_invoice_treeview = cctk.cctkTreeView(self.item_treeview_frame, width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ReceptionID:{int(width*.115)}-tc/ClientName:x-tl/Total:{int(width*.1)}-tr/Date:{int(width*.15)}-tc!33!35',
                                           double_click_command= self.load_invoice_content)
        self.active = self.item_invoice_treeview
        self.item_invoice_treeview.pack()

        self.proceeed_button = ctk.CTkButton(self.item_treeview_frame, text="Proceed to Payment", image=self.proceed_icon, height=height*0.05, width=width*0.145,font=("DM Sans Medium", 14),
                                             compound="right", command = self.proceed_to_payment)
        self.proceeed_button.pack(side='right', padx=(width*0.005), pady=(width*0.005))
        
        '''INVOICE FRAME ITEMS: END'''
        
        '''SCHEDULING FRAME'''
        self.scheduling_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, corner_radius=0)
        self.scheduling_frame.columnconfigure(0, weight = 1)

        self.scheduling_invoice_treeview = cctk.cctkTreeView(self.scheduling_frame, width= width * .805, height=height * .725, corner_radius=0,
                                                             column_format=f'/No:{int(width*.035)}-#r/ReceptionID:{int(width*.115)}-tc/Owner:x-tl/Pet:x-tl/Service:{int(width*.15)}-tl/Total:{int(width*.085)}-tr/Date:{int(width*.125)}-tc!33!35',)                                                             #column_format=f'/No:{int(width*.025)}-#r/ReceptionID:{int(width*.115)}-tc/Per:x-tl/Services:x-tl/Date:{int(width*.1)}-tc!30!30')
        self.scheduling_invoice_treeview.pack()

        self.selection_svc_pro_frame = ctk.CTkFrame(self.scheduling_frame, fg_color = 'transparent', height= 0.005)
        self.selection_svc_pro_frame.pack(side = 'right', padx=(width*0.005), pady=(width*0.005))

        self.proceeed_button = ctk.CTkButton(self.selection_svc_pro_frame, text="Proceed to Payment", image=self.proceed_icon, height=height*0.05, width=width*0.145,font=("DM Sans Medium", 14),
                                             compound="right", command = self.proceed_to_payment)
        self.proceeed_button.pack(side = 'right', padx=(0, width*0.005))

        self.selection = ctk.CTkOptionMenu(self.selection_svc_pro_frame, height=height*0.05, width=width*0.17,font=("DM Sans Medium", 14),)
        self.selection.set("Select Service Provider")
        self.selection.pack(side = 'right', padx=(0, width*0.005))

        '''SCHEDULING FRAME: END'''
        
        self.show_invoice:ctk.CTkFrame = transaction_popups.add_invoice(self,(width, height), lambda: self.update_invoice_treeview(True), acc_cred[0][0])
        self.scheduled_services_popup: ctk.CTkFrame = transaction_popups.scheduled_services(self, (width, height), self)
        self.update_invoice_treeview()
        self.grid_forget()

    def load_tab(self, i: int = None):
        self.selection.configure(values = [s[-1] for s in database.fetch_data(sql_commands.select_specific_provider, ("Service Provider", ))])
        if i == 0:
            #self.service_treeview_frame.grid_forget()
            self.scheduling_frame.grid_forget()
            self.active = self.item_invoice_treeview
            self.item_treeview_frame.grid(row=0, column=0, sticky="nsew",padx=(0), pady=(width*0.005))
        elif i == 1:
            #self.service_treeview_frame.grid_forget()
            self.item_treeview_frame.grid_forget()
            self.active = self.scheduling_invoice_treeview
            self.scheduling_frame.grid(row=0, column=0, sticky="nsew",padx=(0), pady=(width*0.005))
        self.update_invoice_treeview()

    def post_sent_callback(self, i):
        if i == 1:
            self.active.remove_selected_data()
            messagebox.showinfo("Succeed", 'Transaction record preceeded to payment', parent = self)
        else:
            messagebox.showerror("Error", "An error occured", parent = self)

    def update_invoice_treeview(self, force_load = False):
        self.refresh_btn.configure(state = ctk.DISABLED)
        if force_load:
            self.loaded = [False, False]

        if self.active is None:
            self.active = self.item_invoice_treeview

        index = 0 if self.active == self.item_invoice_treeview else 1 
        if not self.loaded[index]:
            if index == 0:
                self.active.update_table(database.fetch_data(sql_commands.get_invoice_info, (index, )))
                # load the item content treeview
            elif index == 1:
                self.scheduling_invoice_treeview.delete_all_data()
                preceeded_services = database.fetch_data(sql_commands.get_preceeded_services)
                queued_services = database.fetch_data(sql_commands.get_invoice_info_queued, (index, ))
                
                self.scheduling_invoice_treeview._record_text_color = ('White', 'Black')
                for i in range(len(preceeded_services)):
                    self.scheduling_invoice_treeview.add_data(preceeded_services[i])
                    self.scheduling_invoice_treeview.data_frames[-1].configure(og_color = Color.Blue_Yale if i % 2 == 0 else brighten_color(Color.Blue_Yale, .9))
                self.scheduling_invoice_treeview._record_text_color = ('Black', 'White')
                
                for li in queued_services:
                    self.scheduling_invoice_treeview.add_data(li)

                self.active.data_grid_btn_mng.update_buttons()
    
            self.loaded[index] = True
        self.refresh_btn.after(100, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
        

    def cancel_invoice(self, bypass_confirmation: bool = False):
        if self.active.get_selected_data() is None:
            messagebox.showwarning("Fail to proceed", "Select an transaction record to cancel", parent = self)
            return
        if bypass_confirmation:
            database.exec_nonquery([[sql_commands.cancel_invoice, (self.invoice_treeview.get_selected_data()[0], )]])
            self.update_invoice_treeview(True)
        else:
            if(messagebox.askyesno("Cancel Transaction", "Are you really want to cancel this transaction", parent = self)) and self.active != self.scheduling_invoice_treeview:
                database.exec_nonquery([[sql_commands.cancel_invoice, (self.active.get_selected_data()[0], )]])
                #self.update_invoice_treeview(True)
                self.active.remove_selected_data()
                self.active.data_grid_btn_mng.update_buttons()
    
    def load_invoice_content(self, _:any = None):
        if (self.active == self.item_invoice_treeview) and self.active.get_selected_data() is not None:
            transaction_popups.show_invoice_content(self, (width, height)).place(relx = .5, rely = .5, anchor = 'c', invoice_id= self.active.get_selected_data()[0])

    def proceed_to_payment(self):
        data = self.active.get_selected_data()
        if(data):
            if self.selection.get() == "Select Service Provider" and self.active == self.scheduling_invoice_treeview:
                messagebox.showerror("Unable to Proceed", "Select a provider to proceed", parent = self)
                return
            if 'TR# ' not in data[0]:
                #stock_quan = [s[0] for s in database.fetch_data(sql_commands.check_if_stock_can_accomodate, (data[0], ))]
                items_uid_in_invoice = database.fetch_data(sql_commands.check_quan_of_invoice, (data[0], ))
                items_about_to_pay = database.fetch_data(sql_commands.check_quan_of_paying_item)
                current_stock = database.fetch_data(sql_commands.check_feasible_items)
                current_stock = {s[0]: s[1] for s in current_stock}

                for li in items_about_to_pay:
                    if li[0] in current_stock:
                        current_stock[li[0]] = current_stock[li[0]] - li[1]

                can_accomodate = True
                for li in items_uid_in_invoice:
                    if li[1] > current_stock[li[0]]:
                        can_accomodate = False
                        break 
                if can_accomodate:
                    if self.active == self.scheduling_invoice_treeview:
                        if not database.exec_nonquery([[sql_commands.set_provider_to_invoice, (self.selection.get(), self.active.get_selected_data()[0])]]):
                            messagebox.showwarning("Fail to proceed", "Unable to Proceed", parent = self)
                            return
                        database.exec_nonquery([[sql_commands.set_provider_to_invoice, (self.selection.get(), self.active.get_selected_data()[0])]])
                    self.sender_entity.send(data[0])
                else:
                    messagebox.showwarning("Fail to proceed", "Current stock cannot accomodate the transaction", parent = self)
            else:
                if database.exec_nonquery([[sql_commands.mark_preceeding_as_done, (data[0][4:], datetime.datetime.strptime(data[-1], '%B %d, %Y'))]]):
                    messagebox.showinfo("Success", "Service mark as done", parent = self)
                    self.scheduling_invoice_treeview.remove_selected_data()
        else:
            messagebox.showwarning("Fail to proceed", "Select an transaction record before\nheading into the payment", parent = self)

class payment_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        global width, height, acc_cred, acc_info, mainframes, IP_Address, PORT_NO

        '''PAYMENT FRAME: START'''
        self.trash_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(20,20))
        #self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
        #self.service_icon = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(20,20))
        #self.item_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(20,20))
        self.cal_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(20,20))
        self.proceed_icon = ctk.CTkImage(light_image=Image.open("image/rightarrow.png"), size=(15,15))
        self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
        self.payment_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(22,16))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))
        
        self.content_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion)
        self.content_frame.grid(row=0, column=0, sticky='nsew', padx=(width*0.005), pady=(height*0.01))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.upper_frame = ctk.CTkFrame(self.content_frame, height = height*0.05, fg_color = 'transparent')
        self.upper_frame.grid(row = 0, column = 0, sticky = 'nsew', columnspan = 4)
    
        """ self.search_frame = ctk.CTkFrame(self.upper_frame,width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        #self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack(side = ctk.LEFT, padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005, command = self.search_callback)
        self.search_btn.pack(side="left", padx=(0, width*0.0025)) """

        self.refresh_btn = ctk.CTkButton(self.upper_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command = self.update_payment_treeview)
        self.refresh_btn.pack(side = ctk.LEFT, padx=(width*0.005), pady=(height*0.01))
        #self.refresh_btn.grid(row=0, column=1, sticky="w", padx=(0, width*0.0025))

        self.additional_option = ctk.CTkButton(self.upper_frame, width=width*0.05, height = height*0.05, text= "Edit Items", font= ("DM Sans Medium", 16), command = self.add_item_command, image= self.edit_icon)
        self.additional_option.pack(side = ctk.LEFT, padx=(0, width*0.005), pady=(height*0.01))
        #self.additional_option.grid(row=0, column=2, sticky="w", padx=(0, width*0.0025))

        self.void_billing = ctk.CTkButton(self.upper_frame, width=width*0.05, height = height*0.05, text= "Void Transaction", font= ("DM Sans Medium", 16), anchor = ctk.RIGHT, fg_color = '#ff6464', command = self.invoice_callback)
        self.void_billing.pack(side = ctk.RIGHT, padx=(0, width*0.005), pady=(height*0.01))
        #self.void_billing.grid(row=0, column=5, sticky="ew", padx=(0, width*0.0025))
       
        self.payment_treeview_frame = ctk.CTkFrame(self.content_frame)
        self.payment_treeview_frame.grid(row=1, column=0, columnspan=4, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

        self.payment_treeview = cctk.cctkTreeView(self.payment_treeview_frame, width= width * 0.805, height= height *.745, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ReceptionID:{int(width*.115)}-tc/ClientName:x-tl/Services:{int(width*.1)}-tr/Items:{int(width*.1)}-tr/Total:{int(width*.09)}-tr!33!35',)
        self.update_payment_treeview()
        self.payment_treeview.pack()

        self.proceeed_button = ctk.CTkButton(self.content_frame, text="Proceed", image=self.proceed_icon, height=height*0.05, width=width*0.135,font=("DM San Medium", 14), compound="right")
        self.proceeed_button.configure(command= self.proceed_to_pay)
        self.proceeed_button.grid(row=2, column=3, pady=(0,height*0.01),padx=(0, width*0.005), sticky="e")
        self.show_payment_proceed = transaction_popups.show_payment_proceed(self,(width, height), self.reset)

        self.receiving_entity = nsu.network_receiver(IP_Address["MY_NETWORK_IP"], PORT_NO['Billing_Recieving'], self.received_callback)
        self.receiving_entity.start_receiving()

        def void_invoice():
            record_action(acc_cred[0][0], action.INVOICE_TYPE, action.VOID_INVOICE % (acc_cred[0][0], self.void_authorization.user_name_authorized_by, self.payment_treeview.get_selected_data()[0]))
            database.exec_nonquery([[sql_commands.void_invoice, (self.payment_treeview.get_selected_data()[0], )]])
            self.update_payment_treeview()
        self.void_authorization = mini_popup.authorization(self, (width, height), void_invoice)

        self.grid_forget()

    def invoice_callback(self):
        data = self.payment_treeview.get_selected_data()
        if data is None:
            messagebox.showwarning("Fail to proceed", "Select a reception record before\nheading into the payment", parent = self)
            return
        if price_format_to_float(data[2][1:]) != 0:
            messagebox.showwarning("Fail to proceed", "You cannot void a transaction\nwith an availed service/s", parent = self)
            return
        else:
            self.void_authorization.place(relx = .5, rely = .5, anchor = 'c')
        
    def void_callback(self):
        pass
        #need to fix

    def search_callback(self):
        if self.search_entry.get() == "":
            self.payment_treeview.update_table(self.treeview_og_data)
        else:
            searched = [s for s in self.treeview_og_data if self.search_entry.get() in s[0]]
            self.payment_treeview.update_table(searched)

    def received_callback(self, m):
        database.exec_nonquery([[sql_commands.set_invoice_transaction_to_payment, (m, )]])
        data = database.fetch_data(sql_commands.get_specific_payment_invoice_info, (m, ))[0]
        self.payment_treeview.add_data(data, True)
    
    def add_item_command(self):
        if not self.payment_treeview.get_selected_data():
            messagebox.showwarning("Fail to proceed", "Select a reception record before\nheading into the payment", parent = self)
            return 
        uid = self.payment_treeview.get_selected_data()[0]
        transaction_popups.additional_option_invoice(self, (width, height), acc_cred[0][0], uid, self.update_payment_treeview).place(relx = .5, rely = .5, anchor = 'c')
        
    def update_payment_treeview(self):
        self.refresh_btn.configure(state = ctk.DISABLED)
        self.payment_treeview.update_table(database.fetch_data(sql_commands.get_payment_invoice_info))
        self.treeview_og_data = self.payment_treeview._data
        self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))

    def proceed_to_pay(self):
        data = self.payment_treeview.get_selected_data()
        if(data):
            self.show_payment_proceed.place(invoice_data= data, cashier= acc_cred[0][0], treeview_callback= self.update_payment_treeview,
                                            relx = .5, rely = .5, anchor = 'c')
        else:
            messagebox.showwarning("Fail to proceed", "Select a reception record before heading into the payment", parent = self)

    def reset(self):
        for i in mainframes:
            if isinstance(i, dashboard_frame):
                temp: dashboard_frame = i
                temp.show_pie()
                temp.generate_stat_tabs()
                temp.generate_DISumarry()
                temp.load_saled_data_treeview()
                temp.load_scheduled_service()
            if isinstance(i, reports_frame):
                temp: reports_frame = i
                temp.graphs_need_upgrade()
                temp.update_invetory_graph()
            if isinstance(i, sales_frame):
                temp: sales_frame = i
                temp.update_table()
            if isinstance(i, histlog_frame):
                temp: histlog_frame = i
                #temp.load_both()

class customer_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO, SETTINGS_VAL
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()

        def serach_callback():
            temp = database.fetch_data(sql_commands.get_customers_information, (SETTINGS_VAL['Regular_order_count'] , SETTINGS_VAL['Regular_order_count']))
            self.customer_treeview.pack_forget()
            self.customer_treeview.update_table(list_filterer(source=self.search_bar.get(), reference=temp))
            self.customer_treeview.pack()
        
        def open_record():
            if self.customer_treeview.get_selected_data():
                self.view_customer_popup.place(relx=0.5, rely=0.5, anchor='c', info =self.customer_treeview.get_selected_data())
            else:
                messagebox.showwarning("Warning", "No record selected. Select a record first.", parent = self)

        def drp_callback(var):
            if 'Regular' == var:
                temp = database.fetch_data(sql_commands.get_customer_record_regular, (SETTINGS_VAL['Regular_order_count'] , SETTINGS_VAL['Regular_order_count']))
      
            elif 'Non-Regular' == var:
                temp = database.fetch_data(sql_commands.get_customer_record_non_regular, (SETTINGS_VAL['Regular_order_count'] , SETTINGS_VAL['Regular_order_count']))
    
            elif 'All' == var:
                temp =database.fetch_data(sql_commands.get_customers_information, (SETTINGS_VAL['Regular_order_count'] , SETTINGS_VAL['Regular_order_count']))
      
            self.no_data_label.place(relx=0.5, rely=0.5, anchor='c') if not temp else self.no_data_label.place_forget()
            self.customer_treeview.pack_forget()
            self.customer_treeview.update_table(temp)
            self.customer_treeview.pack()
                
        #region Top Frame
        self.view_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(25,25))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, sticky="ns", padx=width*0.005,pady=height*0.01)

        self.top_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.055, corner_radius=0, bg_color=Color.White_Lotion,)
        self.top_frame.grid(row=0, column=0 , sticky="nw",padx=width*0.005,pady=(height*0.01,0))

        self.refresh_btn = ctk.CTkButton(self.top_frame, text="", width=height*0.05, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command= self.refresh_treeview)
        self.refresh_btn.grid(row=0, column=1, padx=(0, width*0.005), pady=(height*0.01,0))

        self.add_customer = ctk.CTkButton(self.top_frame, text="Add Record", image=self.add_icon, font=("DM Sans Medium", 14), width=width*0.1,height = height*0.05,
                                          command = lambda: self.add_customer_popup.place(relx = .5, rely = .5, anchor = 'c',))
        self.add_customer.grid(row=0, column=2, padx=(0, width*0.005), pady=(height*0.01,0))

        self.view_record_btn = ctk.CTkButton(self.top_frame, text="View Record", image=self.view_icon, font=("DM Sans Medium", 14), width=width*0.1,height = height*0.05,
                                             command=open_record)
        self.view_record_btn.grid(row=0, column=3, padx=(0, width*0.005), pady=(height*0.01,0))
        
        self.sub_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0, width*0.005))
        self.sub_frame.grid_rowconfigure(1, weight=1)
        self.sub_frame.grid_columnconfigure(1, weight=1)
        #endregion
        self.optional_frame = ctk.CTkFrame(self.sub_frame, fg_color='transparent', corner_radius=0)
        self.optional_frame.pack(fill='both', expand=1, padx=(width*0.005), pady=(width*0.005))     
        
        self.sort_frame = ctk.CTkFrame(self.optional_frame,  height = height*0.05, fg_color=Color.Platinum)
        self.sort_frame.grid(row=0, column=5, padx=(0), pady=(0), sticky="nse")
        self.sort_frame.grid_rowconfigure(0, weight=1)
        self.sort_frame.grid_columnconfigure((1,2), weight=1)

        ctk.CTkLabel(self.sort_frame, text='Type: ', font=("DM Sans Medium", 12),).grid(row=0, column=0, padx=(width*0.01,0), pady=(height*0.0065), sticky="nsew")
        self.sort_type_option= ctk.CTkOptionMenu(self.sort_frame, values=['All','Regular', 'Non-Regular'], anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, dropdown_font=("DM Sans Medium", 14), command=drp_callback)
        self.sort_type_option.grid(row=0, column=1, padx=(width*0.005), pady=(height*0.0065), sticky="nsew")
    
        self.customer_table_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum, corner_radius=0)
        self.customer_table_frame.pack(fill='both', expand=1, padx=(width*0.005), pady=(0,width*0.005))
       
        self.customer_treeview = cctk.cctkTreeView(self.customer_table_frame, data = [], width=width*0.805, height=height*0.8,
                                               column_format=f'/No:{int(width*.035)}-#r/CustomerID:{int(width*.115)}-tc/CustomerName:x-tl/CustomerType:{int(width*.115)}-tc/ContactNumber:{int(width*.15)}-tr!33!35',
                                               conditional_colors={3 : {"Non-Regular":Color.Near_Expire_Color, "Regular": "green"}})
        self.customer_treeview.pack()
        #self.no_sales_data = ctk.CTkLabel(self.sales_table_frame, text="No sales history data for this filter option", font=("DM Sans Medium", 14) , fg_color='transparent')
        self.search_bar = cctk.cctkSearchBar(self.top_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=serach_callback,
                                             quary_command=sql_commands.get_customer_quary_command, dp_width=width*0.275, place_height=height*0.0125, place_width=width*0.006, font=("DM Sans Medium", 14))
        self.search_bar.grid(row=0, column=0, padx=(width*0.005), pady=(height*0.01,0))
        
        
        self.add_customer_popup = customer_popup.new_customer(self, (width, height, acc_cred, acc_info), self.add_callback)
        self.view_customer_popup = customer_popup.view_record(self, (width, height, acc_cred, acc_info), self.refresh_treeview)
        
        
        self.no_data_label = ctk.CTkLabel(self.customer_treeview, text="No data yet to show.", font=("DM Sans Medium", 14))
        self.refresh_treeview()

    def add_callback(self):
        self.refresh_treeview()
        pass

    def refresh_treeview(self):
        self.refresh_btn.configure(state = ctk.DISABLED)
        self.customer_treeview.pack_forget()
        temp = database.fetch_data(sql_commands.get_customers_information, (SETTINGS_VAL['Regular_order_count'] , SETTINGS_VAL['Regular_order_count']))
        self.customer_treeview.update_table(temp)
        self.customer_treeview.pack()
        self.refresh_btn.after(100, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
        self.no_data_label.place(relx=0.5, rely=0.5, anchor='c') if not temp else self.no_data_label.place_forget()

class services_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()
        
        self.sub_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0, height*0.01))
        self.sub_frame.grid_rowconfigure(1, weight=1)
        self.sub_frame.grid_columnconfigure(0, weight=1)
        
        self.services_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Color[3])
        self.service_item_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Color[3])
        
        self.report_frames=[self.services_frame, self.service_item_frame]
        self.active_report = None

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row=1, column=0, sticky="nsew")

        def refresh(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.update_table()           
            self.refresh_btn.after(100, lambda: self.refresh_btn.configure(state = ctk.NORMAL))

    
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        
        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, sticky="ns", padx=width*0.005,pady=height*0.005)

        ctk.CTkFrame(self.sub_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.0075, bg_color=Color.Blue_Yale).grid(row=0, column=0, columnspan=5, sticky="nsew")
        
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", height = height*0.05, corner_radius=0)
        self.top_frame.grid(row=0, column=0 , sticky="nsw",padx=width*0.005,pady=(height*0.01,0))
        self.top_frame.grid_rowconfigure(0, weight=1)

        self.services_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=Color.Blue_Yale)

        self.services_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.services_button.configure(command=partial(load_main_frame, 0))
        self.inventory_icon = ctk.CTkLabel(self.services_button, text="",image=Icons.get_image("services_icon", (18,20)))
        self.inventory_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_label = ctk.CTkLabel(self.services_button, text="SERVICES", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_label.pack(side="left")
        self.services_button.grid()
        self.services_button.update_children()

        self.service_item_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=Color.Blue_Yale)

        self.service_item_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.service_item_button.configure(command=partial(load_main_frame, 1))
        self.stock_in_icon = ctk.CTkLabel(self.service_item_button, text="",image=Icons.get_image("inventory_icon", (19,20)))
        self.stock_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_in_label = ctk.CTkLabel(self.service_item_button, text="SERVICE ITEMS", text_color="white", font=("DM Sans Medium", 14))
        self.stock_in_label.pack(side="left")
        self.service_item_button.grid()
        self.service_item_button.update_children()
        
        self.button_manager = cctku.button_manager([self.services_button, self.service_item_button,], Color.Blue_Yale, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)
        
        
        """SERVICE"""
        self.button_frame = ctk.CTkFrame(self.services_frame, fg_color='transparent', corner_radius=0, height=height*0.055)
        self.button_frame.pack_propagate(0)
        self.button_frame.pack(fill="x", expand = 1, padx=(width*0.005), pady=(width*0.005))
        
        self.add_service = ctk.CTkButton(self.button_frame, text="Add Service", font=("DM Sans Medium", 14), width=width*0.1, height = height*0.05, image=self.plus,
                                         command=lambda: service_popup.add_service(self,(width, height,  acc_cred[0][0]), self.update_table).place(relx=0.5, rely=0.5, anchor="c"))
        self.add_service.pack(side="left", padx=(0,width*0.005), pady=(0))
        
        self.refresh_btn = ctk.CTkButton(self.button_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh)
        self.refresh_btn.pack(side="left", padx=(0,width*0.005), pady=(0)) 
        
        
        self.service_data_frame = ctk.CTkFrame(self.services_frame, fg_color=Color.White_Platinum, corner_radius=0)
        self.service_data_frame.pack(pady=(0, width*0.005))

        self.services_data = database.fetch_data(sql_commands.get_service_data_test, None)
        
        self.services_treeview = cctk.cctkTreeView(self.service_data_frame, data = self.services_data , width=width*0.805, height=height*0.8,
                                               column_format=f'/No:{int(width*.035)}-#r/ServiceCode:{int(width*.125)}-tc/ServiceName:x-tl/Duration:{int(width*.175)}-tl/Price:{int(width*.115)}-tr!33!35')
        self.services_treeview.pack()
        
        """SERVICE ITEMS"""
        self.svc_button_frame = ctk.CTkFrame(self.service_item_frame, fg_color='transparent', corner_radius=0, height=height*0.055)
        self.svc_button_frame.pack_propagate(0)
        self.svc_button_frame.pack(fill="x", expand = 1, padx=(width*0.005), pady=(width*0.005))
        
        self.svc_add_item = ctk.CTkButton(self.svc_button_frame, text="Add Item", font=("DM Sans Medium", 14), width=width*0.1, height = height*0.05, image=self.plus,
                                         command=lambda: self.add_service_item.place(relx=0.5, rely=0.5, anchor="c"))
        self.svc_add_item.pack(side="left", padx=(0,width*0.005), pady=(0))
        
        self.svc_refresh_btn = ctk.CTkButton(self.svc_button_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh)
        self.svc_refresh_btn.pack(side="left", padx=(0,width*0.005), pady=(0)) 
        
        self.depleted_btn = ctk.CTkButton(self.svc_button_frame, text="Depleted History", width=width*0.025, height = height*0.05, font=("DM Sans Medium", 14), 
                                          fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover, command=lambda: self.deplted_history.place(relx=0.5, rely=0.5, anchor="c"))
        
        self.depleted_btn.pack(side="right", padx=(0), pady=(0))
        
        self.svc_item_data_frame = ctk.CTkFrame(self.service_item_frame, fg_color=Color.White_Platinum, corner_radius=0)
        self.svc_item_data_frame.pack(pady=(0, width*0.005))

        #self.svc_item_data = database.fetch_data(sql_commands.get_service_data_test, None)
        
        self.svc_item_treeview = cctk.cctkTreeView(self.svc_item_data_frame, data =[] , width=width*0.805, height=height*0.8,
                                               column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*.125)}-tc/ItemDescription:x-tl/Status:{int(width*.175)}-tl/ExpirationDate:{int(width*.115)}-tr/Action:{int(width*.085)}-bD!33!35',
                                               bd_message="Are you sure you want to remove one (1) quantity of this item?")
        self.svc_item_treeview.pack()

        load_main_frame(0)
        self.add_service_item = Inventory_popup.add_service_item(self, (width, height), command_callback= None)
        self.deplted_history = Inventory_popup.deplted_history(self, (width, height))
        """SERVICE ITEMS"""
        
        self.svc_button_frame = ctk.CTkFrame(self.service_item_frame, fg_color='transparent', corner_radius=0, height=height*0.055)
        self.svc_button_frame.pack_propagate(0)
        self.svc_button_frame.pack(fill="x", expand = 1, padx=(width*0.005), pady=(width*0.005))
        
        self.svc_add_item = ctk.CTkButton(self.svc_button_frame, text="Add Item", font=("DM Sans Medium", 14), width=width*0.1, height = height*0.05, image=self.plus,
                                         command=lambda: self.add_service_item.place(relx=0.5, rely=0.5, anchor="c"))
        self.svc_add_item.pack(side="left", padx=(0,width*0.005), pady=(0))
        
        self.svc_refresh_btn = ctk.CTkButton(self.svc_button_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh)
        self.svc_refresh_btn.pack(side="left", padx=(0,width*0.005), pady=(0)) 
        
        
        self.svc_item_data_frame = ctk.CTkFrame(self.service_item_frame, fg_color=Color.White_Platinum, corner_radius=0)
        self.svc_item_data_frame.pack(pady=(0, width*0.005))

        #self.svc_item_data = database.fetch_data(sql_commands.get_service_data_test, None)
        
        self.svc_item_treeview = cctk.cctkTreeView(self.svc_item_data_frame, data =[] , width=width*0.805, height=height*0.8,
                                               column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*.125)}-tc/ItemDescription:x-tl/Status:{int(width*.175)}-tl/ExpirationDate:{int(width*.115)}-tr/Action:{int(width*.085)}-bD!33!35',
                                               bd_message="Are you sure you want to remove one (1) quantity of this item?")
        self.svc_item_treeview.pack()
        self.update_items_svc()
        
        def svc_item_bd_command (m):
            data = self.svc_item_treeview._data[m]
            uid = database.fetch_data(sql_commands.find_item_id_by_metainfo, (data[0], data[1]))[0][0]
            database.exec_nonquery([[sql_commands.set_data_to_depleted, (uid, data[3])]])
            self.update_items_svc()
        
        self.svc_item_treeview.bd_commands = svc_item_bd_command
        self.add_service_item = Inventory_popup.add_service_item(self, (width, height, acc_cred), command_callback= self.update_items_svc)
        load_main_frame(0)
        self.update_items_svc()

    def update_items_svc(self):
        self.svc_item_treeview.update_table(database.fetch_data(sql_commands.load_svc_item))
        
    def update_table(self):
        self.services_data = database.fetch_data(sql_commands.get_service_data_test, None)
        self.services_treeview.update_table(self.services_data)
        return

class sales_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()
        
        self.page_row_count = 12
        self.attendant_values = ['All']
        
        def set_date():
            self.source = self.raw_data = database.fetch_data(sql_commands.get_sales_record_by_date,(f'{self.from_date_select_entry._text}',f'{self.to_date_select_entry._text}'))
            self.attendant_sort_option.set("All")
            self.set_table()
            
        def page_callback():
            self.update_table()
            
        def search_callback():
            self.transaction_records = database.fetch_data(sql_commands.get_all_transaction_record)
            self.source = list_filterer(self.search_bar.get(), self.transaction_records)
            temp = self.source
            print(self.source)
            self.show_sale_info.place(relx=0.5, rely=0.5, anchor = 'c', sales_info=self.search_bar.get()[0]) if len(self.search_bar.get()) == 1 else self.set_table(temp)
            self.attendant_sort_option.set("All")
            
        def option_callback(var):
            if 'All' in var:
                self.set_table()
            else:
                temp = list_filterer([((var,))], self.source)
                self.set_table(temp)
        #region Top Frame

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, sticky="ns", padx=width*0.005,pady=height*0.01)

        self.top_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.055, corner_radius=0, bg_color=Color.White_Lotion,)
        self.top_frame.grid(row=0, column=0 , sticky="nw",padx=width*0.005,pady=(height*0.01,0))

        self.refresh_btn = ctk.CTkButton(self.top_frame, text="", width=height*0.05, height = height*0.05, image=Icons.get_image('refresh_icon', (20,20)), fg_color=Color.Green_Pistachio, 
                                         hover_color=Color.Green_Button_Hover_Color, command=self.refresh)
        self.refresh_btn.grid(row=0, column=1, padx=(0, width*0.005), pady=(height*0.01,0))

        self.view_record_btn = ctk.CTkButton(self.top_frame, text="View Record", image=Icons.get_image('view_receipt_icon',(28,28)), font=("DM Sans Medium", 14), width=width*0.1,height = height*0.05,
                                              command=self.view_record, text_color=Color.White_Lotion)
        self.view_record_btn.grid(row=0, column=2, padx=(0, width*0.005), pady=(height*0.01,0))
        
        self.sub_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0, height*0.01))
        self.sub_frame.grid_rowconfigure(1, weight=1)
        self.sub_frame.grid_columnconfigure(1, weight=1)
        #endregion

        #region Date Selection
        self.date_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
        self.date_frame.pack(fill='x', expand=0,  padx=(width*0.005), pady=(height*0.01,height*0.0075))
        
        '''FROM'''
        self.from_date_frame = ctk.CTkFrame(self.date_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.17)
        self.from_date_frame.pack(side="left")
        self.from_date_frame.propagate(0)
        
        ctk.CTkLabel(self.from_date_frame, text="From: ", font=("DM Sans Medium", 14), anchor='e', width=width*0.03).pack(side="left", padx=(width*0.01,width*0.0025))
        #date.today()
        self.from_date_select_entry = ctk.CTkLabel(self.from_date_frame, text=date.today(), font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5)
        self.from_date_select_entry.pack(side="left", fill="both", expand=1,  padx=(0,width*0.0025), pady=(width*0.0025))
        self.from_show_calendar = ctk.CTkButton(self.from_date_frame, text="",image=Icons.get_image("calendar_icon", (22,22)), height=height*0.05,width=height*0.05, fg_color=Color.Blue_Yale,
                                               command=lambda:cctk.tk_calendar(self.from_date_select_entry, "%s", date_format="raw", max_date=datetime.datetime.now(), set_date_callback=set_date))
        self.from_show_calendar.pack(side="left", padx=(0, width*0.0025), pady=(width*0.0025))
        
        '''TO'''
        self.to_date_frame = ctk.CTkFrame(self.date_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.15)
        self.to_date_frame.pack(side="left", padx=(width*0.0025))
        self.to_date_frame.propagate(0)
        
        ctk.CTkLabel(self.to_date_frame, text="To: ", font=("DM Sans Medium", 14), anchor='e', width=width*0.0225).pack(side="left", padx=(width*0.005,width*0.0025))
        
        self.to_date_select_entry = ctk.CTkLabel(self.to_date_frame, text=date.today(), font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5)
        self.to_date_select_entry.pack(side="left", fill="both", expand=1,  padx=(0,width*0.0025), pady=(width*0.0025))
        
        self.to_show_calendar = ctk.CTkButton(self.to_date_frame, text="",image=Icons.get_image("calendar_icon", (22,22)), height=height*0.05,width=height*0.05, fg_color=Color.Blue_Yale,
                                               command=lambda:cctk.tk_calendar(self.to_date_select_entry, "%s", date_format="raw", max_date=datetime.datetime.now(), 
                                                                               min_date= datetime.datetime.strptime(str(self.from_date_select_entry._text), '%Y-%m-%d').date(),set_date_callback=set_date))
        self.to_show_calendar.pack(side="left", padx=(0, width*0.0025), pady=(width*0.0025))
        
        self.sort_frame = ctk.CTkFrame(self.date_frame, fg_color=Color.Platinum, height=height*0.05, width=width*0.15)
        self.sort_frame.pack(side="right", pady=(height*0.0025) )
        self.sort_frame.propagate(0)
        
        ctk.CTkLabel(self.sort_frame, text="Cashier: ", font=("DM Sans Medium", 14), anchor='e', width=width*0.0225).pack(side="left", padx=(width*0.01,width*0.0025))
        self.attendant_sort_option= ctk.CTkOptionMenu(self.sort_frame, values=self.attendant_values, anchor="center", font=("DM Sans Medium", 12), width=width*0.125, height = height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=option_callback, dropdown_font=("DM Sans Medium", 12))
        self.attendant_sort_option.pack(side="left", padx=(0, width*0.0025), pady=(width*0.0025))
        
        #endregion
 
        self.sales_treeview_frame = ctk.CTkFrame(self.sub_frame, corner_radius=0, fg_color=Color.White_Lotion)
        self.sales_treeview_frame.pack(fill='both', expand=1,  padx=(width*0.005), pady=(0,width*0.005))
        #"No", "OR ","Client", "Total", "Date", "Cashier"
        self.sales_treeview = cctk.cctkTreeView(self.sales_treeview_frame, data = [], width= width * .805, height= height*0.665, corner_radius=0,
                                           column_format=f'/No:{int(width*.0325)}-#r/TransactionID:{int(width*0.1)}-tc/Status:{int(width*.1)}-tc/Client:x-tl/Total:{int(width*0.1)}-tr/Date:{int(width*0.115)}-tc/Cashier:{int(width*0.1)}-tl!33!35',)
                                           
        self.sales_treeview.pack()
        #region Bottom
        self.bot_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent",height=height*0.075,)
        self.bot_frame.pack(fill="x", expand=0, padx=(width*0.005), pady=(0,width*0.005))
        
        self.page_counter = cctk.cctkPageNavigator(self.bot_frame,  width=width*0.125, height=height*0.0575, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                             font=("DM Sans Medium", 14), page_limit=1, command=page_callback, disable_timer=100)
        self.page_counter.pack()
        #endregion
       
        self.no_sales_data = ctk.CTkLabel(self.sales_treeview, text="No sales history data for this filter option", font=("DM Sans Medium", 14) , fg_color='transparent')
        
        self.search_bar = cctk.cctkSearchBar(self.top_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=search_callback,
                                             quary_command=sql_commands.get_sales_search_query, dp_width=width*0.275, place_height=height*0.0125, place_width=width*0.006, font=("DM Sans Medium", 14))
        self.search_bar.grid(row=0, column=0, padx=(width*0.005), pady=(height*0.01,0))
        #
        self.raw_data = database.fetch_data(sql_commands.get_sales_record_by_date, (f'{self.from_date_select_entry._text}',f'{self.to_date_select_entry._text}'))
        self.set_table()
        
        #region Popups   
        self.show_sale_info = Sales_popup.show_sales_record_info(self, (width, height, acc_cred, acc_info,))
        #endregion
    
    def view_record(self):
        #print(self.sales_treeview.get_selected_data())
        self.show_sale_info.place(relx=0.5, rely=0.5, anchor = 'c', sales_info=self.sales_treeview.get_selected_data()) if self.sales_treeview.get_selected_data() else messagebox.showerror("Warning", "Select a record first", parent = self)
    
    def refresh(self):
        self.refresh_btn.configure(state = ctk.DISABLED)
        self.sales_treeview.pack_forget()
        self.raw_data = database.fetch_data(sql_commands.get_sales_record_by_date,(f'{self.from_date_select_entry._text}',f'{self.to_date_select_entry._text}'))
        self.source = self.raw_list
        self.attendant_sort_option.configure(values = self.attendant_values + [s[0] for s in database.fetch_data(sql_commands.get_sales_attendant)])
        self.attendant_sort_option.set("All")
        self.set_table()
        
    def set_table(self, given:Optional[list] = None):      
        self.raw_list = given if given else self.raw_data
        self.pages, self.page_count = list_to_parted_list(self.raw_list, self.page_row_count, 1)
        self.page_counter.update_page_limit(self.page_count)
        self.update_table()
        
    def update_table(self):
        self.sales_treeview.pack_forget()
        self.temp = self.pages[self.page_counter.get()-1] if self.pages else []
        if len(self.pages) != 0:
            self.temp = self.pages[self.page_counter.get()-1]; 
            self.no_sales_data.place_forget() 
        else:
            self.temp = []
            self.no_sales_data.place(relx=0.5, rely=0.5, anchor='c')
        self.sales_treeview.update_table(self.temp)
        self.sales_treeview.pack()
        self.refresh_btn.after(100, lambda:self.refresh_btn.configure(state = ctk.NORMAL))
        
    def grid(self, **kwargs):
        self.refresh()
        return super().grid(**kwargs)
        
class inventory_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, mainframes, IP_Address, PORT_NO
    def __init__(self, master):
        current_month = datetime.datetime.now().month

        #if it is the end of the month
        if (datetime.datetime.now() + datetime.timedelta(days= 1)).month != current_month:
            item_statistics = database.fetch_data(sql_commands.get_updated_avg_of_old_statistics, (current_month, ))
            database.exec_nonquery([[sql_commands.update_statistics_info, (s[1], s[2], s[0])] for s in item_statistics])

        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(18,18))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(20,21))
        self.disposal_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
        self.supplier_icon_ = ctk.CTkImage(light_image= Image.open("image/supplier.png"), size=(26,26))
        self.history_icon = ctk.CTkImage(light_image= Image.open("image/histlogs.png"), size=(22,25))
        self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(16,18))
        self.edit_icon = ctk.CTkImage(light_image= Image.open("image/edit_icon.png"), size=(16,16))
        self.info_icon = ctk.CTkImage(light_image= Image.open("image/info.png"), size=(36,36))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.inventory_sub_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.restock_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.supplier_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.disposal_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        
        self.report_frames=[self.inventory_sub_frame, self.restock_frame, self.supplier_frame, self.disposal_frame]
        self.active_report = None

        self.sort_type_option_var = ctk.StringVar(value="Sort by Levels")
        self.sort_status_option_var = ctk.StringVar(value="Normal")

        self.sort_status_var=["Sort by Levels","Sort by Category", "Sort by Expiry"]
        self.sort_type_var=["Normal","Reorder","Critical"]

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.page_row_count = 12
        self.order_page_row_count = 12
        self.supplier_page_count = 12
        self.dispose_page_count = 12
        
        self.sorting_order = {'Out Of Stock': 0, 'Critical': 1, 'Reorder': 2, 'Normal': 3, 'N/A':4}
        
        selected_color = Color.Blue_Yale
        self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
        self.sell_rate = {s[0]: s[1] for s in database.fetch_data(sql_commands.get_selling_rate)}
        self.sort_key = {'Out of Stock': 0, 'Critical': 1, 'Reorder': 2, 'Normal': 3}
        
        #region Functions
        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)
            [search_bar.reset() for search_bar in self.search_bars]

        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            self.data_view1.pack_forget()
            sell_data, item_data = selling_concat_unit(database.fetch_data(sql_commands.get_selling_rate)), item_concat_unit(self.list_show)
            self.raw_data = [tuple(rate[0]) + item for item in item_data for rate in sell_data  if rate[-1] == item[1]]
            set_table()
        
        def update_table_callback():
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            self.sort_status_option.set("All")
            self.sort_type_option.set("Sort by Levels")
            sell_data, item_data = selling_concat_unit(database.fetch_data(sql_commands.get_selling_rate)), item_concat_unit(database.fetch_data(sql_commands.get_inventory_by_group))
            self.list_show = item_data
            self.raw_data = [tuple(rate[0]) + item for item in item_data for rate in sell_data  if rate[-1] == item[1]]
            set_table()
        
        def set_table(given:Optional[list] = None):      
            self.raw_list = given if given else self.raw_data
            self.pages, self.page_count = list_to_parted_list(self.raw_list, self.page_row_count, 1)
            self.page_counter.update_page_limit(self.page_count)
            page_update_table()
        
        def page_callback():
            page_update_table()
        
        def page_update_table():
            self.data_view1.pack_forget()
            self.temp = self.pages[self.page_counter.get()-1] if self.pages else []
            if len(self.pages) != 0:
                self.temp = self.pages[self.page_counter.get()-1]; 
                self.no_item_data.place_forget() 
            else:
                self.temp = []
                self.no_item_data.place(relx=0.5, rely=0.5, anchor='c')
            self.data_view1.update_table(self.temp)
            self.data_view1.pack()
            self.refresh_btn.after(5000, lambda:self.refresh_btn.configure(state = ctk.NORMAL))
            
        def disposal_table_callback():
            sort_status_configuration_callback()
            
        def get_categories():
            data = database.fetch_data("SELECT categ_name FROM categories")
            category_data = ["All Items"]
            for i in range(len(data)):
                category_data.append(data[i][0])
            
            return category_data

        def sort_status_callback(option):
            if "Levels" in option:
                self.sort_status_option.configure(values=["All", "Normal","Reorder","Critical", "Out of Stock"])
                self.sort_status_option.set("All")
                sort_status_configuration_callback()
            elif "Category" in option:
                self.sort_status_option.configure(values=get_categories())
                self.sort_status_option.set("All Items")
                sort_status_configuration_callback()
            else:
                self.sort_status_option.configure(values=["Safe","Nearly Expire", "Expired", "No Expiration"])
                self.sort_status_option.set("Safe")
                sort_status_configuration_callback()

        def sort_status_configuration_callback(_: any = None):
            #self.search_entry.delete(0, ctk.END)
            if "Levels" in self.sort_type_option.get():
                if "All" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
                elif "Normal" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_normal_inventory)
                elif "Reorder" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_reorder_inventory)
                elif "Critical" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_critical_inventory)
                elif "Out of Stock" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_out_of_stock_inventory)
            elif 'Expiry' in self.sort_type_option.get():
                if 'Safe' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_safe_expire_inventory)
                elif 'Nearly' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_near_expire_inventory)
                elif 'Expired' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_expired_inventory)
                elif 'No Exp' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_non_expiry_inventory)
            elif 'Category' in self.sort_type_option.get():
                if "All" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
                else:
                    self.list_show = database.fetch_data(sql_commands.get_category_specific_inventory, (self.sort_status_option.get(), ))
            
            self.dispose_all_btn.place(relx=0,rely=0.5, anchor='w') if 'Expiry' in self.sort_type_option.get() and 'Expired' in self.sort_status_option.get() else self.dispose_all_btn.place_forget()
            self.no_item_data.place(relx=0.5, rely=0.5, anchor='c') if not self.list_show else self.no_item_data.place_forget()
            
            update_tables()

        """ def dispose_expired(_: any = None):
            if self.data_view1.data_grid_btn_mng.active:
                if self.data_view1.get_selected_data()[-1] == 'Expired':
                    if messagebox.askyesno("Dispose Item", "Are you sure you want to dispose\nthe item?", parent = self):
                        data = self.data_view1.get_selected_data()
                        database.exec_nonquery([["Update state = -1 WHERE stock = ? AND Expiry_Date = ?", (data[2], data[4])]])
                        self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
                        update_tables() """
        
        def batch_dispose():
            if self.data_view1._data:
                if messagebox.askyesnocancel("Disposal Confirmation", f"Are you sure you want to dispose {len(self.data_view1._data)} item/s?", parent = self):
                    self.authorization.place(relx=0.5, rely=0.5, anchor='c')
                else:
                    print("Thank you for saving a trash like me")
            else:
                messagebox.showwarning("Error", "No item to dispose", parent = self)

        def search(_: any = None):
            if self.search_entry.get():
                temp = [s for s in self.list_show if self.search_entry.get().lower() in s[0].lower()]
                self.data_view1.update_table(temp)
                del temp
            else:
                update_tables()

        def reset(self):
            self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
            self.data_view1.update_table(self.data1)
            
        def inv_search_callback():
            temp = [database.fetch_data(sql_commands.get_item_brand_name_unit, (data[0],))[0] for data in self.inv_search_bar.get()]
            set_table(custom_sort((list_filterer(source=temp, reference=self.raw_data)), self.sort_key))
        #endregion
        
        #region Tab Setup 
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=4, sticky="n")


        self.inventory_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_button.configure(command=partial(load_main_frame, 0))
        self.inventory_icon = ctk.CTkLabel(self.inventory_button, text="",image=self.inventory_icon)
        self.inventory_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_label = ctk.CTkLabel(self.inventory_button, text="INVENTORY", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_label.pack(side="left")
        self.inventory_button.grid()
        self.inventory_button.update_children()

        self.stock_in_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_in_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.stock_in_button.configure(command=partial(load_main_frame, 1))
        self.stock_in_icon = ctk.CTkLabel(self.stock_in_button, text="",image=self.restock_icon)
        self.stock_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_in_label = ctk.CTkLabel(self.stock_in_button, text="ORDERS", text_color="white", font=("DM Sans Medium", 14))
        self.stock_in_label.pack(side="left")
        self.stock_in_button.grid()
        self.stock_in_button.update_children()

        self.stock_disposal_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_disposal_button.grid(row=0, column=3, sticky="sw", padx=(0,width*0.0025), pady=0)
        self.stock_disposal_button.configure(command=partial(load_main_frame, 3))
        self.stock_disposal_icon = ctk.CTkLabel(self.stock_disposal_button, text="",image=self.trash_icon)
        self.stock_disposal_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_disposal_label = ctk.CTkLabel(self.stock_disposal_button, text="DISPOSED ITEMS", text_color="white", font=("DM Sans Medium", 14))
        self.stock_disposal_label.pack(side="left")
        self.stock_disposal_button.grid()
        self.stock_disposal_button.update_children()
        
        self.supplier_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.supplier_button.grid(row=0, column=2, sticky="sw", padx=(0,width*0.0025), pady=0)
        self.supplier_button.configure(command=partial(load_main_frame, 2))
        self.supplier_icon = ctk.CTkLabel(self.supplier_button, text="",image=self.supplier_icon_)
        self.supplier_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.supplier_label = ctk.CTkLabel(self.supplier_button, text="SUPPLIER", text_color="white", font=("DM Sans Medium", 14))
        self.supplier_label.pack(side="left")
        self.supplier_button.grid()
        self.supplier_button.update_children()

        self.button_manager = cctku.button_manager([self.inventory_button, self.stock_in_button, self.supplier_button, self.stock_disposal_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)
        #endregion
        
        #region Inventory
        '''INVENTORY FRAME: START'''
        self.inventory_sub_frame.pack(fill="both", expand=1,)
        self.inventory_sub_frame.grid_propagate(0)
        self.inventory_sub_frame.grid_rowconfigure(1, weight=1)
        self.inventory_sub_frame.grid_columnconfigure(3, weight=1)
        
        self.inv_refresh_btn = ctk.CTkButton(self.inventory_sub_frame, text="", width=height*0.05, height = height*0.05, image=Icons.get_image('refresh_icon',(20,20)), fg_color="#83BD75",
                                             command = update_table_callback, hover_color=Color.Green_Button_Hover_Color,)
        self.inv_refresh_btn.grid(row=0, column=1, sticky="w")
        
        self.add_item_btn = ctk.CTkButton(self.inventory_sub_frame,width=width*0.08, height = height*0.05, text="Add Item",image=Icons.get_image('add_icon', (15,15)), font=("DM Sans Medium", 14),
                                          command= lambda : self.add_item_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_item_btn.grid(row=0, column=2, sticky="w", padx=(width*0.005), pady=(height*0.01))
        
        self.view_category = ctk.CTkButton(self.inventory_sub_frame, height=height*0.05,width=width*0.07, text="Category",  font=("DM Sans Medium", 14),
                                           command = lambda: self.category_popup.place(relx=0.5, rely=0.5, anchor="c"))
        self.view_category.grid(row=0, column=3, sticky="w", padx=(0,width*0.005), pady=(height*0.01))


        self.sort_frame = ctk.CTkFrame(self.inventory_sub_frame,  height = height*0.05, fg_color=Color.Platinum)
        self.sort_frame.grid(row=0, column=5, padx=(width*0.005), pady=(height*0.01), sticky="nse")
        self.sort_frame.grid_rowconfigure(0, weight=1)
        self.sort_frame.grid_columnconfigure((1,2), weight=1)

        self.sort_type_option= ctk.CTkOptionMenu(self.sort_frame, values=self.sort_status_var, anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=partial(sort_status_callback))
        self.sort_type_option.grid(row=0, column=1, padx=(width*0.0045,0), pady=(height*0.0065), sticky="nsew")

        
        self.sort_status_option= ctk.CTkOptionMenu(self.sort_frame, values=self.sort_type_var, anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=sort_status_configuration_callback)
        self.sort_status_option.grid(row=0, column=2, padx=(width*0.005), pady=(height*0.0065), sticky="nsew")

        self.disposal_btns_frame = ctk.CTkFrame(self.inventory_sub_frame,fg_color='transparent', height = height*0.055)
        
        self.tree_view_frame = ctk.CTkFrame(self.inventory_sub_frame, fg_color="transparent")
        self.tree_view_frame.grid(row=1, column=0,columnspan=6, sticky="nsew",padx=(width*0.005))

        self.data_view1 = cctk.cctkTreeView(self.tree_view_frame, data = [], width= width*0.8, height= height*0.7, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Rate:{int(width*.045)}-tc/ItemBrand:{int(width*.08)}-tl/ItemDescription:x-tl/Stock:{int(width*.085)}-tr/Price:{int(width*.085)}-tr/ExpirationDate:{int(width*.1)}-tc/Status:{int(width*.1)}-tc!33!35',
                                           conditional_colors= {7: {'Reorder':'#ff7900', 'Critical':'red','Normal':'green', 'Out Of Stock': '#555555', 'Safe':'green', 'Nearly Expire':'#FFA500','Expired':'red'},
                                                                1: {'🠉': 'green', '🠋': 'red', '-' : '#AAAAAA'}},)
        self.data_view1.pack()
        
        self.bot_frame = ctk.CTkFrame(self.inventory_sub_frame, fg_color=Color.White_Lotion, height=height*0.065,)
        self.bot_frame.grid(row=2, column=0,columnspan=6, sticky="nsew",padx=(width*0.005), pady=(width*0.005))
        
        self.page_counter = cctk.cctkPageNavigator(self.bot_frame,  width=width*0.125, height=height*0.0575, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                             font=("DM Sans Medium", 14), page_limit=1, disable_timer=100, command=page_callback)
        self.page_counter.place(relx=0.5,rely=0.5, anchor="c")

        self.dispose_btn = ctk.CTkButton(self.bot_frame, width=width*0.1, height = height*0.05, text="Dispose", image=Icons.get_image('trash_icon', (20,17)), font=("DM Sans Medium", 14), fg_color= Color.Red_Pastel,
                                        command= lambda : self.dispose_popup.place(relx = .5, rely = .5, anchor = 'c', data= self.data_view1.get_selected_data()))
        self.dispose_btn.place(relx=0.87,rely=0.5, anchor='e')
        
        self.restock_btn = ctk.CTkButton(self.bot_frame, width=width*0.1, height = height*0.05, text="Stock Order", image=Icons.get_image('restock_icon', (20,17)), font=("DM Sans Medium", 14),
                                        command= lambda : self.restock_popup.place(default_data=self.data_view1.get_selected_data() or None, update_cmds=self.update_tables, relx = .5, rely = .5, anchor = 'c'))
        self.restock_btn.place(relx=1,rely=0.5, anchor='e')
        
        self.dispose_all_btn = ctk.CTkButton(self.bot_frame, width=width*0.1, height = height*0.05, text="Dispose All", image=Icons.delete_all_icon, font=("DM Sans Medium", 14),
                                             fg_color=Color.Red_Pastel, hover_color=Color.Red_Hover, command=batch_dispose)
        
        self.no_item_data = ctk.CTkLabel(self.data_view1, text="No inventory data yet to show.", font=("DM Sans Medium", 14))
        self.sort_type_option.set("Sort by Levels")
        
        self.inv_search_bar = cctk.cctkSearchBar(self.inventory_sub_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=inv_search_callback,
                                                 close_command_callback= update_table_callback,
                                             quary_command=sql_commands.get_item_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
        self.inv_search_bar.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(width*0.005))
        
        
        '''INVENTORY FRAME: END'''
        #endregion
            
        #region Restock
        '''RESTOCK: START'''
        #def refresh_rs_data_view1():
        #    self.refresh_btn.configure(state = ctk.DISABLED)
        #    self.rs_data_view1.update_table(database.fetch_data(sql_commands.get_recieving_items_state))
        #    self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not database.fetch_data(sql_commands.get_recieving_items_state) else self.no_order_data.place_forget()
        #    self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))

        def restocking_callback():
            update_table_callback()
            #self.inventory_button.response()
            refresh_rs_data_view1()
            pass
            
        def disposal_callback(i: int):
            data = self.rs_data_view1._data[i]
            self.disposal_confirm_popup.place(relx=0.5, rely=0.5, anchor='c', data=data)
            
        def _restock(_: any = None):
            if self.rs_data_view1.get_selected_data():
                self.restock_confirm.place(relx= 0.5, rely=0.5, anchor="c", restocking_info= self.rs_data_view1.get_selected_data())
            
        #Pagination
        
        def refresh_rs_data_view1():
            self.rs_refresh_btn.configure(state='disabled')
            self.rs_raw_data = database.fetch_data(sql_commands.get_recieving_items_state)
            rs_set_table()
        
        def rs_set_table(given:Optional[list] = None):      
            self.rs_raw_list = given if given else self.rs_raw_data
            self.rs_pages, self.rs_page_count = list_to_parted_list(self.rs_raw_list, self.page_row_count, 1)
            self.rs_page_counter.update_page_limit(self.rs_page_count)
            rs_page_update_table()
        
        def show_order_info():
            self.order_info.place(relx=0.5, rely=0.5, anchor='c', data= self.rs_data_view1.get_selected_data()) if self.rs_data_view1.get_selected_data() else messagebox.showwarning("Warning", "Please select a record first", parent = self)

        def rs_search_callback():
            rs_set_table(list_filterer(self.rs_search_bar.get(), self.rs_raw_data))
            
        def rs_page_callback():
            rs_page_update_table()
            
        def rs_page_update_table():
            self.rs_data_view1.pack_forget()
            self.rs_temp = self.rs_pages[self.rs_page_counter.get()-1] if self.rs_pages else []
            if len(self.rs_pages) != 0:
                self.rs_temp = self.rs_pages[self.rs_page_counter.get()-1]; 
                self.no_order_data.place_forget() 
            else:
                self.rs_temp = []
                self.no_order_data.place(relx=0.5, rely=0.5, anchor='c')
            self.rs_data_view1.update_table(self.rs_temp)
            self.rs_data_view1.pack()
            self.after(100, lambda: self.rs_refresh_btn.configure(state='normal'))
        
        self.restock_frame.grid_propagate(0)
        self.restock_frame.grid_rowconfigure(1, weight=1)
        self.restock_frame.grid_columnconfigure(3, weight=1)

        self.rs_add_item_btn = ctk.CTkButton(self.restock_frame,width=width*0.1, height = height*0.05, text="Add Order",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command= lambda : self.restock_popup.place(default_data=None, relx = .5, rely = .5, anchor = 'c'))
        self.rs_add_item_btn.grid(row=0, column=2, sticky="w", padx=(0,width*0.005), pady=(width*0.005))

        self.rs_refresh_btn = ctk.CTkButton(self.restock_frame, text="", width=height*0.05, height = height*0.05, image=Icons.get_image('refresh_icon',(20,20)), fg_color="#83BD75",
                                             command = refresh_rs_data_view1, hover_color=Color.Green_Button_Hover_Color,)
        self.rs_refresh_btn.grid(row=0, column=3, sticky="w")

        self.info_btn = ctk.CTkButton(self.restock_frame, width=height*0.05, height = height*0.05, image=Icons.get_image('info_icon', (25,25)), text="", font=("DM Sans Medium", 14),
                                             command=show_order_info,)
        self.info_btn.grid(row=0, column=5, sticky="e", padx=(0,width*0.005), pady=(width*0.005))
        
        self.receive_history = ctk.CTkButton(self.restock_frame, width=width*0.025, height = height*0.05, text="Received Items", image=self.history_icon, font=("DM Sans Medium", 14),
                                             command= lambda: self.history_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.receive_history.grid(row=0, column=3, sticky="e", padx=(0,width*0.005), pady=(height*0.01))

        self.cancelled_orders = ctk.CTkButton(self.restock_frame, width=width*0.025, height = height*0.05, text="Cancelled Orders", image=self.history_icon, font=("DM Sans Medium", 14), fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                             command=lambda: self.cancel_orders.place(relx = 0.5, rely=0.5, anchor = 'c'))
        self.cancelled_orders.grid(row=0, column=4, sticky="e", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_treeview_frame = ctk.CTkFrame(self.restock_frame,fg_color="transparent")
        self.rs_treeview_frame.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=(width*0.005))

        self.rs_data = []
        self.rs_data_view1 = cctk.cctkTreeView(self.rs_treeview_frame, data=self.rs_data, width= width*0.8, height= height*0.7, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/OrderNo:{int(width *.07)}-tc/Status:{int(width *.07)}-tc/ItemName:x-tl/Quantity:{int(width*.1)}-tr/Supplier:{int(width*.135)}-tl/OrderBy:{int(width*.1)}-tl/Action:{int(width*.05)}-bD!33!35',
                                           double_click_command= _restock, bd_commands= disposal_callback, conditional_colors={2:{'On Order':'orange', 'Partial':'red'}} , 
                                           bd_message='Are you sure you want to cancel this order?')
        self.rs_data_view1.pack()
        
        self.rs_bot_frame = ctk.CTkFrame(self.restock_frame, fg_color=Color.White_Lotion, height=height*0.065,)
        self.rs_bot_frame.grid(row=2, column=0,columnspan=6, sticky="nsew",padx=(width*0.005), pady=(width*0.005))
        
        self.rs_page_counter = cctk.cctkPageNavigator(self.rs_bot_frame,  width=width*0.125, height=height*0.0575, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                             font=("DM Sans Medium", 14), page_limit=1, command=rs_page_callback, disable_timer=100)
        self.rs_page_counter.place(relx=0.5,rely=0.5, anchor="c")
    
        self.no_order_data = ctk.CTkLabel(self.rs_data_view1, text="No order data yet to show.", font=("DM Sans Medium", 14))
        self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not self.rs_data else self.no_order_data.place_forget()

        self.rs_search_bar = cctk.cctkSearchBar(self.restock_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=rs_search_callback,
                                                close_command_callback= refresh_rs_data_view1,
                                                quary_command=sql_commands.get_order_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
        self.rs_search_bar.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(width*0.005))
        refresh_rs_data_view1()
        '''RESTOCK FRAME: END'''
        #endregion
        
        #region Disposal 
        '''ITEM DISPOSAL: START'''
        
        def filter_ds_table(_:any = None):
            data = database.fetch_data(sql_commands.get_disposed_filter, (self.ds_sort_category_option.get(), self.ds_sort_type_option.get(), self.from_date_select_entry._text, self.to_date_select_entry._text))
            self.ds_data_view1.pack_forget()
            self.ds_refresh_btn.configure(state = ctk.DISABLED)
            self.ds_data_view1.update_table(data)
            self.ds_data_view1.pack()
            
            self.no_disposal_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_disposal_data.place_forget()
            self.ds_refresh_btn.after(100, lambda:self.ds_refresh_btn.configure(state = ctk.NORMAL))

        def refresh_ds_table():
            self.ds_sort_category_option.configure(values = [category[0] for category in database.fetch_data("SELECT categ_name from categories")])
            
            self.ds_data_view1.pack_forget()
            self.ds_refresh_btn.configure(state = ctk.DISABLED)
            
            data =  database.fetch_data(sql_commands.get_disposed_filter, (self.ds_sort_category_option.get(), self.ds_sort_type_option.get(), self.from_date_select_entry._text, self.to_date_select_entry._text))
            self.ds_data_view1.update_table(data)
            self.ds_data_view1.pack()
            
            self.no_disposal_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_disposal_data.place_forget()
            self.ds_refresh_btn.after(100, lambda:self.ds_refresh_btn.configure(state = ctk.NORMAL))
            
        self.disposal_frame.grid_propagate(0)
        self.disposal_frame.grid_rowconfigure(1, weight=1)
        self.disposal_frame.grid_columnconfigure(2, weight=1)
        
        self.ds_sort_frame = ctk.CTkFrame(self.disposal_frame,  height = height*0.05, fg_color=Color.Platinum)
        self.ds_sort_frame.grid(row=0, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nse")
        self.ds_sort_frame.grid_rowconfigure(0, weight=1)
        self.ds_sort_frame.grid_columnconfigure((1,2), weight=1)
        
        self.ds_sort_category_option= ctk.CTkOptionMenu(self.ds_sort_frame, values=[category[0] for category in database.fetch_data("SELECT categ_name from categories")], anchor="center", font=("DM Sans Medium", 12), width=width*0.115, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=filter_ds_table)
        self.ds_sort_category_option.grid(row=0, column=1, padx=(width*0.0045), pady=(width*0.0045), sticky="nsew")
        
        
        self.ds_sort_type_option= ctk.CTkOptionMenu(self.ds_sort_frame, values=["Defective/Damaged", "Expired"], anchor="center", font=("DM Sans Medium", 12), width=width*0.115, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=filter_ds_table)
        self.ds_sort_type_option.grid(row=0, column=3, padx=(0, width*0.0045), pady=(width*0.0045), sticky="nsew")
        

        self.ds_refresh_btn = ctk.CTkButton(self.disposal_frame,text="", width=width*0.03, height = width*0.03, image=self.refresh_icon, fg_color="#83BD75", command=refresh_ds_table)
        self.ds_refresh_btn.grid(row=0, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
        
        self.date_frame = ctk.CTkFrame(self.disposal_frame, fg_color='transparent', height = height*0.05,)
        self.date_frame.grid(row=0, column=3, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.date_frame.propagate(1)
            
        '''FROM'''
        self.from_date_frame = ctk.CTkFrame(self.date_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.17)
        self.from_date_frame.pack(side="left")
        self.from_date_frame.propagate(0)
        
        ctk.CTkLabel(self.from_date_frame, text="From: ", font=("DM Sans Medium", 14), anchor='e', width=width*0.03).pack(side="left", padx=(width*0.01,width*0.0025))
        #date.today()
        self.from_date_select_entry = ctk.CTkLabel(self.from_date_frame, text=date.today(), font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5)
        self.from_date_select_entry.pack(side="left", fill="both", expand=1,  padx=(0,width*0.0025), pady=(width*0.0025))
        self.from_show_calendar = ctk.CTkButton(self.from_date_frame, text="",image=Icons.get_image("calendar_icon", (22,22)), height=height*0.05,width=height*0.05, fg_color=Color.Blue_Yale,
                                               command=lambda:cctk.tk_calendar(self.from_date_select_entry, "%s", date_format="raw", max_date=datetime.datetime.now(), set_date_callback=filter_ds_table))
        self.from_show_calendar.pack(side="left", padx=(0, width*0.0025), pady=(width*0.0025))
        
        '''TO'''
        self.to_date_frame = ctk.CTkFrame(self.date_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.15)
        self.to_date_frame.pack(side="left", padx=(width*0.0025))
        self.to_date_frame.propagate(0)
        
        ctk.CTkLabel(self.to_date_frame, text="To: ", font=("DM Sans Medium", 14), anchor='e', width=width*0.0225).pack(side="left", padx=(width*0.005,width*0.0025))
        
        self.to_date_select_entry = ctk.CTkLabel(self.to_date_frame, text=date.today(), font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5)
        self.to_date_select_entry.pack(side="left", fill="both", expand=1,  padx=(0,width*0.0025), pady=(width*0.0025))
        
        self.to_show_calendar = ctk.CTkButton(self.to_date_frame, text="",image=Icons.get_image("calendar_icon", (22,22)), height=height*0.05,width=height*0.05, fg_color=Color.Blue_Yale,
                                               command=lambda:cctk.tk_calendar(self.to_date_select_entry, "%s", date_format="raw", max_date=datetime.datetime.now(), 
                                                                               min_date= datetime.datetime.strptime(str(self.from_date_select_entry._text), '%Y-%m-%d').date(),set_date_callback=filter_ds_table))
        self.to_show_calendar.pack(side="left", padx=(0, width*0.0015), pady=(width*0.0025))
        
        self.ds_treeview_frame = ctk.CTkFrame(self.disposal_frame,fg_color="transparent")
        self.ds_treeview_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005)

        self.ds_data_view1 = cctk.cctkTreeView(self.ds_treeview_frame, data = None, width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/DisposalID:{int(width*0.085)}-tc/ItemName:x-tl/Quantity:{int(width*0.1)}-tr/Reason:{int(width*.135)}-tl/DisposedDate:{int(width*.1)}-tc/DisposedBy:{int(width*.1)}-tl!33!35',)
        self.ds_data_view1.pack()
        
        self.no_disposal_data = ctk.CTkLabel(self.ds_data_view1, text="No disposal data for this filter option.", font=("DM Sans Medium", 14))
        refresh_ds_table()

        '''ITEM DISPOSAL: END'''
        #endregion
        
        #region Supplier
        
        def supplier_search_callback():
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.supplier_treeview.pack_forget()
            self.supplier_treeview.update_table(list_filterer(self.supplier_search_bar.get(), (database.fetch_data(sql_commands.get_supplier_info))))
            self.supplier_treeview.pack()
            self.refresh_btn.after(100,lambda:self.refresh_btn.configure(state = ctk.NORMAL))
        def refresh_supplier_table():
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.supplier_treeview.pack_forget()
            self.supplier_treeview.update_table(database.fetch_data(sql_commands.get_supplier_info))
            self.supplier_treeview.pack()
            self.refresh_btn.after(100,lambda:self.refresh_btn.configure(state = ctk.NORMAL))

        def view_supplier_record():
                if self.supplier_treeview.get_selected_data():
                    self.view_supplier_popup.place(relx=0.5, rely=0.5, anchor="c", record_id = self.supplier_treeview.get_selected_data()[0])
                else:
                    messagebox.showwarning('Warning','No record is selected', parent = self) 
                    
        self.main_frame = ctk.CTkFrame(self.supplier_frame, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(2,weight=1) 
               
        self.add_item_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Add Supplier",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command=lambda: self.new_supplier_popup.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_item_btn.grid(row=1, column=2, sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width=height*0.05, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", hover_color=Color.Green_Button_Hover_Color,
                                              command=refresh_supplier_table)
        self.refresh_btn.grid(row=1, column=1, sticky="w")
            
        self.view_btn = ctk.CTkButton(self.main_frame,width=width*0.085, height = height*0.05, text="View Record", font=("DM Sans Medium", 14), command=view_supplier_record)
        self.view_btn.grid(row=1, column=3, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.treeview_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

        self.supplier_treeview = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .8, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/SupplierNo:{int(width*.115)}-tc/SupplierName:x-tl/ContactPerson:{int(width*.15)}-tl/ContactNumber:{int(width*.135)}-tc/Address:{int(width*.185)}-tl!33!35')
        self.supplier_treeview.pack()
        
        self.supplier_treeview.update_table(database.fetch_data(sql_commands.get_supplier_info))
        
        self.supplier_search_bar = cctk.cctkSearchBar(self.main_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=supplier_search_callback,
                                                close_command_callback=refresh_supplier_table, 
                                                quary_command=sql_commands.get_supplier_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
        self.supplier_search_bar.grid(row=1, column=0,sticky="nsew", padx=(width*0.005), pady=(width*0.005))
        
        #endregion
        
        self.search_bars = [self.inv_search_bar, self.rs_search_bar, self.supplier_search_bar]
        
        '''POP UP INITIALIZATION'''
        self.disposal_confirmation = Inventory_popup.item_disposal_confirmation(self,(width, height, acc_cred, acc_info), command_callback=disposal_table_callback)
        self.disposal_popup = Inventory_popup.disposal_history(self, (width, height, acc_cred, acc_info))
        self.history_popup = Inventory_popup.receive_history(self, (width, height, acc_cred, acc_info))
        self.cancel_orders = Inventory_popup.cancel_orders(self, (width, height, acc_cred, acc_info))
        self.restock_popup = Inventory_popup.restock(self, (width, height, acc_cred, acc_info), self.rs_data_view1, command_callback=refresh_rs_data_view1)
        self.dispose_popup = mini_popup.stock_disposal(self, (width, height, acc_cred, acc_info), update_table_callback)
        self.add_item_popup = Inventory_popup.add_item(self, (width, height, acc_cred, acc_info), command_callback=update_table_callback)
        self.supplier_list_popup = Inventory_popup.supplier_list(self,(width, height, acc_cred, acc_info))
        self.category_popup = Inventory_popup.show_category(self, (width, height, acc_cred, acc_info))
        self.restock_confirm = Inventory_popup.restock_confirmation(self, (width, height, acc_cred, acc_info), command_callback=restocking_callback)
        self.disposal_confirm_popup = Inventory_popup.disposal_confirmation(self,(width, height, acc_cred, acc_info), command_callback=refresh_rs_data_view1)
        self.order_info = Inventory_popup.order_info_screen(self, (width, height))
        self.new_supplier_popup = Inventory_popup.new_supplier(self, (width, height, acc_cred, acc_info), command_callback=refresh_supplier_table)
        self.view_supplier_popup = Inventory_popup.view_supplier(self, (width, height, acc_cred, acc_info), command_callback=refresh_supplier_table)
        self.authorization = mini_popup.authorization(self,(width, height), command_callback=lambda:self.disposal_confirmation.place(relx=0.5, rely=0.5, anchor='c', data='Expired'))
        
        sort_status_callback("View by Levels")
        load_main_frame(0)

    def update_order_treeview(self):
        pass
    def update_disposal_treeview(self):
        self.ds_data_view1.update_table(sql_commands.get_disposed_filter, (self.ds_sort_category_option.get(), self.ds_sort_type_option.get(), self.from_date_select_entry._text, self.to_date_select_entry._text))
    
    
    def update_tables(self):
        for i in mainframes:
            if isinstance(i, dashboard_frame):
                temp: dashboard_frame = i
                temp.show_pie()
                temp.generate_stat_tabs()
                temp.generate_DISumarry()
                temp.load_saled_data_treeview()
                temp.load_scheduled_service()
            if isinstance(i, reports_frame):
                temp: reports_frame = i
                temp.graphs_need_upgrade()
                temp.update_invetory_graph()
            if isinstance(i, sales_frame):
                temp: sales_frame = i
                temp.update_table()
            if isinstance(i, histlog_frame):
                temp: histlog_frame = i
                temp.load_both()
  
class patient_info_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.sort_status=["Sort by Owner", "Sort by Pet Name", "Sort by ID"]
        
        
        def update_table():
            self.refresh_btn.configure(state = "disabled")
            sort_status_callback(self.sort_type_option.get())
            
            
        def sort_table(sql):
            self.pet_data_view.pack_forget()
            self.data = database.fetch_data(sql)
            self.pet_data_view.update_table(self.data)
            self.pet_data_view.pack()
            self.refresh_btn.after(100, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            
        def search_bar_callback():
            matched_res = []
             
            if len(self.search_bar.get()) == 1:
                self.record_view.place(relx = .5, rely = .5, anchor = 'c', pet_data=self.search_bar.get()[0])
            else:
                for res in self.search_bar.get():
                    for data in self.data:
                        if set(res).issubset(data):
                             matched_res.append(data)
                self.pet_data_view.pack_forget()
                self.pet_data_view.update_table(matched_res)
                self.pet_data_view.pack()
        def sort_status_callback(var):
            if self.sort_status[0] in var:
                sort_table(sql_commands.get_pet_record)
            elif self.sort_status[1]  in var:
                sort_table(sql_commands.get_pet_info_sort_by_pet_name)
            elif self.sort_status[2] in var: 
                sort_table(sql_commands.get_pet_info_sort_by_id)
        
        self.search_quary = sql_commands.get_pet_record_search_query

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        
        self.search_var = ctk.StringVar()
        self.sort_status_var = ctk.StringVar(value="Sort by Owner")

        self.close = ctk.CTkImage(light_image=Image.open("image/close.png"),size=(16,16))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.supplier_icon_ = ctk.CTkImage(light_image= Image.open("image/supplier.png"), size=(24,24))
        self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(22,25))
        self.gen_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(18,20))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, padx=(width*0.005), pady=(height*0.01))

        '''SEARCH FRAME'''
        self.top_frame =ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.06, corner_radius=0)
        self.top_frame.grid(row=0, column=0, sticky="nsw", padx=(width*0.005,0), pady=(height*0.01,0))
        
        self.refresh_btn = ctk.CTkButton(self.top_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=update_table, hover_color=Color.Green_Button_Hover_Color)
            
        self.add_record_btn = ctk.CTkButton(self.top_frame, width=width*0.08, height = height*0.05, text="Add Record",image=self.add_icon, font=("DM Sans Medium", 14),
                                            command=lambda:self.new_record.place(relx = .5, rely = .5, anchor = 'c'))
        
    
        self.view_record_btn = ctk.CTkButton(self.top_frame, text="View Record", image=self.gen_icon, font=("DM Sans Medium", 14), width=width*0.1,height = height*0.05,
                                              command=self.view_record)
        
        self.content_frame =ctk.CTkFrame(self,fg_color=Color.White_Lotion,corner_radius=0)
        self.content_frame.grid(row=1, column=0, columnspan=5,sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        self.sort_frame = ctk.CTkFrame(self.content_frame, height = height*0.05, fg_color=Color.Platinum)
        self.sort_frame.grid(row=0, column=0, padx=(width*0.005), pady=(0,height*0.007), sticky="nsw")

        self.sort_type_option= ctk.CTkOptionMenu(self.sort_frame, values=self.sort_status, anchor="center", font=("DM Sans Medium", 12), width=width*0.115, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=partial(sort_status_callback))
        self.sort_type_option.grid(row=0, column=0, padx=(width*0.0045), pady=(height*0.0065), sticky="e")
        
        '''TREEVIEW'''
        self.treeview_frame =ctk.CTkFrame(self.content_frame,fg_color="transparent",corner_radius=0)
        self.treeview_frame.grid(row=1, column=0, columnspan=5,sticky="nsew",padx=(width*0.005), pady=(0, height*0.01))

        self.data = database.fetch_data(sql_commands.get_pet_record)
        
        self.pet_data_view = cctk.cctkTreeView(self.treeview_frame, data=self.data,width= width * .805, height= height * .79, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/PetID:{int(width*.075)}-tc/PetName:x-tl/PetBreed:{int(width*.2)}-tl/OwnerName:{int(width*.15)}-tl/ContactNumber:{int(width*.115)}-tc!33!35',)
        self.pet_data_view.pack()
        
        '''BOTTOM FRAME'''
        """ 
        self.bot_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent",)
        self.bot_frame.grid(row=2, column=0, columnspan=5,sticky="nsew",padx=(width*0.005), pady=(0, height*0.01))
        
        self.page_counter = cctk.cctkPageNavigator(self.bot_frame,  width=width*0.115, height=height*0.055, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                             font=("DM Sans Medium", 16), page_limit=1)
        self.page_counter.pack() """
        
        self.search_bar = cctk.cctkSearchBar(self.top_frame, height=height*0.055, width=width*0.3, m_height=height, m_width=width,  command_callback=search_bar_callback, fg_color=Color.Platinum,
                                             quary_command=self.search_quary, dp_width=width*0.25, place_height=height*0.0125, place_width=width*0.006, font=("DM Sans Medium", 14))
        self.search_bar.pack(side="left", padx=(width*0.005), pady=(height*0.01, height*0.0115))
        
        self.refresh_btn.pack(side="left")
        self.add_record_btn.pack(side="left",padx=(width*0.005), pady=(height*0.01))
        self.view_record_btn.pack(side="left",padx=(0,width*0.005), pady=(height*0.01))
        
        self.new_record = Pet_info_popup.new_record(self, (width, height, acc_cred, acc_info), update_table)
        self.record_view = Pet_info_popup.view_record(self, (width, height, acc_cred, acc_info), update_table)
        
    def update(self) -> None:
        self.data = database.fetch_data(sql_commands.get_pet_record)
        self.pet_data_view.update_table(self.data)
        return super().update()
    
    def view_record(self):
        pet_data = self.pet_data_view.get_selected_data()
        if pet_data:
            self.record_view.place(relx = .5, rely = .5, anchor = 'c', pet_data=pet_data)
        else:
            messagebox.showwarning('Warning','No Record is selected', parent = self)

class reports_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        '''constants'''
        self.months = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]
        self.days = [*range(1, 13, 1)]
        

        '''variables'''
        self.data_loading_manager: List[bool] = [False for _ in range(3)]
        self.previous_date = '0';
        self.previous_month = '0';
        self.previous_year = '0';

        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.generate_report_icon = ctk.CTkImage(light_image=Image.open("image/gen_report.png"),size=(26,26))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.sales_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])
        self.inventory_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])

        self.sales_report_frame.grid_columnconfigure(0, weight=1)
        self.sales_report_frame.grid_rowconfigure((1,2), weight=1)

        self.inventory_report_frame.grid_columnconfigure(1, weight=1)
        self.inventory_report_frame.grid_rowconfigure(1, weight=1)

        self.report_frames=[self.sales_report_frame, self.inventory_report_frame]
        self.active_report = None

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.daily_pie_canvas = None
        self.daily_hbar_canvas = None
        self.monthly_vbar_canvas = None
        self.yearly_vbar_canvas = None

        selected_color = Color.Blue_Yale

        '''events'''
        self.label=["Items", "Services"]
        self.info = [width*0.0055,height*0.005,Color.White_Platinum]

        monthly_label = [*range(1, calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[-1]+1, 1)]
        monthly_data_items = [database.fetch_data(sql_commands.get_items_daily_sales_sp, (f'2023-07-{s}',))[0][0] or 0 for s in monthly_label]
        monthly_data_service = [database.fetch_data(sql_commands.get_services_daily_sales_sp, (f'2023-07-{s}',))[0][0] or 0 for s in monthly_label]

        yearly_data_items = [database.fetch_data(sql_commands.get_items_monthly_sales_sp, (s, datetime.datetime.year))[0][0] or 0 for s in self.months]
        yearly_data_service = [database.fetch_data(sql_commands.get_services_monthly_sales_sp, (s, datetime.datetime.year))[0][0] or 0 for s in self.months]

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row =1, column =0, sticky = 'nsew',padx=width*0.005, pady=height*0.005)

        def report_menu_callback(report_type):
            if "Daily" in report_type:
                self.refresh_btn.pack_forget()
                self.monthly_graph.grid_forget()
                self.month_option.pack_forget()
                self.year_option.pack_forget()
                self.yearly_graph.grid_forget()
                self.daily_data_view.pack()
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack_forget()
                self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.date_selected_label.pack(side="left", padx=(0, width*0.005))
                self.show_calendar.pack(side="left",  padx=(0, width*0.005))
                self.refresh_btn.pack(side="left",  padx=(0, width*0.0025))

            elif "Monthly" in report_type:
                self.refresh_btn.pack_forget()
                self.date_selected_label.pack_forget()
                self.show_calendar.pack_forget()
                self.daily_graph.pack_forget()
                self.daily_data_view.pack_forget()
                self.yearly_graph.grid_forget()
                self.yearly_data_view.pack_forget()
                self.year_option.pack_forget()
                self.monthly_data_view.pack()
                self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.month_option.pack(side="left", padx=(0, width*0.005))
                self.year_option.pack(side="left", padx=(0, width*0.005))
                self.refresh_btn.pack(side="left",  padx=(0, width*0.0025))

            elif "Yearly" in report_type:
                self.refresh_btn.pack_forget()
                self.date_selected_label.pack_forget()
                self.show_calendar.pack_forget()
                self.month_option.pack_forget()
                self.daily_graph.pack_forget()
                self.daily_data_view.pack_forget()
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack()
                self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.year_option.pack(side="left", padx=(0, width*0.005))
                self.refresh_btn.pack(side="left",  padx=(0, width*0.0025))

            self.update_graphs()

        def set_date():
            cctk.tk_calendar(self.date_selected_label,"%s", date_format="word", max_date = datetime.date.today(),
                             set_date_callback= self.update_graphs,
                             date_select_default= datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y'))

        operational_year = [str(s[0]) for s in database.fetch_data(sql_commands.get_active_year_transaction)] or [str(datetime.datetime.now().year)]
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]


        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")


        self.sales_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.sales_report_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.sales_report_button.configure(command=partial(load_main_frame, 0))
        self.sales_report_icon = ctk.CTkLabel(self.sales_report_button, text="",image=self.sales_icon)
        self.sales_report_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.sales_report_label = ctk.CTkLabel(self.sales_report_button, text="SALES REPORT", text_color="white", font=("DM Sans Medium", 14))
        self.sales_report_label.pack(side="left")
        self.sales_report_button.grid()
        self.sales_report_button.update_children()

        self.inventory_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_report_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_report_button.configure(command=partial(load_main_frame, 1))
        self.inventory_report_icon = ctk.CTkLabel(self.inventory_report_button, text="",image=self.inventory_icon)
        self.inventory_report_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_report_label = ctk.CTkLabel(self.inventory_report_button, text="INVENTORY REPORT", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_report_label.pack(side="left")
        self.inventory_report_button.grid()
        self.inventory_report_button.update_children()

        self.button_manager = cctku.button_manager([self.sales_report_button, self.inventory_report_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        '''SALES REPORT'''
        self.report_option_var = ctk.StringVar(value="Daily Report")
        
        self.top_con_frame = ctk.CTkFrame(self.sales_report_frame, fg_color="transparent")
        self.top_con_frame.grid(row=0, column=0, sticky="nsew", pady=(height*0.005,0) )

        self.sales_report_top = ctk.CTkFrame(self.top_con_frame, fg_color=Color.White_Platinum, height=height*0.0575)
        self.sales_report_top.pack(side="left", fill="y")
        
        self.report_type_menu = ctk.CTkOptionMenu(self.sales_report_top, values=["Daily Report", "Monthly Report", "Yearly Report"], variable=self.report_option_var,anchor="center",
                                                  font=("DM Sans Medium",14), height=height*0.045, width=width*0.135,
                                                  command= report_menu_callback)
        self.report_type_menu.pack(side="left", padx=(width*0.003, width*0.005))

        self.date_selected_label = ctk.CTkLabel(self.sales_report_top, text=f"{date.today().strftime('%B %d, %Y')}", fg_color=Color.White_Color[3], corner_radius=5, height=height*0.045, font=("DM Sans Medium",14),
                                                width=width*0.125)
        self.date_selected_label.pack(side="left", padx=(0, width*0.005))

        self.show_calendar = ctk.CTkButton(self.sales_report_top, text="", image=self.calendar_icon, height=height*0.045, width=width*0.025, command=set_date)
        self.show_calendar.pack(side="left",  padx=(0, width*0.0025))

        self.refresh_btn = ctk.CTkButton(self.sales_report_top, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command= lambda: self.update_graphs(True))
        #self.refresh_btn.grid(row=0, column=1, sticky="w",  padx=(width*0.0025), pady=(height*0.005,0))
        
        self.show_gen_report = ctk.CTkButton(self.top_con_frame, image=self.generate_report_icon, width=width*0.125,  text="Generate Report", height=height*0.0575, font=("DM Sans Medium", 14),
                                             command = lambda: self.save_as_popup.place(daily_selected_date = self.date_selected_label._text, month_selected_date = self.month_option.get(),year_selected_date = self.year_option.get(), relx = .5, rely = .5, anchor = 'c', default_config = self.report_type_menu.get()))
        self.show_gen_report.pack(side="right")
        #generating reports end

        self.month_option = ctk.CTkOptionMenu(self.sales_report_top, values= self.months, anchor="center", width=width*0.1, font=("DM Sans Medium",14), height=height*0.045, command= self.update_graphs)
        self.month_option.set(f"{date.today().strftime('%B')}")
        self.year_option = ctk.CTkOptionMenu(self.sales_report_top, values=operational_year, width=width*0.075, font=("DM Sans Medium",14), height=height*0.045, anchor="center", command= self.update_graphs)
        self.year_option.set(f"{date.today().strftime('%Y')}")

        self.daily_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
        self.daily_graph.grid_columnconfigure((3), weight=2)
        self.daily_graph.grid_rowconfigure((0), weight=1)

        self.sales_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color=Color.White_Platinum)
        self.sales_daily_graph.grid(row=0, column= 0,columnspan=3, sticky="nsew",  padx=(width*0.005,0), pady=(height*0.01))

        self.items_total = ctk.CTkLabel(self.daily_graph,  text=f"Item:        {format_price(self.data[0])}", corner_radius=5, fg_color=Color.Light_Green,  font=("DM Sans Medium",14), height=height*0.05)
        self.items_total.grid(row=1, column=0, sticky="nsew", padx=(width*0.005,0), pady=(0,height*0.007))
        self.service_total = ctk.CTkLabel(self.daily_graph,text=f"Services     {format_price(self.data[1])}", corner_radius=5, fg_color=Color.Blue_Cornflower,  font=("DM Sans Medium",14), height=height*0.05)
        self.service_total.grid(row=1, column=1, sticky="nsew",padx=(width*0.005), pady=(0,height*0.007))
        self.income_total = ctk.CTkLabel(self.daily_graph,text=f"Total    {format_price(self.data[0] + self.data[1])}", corner_radius=5, fg_color=Color.White_Lotion,  font=("DM Sans Medium",14), height=height*0.05)
        self.income_total.grid(row=1, column=2, sticky="nsew", pady=(0,height*0.007))

        self.bars_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color=Color.White_Platinum, height=height*0.35)
        self.bars_daily_graph.grid(row=0, column= 3, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
        self.bars_daily_graph.pack_propagate(0)

        self.data_frame = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum, corner_radius=0, height=height*0.35)
        self.data_frame.grid(row=2, column=0, sticky="nsew", columnspan = 2,pady=(0, height*0.0075))

        self.daily_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.8, height=height *0.4,
                                           column_format=f'/No:{int(width*0.035)}-#c/OR:{int(width*0.095)}-tc/Client:x-tl/Item:{int(width*.115)}-tr/Service:{int(width*.115)}-tr/Discount:{int(width*0.115)}-tr/Total:{int(width*0.135)}-tr!33!35')
        self.daily_data_view.pack()


        self.monthly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.monthly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.8, height=height *0.5,
                                           column_format=f"/No:{int(width*.035)}-#c/Date:x-tl/Item:{int(width*.115)}-tr/Service:{int(width*.115)}-tr/Discount:{int(width*.115)}-tr/Total:{int(width*.135)}-tr!33!35")
        self.monthly_data_view.pack()

        self.monthly_vbar_canvas = self.show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=monthly_label)
        self.monthly_vbar_canvas.get_tk_widget().pack(pady=(10))

        self.yearly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.yearly_data_view = cctk.cctkTreeView(self.data_frame,  width=width*0.8, height=height *0.5,
                                           column_format=f"/No:{int(width*.035)}-#c/Month:x-tl/Item:{int(width*.115)}-tr/Service:{int(width*.115)}-tr/Discount:{int(width*.115)}-tr/Total:{int(width*.135)}-tr!33!35")
        self.yearly_data_view.pack()

        self.yearly_vbar_canvas = self.show_bar(self.yearly_graph, data_item=yearly_data_items, data_service=yearly_data_service, info=[width*0.01,height*0.005,Color.White_Platinum], label=self.months)
        self.yearly_vbar_canvas.get_tk_widget().pack(pady=(10))
        report_menu_callback("Daily")

        #region: inv rep
        '''INVENTORY REPORT'''
        """  self.search_frame = ctk.CTkFrame(self.inventory_report_frame,width=width*0.3, height = height*0.05, fg_color=Color.White_Platinum)
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.0025), pady=(height*0.005,0))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0,font=("DM Sans Medium", 14), text_color="black", fg_color=Color.White_Color[3])
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1) """

        self.rep_refresh_btn = ctk.CTkButton(self.inventory_report_frame, text="", width=width*0.03, height = height*0.0575, image=self.refresh_icon, fg_color="#83BD75")
        self.rep_refresh_btn.grid(row=0, column=1, sticky="w", pady=(height*0.005), padx=(width*0.005))
        
        self.generate_rep_btn = ctk.CTkButton(self.inventory_report_frame,  image=self.generate_report_icon, width=width*0.175,  text="Generate Inventory Report", height=height*0.0575, font=("DM Sans Medium", 14),
                                              command = lambda: self.save_as_inventory_rep_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.generate_rep_btn.grid(row=0, column=0, sticky="w", pady=(height*0.005))

        #self.receive_btn = ctk.CTkButton(self.inventory_report_frame, text="Receive History", height=height*0.0575, font=("DM Sans Medium", 14),
        #                                      command = lambda: self.receive_report.place(relx= 0.5, rely=0.5, anchor='c'))
        #self.receive_btn.grid(row=0, column=2, sticky="w", pady=(height*0.005))

        self.bought_item_con_col = None

        self.rep_treeview_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="transparent")
        self.rep_treeview_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=(width*0.0025), pady=(height*0.005,0))

        self.inventory_rep_treeview = cctk.cctkTreeView(self.rep_treeview_frame, width=width*0.8, height=height *0.8,
                                           column_format=f"/No:{int(width*.025)}-#c/ItemID:{int(width*.1)}-tc/ItemName:x-tl/CurrentStockPcs:{int(width*.125)}-tr!33!35")
        self.inventory_rep_treeview.pack()
        
        self.update_invetory_graph()
        self.update_invetory_graph()
        #endregion


        self.save_as_popup = save_as_popup.show_popup(self, (width , height), acc_cred[0][0], acc_info[0][1], acc_info[0][2])
        self.save_as_inventory_rep_popup = save_as_popup.show_popup_inventory(self, (width, height), acc_cred[0][0], acc_info[0][1], acc_info[0][2])
        self.receive_report = Inventory_popup.receive_report(self, (width, height, acc_cred, acc_info))
        
        load_main_frame(0)

    def update_invetory_graph(self):
        current_stock = database.fetch_data(sql_commands.get_inventory_report)
        #bought_item = database.fetch_data(sql_commands.get_all_bought_items_group_by_name)
        #bought_item_dict = {s[0]: s[1] for s in bought_item}
        #bought_item_con_col = {1: {s[0]: 'blue' for s in bought_item}}

        #inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item_dict else bought_item_dict[s[0]]), s[1]) for s in current_stock]
        #self.inventory_rep_treeview._conditional_colors = bought_item_con_col
        self.inventory_rep_treeview.update_table(current_stock)


    def show_pie(self, data = None):
        if(self.daily_pie_canvas is not None):
            self.daily_pie_canvas.get_tk_widget().destroy()
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)] if data is None else data
        height = self.info[1]
        width =self.info[0]
        fg_color = self.info[2]

        data = self.data if self.data[0] + self.data[1] > 0 else [0,1]

        label = self.label
        pie_figure= Figure(figsize=(width, height), dpi=100)
        pie_figure.set_facecolor(fg_color)
        ax =pie_figure.add_subplot(111)
        #ax.pie(data, labels=label, autopct='%1.1f%%', startangle=90,counterclock=0, textprops={'fontsize':12, 'color':"black", 'family':'monospace'}, colors=[Color.Light_Green,Color.Blue_Cornflower])
        
        #pie chart copied from dashboard
        ax.pie(data, labels=label, autopct=f"{'%1.1f%%'if self.data[0] + self.data[1] > 0 else ''}", 
               startangle=90, counterclock=0, explode=(0.1,0), colors=[Color.Light_Green, Color.Blue_Cornflower] if self.data[0] + self.data[1] > 0 else [Color.White_Gray],
                textprops={'fontsize':17, 'color': Color.Blue_Maastricht, 'family':'monospace', 'weight':'bold' },)

        self.daily_pie_canvas = FigureCanvasTkAgg(pie_figure, self.sales_daily_graph,)
        self.daily_pie_canvas.draw()
        self.daily_pie_canvas.get_tk_widget().pack()

    def show_hbar(self, data = None):
        if self.daily_hbar_canvas is not None:
            self.daily_hbar_canvas.get_tk_widget().destroy()
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)] if data is None else data

        height = self.info[1]
        width =self.info[0]
        fg_color = self.info[2]

        #data = self.data if self.data[0] + self.data[1] > 0 else [0,1]
        label = self.label

        bar_figure= Figure(figsize=(width, height), dpi=100)
        bar_figure.set_facecolor(fg_color)
        ax =bar_figure.add_subplot(111)
        ax.barh(label, self.data, align='center',  color=[Color.Light_Green,Color.Blue_Cornflower])
        #ax.set_xlabel("Income")
        self.daily_hbar_canvas = FigureCanvasTkAgg(bar_figure, self.bars_daily_graph)
        self.daily_hbar_canvas.draw()
        self.daily_hbar_canvas.get_tk_widget().pack()

    def show_bar(self, master, data_service, data_item, info=[], label=[]):
        height = info[1]
        width =info[0]
        fg_color = info[2]

        _label = label
        _data_service = data_service
        _data_item = data_item

        x_axis = np.arange(len(_label))

        bar_figure= Figure(figsize=(width, height), dpi=100)
        bar_figure.set_facecolor(fg_color)
        ax = bar_figure.add_subplot(111)

        ax.bar(x_axis-0.2, _data_item, width=0.4, label=_label[0], color=Color.Light_Green)
        ax.bar(x_axis+0.2, _data_service, width=0.4, label = _label[1], color= Color.Blue_Cornflower)
        ax.legend(["Item Sales", "Services"])
        ax.set_xticks(x_axis,_label)
        #ax.set_xlabel("Income")

        canvas = FigureCanvasTkAgg(bar_figure, master)
        #canvas.draw()
        canvas.get_tk_widget().pack(pady=(10))
        return canvas
    
    def update_graphs(self, force_reload: bool = False):
        self.refresh_btn.configure(state = ctk.DISABLED)
        force_reload = str(force_reload) == 'True'
        #as some of the caller of the function return their value, this will recheck the bool of the argument

        if 'Daily' in self.report_option_var.get():
            if not self.data_loading_manager[0] or self.date_selected_label._text != self.previous_date or force_reload:
                date = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%Y-%m-%d')
                self.data = [float(database.fetch_data(sql_commands.get_items_daily_sales_sp, (date,))[0][0] or 0),
                            float(database.fetch_data(sql_commands.get_services_daily_sales_sp, (date,))[0][0] or 0)]
                self.show_pie(self.data)
                self.show_hbar(self.data)
                self.items_total.configure(text=f"Item:        {format_price(self.data[0])}")
                self.service_total.configure(text=f"Services:        {format_price(self.data[1])}")
                self.income_total.configure(text=f"Total:        {format_price(self.data[0]+self.data[1])}")
                #self.daily_data_view.update_table(self.data) for adding data in the bottom treeview
                self.previous_date = self.date_selected_label._text
                self.data_loading_manager[0] = True
                self.daily_data_view.update_table(database.fetch_data(sql_commands.daily_report_treeview_data, (date, )))

        if 'Monthly' in self.report_option_var.get():
            if not self.data_loading_manager[1] or (self.year_option.get()+self.month_option.get()) != self.previous_year+self.previous_month or force_reload:
                m = datetime.datetime.strptime(self.month_option.get(), '%B').strftime('%m')
                y = self.year_option.get()
                monthly_label = [*range(1, calendar.monthrange(datetime.datetime.now().year, int(m))[-1]+1, 1)]
                monthly_data_items = [database.fetch_data(sql_commands.get_items_daily_sales_sp, (f'{y}-{m}-{s}',))[0][0] or 0 for s in monthly_label]
                monthly_data_service = [database.fetch_data(sql_commands.get_services_daily_sales_sp, (f'{y}-{m}-{s}',))[0][0] or 0 for s in monthly_label]

                self.monthly_vbar_canvas.get_tk_widget().destroy()
                self.monthly_vbar_canvas = self.show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=monthly_label)
                self.monthly_vbar_canvas.get_tk_widget().pack()

                self.data_loading_manager[1] = True
                self.previous_month = self.month_option.get()
                self.previous_year = self.year_option.get()
                self.monthly_data_view.update_table(database.fetch_data(sql_commands.monthly_report_treeview_data, (m, y)))

        if 'Yearly' in self.report_option_var.get():
            if not self.data_loading_manager[2] or self.year_option.get() != self.previous_year or force_reload:
                y = self.year_option.get()

                monthly_data_items = [database.fetch_data(sql_commands.get_items_monthly_sales_sp, (self.months.index(s)+1, y))[0][0] or 0 for s in self.months]
                monthly_data_service = [database.fetch_data(sql_commands.get_services_monthly_sales_sp, (self.months.index(s)+1, y))[0][0] or 0 for s in self.months]

                self.yearly_vbar_canvas.get_tk_widget().destroy()
                self.yearly_vbar_canvas = self.show_bar(self.yearly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=self.months)
                self.yearly_vbar_canvas.get_tk_widget().pack()

                self.data_loading_manager[2] = True
                self.previous_year = self.year_option.get()
                self.yearly_data_view.update_table(database.fetch_data(sql_commands.yearly_report_treeview_data, (y, )))
        #set the previous selection to avoid repeating load
        self.refresh_btn.after(5000, lambda:self.refresh_btn.configure(state = ctk.NORMAL))


    def graphs_need_upgrade(self):
        self.data_loading_manager = [False for _ in range(3)]
        print("RUNNING")
        self.update_graphs(True)

class user_setting_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        selected_color = Color.Blue_Yale
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
        self.accounts_icon = ctk.CTkImage(light_image=Image.open("image/accounts.png"), size=(24,24))
        self.account_creation_icon = ctk.CTkImage(light_image = Image.open("image/create_acc.png"), size=(24,24))
        self.roles_icon = ctk.CTkImage(light_image = Image.open("image/role.png"), size=(24,24))
        self.deactivated_icon = ctk.CTkImage(light_image = Image.open("image/deact.png"), size=(24,24))

        '''TAB SETUP'''
        self.base_frame = ctk.CTkFrame(self, corner_radius=0,fg_color=Color.White_Lotion)
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(0, weight=1)

        self.account_base_frame = acc_creation.accounts_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.acc_creation_frame = acc_creation.creation_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.role_account_frame = acc_creation.roles_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.deactivated_frame = acc_creation.deactivated_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)

        self.report_frames=[self.account_base_frame, self.acc_creation_frame, self.role_account_frame, self.deactivated_frame]
        self.active_report = None

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row=0, column=0, sticky="nsew")

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(4, weight=1)
        
        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=6, sticky="nsew")
        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15), fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=5, sticky="n")

        '''ACCOUNTS BUTTON TAB'''
        self.accounts_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.accounts_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.accounts_button.configure(command=partial(load_main_frame, 0))
        self.account_tab_icon = ctk.CTkLabel(self.accounts_button, text="",image=self.accounts_icon)
        self.account_tab_icon.pack(side="left", padx=(width*0.01,width*0.0025))
        self.accounts_label = ctk.CTkLabel(self.accounts_button, text="ACCOUNTS", text_color="white",font=('DM Sans Medium', 14))
        self.accounts_label.pack(side="left")
        self.accounts_button.grid()
        self.accounts_button.update_children()
        
        '''ACCOUNT CREATION TAB'''
        self.account_creation_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125, fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.account_creation_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.account_creation_button.configure(command=partial(load_main_frame, 1))
        self.account_creation_tab_icon = ctk.CTkLabel(self.account_creation_button, text="",image=self.account_creation_icon)
        self.account_creation_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.account_creation_label = ctk.CTkLabel(self.account_creation_button, text="CREATION", text_color="white",font=('DM Sans Medium', 14))
        self.account_creation_label.pack(side="left")
        self.account_creation_button.grid()
        self.account_creation_button.update_children()

        '''ROLES CREATION TAB'''
        self.roles_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.roles_button.grid(row=0, column=2, sticky="s", padx=(0,width*0.0025), pady=0)
        self.roles_button.configure(command=partial(load_main_frame, 2))
        self.roles_tab_icon = ctk.CTkLabel(self.roles_button, text="",image=self.roles_icon)
        self.roles_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.roles_label = ctk.CTkLabel(self.roles_button, text="ROLES", text_color="white",font=('DM Sans Medium', 14))
        self.roles_label.pack(side="left")
        self.roles_button.grid()
        self.roles_button.update_children()

        '''DEACTIVATED TAB'''
        self.deactivated_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.135, fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.deactivated_button.grid(row=0, column=3, sticky="s", padx=(0,width*0.0025), pady=0)
        self.deactivated_button.configure(command=partial(load_main_frame, 3))
        self.deactivated_tab_icon = ctk.CTkLabel(self.deactivated_button, text="",image=self.deactivated_icon)
        self.deactivated_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.deactivated_label = ctk.CTkLabel(self.deactivated_button, text="DEACTIVATED", text_color="white",font=('DM Sans Medium', 14))
        self.deactivated_label.pack(side="left")
        self.deactivated_button.grid()
        self.deactivated_button.update_children()

        self.button_manager = cctku.button_manager([self.accounts_button, self.account_creation_button, self.roles_button, self.deactivated_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        """
        self.creationFrame = acc_creation.creation_frame(self.acc_creation_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.creationFrame.grid(row=1, column=1, sticky="w")

        self.rolesFrame = acc_creation.roles_frame(self.roles_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.rolesFrame.grid(row=1, column=1, sticky="w")

        self.deactivatedFrame = acc_creation.deactivated_frame(self.deactivated_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.deactivatedFrame.grid(row=1, column=1, sticky="w")
        #self.changeFrame.usn_option.configure(values = [s [0] for s in database.fetch_data('SELECT usn from acc_cred')], command = set_checkBox)
        #self.changeFrame.accept_button.configure(state = ctk.DISABLED, command = update_staff_acc);

        #account creation tab
        #account creation frame
        self.box_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="white")
        self.box_frame.pack(fill=tk.BOTH, expand=True)

        def create_new_acc():
            password1 = encrypt.pass_encrypt(self.acc_create.name_entry.get())
            aula = (self.acc_create.name_entry.get(),)
            temp = []
            for i in range(len(self.acc_create.access_lvls)):
                temp.append(self.acc_create.check_boxes[self.acc_create.access_lvls[i]].get())
            aula = aula + tuple(temp);
            database.exec_nonquery([['INSERT INTO acc_cred VALUES(?, ?, ?, NULL)',(self.acc_create.name_entry.get(), password1['pass'], password1['salt'])],
                                    ['INSERT INTO acc_info VALUES(?, ?, ?)', (self.acc_create.name_entry.get(), self.acc_create.name_entry.get(), self.acc_create.position_option.get())],
                                    ['INSERT INTO account_access_level VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', aula]])
            #add_new_acc()
            #clear_acc_creation_fields()
            #get_staff_name()
            #refresh_staff_names()

        '''ACCOUNT CREATION: START'''
        
        '''temporary implementation'''
        
        def enable_checkboxes(e:any = None):
            data = database.fetch_data('SELECT * FROM user_level_access WHERE Title = ?', (self.acc_create.position_option.get(),))[0]

            self.acc_create.access_lvls
            self.acc_create.check_boxes
            for i in range(len(self.acc_create.access_lvls)):
                if data[i+2] == 1:
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(state = ctk.NORMAL) 
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].select(False)
                else:
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].deselect(False)
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(state = ctk.DISABLED)
                #self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(value = data[i + 2])

        self.acc_create = acc_creation.creation_frame(self.box_frame, width * .85, height * .82, 5, fg_color= 'light grey')
        self.acc_create.grid(row=1, column=1, sticky="w")
        '''
        roles_list = database.fetch_data('SELECT title FROM user_level_access')
        roles_list = [s[0] for s in roles_list]
        #roles = roles_list = [s[0] for s in roles_list]
        self.acc_create.position_option.set('Select Position');
        self.acc_create.position_option.configure(values = roles_list, command = enable_checkboxes)

        self.acc_create.accept_button.configure(command = create_new_acc)
        ''' """
        load_main_frame(0)

class histlog_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
        self.histlog = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
        self.action = ctk.CTkImage(light_image=Image.open("image/patient.png"), size=(18,21))
        self.calendar = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(17,18))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.action_log_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.log_history_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.attempts_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])

        self.action_log_frame.grid_columnconfigure(2, weight=1)
        self.action_log_frame.grid_rowconfigure(1, weight=1)
        
        self.log_history_frame.grid_columnconfigure(2, weight=1)
        self.log_history_frame.grid_rowconfigure(1, weight=1)

        self.attempts_frame.grid_columnconfigure(2, weight=1)
        self.attempts_frame.grid_rowconfigure(1, weight=1)
        
        self.report_frames=[self.action_log_frame, self.log_history_frame, self.attempts_frame]
        self.active_report = None
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        selected_color = Color.Blue_Yale

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)
            
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=4, sticky="n")


        self.action_log_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.13,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.action_log_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.action_log_button.configure(command=partial(load_main_frame, 0))
        self.action_log_icon = ctk.CTkLabel(self.action_log_button, text="",image=self.action)
        self.action_log_icon.pack(side="left", padx=(width*0.01,width*0.005)) 
        self.action_log_label = ctk.CTkLabel(self.action_log_button, text="ACTION HISTORY", text_color="white", font=("DM Sans Medium", 14))
        self.action_log_label.pack(side="left")
        self.action_log_button.grid()
        self.action_log_button.update_children()

        self.log_in_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.log_in_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.log_in_button.configure(command=partial(load_main_frame, 1))
        self.log_in_icon = ctk.CTkLabel(self.log_in_button, text="",image=self.histlog)
        self.log_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.log_in_label = ctk.CTkLabel(self.log_in_button, text="LOGIN HISTORY", text_color="white", font=("DM Sans Medium", 14))
        self.log_in_label.pack(side="left")
        self.log_in_button.grid()
        self.log_in_button.update_children()

        self.attempts_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.attempts_button.grid(row=0, column=2, sticky="s", padx=(0,width*0.0025), pady=0)
        self.attempts_button.configure(command=partial(load_main_frame, 2))
        self.attemps_button_lbl = ctk.CTkLabel(self.attempts_button, text="",image=self.histlog)
        self.attemps_button_lbl.pack(side="left", padx=(width*0.01,width*0.005))
        self.attempts_lbl = ctk.CTkLabel(self.attempts_button, text="LOGIN ATTEMPS", text_color="white", font=("DM Sans Medium", 14))
        self.attempts_lbl.pack(side="left")
        self.attempts_button.grid()
        self.attempts_button.update_children()

        self.button_manager = cctku.button_manager([self.action_log_button, self.log_in_button, self.attempts_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"))
        self.button_manager.click(self.button_manager._default_active, None)

        '''ACTION HISTORY - START'''
        
        self.sort_date_frame = ctk.CTkFrame(self.action_log_frame,width=width*0.25, height = height*0.055,fg_color=Color.Platinum)
        self.sort_date_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.sort_date_frame.pack_propagate(0)
        
        ctk.CTkLabel(self.sort_date_frame, text="Sort by Date:", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side="left", padx=(width*0.01, width*0.001),pady=(height*0.01))
        self.date_sort_label = ctk.CTkLabel(self.sort_date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, corner_radius=5, fg_color=Color.White_Lotion)
        self.date_sort_label.pack(side="left", fill="both", expand=1,pady=(height*0.0065),padx=(width*0.001) )
        
        self.date_button = ctk.CTkButton(self.sort_date_frame, text="", height=height*0.045, width=width*0.025, image=self.calendar,
                                         command=lambda: cctk.tk_calendar(self.date_sort_label, "%s", date_format="word", max_date=datetime.datetime.now(), set_date_callback= self.update_action_content))
        self.date_button.pack(side="left",padx=(0,width*0.005),pady=(height*0.0065))
        
        self.sort_role_frame = ctk.CTkFrame(self.action_log_frame, width=width*0.1,  height = height*0.055,fg_color=Color.Platinum)
        self.sort_role_frame.grid(row=0, column=1, sticky="nsew", padx=(0,width*0.005), pady=(height*0.01))
        
        roles = database.fetch_data('SELECT DISTINCT TITLE FROM user_level_access')
        roles = [s[0] for s in roles]

        self.sort_role_option = ctk.CTkOptionMenu(self.sort_role_frame, values= roles, anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts,
                                                 command= self.update_action_content)
        self.sort_role_option.pack(fill="both", expand=1,pady=(height*0.0065),padx=(width*0.0045))
        
        self.refresh_btn = ctk.CTkButton(self.action_log_frame,text="", width=width*0.03, height = height*0.055, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w",padx=(0,width*0.005), pady=(height*0.01))
        
        '''Table'''
        self.action_table_frame = ctk.CTkFrame(self.action_log_frame, fg_color=Color.Platinum)
        self.action_table_frame.grid(row=1, column=0,padx=(width*0.005), pady=(0,height*0.01), sticky="nsew", columnspan=3)
        self.action_table_frame.grid_columnconfigure(0, weight=1)
        self.action_table_frame.grid_rowconfigure(0, weight=1)
        
        self.action_table_style = ttk.Style()
        self.action_table_style.theme_use("clam")
        self.action_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
        self.action_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
        self.action_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
        self.action_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
        self.columns = ("rec_no", "username","role","action","time")
        self.column_names = ("No", "Username","Type", "Description", "Time")
        
            
        self.action_tree = ttk.Treeview(self.action_table_frame, columns=self.columns, show="headings",)
        
        for i in range(len(self.columns)):
            self.action_tree.heading(f"{self.columns[i]}", text=f"{self.column_names[i]}")

        self.action_tree.column("rec_no", width=int(width*0.01),anchor="w")
        self.action_tree.column("username", width=int(width*0.15), anchor="w")
        self.action_tree.column("role", width=int(width*0.18), anchor="w")
        self.action_tree.column("action", width=int(width*0.45), anchor="w")
        self.action_tree.column("time", width=int(width*0.15), anchor="c")
            
        self.action_tree.tag_configure("odd",background=Color.White_AntiFlash)
        self.action_tree.tag_configure("even",background=Color.White_Ghost)
            
        self.action_tree.grid(row=0, column=0, sticky="nsew")
            
        self.y_scrollbar = ttk.Scrollbar(self.action_table_frame, orient=tk.VERTICAL, command=self.action_tree.yview)
        self.action_tree.configure(yscroll=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")

        """Table End"""
        
        '''ACTION HISTORY - END'''
        
        '''LOGIN HISTORY - START'''
        
        self.sort_date_frame = ctk.CTkFrame(self.log_history_frame,width=width*0.25, height = height*0.055,fg_color=Color.Platinum)
        self.sort_date_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.sort_date_frame.pack_propagate(0)
        
        ctk.CTkLabel(self.sort_date_frame, text="Sort by Date:", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side="left", padx=(width*0.01, width*0.001),pady=(height*0.01))
        self.login_date_sort_label = ctk.CTkLabel(self.sort_date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, corner_radius=5, fg_color=Color.White_Lotion)
        self.login_date_sort_label.pack(side="left", fill="both", expand=1,pady=(height*0.0065),padx=(width*0.001) )
        
        self.date_button_log = ctk.CTkButton(self.sort_date_frame, text="", height=height*0.045, width=width*0.025, image=self.calendar,
                                         command=lambda: cctk.tk_calendar(self.login_date_sort_label, "%s", date_format="word", max_date=datetime.datetime.now(),
                                                                          set_date_callback= self.update_login_audit))
        self.date_button_log.pack(side="left",padx=(0,width*0.005),pady=(height*0.0065))
        
        self.refresh_btn = ctk.CTkButton(self.log_history_frame,text="", width=width*0.03, height = height*0.055, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1, sticky="w",padx=(0,width*0.005), pady=(height*0.01))
        
        '''Table'''
        
        self.login_table_frame = ctk.CTkFrame(self.log_history_frame, fg_color=Color.Platinum)
        self.login_table_frame.grid(row=1, column=0,padx=(width*0.005), pady=(0,height*0.01), sticky="nsew", columnspan=3)
        self.login_table_frame.grid_columnconfigure(0, weight=1)
        self.login_table_frame.grid_rowconfigure(0, weight=1)
        
        self.login_table_style = ttk.Style()
        self.login_table_style.theme_use("clam")
        self.login_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
        self.login_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
        self.login_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
        self.login_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
        self.columns = ("rec_no", "username","role","date","time_in","time_out")
        self.column_names = ("No", "Username","Role", "Date", "TimeIn", "TimeOut")
        
            
        self.log_audit_tree = ttk.Treeview(self.login_table_frame, columns=self.columns, show="headings",)
           
        for i in range(len(self.columns)):
            self.log_audit_tree.heading(f"{self.columns[i]}", text=f"{self.column_names[i]}")

        self.log_audit_tree.column("rec_no", width=int(width*0.01),anchor="w")
        self.log_audit_tree.column("username", width=int(width*0.35), anchor="w")
        self.log_audit_tree.column("role", width=int(width*0.15), anchor="w")
        self.log_audit_tree.column("date", width=int(width*0.15), anchor="c")
        self.log_audit_tree.column("time_in", width=int(width*0.15), anchor="c")
        self.log_audit_tree.column("time_out", width=int(width*0.15), anchor="c")
            
        self.log_audit_tree.tag_configure("odd",background=Color.White_AntiFlash)
        self.log_audit_tree.tag_configure("even",background=Color.White_Ghost)
            
        self.log_audit_tree.grid(row=0, column=0, sticky="nsew")
            
        self.y_scrollbar = ttk.Scrollbar(self.login_table_frame, orient=tk.VERTICAL, command=self.log_audit_tree.yview)
        self.log_audit_tree.configure(yscroll=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        """Table End"""
        
        '''LOGIN HISTORY - END'''

        '''ATTEMPTS - START'''     
        self.attempts_treeview = cctk.cctkTreeView(self.attempts_frame, width = 1040, height = 780, column_format="/AttemptingUSN:x-tl/UsedUSN:x-tl/DateAttempted:x-tr!30!30")
        self.attempts_treeview.pack()
        '''ATTEMPTS - END'''     
        
        self.update_login_audit()
        self.update_action_content()
        self.update_attempt_audit()
        load_main_frame(0)
    
    def update_action_content(self, e: any = None):
        for i in self.action_tree.get_children():
            self.action_tree.delete(i)
        temp = database.fetch_data(sql_commands.get_raw_action_history, (datetime.datetime.strptime(self.date_sort_label._text, '%B %d, %Y').strftime('%Y-%m-%d'), self.sort_role_option.get()))
        modified_data = [(temp.index(s) + 1, s[1], s[2].capitalize(), decode_action(s[3]), s[4].strftime("%B %d, %Y")) for s in temp]
        for i in range(len(modified_data)):
            if (i % 2) == 0:
                tag = "even"
            else:
                tag ="odd"
            self.action_tree.insert(parent='', index='end', iid=i, text="", values= modified_data[i], tags=tag )
    

    def update_login_audit(self, e: any = None):
        for i in self.log_audit_tree.get_children():
            self.log_audit_tree.delete(i)
        temp = database.fetch_data(sql_commands.get_log_history, (datetime.datetime.strptime(self.login_date_sort_label._text, '%B %d, %Y'), ))
        temp = [(s[0], s[1], s[2].strftime('%m/%d/%y'), s[3], s[4]) for s in temp]
        for i in range(len(temp)):
            if (i % 2) == 0:
                tag = "even"
            else:
                tag ="odd"
            self.log_audit_tree.insert(parent='', index='end', iid=i, text="", values= (i + 1, )+ temp[i], tags=tag )

    def update_attempt_audit(self, e: any = None):
        self.attempts_treeview.pack_forget()
        self.attempts_treeview.update_table(database.fetch_data("Select COALESCE(attempt_usn, '<None>'), usn_used, DATE_FORMAT(date_created, '%M %d, %Y at %h:%i %p') from login_report"))
        self.attempts_treeview.pack()
                  
class admin_settings_frame(ctk.CTkFrame):
    global width, height, IP_Address, PORT_NO
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
        self.inventory = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(18,21))
        self.service = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(18,21))
        self.calendar = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(17,18))
        self.show = ctk.CTkImage(light_image=Image.open("image/show.png"), size=(25,25))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        #self.general_frame = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        self.service_frame = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        self.inventory_frame = ctk.CTkFrame(self.base_frame, fg_color="transparent")

        #self.general_frame.grid_columnconfigure(0, weight=1)
        #self.general_frame.grid_rowconfigure(1, weight=1)
        
        self.service_frame.grid_columnconfigure(0, weight=1)
        self.service_frame.grid_rowconfigure(1, weight=1)
        
        self.inventory_frame.grid_columnconfigure(2, weight=1)
        self.inventory_frame.grid_rowconfigure(1, weight=1)
        
        self.report_frames=[self.service_frame, self.inventory_frame]
        self.active_report = None
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        selected_color = Color.Blue_Yale

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)
            
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=4, sticky="n")

        self.service_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.1,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.service_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.service_button.configure(command=partial(load_main_frame, 0))
        self.service_icon = ctk.CTkLabel(self.service_button, text="",image=self.service)
        self.service_icon.pack(side="left", padx=(width*0.01,width*0.005)) 
        self.service_label = ctk.CTkLabel(self.service_button, text="SERVICE", text_color="white", font=("DM Sans Medium", 14))
        self.service_label.pack(side="left")
        self.service_button.grid()
        self.service_button.update_children()

        self.inventory_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_button.grid(row=0, column=2, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_button.configure(command=partial(load_main_frame, 1))
        self.inventory_icon = ctk.CTkLabel(self.inventory_button, text="",image=self.inventory)
        self.inventory_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_label = ctk.CTkLabel(self.inventory_button, text="INVENTORY", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_label.pack(side="left")
        self.inventory_button.grid()
        self.inventory_button.update_children()

        self.button_manager = cctku.button_manager([self.service_button, self.inventory_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        
        def refresh_service():
            self.service_refresh_btn.configure(state=ctk.DISABLED)
            self.load_service_data()
            self.after(200, lambda:  self.service_refresh_btn.configure(state=ctk.NORMAL))
            
        def refresh_item():
            self.item_refresh_btn.configure(state=ctk.DISABLED)
            self.load_inventory_data()
            self.after(200, lambda:  self.item_refresh_btn.configure(state=ctk.NORMAL))
            
            
        def open_service_record():
            if self.service_data_view.get_selected_data():
                self.show_service_info.place(relx=0.5, rely=0.5, anchor="c", service_info=self.service_data_view.get_selected_data(), service_reload_callback = refresh_service)
                
            else:
                messagebox.showerror("Missing Selection", "Select a record first", parent = self)
                
        def open_item_record():
            if self.inventory_data_view.get_selected_data():
                self.show_item_info.place(relx=0.5, rely=0.5, anchor="c", item_info=self.inventory_data_view.get_selected_data(), item_reload_callback = refresh_item)
            else:
                messagebox.showerror("Missing Selection", "Select a record first", parent = self)
        
        def service_search_callback(): 
            temp = list_filterer(source=self.service_settings_search_bar.get(), reference=self.raw_service_data)  
            self.show_service_info.place(relx=0.5, rely=0.5, anchor="c", service_info=temp[0], service_reload_callback = refresh_service) if len(temp) == 1 else self.service_data_view.update_table(temp)
        
        def item_search_callback():
            temp = list_filterer(source=self.item_settings_search_bar.get(), reference=self.raw_inventory_data)  
            self.show_item_info.place(relx=0.5, rely=0.5, anchor="c", service_info=temp[0], item_reload_callback = refresh_item) if len(temp) == 1 else self.inventory_data_view.update_table(temp)
        
        self.service_top_frame = ctk.CTkFrame(self.service_frame, fg_color='transparent')
        self.service_top_frame.grid(row=0, column=0, sticky="nsew",  padx=(width*0.005), pady=(height*0.01))
        
        self.service_refresh_btn = ctk.CTkButton(self.service_top_frame,text="", width=width*0.03, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", hover_color=Color.Green_Button_Hover_Color,command=refresh_service)
        
        self.service_view_button = ctk.CTkButton(self.service_top_frame, text="View", image=self.show, fg_color=Color.Blue_Tufts, height=height*0.05, width=width*0.075, font=("DM Sans Medium", 14),
                                         command= open_service_record)
        
        
        '''TREEVIEW FRAME'''
        
        self.service_treeview_frame = ctk.CTkFrame(self.service_frame, fg_color="transparent")
        self.service_treeview_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
        
        self.service_data_view = cctk.cctkTreeView(self.service_treeview_frame,width= width * .805, height= height * .775, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ServiceID:{int(width*.085)}-tc/ServiceName:x-tl/DurationType:{int(width*.165)}-tl/Price:{int(width*.125)}-tr!33!35',
                                           double_click_command = lambda _: self.show_service_info.place(relx=0.5, rely=0.5, anchor="c", service_info=self.service_data_view.get_selected_data(), service_reload_callback = refresh_service))
        self.service_data_view.pack()
        '''SERVICE FRAME - END'''
        
        '''INVENTORY FRAME - START'''
        self.items_top_frame = ctk.CTkFrame(self.inventory_frame, fg_color='transparent')
        self.items_top_frame.grid(row=0, column=0, sticky="nsew",  padx=(width*0.005), pady=(height*0.01))
        
        self.item_refresh_btn = ctk.CTkButton(self.items_top_frame,text="", width=height*0.05, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh_item)
        
        
        self.item_view_button = ctk.CTkButton(self.items_top_frame, text="View", image=self.show, fg_color=Color.Blue_Tufts, height=height*0.05, width=width*0.075, font=("DM Sans Medium", 14), 
                                         command=open_item_record)
        
        
        
        '''TREEVIEW FRAME'''
        
        self.inventory_treeview_frame = ctk.CTkFrame(self.inventory_frame, fg_color="transparent")
        self.inventory_treeview_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
        
        self.inventory_data_view = cctk.cctkTreeView(self.inventory_treeview_frame,width= width * .805, height= height * .775, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ItemID:{int(width*.085)}-tc/ItemName:x-tl/Category:{int(width*.125)}-tl/Price:{int(width*.125)}-tr!33!35',
                                           double_click_command = lambda _: self.show_item_info.place(relx=0.5, rely=0.5, anchor="c", item_info=self.inventory_data_view.get_selected_data(),  item_reload_callback = refresh_item))
        self.inventory_data_view.pack()
        '''INVENTORY FRAME - END'''
        
        self.load_service_data()
        self.load_inventory_data()

        self.show_service_info = admin_popup.show_service_info(self,(width, height))
        self.show_item_info = admin_popup.show_item_info(self,(width, height))
        
        self.service_settings_search_bar = cctk.cctkSearchBar(self.service_top_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=service_search_callback,
                                                 close_command_callback=self.load_service_data,
                                             quary_command=sql_commands.get_service_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
        self.service_settings_search_bar.pack(side='left')
        self.service_refresh_btn.pack(side='left', padx=(width*0.005))
        self.service_view_button.pack(side='left', padx=(0, width*0.005))
        
        self.item_settings_search_bar = cctk.cctkSearchBar(self.items_top_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=item_search_callback,
                                                 close_command_callback=self.load_inventory_data,
                                             quary_command=sql_commands.get_item_search_query, dp_width=width*0.25, place_height=height*0, place_width=width*0, font=("DM Sans Medium", 14))
        self.item_settings_search_bar.pack(side='left')
        self.item_refresh_btn.pack(side='left', padx=(width*0.005))
        self.item_view_button.pack(side='left', padx=(0,width*0.005))
        
        load_main_frame(0)
    
    def load_inventory_data(self):
        self.inventory_data_view.pack_forget()
        self.raw_inventory_data = database.fetch_data(sql_commands.get_inventory)
        self.inventory_data_view.update_table(self.raw_inventory_data) 
        self.inventory_data_view.pack()
    
    def load_service_data(self):
        self.service_data_view.pack_forget()
        self.raw_service_data = database.fetch_data(sql_commands.get_service_data_test)
        self.service_data_view.update_table(self.raw_service_data)
        self.service_data_view.pack()

    def load_both(self):
        self.load_inventory_data()
        self.load_service_data()    

#dashboard(None, 'admin', datetime.datetime.now())