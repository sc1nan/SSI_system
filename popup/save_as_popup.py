from typing import *
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import os
from tkinter import filedialog
import datetime
import re
from PIL import Image
from util import *
import sql_commands
import calendar
from constants import *
from customcustomtkinter import customcustomtkinter as cctk
from popup import preview_pdf_popup as ppdfp

def show_popup(master, info:tuple, user: str, full_name: str, position: str) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple, user: str):
            self.DEFAULT_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
            self.DEFAULT_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August","September","October", "November", "December"]
            self.CURRENT_DAY = datetime.datetime.now()
            self.DEFAULT_YEAR = [str(self.CURRENT_DAY.year)]
            self.user = user
            self.full_name = full_name
            self.position = position
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master,  corner_radius= 0, fg_color="#B3B3B3")
            #the actual frame, modification on the frame itself goes here
            
            self.gen_report = ctk.CTkImage(light_image=Image.open("image/gen_report.png"), size=(26,26))
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),  size=(20,20)) 
            self.folder_icon = ctk.CTkImage(light_image=Image.open("image/folder.png"), size=(25,25))   
                        
            '''events'''
            def generate_callback():
                temp_f_path = 'file'
                if self.file_name_entry.get().endswith('.pdf'):
                    temp_f_path = f'{self.path_entry.get()}\\{self.file_name_entry.get()}'
                else:
                    temp_f_path = f'{self.path_entry.get()}\\{self.file_name_entry.get()}.pdf'
                if self.file_name_entry.get() == "":
                    messagebox.showwarning('Invalid', 'Fill the name of the report', parent = self)
                    return
                elif not os.path.isdir(self.path_entry.get()):
                    messagebox.showwarning('Invalid', 'Invalid File Path')
                    return
                elif os.path.isfile(temp_f_path):
                    question = messagebox.askyesnocancel('Warning!', 'File already exist! do you want to replace it?', parent = self)
                    if question == False:
                        ctr = 1
                        change_name_entry(self.file_name_entry.get()+f'({ctr})')
                        temp_f_path = temp_f_path.removesuffix('.pdf')
                        temp_f_path += f'({ctr}).pdf'
                        while os.path.isfile(temp_f_path):
                            ctr += 1
                            change_name_entry(self.file_name_entry.get().removesuffix(f'({ctr-1})'))
                            change_name_entry(self.file_name_entry.get()+f'({ctr})')
                            temp_f_path = temp_f_path.removesuffix(f'({ctr-1}).pdf')
                            temp_f_path += f'({ctr}).pdf'
                    elif question == None:
                        return
                generate_report(self.report_type_option.get(), self.user, self.full_name, self.position, self.CURRENT_DAY.strftime('%B %d, %Y'),
                                monthly_date_text_var.get(), annual_date_text_var.get(), self.CURRENT_DAY.strftime('%B %d, %Y'),
                                self.path_entry.get(), annual_date_text_var.get(), self.include_graphs_checkbox.get(), self.file_name_entry.get(), 1, self)
                reset()
                
            def preview_pdf_popup():
                generate_report(self.report_type_option.get(), self.user, self.full_name, self.position, self.CURRENT_DAY.strftime('%B %d, %Y'),
                                monthly_date_text_var.get(), annual_date_text_var.get(), self.CURRENT_DAY.strftime('%B %d, %Y'),
                                'image', annual_date_text_var.get(), self.include_graphs_checkbox.get(), 'sample.pdf', 0, self)
                #ppdfp.preview_pdf_popup(0)
                ppdfp.preview_pdf_popup(receipt=0, title="Report Viewer")

            def change_name_entry(name: str = None):
                self.file_name_entry.delete(0, ctk.END)
                self.file_name_entry.insert(0, name)

            def daily_callback(e: any = None):
                change_name_entry('_'.join(re.findall(r'(\w+)',  daily_date_text_var_split))+'_Daily_Sales_Report.pdf')

            def monthly_callback(e: any = None):
                change_name_entry(f'{monthly_date_text_var.get()}_{annual_date_text_var.get()}_Monthly_Sales_report.pdf')

            def yearly_callback(e: any = None):
                change_name_entry(f'{annual_date_text_var.get()}_Annual_Sales_Report.pdf')

            def change_date_entry(date: str = None):
                #self.daily_date_entry.configure(state = ctk.NORMAL)
                #self.daily_date_entry.delete(0, ctk.END)
                #self.daily_date_entry.insert(0, date or self.CURRENT_DAY.strftime('%B %d, %Y'))
                #self.daily_date_entry.configure(state = 'readonly')
                self.daily_date_entry.configure(text=f"{date or self.CURRENT_DAY.strftime('%B %d, %Y')}")

            def path_save_cmd():
                save_path = filedialog.askdirectory(title= 'Save')
                #callback
                if save_path:
                    self.path_entry.delete(0, ctk.END)
                    self.path_entry.insert(0, save_path)

            def show_report_fill(e: any = None):
                if self.report_type_option.get() == 'Daily':
                    self.title_setting.configure(text = 'Select Date:')
                    self.mothly_month_option.pack_forget()
                    self.mothly_year_option.pack_forget()
                    self.yearly_option.pack_forget()
                    self.daily_date_entry.pack(side = ctk.LEFT, fill="x", expand=1, padx = (width * .005), pady=(height*0.005))
                    self.daily_calendar_button.pack(side = ctk.LEFT, padx = (0, width * .005), pady=(height*0.005))
                    daily_callback()
                if self.report_type_option.get() == 'Monthly':
                    self.title_setting.configure(text = 'Select Month and Year:')
                    self.daily_date_entry.pack_forget()
                    self.daily_calendar_button.pack_forget()
                    self.yearly_option.pack_forget()
                    self.mothly_month_option.pack(side = ctk.LEFT,fill="x", expand=1, padx = (width * .005))
                    self.mothly_year_option.pack(side = ctk.LEFT,fill="x", expand=1, padx = (0, width * .005))
                    monthly_callback()
                if self.report_type_option.get() == 'Yearly':
                    self.title_setting.configure(text = 'Select Year:')
                    self.daily_date_entry.pack_forget()
                    self.daily_calendar_button.pack_forget()
                    self.mothly_month_option.pack_forget()
                    self.mothly_year_option.pack_forget()
                    self.yearly_option.pack(side = ctk.LEFT,fill="x", expand=1, padx = (width * .005))
                    yearly_callback()

            #j
            #create global variable for daily date text
            global daily_date_text_var
            daily_date_text_var = StringVar(value=datetime.datetime.now().strftime("%B %d, %Y"))
            #create global variable for a better formate of daily date text
            global daily_date_text_var_split
            r=re.split("[^a-zA-Z\d]+",daily_date_text_var.get())
            daily_date_text_var_split='_'.join([ i for i in r if len(i) > 0 ])
            #callback for changing file name to current selected daily date
            def write_callback(var, index, mode):
                r=re.split("[^a-zA-Z\d]+",daily_date_text_var.get())
                global daily_date_text_var_split
                daily_date_text_var_split='_'.join([ i for i in r if len(i) > 0 ])
                #change file name
                daily_callback()
            #add trace for whenever string var is changed
            daily_date_text_var.trace_add('write', callback=write_callback)

            #create global variable for monthly date text
            global monthly_date_text_var
            monthly_date_text_var = StringVar(value=datetime.datetime.now().strftime("%B"))
            #callback for changing file name to current selected daily date
            def change_month_name_callback(var, index, mode):
                #change file name
                monthly_callback()
            #add trace for whenever string var is changed
            monthly_date_text_var.trace_add('write', callback=change_month_name_callback)

            #create global variable for daily date text
            global annual_date_text_var
            annual_date_text_var = StringVar(value=datetime.datetime.now().strftime("%Y"))
            #callback for changing file name to current selected daily date
            def change_year_name_callback(var, index, mode):
                #change file name
                yearly_callback()
            #add trace for whenever string var is changed
            annual_date_text_var.trace_add('write', callback=change_year_name_callback)

            
            def reset():
                self.place_forget()
            '''code goes here'''
            #From here
            self.main_frame = ctk.CTkFrame(self, width=width*0.385, height=height*0.625, fg_color=Color.White_Lotion, corner_radius=0)
            self.main_frame.pack(fill=BOTH, expand=True)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((1,7), weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.gen_report).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="GENERATE REPORT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            #ctk.CTkButton(self.main_frame, text='X', command=lambda: self.place_forget(),font=("DM Sans Medium", (height*0.023)), fg_color='red', text_color='white', width=width*0.025).grid(row=0, column=0, padx=(width*0.006), pady=((height*0.01), (height*0.03)), sticky="ne")

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))

            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill=BOTH, expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure(0, weight=1)
            
            '''FILE NAME'''
            self.file_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.file_name_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.025,height*0.01))
            ctk.CTkLabel(self.file_name_frame, text='File Name:  ',font=("DM Sans Medium", 14), fg_color='transparent', text_color=Color.Blue_Maastricht, height=height*0.055, width=width*0.075, anchor="e").pack(side="left")
            self.file_name_entry = ctk.CTkEntry(self.file_name_frame, placeholder_text='report', fg_color=Color.White_Lotion, font=("DM Sans Medium", 14),height=height*0.055)
            self.file_name_entry.pack(side="left", fill='x', expand=1)
            #(height*0.023)

            '''PATH FRAME'''
            self.path_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.path_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
            ctk.CTkLabel(self.path_frame, text='File Path:  ',font=("DM Sans Medium", 14), fg_color='transparent', text_color=Color.Blue_Maastricht,height=height*0.055, width=width*0.075, anchor="e").pack(side="left")
            self.path_entry = ctk.CTkEntry(self.path_frame, font=("DM Sans Medium", 14),height=height*0.055)
            self.path_entry.insert(0, self.DEFAULT_PATH)
            self.path_entry.pack(side="left", fill='x', expand=1)
            ctk.CTkButton(self.path_frame, text='', command=path_save_cmd,font=("DM Sans Medium", 14), text_color='white', height=height*0.055, width=width*0.03, image=self.folder_icon).pack(side="left")
            #self.file_type_entry = ctk.CTkEntry(self.main_frame, height=height*0.03, corner_radius=20, font=("DM Sans Medium", (height*0.023)), show='*')
            #self.file_type_entry.grid(row=6, column=0, padx=(width*0.006), pady=(0, (height*0.01)), sticky="nsw")
            
            '''FILE TYPE FRAME'''
            self.file_type_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.file_type_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
            ctk.CTkLabel(self.file_type_frame, text='File Type:  ',font=("DM Sans Medium", 14), fg_color='transparent', text_color=Color.Blue_Maastricht, height=height*0.055, width=width*0.075, anchor="e").pack(side="left")
            self.report_type_option = ctk.CTkOptionMenu(self.file_type_frame,values=["Daily", "Monthly", "Yearly"], height=height*0.055,  width=width*0.25, font=("DM Sans Medium", 14), dropdown_font=("DM Sans Medium", 12), command=show_report_fill)
            self.report_type_option.pack(side="left", fill='x', expand=1)

            #checkbox if include graphs
            self.include_graphs_checkbox = ctk.CTkCheckBox(self.sub_frame, text = 'Include Graphs', font=("DM Sans Medium", 14))
            self.include_graphs_checkbox.grid(row=3, column=0, sticky="nsew", padx=(width*0.085))



            self.preview_pdf_btn = ctk.CTkButton(self.sub_frame, text='Preview PDF', command= preview_pdf_popup,font=("DM Sans Medium", 14),height=height*0.055, 
                                                 fg_color=Color.Green_Pistachio, hover_color=Color.Green_Aparagus, text_color="white")
            self.preview_pdf_btn.grid(row=7, column=0, sticky="nse", padx=(width*0.005), pady=(height*0.01,0))
                
                
            '''TITLE SETTING'''
            self.title_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.title_frame.grid(row=5, column=0, sticky="nsew", padx=(width*0.005))
            self.title_setting = ctk.CTkLabel(self.title_frame, text= 'Select Date:', font=("DM Sans Medium", 14))
            self.title_setting.grid(row = 0, column = 0, sticky = 'w', padx=(width*0.006), pady=(height*0.02, 0))
            
            self.setting_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum, height=height * .075)
            self.setting_frame.pack_propagate(0)
            self.setting_frame.grid(row=6, column=0, sticky = 'nsew', padx=(width*0.005))
            
            #daily
            #j
            #added textvariable for self.daily_date_entry
            self.daily_date_entry = ctk.CTkLabel(self.setting_frame, width * .213, height * .05,  fg_color=Color.White_Lotion, font=("DM Sans Medium", 14), corner_radius=5, textvariable=daily_date_text_var)
            change_date_entry()
            self.daily_calendar_button = ctk.CTkButton(self.setting_frame, height=height*0.055, width=width*0.03, text="", image=self.calendar_icon,#changed label value to global StringVar
                                                       command=lambda:cctk.tk_calendar(daily_date_text_var, "%s", date_format="word", max_date=datetime.datetime.now()) )
            #monthly
            self.mothly_month_option = ctk.CTkOptionMenu(self.setting_frame, width * .15, height * .05, font=("DM Sans Medium", (height*0.023)), values = self.DEFAULT_MONTHS, command= monthly_callback, anchor="center", variable = monthly_date_text_var)
            monthly_date_text_var.set(self.CURRENT_DAY.strftime('%B'))
            self.mothly_year_option = ctk.CTkOptionMenu(self.setting_frame, width * .1, height * .05, font=("DM Sans Medium", (height*0.023)), values = self.DEFAULT_YEAR, command= monthly_callback, anchor="center", variable = annual_date_text_var)

            #yearly
            self.yearly_option = ctk.CTkOptionMenu(self.setting_frame, width * 25, height * .05, font=("DM Sans Medium", (height*0.023)), values= ["2023", "2024"], command= yearly_callback, anchor="center", variable = annual_date_text_var)
            show_report_fill()

            #Generate button
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, text='Cancel', command=reset, font=("DM Sans Medium", 14), height=height*0.055, fg_color=Color.Red_Pastel, hover_color='#ff392e')
            self.cancel_btn.pack(side="left")

            self.generate_btn = ctk.CTkButton(self.bottom_frame, text='Generate Report', command= generate_callback,font=("DM Sans Medium", 14),height=height*0.055)
            self.generate_btn.pack(side="right")
            
        def place(self, month_selected_date, year_selected_date, daily_selected_date, **kwargs):
            if 'default_config' in kwargs:
                txt = 'Daily' if 'Daily' in kwargs['default_config'] else 'Monthly' if 'Monthly' in kwargs['default_config'] else 'Yearly'
                self.report_type_option.set(txt)
                self.report_type_option._command()
                if 'Daily' in kwargs['default_config']:
                    daily_date_text_var.set(daily_selected_date)
                elif 'Monthly' in kwargs['default_config']:
                    monthly_date_text_var.set(month_selected_date)
                else:
                    annual_date_text_var.set(year_selected_date)
                kwargs.pop('default_config')
                #change daily date value in save as popup to current selected
                
                
            return super().place(**kwargs)

    return add_item(master, info, user)

def show_popup_inventory(master, info:tuple, user: str, full_name: str, position: str) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple, user: str):
            self.DEFAULT_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
            self.DEFAULT_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August","September","October", "November", "December"]
            self.CURRENT_DAY = datetime.datetime.now()
            self.DEFAULT_YEAR = [str(self.CURRENT_DAY.year)]
            self.user = user
            self.full_name = full_name
            self.position = position
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, width, height, corner_radius= 0, fg_color="#B3B3B3")
            #the actual frame, modification on the frame itself goes here

            self.gen_report = ctk.CTkImage(light_image=Image.open("image/gen_report.png"), size=(26,26))
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),  size=(20,20)) 
            self.folder_icon = ctk.CTkImage(light_image=Image.open("image/folder.png"), size=(25,25))  
            
            '''events'''
            def generate_callback():
                temp_f_path = 'file'
                if self.file_name_entry.get().endswith('.pdf'):
                    temp_f_path = f'{self.path_entry.get()}\\{self.file_name_entry.get()}'
                else:
                    temp_f_path = f'{self.path_entry.get()}\\{self.file_name_entry.get()}.pdf'
                if self.file_name_entry.get() == "":
                    messagebox.showwarning('Invalid', 'Fill the name of the report', parent = self)
                    return
                elif not os.path.isdir(self.path_entry.get()):
                    messagebox.showwarning('Invalid', 'Invalid File Path')
                    return
                elif os.path.isfile(temp_f_path):
                    question = messagebox.askyesnocancel('Warning!', 'File already exist! do you want to replace it?', parent = self)
                    if question == False:
                        ctr = 1
                        change_name_entry(self.file_name_entry.get()+f'({ctr})')
                        temp_f_path = temp_f_path.removesuffix('.pdf')
                        temp_f_path += f'({ctr}).pdf'
                        while os.path.isfile(temp_f_path):
                            ctr += 1
                            change_name_entry(self.file_name_entry.get().removesuffix(f'({ctr-1})'))
                            change_name_entry(self.file_name_entry.get()+f'({ctr})')
                            temp_f_path = temp_f_path.removesuffix(f'({ctr-1}).pdf')
                            temp_f_path += f'({ctr}).pdf'
                    elif question == None:
                        return
                daily_date_select_temp = datetime.datetime.now()#datetime.datetime.strptime(self.daily_date_entry._text, '%B %d, %Y')
                generate_inventory_report(self.user, self.file_name_entry.get(), self.full_name, self.position, daily_date_select_temp.strftime('%Y-%m-%d'),
                                          #self.daily_date_entry._text, daily_date_select_temp.month, daily_date_select_temp.year,
                                          daily_date_select_temp, daily_date_select_temp.month, daily_date_select_temp.year,
                                          self.path_entry.get(), 1, self)
                reset()

            def preview_pdf_popup():
                daily_date_select_temp = datetime.datetime.now()
                generate_inventory_report(self.user, 'sample.pdf', self.full_name, self.position, daily_date_select_temp.strftime('%Y-%m-%d'),
                                          daily_date_select_temp, daily_date_select_temp.month, daily_date_select_temp.year,
                                          'image', 0, self)
                ppdfp.preview_pdf_popup(receipt=0, title="Inventory Viewer")

   
            #create global variable for inventory date text
            global inventory_date_text_var
            inventory_date_text_var = StringVar(value=datetime.datetime.now().strftime("%B %d, %Y"))
            #create global variable for a better formate of inventory date text
            global inventory_date_text_var_split
            r=re.split("[^a-zA-Z\d]+",inventory_date_text_var.get())
            inventory_date_text_var_split='_'.join([ i for i in r if len(i) > 0 ])
            #callback for changing file name to current selected inventory date
            def write_inventory_callback(var, index, mode):
                r=re.split("[^a-zA-Z\d]+",inventory_date_text_var.get())
                global inventory_date_text_var_split
                inventory_date_text_var_split='_'.join([ i for i in r if len(i) > 0 ])
                #change file name
                inventory_date_callback()
            #add trace for whenever string var is changed
            inventory_date_text_var.trace_add('write', callback=write_inventory_callback)

            
            def change_name_entry(name: str = None):
                self.file_name_entry.delete(0, ctk.END)
                self.file_name_entry.insert(0, name)

            def change_date_entry(date: str = None):
                #self.daily_date_entry.configure(state = ctk.NORMAL)
                #self.daily_date_entry.delete(0, ctk.END)
                #self.daily_date_entry.insert(0, date or self.CURRENT_DAY.strftime('%B %d, %Y'))
                #self.daily_date_entry.configure(state = 'readonly')
                self.daily_date_entry.configure(text=f"{date or self.CURRENT_DAY.strftime('%B %d, %Y')}")

            def inventory_date_callback(e: any = None):
                change_name_entry('_'.join(re.findall(r'(\w+)',  inventory_date_text_var_split))+'_Inventory_Report.pdf')

            def path_save_cmd():
                save_path = filedialog.askdirectory(title= 'Save')
                #callback
                if save_path:
                    self.path_entry.delete(0, ctk.END)
                    self.path_entry.insert(0, save_path)
            
            def reset():
                self.place_forget()

            '''code goes here'''
            #From here
            self.main_frame = ctk.CTkFrame(self, width=width*0.385, height=height*0.55, fg_color=Color.White_Lotion, corner_radius=0)
            self.main_frame.pack(fill=BOTH, expand=True)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.gen_report).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="GENERATE INVENTORY REPORT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            #ctk.CTkButton(self.main_frame, text='X', command=lambda: self.place_forget(),font=("DM Sans Medium", (height*0.023)), fg_color='red', text_color='white', width=width*0.025).grid(row=0, column=0, padx=(width*0.006), pady=((height*0.01), (height*0.03)), sticky="ne")

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))

            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill=BOTH, expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure(0, weight=1)
            
            '''FILE NAME'''
            self.file_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.file_name_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.025,height*0.01))
            ctk.CTkLabel(self.file_name_frame, text='File Name:  ',font=("DM Sans Medium", 14), fg_color='transparent', text_color=Color.Blue_Maastricht, height=height*0.055, width=width*0.075, anchor="e").pack(side="left")
            self.file_name_entry = ctk.CTkEntry(self.file_name_frame, placeholder_text='report', fg_color=Color.White_Lotion, font=("DM Sans Medium", 14),height=height*0.055)
            self.file_name_entry.pack(side="left", fill='x', expand=1)
            
            '''PATH FRAME'''
            self.path_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.path_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
            ctk.CTkLabel(self.path_frame, text='File Path:  ',font=("DM Sans Medium", 14), fg_color='transparent', text_color=Color.Blue_Maastricht,height=height*0.055, width=width*0.075, anchor="e").pack(side="left")
            self.path_entry = ctk.CTkEntry(self.path_frame, font=("DM Sans Medium", 14),height=height*0.055)
            self.path_entry.insert(0, self.DEFAULT_PATH)
            self.path_entry.pack(side="left", fill='x', expand=1)
            ctk.CTkButton(self.path_frame, text='', command=path_save_cmd,font=("DM Sans Medium", 14), text_color='white', height=height*0.055, width=width*0.03, image=self.folder_icon).pack(side="left")
            
            '''TITLE SETTING'''
            #self.title_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            #self.title_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005))
            #self.title_setting = ctk.CTkLabel(self.title_frame, text= 'Select Date:', font=("DM Sans Medium", 14))
            #self.title_setting.grid(row = 0, column = 0, sticky = 'w', padx=(width*0.006), pady=(height*0.02, 0))
            
            #self.setting_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum, height=height * .075)
            #self.setting_frame.pack_propagate(0)
            #self.setting_frame.grid(row=5, column=0, sticky = 'nsew', padx=(width*0.005))
            #daily
            #self.daily_date_entry = ctk.CTkLabel(self.setting_frame, width * .213, height * .05,  fg_color=Color.White_Lotion, font=("DM Sans Medium", 14), corner_radius=5, textvariable=inventory_date_text_var)
            #self.daily_date_entry.pack(side = ctk.LEFT, fill="x", expand=1, padx = (width * .005), pady=(height*0.005))
            #change_date_entry()
            change_name_entry('_'.join(re.findall(r'(\w+)', inventory_date_text_var_split))+'_Inventory_Report.pdf')
            #self.daily_calendar_button = ctk.CTkButton(self.setting_frame, height=height*0.055, width=width*0.03, text="", image=self.calendar_icon,
            #                                          command=lambda:cctk.tk_calendar(inventory_date_text_var, "%s", date_format="word", max_date=datetime.datetime.now()) )
            #self.daily_calendar_button.pack(side = ctk.LEFT, padx = (0, width * .005), pady=(height*0.005))
            
            self.preview_pdf_btn = ctk.CTkButton(self.sub_frame, text='Preview PDF', command= preview_pdf_popup,font=("DM Sans Medium", 14),height=height*0.055, 
                                                 fg_color=Color.Green_Pistachio, hover_color=Color.Green_Aparagus, text_color="white")
            self.preview_pdf_btn.grid(row=7, column=0, sticky="nse", padx=(width*0.005), pady=(height*0.01,0))
            
            
            
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, text='Cancel', command=reset, font=("DM Sans Medium", 14), height=height*0.055, fg_color=Color.Red_Pastel, hover_color='#ff392e')
            self.cancel_btn.pack(side="left")
            
            self.generate_btn = ctk.CTkButton(self.bottom_frame, text='Generate Report', command= generate_callback, font=("DM Sans Medium", 14),height=height*0.055)
            self.generate_btn.pack(side="right")

            
            """ #file name label
            ctk.CTkLabel(self.box_frame, text='File Name:',font=("DM Sans Medium", (height*0.023)), text_color="#06283D").grid(row=1, column=0, padx=(width*0.006), pady=((height*0.01),0), sticky="w")
            #file name entry
            self.file_name_entry = ctk.CTkEntry(self.box_frame, placeholder_text='report', height=height*0.03, width=width*0.25, corner_radius=20, font=("DM Sans Medium", (height*0.023)))
            self.file_name_entry.grid(row=2, column=0, padx=(width*0.006), pady=(0, (height*0.01)), sticky="w")

            #path label
            ctk.CTkLabel(self.box_frame, text='Path:',font=("DM Sans Medium", (height*0.023)), text_color="#06283D").grid(row=3, column=0, padx=(width*0.006), pady=((height*0.01),0), sticky="w")
            self.path_frame = ctk.CTkFrame(self.box_frame,fg_color="white")
            self.path_frame.grid(row=4, column=0)
            #path entry
            self.path_entry = ctk.CTkEntry(self.path_frame, height=height*0.03,  width=width*0.22, corner_radius=20, font=("DM Sans Medium", (height*0.023)))
            self.path_entry.insert(0, self.DEFAULT_PATH)
            self.path_entry.grid(row=4, column=0, padx=((width*0.006),(width*0.00)), pady=(0, (height*0.01)), sticky="w")
            #path button
            ctk.CTkButton(self.path_frame, text='...', command=path_save_cmd,font=("DM Sans Medium", (height*0.023)), fg_color='#2678F3', text_color='white', width=width*0.025).grid(row=4, column=1, padx=((width*0.002),(width*0.006)), pady=(0, (height*0.01)), sticky="ne")

            #file type label
            #file type entry
            #self.file_type_entry = ctk.CTkEntry(self.box_frame, height=height*0.03, corner_radius=20, font=("DM Sans Medium", (height*0.023)), show='*')
            #self.file_type_entry.grid(row=6, column=0, padx=(width*0.006), pady=(0, (height*0.01)), sticky="nsw")
            self.title_setting = ctk.CTkLabel(self.box_frame, text= 'Select Date', font=("DM Sans Medium", (height*0.015)))
            self.title_setting.grid(row = 7, column = 0, sticky = 'w', padx=(width*0.006), pady=(height*0.023, 0))

            self.setting_frame = ctk.CTkFrame(self.box_frame, fg_color='transparent', height=height * .05)
            self.setting_frame.pack_propagate(0)
            self.setting_frame.grid(row = 8, column = 0, sticky = 'nwe', padx=(width*0.006)) """

            #daily
            """ self.daily_date_entry = ctk.CTkEntry(self.setting_frame, width * .213, height * .05, state='readonly', font=("DM Sans Medium", (height*0.023)))
            change_date_entry()
            change_name_entry('_'.join(re.findall(r'(\w+)', self.daily_date_entry.get()))+'_report.pdf')
            self.daily_calendar_button = ctk.CTkButton(self.setting_frame, width * .027, width *.03)
            self.daily_date_entry.pack(side = ctk.LEFT, padx = (width * .0025))
            self.daily_calendar_button.pack(side = ctk.LEFT, padx = (0, width * .0025)) """

            #Generate button
            """ self.generate_btn = ctk.CTkButton(self.box_frame, text='Generate', command= generate_callback,font=("DM Sans Medium", (height*0.023)), fg_color='#2678F3', text_color='white')
            self.generate_btn.grid(row=9, column=0, padx=(width*0.01), pady=((height*0.05), (height*0.01)), sticky="sew") """

        def place(self, **kwargs):
            if 'default_config' in kwargs:
                txt = 'Daily' if 'Daily' in kwargs['default_config'] else 'Monthly' if 'Monthly' in kwargs['default_config'] else 'Yearly'
                #self.report_type_option.set(txt)
                #self.report_type_option._command()
                kwargs.pop('default_config')
            return super().place(**kwargs)

    return add_item(master, info, user)

def generate_report(report_type: str, acc_name_preparator: str, acc_full_name: str, acc_pos: str, date_creation: str, monthly_month: str|int, monthly_year: str|int, daily_full_date: str, file_path: str, yearly_year: str|int, include_graphs: int, file_name: str, finish_alerts: int, master: any):
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.pdfgen.canvas import Canvas
    from datetime import datetime as datetime_temp
    from reportlab.lib import colors
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import Table
    from reportlab.platypus import TableStyle
    from PyPDF2 import PdfWriter, PdfReader
    import math
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw


    ttfFile = os.path.join('C:\Windows\Fonts', 'Times.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman", ttfFile))
    ttfFile = os.path.join('C:\Windows\Fonts', 'Timesbd.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman-Bold", ttfFile))
    #pdfmetrics.registerFont(TTFont('Times New Roman', 'TimesNewRoman.ttf'))
    months_Text = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]
    #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    desktop = file_path

    def round_up_to_nearest_100000(num):
        return math.ceil(num / 10000) * 10000
    
    def calculate_step_count(i: int, len_count: int = 1):
        count = round(i/len_count)
        len_div = len(str(count)[1:])
        return math.ceil(count/10 ** len_div) * 10 ** len_div
    #get percentage on pie chart
    def percentage(part, whole):
        if not part:
            return
        Percentage = 100 * float(part)/float(whole)
        return str(round(Percentage, 2)) + '%'
    
    #generate footer based on number of pages
    def footer_generator(page_count: int):
        #footer
        filename = f'image/footer.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter,
        )
        pdf.bottomMargin = 20
        pdf.leftMargin = 20
        pdf.rightMargin = 20

        tbl_footer_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (0, -1), 14),
            ('FONTSIZE', (0, 0), (0, 0), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.lightgrey),
            #space at the bottom
            ('TOPPADDING', (0, 0), (0, -1), 670),
            ('RIGHTPADDING', (0, 0), (0, 0), 300),
            ]
        )
        elems = []
        footer_content = []
        for page in range(page_count):
            footer_content.append([["Dr. Joseph Z. Angeles Veterinary Clinic", f"Page {page+1} of {page_count}"]])
        for footer_page in range(len(footer_content)):
            table_footer = Table(footer_content[footer_page])
            table_footer.setStyle(tbl_footer_style)
            elems.append(table_footer)

        pdf.build(elems)

    def footer_gen2():
        filename = f'image/footer2.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter,
        )
        footer_content = [['', '', ''],
                          ['Prepared by:', '', 'Prepared Date/Time:'],
                          [f'{acc_full_name}', '', f'{datetime.datetime.now().strftime("%x     %I:%M:%S %p")}'],
                          [f'{acc_pos}', '', ''],]
        table_footer = Table(footer_content)
        tbl_footer_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            #grid goes like this (x, y) x goes from left to right
            #('ALIGN', (3, 1), (3, 1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            #font style
            ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('FONTSIZE', (0, 3), (0, 3), 8),
            #('FONTSIZE', (1, 2), (1, 2), 8),
            #space at the bottom
            ('TOPPADDING', (0, 0), (-1, 0), 540),#670
            #('BOTTOMPADDING', (0, 2), (0, -1), -20),
            ('TOPPADDING', (0, 3), (0, 3), -40),
            ('TOPPADDING', (0, 2), (0, 2), 20),
            ('RIGHTPADDING', (1, 1), (1, -1), 200),
            #Signature line
            ('LINEBELOW', (0,2), (0,2), 0.5, colors.black),
           #('BOX', (0,0), (-1,-1), 0.5, colors.red)
            ]
        )
        table_footer.setStyle(tbl_footer_style)
        elems = []
        elems.append(table_footer)
        pdf.build(elems)

    def chart_generator(data_for_items_temp, data_for_services_temp, labels_angle, category_names, type_of_sales, date_for_legends, piechart_x, piechart_y, piechart_width, piechart_height, include_vbarchart, vbc_label_location):
        #path for charts
        my_path = f'image\charts.pdf'
        #create page with letter size
        d = Drawing(612, 792)
        if include_vbarchart:
            #get ceiling amount for bar chart
            step_val = 0
            data_max_val= 0
            for x in data_for_items_temp:
                if x > data_max_val:
                    data_max_val= x
            for x in data_for_services_temp:
                if x > data_max_val:
                    data_max_val= x

            data_max_val = math.ceil(data_max_val/1000) * 1000
            step_val = calculate_step_count(data_max_val, 10)
            data_max_val = data_max_val + step_val
            #create bar chart
            bc = VerticalBarChart()
            bc.x = 111
            bc.y = 500
            bc.height = 220
            bc.width = 430
            bc.data = [data_for_items_temp , data_for_services_temp]
            bc.strokeColor = colors.black
            bc.groupSpacing = 10
            bc.barSpacing = 1
            #change bar color
            #changed colors
            bc.bars[0].fillColor = colors.lightgreen
            bc.bars[1].fillColor = colors.cornflowerblue
            bc.valueAxis.valueMin = 0
            bc.valueAxis.valueMax = data_max_val
            bc.valueAxis.valueStep = step_val or 1
            bc.categoryAxis.labels.fontSize = 12
            bc.categoryAxis.labels.fontName = 'Times-New-Roman'
            bc.categoryAxis.labels.boxAnchor = 'ne'
            bc.categoryAxis.labels.dx = 5
            bc.categoryAxis.labels.dy = -2
            bc.categoryAxis.labels.angle = labels_angle
            bc.categoryAxis.categoryNames = category_names
            #legends
            d.add(String(vbc_label_location[0],vbc_label_location[1], f'{type_of_sales} Sales Graph as of {date_for_legends}', fontName = 'Times-New-Roman', fontSize=16)),
            d.add(String(260,375, f'{type_of_sales} Sales', fontName = 'Times-New-Roman', fontSize=16))
            d.add(Rect(90, 180, 430, 220, fillColor=colors.transparent, strokeColor=colors.gray))
            d.add(Rect(350, 440, 15, 15, fillColor=colors.cornflowerblue))
            d.add(Rect(250, 440, 15, 15, fillColor=colors.lightgreen))
            d.add(String(370,440, 'Services', fontName = 'Times-New-Roman', fontSize=12))
            d.add(String(270,440, 'Sales', fontName = 'Times-New-Roman', fontSize=12))
            #add barchart to drawing
            d.add(bc, '')
            #get total amount for service and items income
            total_item_income_temp = 0
            for income in data_for_items_temp:
                total_item_income_temp += income
            total_service_income_temp = 0
            for income in data_for_services_temp:
                total_service_income_temp += income
            total_income_temp = total_item_income_temp + total_service_income_temp
        #for daily sales
        if not include_vbarchart:
            d.add(Rect(120, 185, 380, 280, fillColor=colors.transparent, strokeColor=colors.gray))
            d.add(String(265,450, 'Daily Sales', fontName = 'Times-New-Roman', fontSize=16))
        #create piechart
        pc = Pie()
        pc.x = piechart_x
        pc.y = piechart_y
        pc.height = piechart_height
        pc.width = piechart_width
        pc.slices.strokeWidth=0
        pc.slices.fontSize = 10
        pc.slices.fontName = 'Times-New-Roman'
        pc.simpleLabels = 0
        pc.slices.label_simple_pointer = 1
        if include_vbarchart:
            pc.data = [total_item_income_temp, total_service_income_temp]
            pc.labels = [f'Sales\nP{total_item_income_temp:,.2f}\n({percentage(total_item_income_temp, total_income_temp)})', f'Services\nP{total_service_income_temp:,.2f}\n({percentage(total_service_income_temp, total_income_temp)})']
        else:
            service_max = 1

            if data_for_items_temp > service_max:
                service_max = data_for_items_temp
            if data_for_services_temp > service_max:
                service_max = data_for_services_temp
            total_data_temp = float(data_for_items_temp) + float(data_for_services_temp)
            
            pc.data = [data_for_items_temp, data_for_services_temp]
            pc.labels = [f'Sales\nP{data_for_items_temp:,.2f}\n({percentage(data_for_items_temp, total_data_temp)})', f'Services\nP{data_for_services_temp:,.2f}\n({percentage(data_for_services_temp, total_data_temp)})']

        pc.slices[0].fillColor = colors.lightgreen
        pc.slices[1].fillColor = colors.cornflowerblue
        pc.slices[1].popout = 10
        #add piechart on drawing
        d.add(pc, '')
        #create pdf
        renderPDF.drawToFile(d, my_path, '')
    #Daily Income Report Content
    def sales_gen():
        date_temp = datetime.datetime.strptime(daily_date_text_var.get(), '%B %d, %Y').strftime('%Y-%m-%d')
        service_total_temp = 0
        sales_total_temp = 0
        #path for charts
        sales_filename = f'image\sales.pdf'
        pdf = SimpleDocTemplate(
            filename=sales_filename,
            pagesize=letter
        )
        daily_service_report_content_temp = [
            ['Services', '', '', ''],
            ['OR#', 'Client Name', 'Service Description', 'Price'],
                                           ]
        
        daily_sales_report_content_temp = [
            ['Sales', '', '', '', ''],
            ['OR#', 'Particular', 'Quantity', 'Price', 'Total Price'],
                                           ]
        #add data for tables
        for x in database.fetch_data(sql_commands.get_services_daily_report_content, (date_temp,)):
            temp_data = []
            temp_data.append(x[0])
            temp_data.append(x[1])
            temp_data.append(x[2])
            temp_data.append(x[3])
            service_total_temp += float(x[4])
            daily_service_report_content_temp.append(temp_data)
        daily_service_report_content_temp.append(['Total:', '', '', f'P{service_total_temp:,.2f}'])
        for x in database.fetch_data(sql_commands.get_sales_daily_report_content, (date_temp,)):
            temp_data = []
            temp_data.append(x[0])
            length_counter = 0
            item_name = x[1]
            itm_name = ''
            for i_name in item_name.split():
                length_counter += len(i_name)
                if length_counter > 21:
                    length_counter = len(i_name)
                    itm_name += f'\n{i_name}'
                else:
                    itm_name += f'{i_name} '
            temp_data.append(itm_name)
            temp_data.append(x[2])
            temp_data.append(x[3])
            temp_data.append(x[4])
            sales_total_temp += float(x[5])
            daily_sales_report_content_temp.append(temp_data)
        daily_sales_report_content_temp.append(['Total:', '', '', '', f'P{sales_total_temp:,.2f}'])

        table_content = Table(daily_service_report_content_temp)
        table_content2 = Table(daily_sales_report_content_temp)
        empty_space = Table([''], [''])
        
        #add table style
        tbl_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            #centers or num column
            ('ALIGN', (0, 2), (0, -1), 'CENTER'),
            #aligns left client name column
            ('ALIGN', (1, 2), (1, -1), 'LEFT'),
            #aligns left service name column
            ('ALIGN', (2, 2), (2, -1), 'LEFT'),
            #aligns right price column
            ('ALIGN', (3, 2), (3, -1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
            #for total
            ('SPAN', (0, len(daily_service_report_content_temp)-1), (2, len(daily_service_report_content_temp)-1)),
            ('ALIGN', (0, len(daily_service_report_content_temp)-1), (-1, len(daily_service_report_content_temp)-1), 'RIGHT'),
            ]
        )

        tbl_style2 = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            #centers or num column
            ('ALIGN', (0, 2), (0, -1), 'CENTER'),
            #aligns left particulars column
            ('ALIGN', (1, 2), (1, -1), 'LEFT'),
            #aligns left quantity name column
            ('ALIGN', (2, 2), (2, -1), 'RIGHT'),
            #aligns right price column
            ('ALIGN', (3, 2), (3, -1), 'RIGHT'),
            #aligns right total price column
            ('ALIGN', (4, 2), (4, -1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
            #for total
            ('SPAN', (0, len(daily_sales_report_content_temp)-1), (3, len(daily_sales_report_content_temp)-1)),
            ('ALIGN', (0, len(daily_sales_report_content_temp)-1), (-1, len(daily_sales_report_content_temp)-1), 'RIGHT'),
            ]
        )

        empty_style = TableStyle(
            [
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
            ]
        )

        table_content.setStyle(tbl_style)
        table_content2.setStyle(tbl_style2)
        empty_space.setStyle(empty_style)
        #alternate background color
        rowNumb = len(daily_service_report_content_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content.setStyle(ts)

        rowNumb = len(daily_sales_report_content_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content2.setStyle(ts)

        #add borders
        ts = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_content.setStyle(ts)
        table_content2.setStyle(ts)

        elems = []
        elems.append(table_content)
        elems.append(empty_space)
        elems.append(table_content2)

        pdf.build(elems)
    #yearly

    if 'Yearly' == report_type:
        #start of data collection
        #get monthly_year
        y_temp = yearly_year
        months_temp = [*range(1, 13, 1)]
        monthly_data_items_temp = [database.fetch_data(sql_commands.get_items_monthly_sales_sp_temp, (s, y_temp))[0][0] or 0 for s in months_temp]
        monthly_data_service_temp = [database.fetch_data(sql_commands.get_services_monthly_sales_sp_temp, (s, y_temp))[0][0] or 0 for s in months_temp]
        #end of data collection
        #content
        if file_name.endswith('.pdf'):
            filename = f'{desktop}\\{file_name}'
        else:
            filename = f'{desktop}\\{file_name}.pdf'
        
        #filename = f'{desktop}\\{y_temp}_yearly_report.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter
        )
        #header
        report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
                        ['SJDM City, Bulacan Hardware 2000 Bldg.'],
                            ['Brgy. Graceville, SJDM City, Bulacan'],
                            ['Tel.: 8994-9043'],
                            ['Cel.: 0922-976-9287 / 0927-887-0270 / 0922-408-7709']]
        report_header = Table(report_header_temp)
        tbl_header_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (0, 0), 18),
            ('FONTSIZE', (0, 1), (0, -1), 12),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (0, 0), 20),
            ('BOTTOMPADDING', (0, len(report_header_temp)-1), (0, len(report_header_temp)-1), 25),
            ]
        )

        report_header.setStyle(tbl_header_style)

        total_item_income_temp = 0
        for income in monthly_data_items_temp:
            total_item_income_temp += income
        total_service_income_temp = 0
        for income in monthly_data_service_temp:
            total_service_income_temp += income
        total_income_temp = total_item_income_temp + total_service_income_temp
        #header for table columns
        yearly_report_content_temp = [[f'Annual Sales Report as of {y_temp}'], ['Month', 'Sales', 'Services', 'Total Income']]
        #add data for table
        yearly_report_total_items_temp = 0
        yearly_report_total_services_temp = 0
        monthlength = len(monthly_data_items_temp)
        for i in range(0, monthlength):
            yearly_report_temp_data = []
            yearly_report_temp_data.append(months_Text[i])
            yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i])}')
            yearly_report_temp_data.append(f'P{format_price(monthly_data_service_temp[i])}')
            yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i] + monthly_data_service_temp[i])}')
            yearly_report_content_temp.append(yearly_report_temp_data)
            yearly_report_total_items_temp += monthly_data_items_temp[i]
            yearly_report_total_services_temp += monthly_data_service_temp[i]
        
        yearly_report_total_all_temp = yearly_report_total_items_temp + yearly_report_total_services_temp
        yearly_report_content_temp.append(["Total: ", f'P{format_price(yearly_report_total_items_temp)}', f'P{format_price(yearly_report_total_services_temp)}', f'P{format_price(yearly_report_total_all_temp)}'])
        table_content = Table(yearly_report_content_temp)

        #add table style
        tbl_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('SPAN', (0, 0), (-1, 0)),
            #('SPAN', (0, 1), (1, 1)),
            #('SPAN', (2, 1), (3, 1)),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('ALIGN', (0, 2), (0, -1), 'LEFT'),
            ('ALIGN', (0, 2), (0, -1), 'LEFT'),
            ('ALIGN', (1, 2), (-1, -1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 3), (-1, -1), 10),
            ]
        )

        table_content.setStyle(tbl_style)

        #alternate background color
        rowNumb = len(yearly_report_content_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content.setStyle(ts)

        #add borders
        ts = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_content.setStyle(ts)
        elems = []
        elems.append(report_header)
        elems.append(table_content)
        pdf.build(elems)
        #pdf compilation
        
        #check if include_graphs is checked
        if include_graphs:
            merger = PdfWriter()
            chart_generator(monthly_data_items_temp , monthly_data_service_temp, 30, months_Text, 'Annual', y_temp, 256, 225, 100, 100, 1, [225,750])
            input1 = open(f"image/charts.pdf", "rb")
            input2 = open(filename, "rb")
            # add the first 3 pages of input1 document to output
            merger.append(input2)
            merger.append(input1)
            # Write to an output PDF document
            output = open(filename, "wb")
            merger.write(output)
            # Close File Descriptors
            merger.close()
            output.close()
        #add footer
        from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw
        
        p1 = pdfrw1(filename)
        footer_generator(len(p1.pages))
        p2 = pdfrw1("image/footer.pdf")
        footer_gen2()
        p3 = pdfrw1("image/footer2.pdf")

        for page in range(len(p1.pages)):
            merger = pdfrw(p1.pages[page])
            merger.add(p2.pages[page]).render()
            if page == (len(p1.pages)-1):
                merger.add(p3.pages[0]).render()

        writer = pdfrw2()
        writer.write(filename, p1)
        if finish_alerts:
            messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Yearly Report.", parent = master)
    
    #monthly
    if 'Monthly' == report_type:
        #start of data collection
        m_temp = months_Text.index(monthly_month)+1
        y_temp = monthly_year

        monthly_label_temp = [*range(1, calendar.monthrange(int(y_temp), m_temp)[-1]+1, 1)]
        monthly_data_items_temp2 = [database.fetch_data(sql_commands.get_items_daily_sales_sp_temp, (f'{monthly_year}-{m_temp}-{s}',))[0][0] for s in monthly_label_temp]
        monthly_data_service_temp2 = [database.fetch_data(sql_commands.get_services_daily_sales_sp_temp, (f'{monthly_year}-{m_temp}-{s}',))[0][0] for s in monthly_label_temp]

        monthly_data_items_temp = []
        monthly_data_service_temp = []

        for monthly_month in monthly_data_items_temp2:
            if monthly_month == None:
                monthly_data_items_temp.append(0)
            else:
                monthly_data_items_temp.append(monthly_month)

        for monthly_month in monthly_data_service_temp2:
            if monthly_month == None:
                monthly_data_service_temp.append(0)
            else:
                monthly_data_service_temp.append(monthly_month)

        monthly_label_temp2 = []
        for monthly_month in monthly_label_temp:
            monthly_label_temp2.append(str(monthly_month))

        full_date_temp = months_Text[m_temp-1]

        #content
        if file_name.endswith('.pdf'):
            filename = f'{desktop}\\{file_name}'
        else:
            filename = f'{desktop}\\{file_name}.pdf'
        #filename = f'{desktop}\\{full_date_temp}_{y_temp}_monthly_report.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter
        )
        #header
        report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
                        ['SJDM City, Bulacan Hardware 2000 Bldg.'],
                            ['Brgy. Graceville, SJDM City, Bulacan'],
                            ['Tel.: 8994-9043'],
                            ['Cel.: 0922-976-9287 / 0927-887-0270 / 0922-408-7709']]
        report_header = Table(report_header_temp)
        tbl_header_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (0, 0), 18),
            ('FONTSIZE', (0, 1), (0, -1), 12),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (0, 0), 20),
            ('BOTTOMPADDING', (0, len(report_header_temp)-1), (0, len(report_header_temp)-1), 25),
            ]
        )

        report_header.setStyle(tbl_header_style)
        #header for table columns
        yearly_report_content_temp = [
            [f'Monthly Sales Report as of {full_date_temp} {y_temp}'], ['Day', 'Sales', 'Services', 'Total Income']
        ]
        #add data for table
        yearly_report_total_items_temp = 0
        yearly_report_total_services_temp = 0
        monthlength = len(monthly_data_items_temp)
        for i in range(0, monthlength):
            yearly_report_temp_data = []
            yearly_report_temp_data.append(monthly_label_temp[i])
            yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i])}')
            yearly_report_temp_data.append(f'P{format_price(monthly_data_service_temp[i])}')
            yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i] + monthly_data_service_temp[i])}')
            yearly_report_content_temp.append(yearly_report_temp_data)
            yearly_report_total_items_temp += monthly_data_items_temp[i]
            yearly_report_total_services_temp += monthly_data_service_temp[i]
        
        yearly_report_total_all_temp = yearly_report_total_items_temp + yearly_report_total_services_temp
        yearly_report_content_temp.append(["Total: ", f'P{format_price(yearly_report_total_items_temp)}', f'P{format_price(yearly_report_total_services_temp)}', f'P{format_price(yearly_report_total_all_temp)}'])
        table_content = Table(yearly_report_content_temp)

        #add table style
        tbl_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('ALIGN', (0, 2), (0, -1), 'LEFT'),
            ('ALIGN', (1, 2), (-1, -1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 3), (-1, -1), 10),
            ]
        )

        table_content.setStyle(tbl_style)
        #alternate background color
        rowNumb = len(yearly_report_content_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content.setStyle(ts)

        #add borders
        ts = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_content.setStyle(ts)
        elems = []
        elems.append(report_header)
        elems.append(table_content)
        pdf.build(elems)
        #check if include_graphs is checked
        if include_graphs:
            #pdf compilation
            merger = PdfWriter()
            chart_generator(monthly_data_items_temp , monthly_data_service_temp, 0, monthly_label_temp2, 'Monthly',  f'{full_date_temp} {y_temp}', 256, 225, 100, 100, 1, [195,750])
            input1 = open(f"image/charts.pdf", "rb")
            input2 = open(f"{filename}", "rb")
            # add the first 3 pages of input1 document to output
            merger.append(input2)
            merger.append(input1)
            # Write to an output PDF document
            output = open(filename, "wb")
            merger.write(output)
            # Close File Descriptors
            merger.close()
            output.close()
        #add footer
        from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw
        p1 = pdfrw1(filename)
        footer_generator(len(p1.pages))
        p2 = pdfrw1("image/footer.pdf")
        footer_gen2()
        p3 = pdfrw1("image/footer2.pdf")

        for page in range(len(p1.pages)):
            merger = pdfrw(p1.pages[page])
            merger.add(p2.pages[page]).render()
            if page == (len(p1.pages)-1):
                merger.add(p3.pages[0]).render()

        writer = pdfrw2()
        writer.write(filename, p1)
        if finish_alerts:
            messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Monthly Report.", parent = master)

    #daily
    if 'Daily' == report_type:
        #start of data collection
        #j
        #get the current date on global daily date variable
        date_temp = datetime.datetime.strptime(daily_date_text_var.get(), '%B %d, %Y').strftime('%Y-%m-%d')

        full_date_temp = daily_date_text_var.get() #j get the global string variable value

        day_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%d')
        month_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%B')

        data_temp = [float(database.fetch_data(sql_commands.get_items_daily_sales_sp_temp, (date_temp,))[0][0] or 0),
                        float(database.fetch_data(sql_commands.get_services_daily_sales_sp_temp, (date_temp,))[0][0] or 0)]

        m_temp = monthly_month
        y_temp = monthly_year
        #end
        
        #content
        if file_name.endswith('.pdf'):
            filename = f'{desktop}\\{file_name}'
        else:
            filename = f'{desktop}\\{file_name}.pdf'
        #filename = f'{desktop}\\{month_date_temp}_{day_date_temp}_{y_temp}_daily_report.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter
        )
        #header
        report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
                        ['SJDM City, Bulacan Hardware 2000 Bldg.'],
                            ['Brgy. Graceville, SJDM City, Bulacan'],
                            ['Tel.: 8994-9043'],
                            ['Cel.: 0922-976-9287 / 0927-887-0270 / 0922-408-7709']]
        report_header = Table(report_header_temp)
        tbl_header_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (0, 0), 18),
            ('FONTSIZE', (0, 1), (0, -1), 12),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (0, 0), 20),
            ('BOTTOMPADDING', (0, len(report_header_temp)-1), (0, len(report_header_temp)-1), 20),
            ]
        )

        report_header.setStyle(tbl_header_style)
        
        yearly_report_content_temp = [[f'Daily Sales Report as of {month_date_temp} {day_date_temp}, {y_temp}'], ['Sales', f'P{format_price(data_temp[0])}'], 
                                        ['Services', f'P{format_price(data_temp[1])}'],
                                        ['Total Income', f'P{format_price(data_temp[0] + data_temp[1])}']]
        
        inventory_report_temp = [['']]

        inventory_report_data_temp = [[f'Inventory Report as of {y_temp}'], ['Item', 'Stock', 'Status']]
        #add data for table
        for x in database.fetch_data(sql_commands.get_inventory_by_group):
            temp_data = []
            temp_data.append(x[0])
            temp_data.append(x[1])
            temp_data.append(x[4])
            inventory_report_data_temp.append(temp_data)
        
        table_content = Table(yearly_report_content_temp)
        table_content2 = Table(inventory_report_temp)
        table_content3 = Table(inventory_report_data_temp)
        
        #add table style
        from reportlab.platypus import TableStyle
        tbl_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            #space at the bottom
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
            ]
        )

        tbl_style2 = TableStyle(
            [
            #font style
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            #space at the bottom
            ('TOPPADDING', (0, 0), (-1, -1), 60),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 45),
            ]
        )

        table_content.setStyle(tbl_style)
        table_content2.setStyle(tbl_style2)
        table_content3.setStyle(tbl_style)
        #alternate background color
        rowNumb = len(yearly_report_content_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content.setStyle(ts)

        rowNumb = len(inventory_report_data_temp)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.white
            else:
                bc = colors.lightgrey

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
            )
            table_content3.setStyle(ts)

        #add borders
        ts = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table_content.setStyle(ts)
        table_content3.setStyle(ts)
        
        ts = TableStyle([
            ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
        ])
        #table_content.setStyle(ts)
        elems = []
        elems.append(report_header)
        elems.append(table_content)

        pdf.build(elems)
        #pdf compilation
        sales_gen()

        merger = PdfWriter()
        input1 = open(f"image/sales.pdf", "rb")
        input2 = open(f"{filename}", "rb")
        # add the first 3 pages of input1 document to output
        merger.append(input2)
        merger.append(input1)
        # Write to an output PDF document
        output = open(filename, "wb")
        merger.write(output)
        # Close File Descriptors
        merger.close()
        output.close()

        merger = PdfWriter()
        input1 = open(f"image\charts.pdf", "rb")
        input2 = open(filename, "rb")
        
        # add the first 3 pages of input1 document to output
        merger.append(input2)
        # Write to an output PDF document
        output = open(filename, "wb")
        merger.write(output)
        # Close File Descriptors
        merger.close()
        output.close()
        #add footer
        p1 = pdfrw1(filename)
        footer_generator(len(p1.pages))
        p2 = pdfrw1("image/footer.pdf")
        if include_graphs:
            chart_generator(data_temp[0] , data_temp[1], 0, [''], 'Daily',  '', 231, 245, 150, 150, 0, [265,380])
            p3 = pdfrw1("image/charts.pdf")
        footer_gen2()
        p4 = pdfrw1("image/footer2.pdf")

        for page in range(len(p1.pages)):
            merger = pdfrw(p1.pages[page])
            merger.add(p2.pages[page]).render()
            #if page == (len(p1.pages)-1):
            if page == 0:
                merger.add(p4.pages[0]).render()
        if include_graphs:
            merger = pdfrw(p1.pages[0])
            merger.add(p3.pages[0]).render()

        writer = pdfrw2()
        writer.write(filename, p1)

        if finish_alerts:
            messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Daily Report.", parent = master)

        #Inventory Report
        
def generate_inventory_report(acc_name_preparator: str, file_name: str, acc_full_name: str, acc_pos: str, date_num: str, date_txt: str, month: int|str, year: int|str, path: str, finish_alerts: int, master: any):
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.pdfgen.canvas import Canvas
    from datetime import datetime as datetime_temp
    from reportlab.lib import colors
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import Table
    from reportlab.platypus import TableStyle
    from PyPDF2 import PdfWriter, PdfReader
    import math
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw

    ttfFile = os.path.join('C:\Windows\Fonts', 'Times.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman", ttfFile))
    ttfFile = os.path.join('C:\Windows\Fonts', 'Timesbd.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman-Bold", ttfFile))

    def footer_generator(page_count: int):
        #footer
        filename = f'image/footer.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter,
        )
        pdf.bottomMargin = 20
        pdf.leftMargin = 20
        pdf.rightMargin = 20

        tbl_footer_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
            #font style
            ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, 0), (0, -1), 14),
            ('FONTSIZE', (0, 0), (0, 0), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.lightgrey),
            #space at the bottom
            ('TOPPADDING', (0, 0), (0, -1), 670),
            ('RIGHTPADDING', (0, 0), (0, 0), 300),
            ]
        )
        elems = []
        footer_content = []
        for page in range(page_count):
            footer_content.append([["Dr. Joseph Z. Angeles Veterinary Clinic", f"Page {page+1} of {page_count}"]])
        for footer_page in range(len(footer_content)):
            table_footer = Table(footer_content[footer_page])
            table_footer.setStyle(tbl_footer_style)
            elems.append(table_footer)

        pdf.build(elems)

    def footer_gen2():
        filename = f'image/footer2.pdf'
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter,
        )
        footer_content = [['', '', ''],
                          ['Prepared by:', '', 'Prepared Date/Time:'],
                          [f'{acc_full_name}', '', f'{datetime.datetime.now().strftime("%x     %I:%M:%S %p")}'],
                          [f'{acc_pos}', '', ''],]
        table_footer = Table(footer_content)
        tbl_footer_style = TableStyle(
            [
            #text alignment, starting axis, -1 = end
            #grid goes like this (x, y) x goes from left to right
            #('ALIGN', (3, 1), (3, 1), 'RIGHT'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            #font style
            ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('FONTSIZE', (0, 3), (0, 3), 8),
            #('FONTSIZE', (1, 2), (1, 2), 8),
            #space at the bottom
            ('TOPPADDING', (0, 0), (-1, 0), 540),#670
            #('BOTTOMPADDING', (0, 2), (0, -1), -20),
            ('TOPPADDING', (0, 3), (0, 3), -40),
            ('TOPPADDING', (0, 2), (0, 2), 20),
            ('RIGHTPADDING', (1, 1), (1, -1), 200),
            #Signature line
            ('LINEBELOW', (0,2), (0,2), 0.5, colors.black),
           #('BOX', (0,0), (-1,-1), 0.5, colors.red)
            ]
        )
        table_footer.setStyle(tbl_footer_style)
        elems = []
        elems.append(table_footer)
        pdf.build(elems)
    
    
    '''date_temp = 1
    if self.date_selected_label._text.startswith(self.year_option.get()):
        date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%Y-%m-%d')
    else:
        date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%Y-%m-%d')

    full_date_temp = 1
    if self.date_selected_label._text.startswith(self.year_option.get()):
        full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%B %d, %Y')
    else:
        full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%B %d, %Y')'''
    current_date = datetime.datetime.now().strftime('%B %d, %Y')
    #print('BRUH',date_txt, type(date_txt))
    #day_date_temp = datetime.datetime.strftime(date_txt, '%B %d, %Y').strftime('%d')
    #month_date_temp = datetime.datetime.strftime(date_txt, '%B %d, %Y').strftime('%B')
    day_date_temp, month_date_temp, y_temp = date_txt.strftime('%d'), date_txt.strftime('%B'), year
    #y_temp = year
    #end
    
    #footer
    filename = f'image/footer.pdf'
    pdf = SimpleDocTemplate(
        filename=filename,
        pagesize=letter,
    )
    pdf.bottomMargin = 20
    pdf.leftMargin = 20
    pdf.rightMargin = 20
    footer_content = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 1 of 1']]
    table_footer = Table(footer_content)
    tbl_footer_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (0, -1), 14),
        ('FONTSIZE', (0, 0), (0, 0), 10),
        #space at the bottom
        ('TOPPADDING', (0, 0), (0, -1), 670),
        ('RIGHTPADDING', (0, 0), (0, 0), 300),
        ]
    )
    table_footer.setStyle(tbl_footer_style)
    elems = []
    elems.append(table_footer)
    pdf.build(elems)

    #content
    if file_name.endswith('.pdf'):
        filename = f'{path}\\{file_name}'
    else:
        filename = f'{path}\\{file_name}.pdf'
    #filename = f'{path}\\{file_name}'
    pdf = SimpleDocTemplate(
        filename=filename,
        pagesize=letter
    )
    #header
    report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
                    ['SJDM City, Bulacan Hardware 2000 Bldg.'],
                        ['Brgy. Graceville, SJDM City, Bulacan'],
                        ['Tel.: 8994-9043'],
                        ['Cel.: 0922-976-9287 / 0927-887-0270 / 0922-408-7709']]
    report_header = Table(report_header_temp)
    tbl_header_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (0, 0), 18),
        ('FONTSIZE', (0, 1), (0, -1), 12),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (0, 0), 20),
        ('BOTTOMPADDING', (0, len(report_header_temp)-1), (0, len(report_header_temp)-1), 25),
        ]
    )

    report_header.setStyle(tbl_header_style)

    inventory_report_data_temp = [[f'Inventory Report as of {month_date_temp} {day_date_temp}, {y_temp}'], ['Item Code', 'Item Description', 'Quantity']]
    #add data for table
    current_stock = database.fetch_data(sql_commands.get_inventory_info_with_uid)
    bought_item = database.fetch_data(sql_commands.get_all_bought_items_group_by_name)
    bought_item_dict = {s[0]: s[1] for s in bought_item}
    inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item_dict else bought_item_dict[s[0]]), s[1], s[2]) for s in current_stock]
    
    ctr = 0
    for x in inventory_report_data:
        temp_data = []
        #new comment, not yet applied for quantity unit name
        #comment by chris
        length_counter = 0
        item_name = x[2]
        itm_name = ''
        for i_name in item_name.split():
            length_counter += len(i_name)
            if length_counter > 25:
                length_counter = len(i_name)
                itm_name += f'\n{i_name}'
            else:
                itm_name += f'{i_name} '
        temp_data.append(x[0])
        temp_data.append(itm_name)
        temp_data.append(x[3])
        inventory_report_data_temp.append(temp_data)
    table_content = Table(inventory_report_data_temp)
    
    #add table style
    tbl_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (1, 0), (1, -1), 10),
        ]
    )

    tbl_style2 = TableStyle(
        [
        #font style
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        #space at the bottom
        ('TOPPADDING', (0, 0), (-1, -1), 60),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 45),
        ]
    )

    table_content.setStyle(tbl_style)
    #alternate background color

    rowNumb = len(inventory_report_data_temp)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table_content.setStyle(ts)

    #add borders
    ts = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table_content.setStyle(ts)
    
    ts = TableStyle([
        ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
    ])
    table_content.setStyle(ts)

    footer_content = [['', '', ''],
                    ['Prepared by:', '', 'Prepared Date/Time:'],
                    [f'{acc_full_name}', '', f'{datetime.datetime.now().strftime("%x     %I:%M:%S %p")}'],
                    [f'{acc_pos}', '', ''],]
    table_footer = Table(footer_content)
    tbl_footer_style = TableStyle(
        [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
        ('FONTSIZE', (0, 3), (0, 3), 8),
        #space at the bottom
        ('TOPPADDING', (0, 3), (0, 3), -40),
        ('TOPPADDING', (0, 2), (0, 2), 20),
        ('RIGHTPADDING', (1, 1), (1, -1), 200),
        #Signature line
        ('LINEBELOW', (0,2), (0,2), 0.5, colors.black),
        ]
    )
    table_footer.setStyle(tbl_footer_style)

    elems = []
    elems.append(report_header)
    elems.append(table_content)
    elems.append(table_footer)
    pdf.build(elems)
    #pdf compilation
    
    #add footer
    writer = pdfrw2()
    Writing = PdfWriter()
    input_file = open(f"{filename}", "rb")
    footer_input = open(f"image/footer2.pdf", "rb")
    stop_foot_gen2 = 0
    if not len(inventory_report_data_temp) % 19:
        # add the first 3 pages of input1 document to output
        Writing.append(input_file)
        Writing.append(footer_input)
        # Write to an output PDF document
        writing_output = open(filename, "wb")
        Writing.write(writing_output)
        # Close File Descriptors
        Writing.close()
        writing_output.close()
        stop_foot_gen2 = 1

    p1 = pdfrw1(filename)
    footer_generator(len(p1.pages))
    p2 = pdfrw1("image/footer.pdf")
    footer_gen2()
    #p3 = pdfrw1("image/footer2.pdf")
    for page in range(len(p1.pages)):
        merger = pdfrw(p1.pages[page])
        merger.add(p2.pages[page]).render()
        #if page == (len(p1.pages)-1):
        #    if not stop_foot_gen2:
        #        merger.add(p3.pages[0]).render()
        #else:
        #    merger.add(p2.pages[page]).render()

    
    writer.write(filename, p1)
    if finish_alerts:
        messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Inventory Report.", parent = master)