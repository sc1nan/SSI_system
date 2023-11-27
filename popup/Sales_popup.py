import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from Theme import Color
from util import database
from util import *
from tkinter import messagebox
from popup import preview_pdf_popup as ppdfp
from util import *
from datetime import date
from popup import mini_popup

def show_sales_record_info(master, info:tuple) -> ctk.CTkFrame:
    class sales_record(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            acc_cred = info[3]
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            #self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            
            def reset():
                self.place_forget()
            
            def show_receipt():
                global raw_items, raw_service_info, raw_transaction_info
                if self.client_name._text in r'N/A':
                    or_num = f"{self.date_label._text.replace('-', '_')}_noname_{self.or_label._text}_receipt"
                else:
                    or_num = f"{self.date_label._text.replace('-', '_')}_{self.client_name._text}_{self.or_label._text}_receipt"
                formatted_items = []
                for i in raw_items:
                    temp_items = [0, 1]
                    for it in i:
                        temp_items.append(it)
                    formatted_items.append(temp_items)
                
                ppdfp.preview_pdf_popup(receipt=0, view_receipt_by_or=or_num, ornum=raw_transaction_info[0], cashier=raw_transaction_info[4], client=raw_transaction_info[1], pet='s[1]', item=formatted_items, service=raw_service_info, total=(raw_transaction_info[2]), paid=(raw_transaction_info[2]), title="Transaction Receipt Viewer", is_receipt=1, deduction=raw_transaction_info[6])
            def view_removed():
                _temp = [(data[0],) + (f'{data[1]} ({data[2]})',) + data[3:] if data[2] else (data[0], data[1], data[3:]) for data in database.fetch_data(sql_commands.get_replaced_items_by_id, (self.or_label._text,))]
                self.replaced.place(relx=0.5, rely=0.5, anchor='c', info=(self.or_label._text, self.client_name._text), data=_temp)
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('view_receipt_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="SALES RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            '''INFO PART'''
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(width*0.005))
            
            #CASHIER
            self.cashier_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.175)
            self.cashier_frame.pack(side="left", padx=(width*0.0045), pady=(width*0.005))
            self.cashier_frame.pack_propagate(0)
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.055, anchor="e").pack(side="left", padx=(width*0.0045,0))
            self.cashier_name_label = ctk.CTkLabel(self.cashier_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cashier_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
        
            #DATE
            self.status = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.125)
            self.status.pack(side="left", padx=(0, width*0.005), pady=(width*0.005))
            ctk.CTkLabel(self.status, text="Status: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.035, anchor="e").pack(side="left", padx=(width*0.01,0))
            self.status_label = ctk.CTkLabel(self.status, text="", font=("DM Sans Medium", 14), height=height*0.05,padx=(int(width*0.01)))
            self.status_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
        
            #DATE
            self.date_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.2)
            self.date_frame.pack(side="right", padx=(0, width*0.005), pady=(width*0.005))
            self.date_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_frame, text="Transaction Date: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.035, anchor="e").pack(side="left", padx=(width*0.01,0))
            self.date_label = ctk.CTkLabel(self.date_frame, text="Date", font=("DM Sans Medium", 14))
            self.date_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.015))
            
            
            '''TRANSACTION INFO'''
            
            self.client_info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=2, column=0,sticky="nsew", padx=width*0.005, pady=(0,width*0.005))
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            self.client_info_frame.grid_rowconfigure(1, weight=1)
            
            #OR NUMBER 
            self.or_label = ctk.CTkLabel(self.client_info_frame, text="OR#001", fg_color=Color.White_Lotion, font=("DM Sans Medium", 14), corner_radius=5, height=height*0.05, width=width*0.115)
            self.or_label.grid(row=0, column=0, padx=(width*0.005), pady= width*0.005)
            
            #CLIENT 
            self.client_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= width*0.005)
            self.client_frame.pack_propagate(0)
            
            self.view_receipt = ctk.CTkButton(self.client_info_frame, text="View Receipt", font=("DM Sans Medium", 14), image=Icons.get_image("receipt_icon", (25,25)),
                                               fg_color=Color.Green_Pistachio, hover_color=Color.Green_Button_Hover_Color, text_color=Color.White_Lotion, command=show_receipt)
            self.view_receipt.grid(row=0, column=2, sticky="nse",padx=(0,width*0.005), pady= width*0.005)
            
            self.change_order_btn = ctk.CTkButton(self.client_info_frame, text="Replace Item", font=("DM Sans Medium", 14), image=Icons.get_image("replaced_icon", (25,25)),
                                                  text_color=Color.White_Lotion)
                                                 #command=lambda:self.change_order.place(relx=0.5, rely=0.5, anchor='c', info=self.or_label._text, items=self.items))
            
            self.replaced_item_btn = ctk.CTkButton(self.client_info_frame, text="Replaced Item", font=("DM Sans Medium", 14), cursor='hand2', text_color=Color.White_Lotion,
                                                   image=Icons.get_image('replaced_icon', (25,25)), command=view_removed,
                                                   fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,0))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14), fg_color="transparent")
            self.client_name.pack(side="left", fill='x', expand=1)
            
            #TABLE
            self.receipt_table_frame = ctk.CTkFrame(self.client_info_frame)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005, pady=(0,width*0.005) )
           
            self.receipt_treeview = cctk.cctkTreeView(self.receipt_table_frame, width= width * .795, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Particulars:x-tl/UnitPrice:{int(width*.1)}-tr/Quantity:{int(width*.115)}-tr/Total:{int(width*.1)}-tr!30!30')
            
            self.receipt_treeview.pack()
            '''TOTAL'''
            self.bottom_frame = ctk.CTkFrame(self.client_info_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=width*0.005, pady=(width*0.005))
            
            self.receipt_total_frame = ctk.CTkFrame(self.bottom_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.pack(side='right')
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ ---,---.--",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
          
            self.labels = [self.or_label, self.client_name, self.receipt_total_amount, self.date_label, self.cashier_name_label]
        
            self.change_order = change_order(self,(width, height, acc_info, acc_cred))
            self.replaced = view_removed_items(self,(width, height, acc_info, acc_cred))
            self.replace_authorization = mini_popup.authorization(self, (width, height), lambda:self.change_order.place(relx=0.5, rely=0.5, anchor='c', info=self.or_label._text, items=self.items))
            self.change_order_btn.configure(command = lambda: self.replace_authorization.place(relx = .5, rely = .5, anchor = 'c'))

        def set_values(self):
            [self.labels[i].configure(text=f"{self.transact_info[i]}") for i in range(len(self.labels))]     
            self.status_label.configure(text=f"{'Paid' if self.transact_info[-1] == 1 else 'Paid and Replaced'}")
            #change to -2 since the -1 became the deduction
            
            if self.transact_info[-2] == 1:
                self.change_order_btn.grid(row=0, column=3, sticky="nse",padx=(0,width*0.005), pady= width*0.005)  
                self.replaced_item_btn.grid_forget()
            else:
                self.change_order_btn.grid_forget()
                self.replaced_item_btn.grid(row=0, column=3, sticky="nse",padx=(0,width*0.005), pady= width*0.005)                 
            
            if not self.items: #removve replace item when theres non item in the record
                self.change_order_btn.grid_forget()
            else:
                self.change_order_btn.grid(row=0, column=3, sticky="nse",padx=(0,width*0.005), pady= width*0.005) 
        
        def place(self, sales_info, **kwargs):
            try:
                return super().place(**kwargs)
            finally:
                global raw_items, raw_service_info, raw_transaction_info
                raw_items = database.fetch_data(sql_commands.get_item_record, (sales_info[0],))
                raw_service = database.fetch_data(sql_commands.get_service_record, (sales_info[0],))
                self.transact_info = database.fetch_data(sql_commands.get_sales_record_info, (sales_info[0],))[0]  
                raw_service_info = database.fetch_data(sql_commands.get_service_record_temp, (sales_info[0],))
                raw_transaction_info = database.fetch_data(sql_commands.get_sales_record_info_temp, (sales_info[0],))[0]      
                
                temp = [split_unit(item[0])+(item[1:]) for item in raw_items]
                self.items = [((f'{database.fetch_data(sql_commands.get_item_brand, database.fetch_data(sql_commands.get_uid, (temp[0], temp[1]))[0])[0][0]} {temp[0]} ({temp[1]})'),) +  temp[2:] if len(temp)==5 else 
                            ((f'{database.fetch_data(sql_commands.get_item_brand, database.fetch_data(sql_commands.get_uid_null_unit, (temp[0],))[0])[0][0]} {temp[0]}'),) +  temp[1:] for temp in temp]
                raw_data =  raw_service + self.items
                self.tree_data = [(data[0],  f"₱{format_price(data[2])}", data[1], f"₱{format_price(data[3])}") for data in raw_data]
                self.receipt_treeview.update_table(self.tree_data) 
            
                self.set_values()
            
    return sales_record(master, info)


def change_order(master, info:tuple) -> ctk.CTkFrame:
    class change_order(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            #self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            self.replaced_items = []
            self.added_items = []
            
            def reset():
                if messagebox.askyesno("Close","Are you sure you want to cancel this process?\nThis will erase your current progress."):
                    self.replace_item_btn.configure(text=f"Replaced Items (0)")
                    self.replaced_items.clear()
                    self.status_check()
                    self.place_forget()
            
            def change_callback(event):
                if self.change_btn.cget('state') == 'disabled':
                    messagebox.showwarning("Warning","New total is not equal or greater than the original \nor you have not add any changes.\nPlease check your inputs.")
           
            def confirm_chage():
                total_items = sum_similar_elements([(data[0], data[1], data[2], data[4]) for data in self.replaced_items])
                
                replaced_items = [((item[0],) + split_unit(item[1]) + item[2:]) for item in total_items]
                items_inventory = count_inventory(combine_lists(lists=[self.table_data, total_items, self.table_values()], key_index=(0,3)))
                updated_items = [(data[0],) + split_unit(data[1]) + data[2:] for data in self.table_values()]
                
                self.replace_to_record = [(database.fetch_data(sql_commands.get_item_info, (data[1], data[2]))[0][0],) + (data[0],) + (f'{data[1]} ({data[2]})',) + data[3:] if len(data) == 7 
                                          else (database.fetch_data(sql_commands.get_item_info_null_unit, (data[1],))[0][0],) + data for data in replaced_items]
                self.inventory_update_stock = [(database.fetch_data(sql_commands.get_item_info, (data[1], data[2]))[0][0],) + (data[0],) + (f'{data[1]} ({data[2]})',) + (data[3],) if len(data) == 4 
                                               else (database.fetch_data(sql_commands.get_item_info_null_unit, (data[1],))[0][0],) + data for data in items_inventory]
                self.updated_items_id = [(database.fetch_data(sql_commands.get_item_info, (data[1], data[2]))[0][0],) + (data[0],) + (f'{data[1]} ({data[2]})',) + data[3:] if len(data) == 6 
                                         else (database.fetch_data(sql_commands.get_item_info_null_unit, (data[1],))[0][0],) + data for data in updated_items if data[-2] != 0]
                
                #print(self.replace_to_record,"\n",self.inventory_update_stock, '\n',self.updated_items_id,)
                
                if price_format_to_float(self.new_total_label._text[1:]) >= price_format_to_float(self.original_total_label._text[1:]):
                    if messagebox.showinfo("Replacement Confirmation", "You will proceed to the payment."):
                        self.show_payment_proceed.place(relx=0.5,rely=0.5,anchor='c', info=self.or_label._text, items=self.table_values(), info_lists = (self.replace_to_record, self.inventory_update_stock, self.updated_items_id),
                                                        item_total=self.new_total_label._text, service_total=self.service_total, or_num=self.or_label._text, cashier=acc_info[0][0], client=self.client_name_label._text)
                        
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure((1), weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('view_receipt_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="CHANGE ORDER", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            #region Sales Table
            
            self.sales_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5,)
            self.sales_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=width*0.005, pady=width*0.005)
            self.sales_frame.grid_propagate(0)
            
            '''Client Frame'''
            self.client_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.client_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=width*0.005, pady=(width*0.005,0))
            
            self.or_label = ctk.CTkLabel(self.client_frame, text='', font=('DM Sans Medium', 14), fg_color=Color.White_Lotion, width=width*0.125, height=height*0.055, corner_radius=5)
            self.or_label.pack(side='left',padx=(width*0.005,0), pady=(width*0.005))
            
            '''Client Name Frame'''
            self.client_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.client_name_frame.pack(side="left", padx=(width*0.005), pady=(width*0.005))
            self.client_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.client_name_frame, text="Client: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.client_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Date Frame'''
            self.date_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.date_frame.pack(side="right", expand=0, padx=(0,width*0.005), pady=(width*0.005))
            self.date_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_frame, text="Date: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.date_label = ctk.CTkLabel(self.date_frame, text="2023-11-01", font=("DM Sans Medium", 14))
            self.date_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Cashier Name Frame'''
            self.cashier_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.cashier_name_frame.pack(side="right", padx=(width*0.005), pady=(width*0.005))
            self.cashier_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.cashier_name_frame, text="Cashier: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.cashier_name_label = ctk.CTkLabel(self.cashier_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cashier_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Button Frame'''
            self.button_frame = ctk.CTkFrame(self.sales_frame, fg_color='transparent',height=height*0.055)
            self.button_frame.pack(fill='x', expand=0 ,padx=(width*0.005), pady=(width*0.005))
            
            self.add_item_btn = ctk.CTkButton(self.button_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 14), text='Add Item',
                                         command=lambda:self.add_item.place(relx=0.5, rely=0.5, anchor='c'))
           
            
            self.replace_item_btn = ctk.CTkButton(self.button_frame, width=width*0.125, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 14), text='Replaced Items (0)', 
                                            command=lambda:self.removed_item.place(relx=0.5, rely=0.5, anchor='c', info=(self.or_label._text, self.client_name_label._text), data=self.replaced_items))
            self.replace_item_btn.pack(side="left", padx=(0), pady=(0))
            
            '''Treeview'''
            self.client_treeview_frame = ctk.CTkFrame(self.sales_frame, corner_radius=0,fg_color=Color.White_Platinum)
            self.client_treeview_frame.pack(fill='both', expand=0, padx=(width*0.005), pady=(0,width*0.005))
            
            self.client_treeview = cctk.cctkTreeView(self.client_treeview_frame, data=[], width= width*0.795, height= height*0.57, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*.08)}-tl/ItemDescription:x-tl/UnitPrice:{int(width*.085)}-tr/QuantityPcs:{int(width*.115)}-id/Total:{int(width*.085)}-tr!30!35',
                                           bd_message="Are you sure want to remove this item?")
            self.client_treeview.pack()
            
            #endregion 
    
            #region Financial Additionals
            
            self.finance_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5, height=height*0.065)
            self.finance_frame.grid(row=3, column=0, columnspan=1, rowspan=1, sticky='nsew', padx=(width*0.005), pady=(0,width*0.005))
            
            self.original_total_frame = ctk.CTkFrame(self.finance_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.original_total_frame.pack(side="left", padx=(width*0.005), pady=(width*0.005))
            self.original_total_frame.pack_propagate(0)
            ctk.CTkLabel(self.original_total_frame, text="Original Item Total: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.015,0))
            self.original_total_label = ctk.CTkLabel(self.original_total_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14), anchor='e')
            self.original_total_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.015))
            
            self.new_total_frame = ctk.CTkFrame(self.finance_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.new_total_frame.pack(side="right", padx=(width*0.005), pady=(width*0.005))
            self.new_total_frame.pack_propagate(0)
            ctk.CTkLabel(self.new_total_frame, text="New Item Total: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.015,0))
            self.new_total_label = ctk.CTkLabel(self.new_total_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14), anchor='e')
            self.new_total_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.015))
            
            #endregion
            
            #region Action
            
            self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5, width=width*0.215, height=height*0.065)
            self.action_frame.grid(row=3, column=1, columnspan=1, sticky='nsew', padx=(0, width*0.005), pady=(0,width*0.005))
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.085, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left", padx=(width*0.005,0), pady=(width*0.005)) 
            
            self.change_btn = ctk.CTkButton(self.action_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Change Order',
                                         command=confirm_chage, state='disabled')
            self.change_btn.pack(side="left",fill='x', expand=1,padx=(width*0.005), pady=(width*0.005))
            self.change_btn.bind("<Button-1>", change_callback)
            #endregion
            
            self.labels = [self.or_label, self.client_name_label, self.original_total_label, self.date_label, self.cashier_name_label]

            self.confirm_removal = confirm_removal(self,(width, height, acc_info), command_callback=self.close_callback)
            self.removed_item = removed_items(self,(width, height, acc_info))
            self.show_payment_proceed = show_payment_proceed(self, (width, height, acc_info))
            self.add_item = add_item(self, (width, height), self.client_treeview, command_callback = self.update_table_buttons)
            
        
        def status_check(self):
            if price_format_to_float(self.new_total_label._text[1:]) >= price_format_to_float(self.original_total_label._text[1:]) and len(self.replaced_items) != 0:
                self.change_btn.configure(state='normal')
            else:
                self.change_btn.configure(state='disabled')
                
            if len(self.replaced_items) != 0:
                self.add_item_btn.pack(side="right",padx=(0), pady=(0))
            else:
                self.add_item_btn.pack_forget()
                
        def close_callback(self, res):
            if not res[0]:
                self.origin.master.change_value()
            else:
                self.row_root.winfo_children()[5].configure(text=f"₱{format_price(price_format_to_float(remove_special_char(self.row_data[2],['₱'])) * float(self.row_count))}")
                self.replaced_items.append(res[1])
            self.update_new_total()
            self.replace_item_btn.configure(text=f"Replaced Items ({len(self.replaced_items)})")
            
        def row_values(self, event):
            self.row_root, self.origin = event.widget.master.master.master.master, event.widget.master
            self.row_data = (self.row_root.winfo_children()[1]._text, self.row_root.winfo_children()[2]._text, self.row_root.winfo_children()[3]._text, self.row_root.winfo_children()[5]._text)
            self.row_count, self.val_range = self.row_root.winfo_children()[4].winfo_children()[0].get(), self.row_root.winfo_children()[4].winfo_children()[0].get_val_range()
            


            if self.origin.cget('state') != 'disabled' and self.origin._text == '-':
                self.confirm_removal.place(relx=0.5, rely=0.5, anchor='c', data = self.row_data)
            elif self.origin._text == '+':
                if messagebox.askyesno("Replacement Confirmation", "Are you sure on replacing or adding this item?"):
                    self.row_root.winfo_children()[5].configure(text=f"₱{format_price(price_format_to_float(remove_special_char(self.row_data[2],['₱'])) * float(self.row_count))}")
                    self.update_new_total()
                else:
                    self.origin.master.change_value(-1)
                
            if self.row_count != 0:
                self.row_root.winfo_children()[4].winfo_children()[0].winfo_children()[0].configure(state='normal')
            else:
                self.row_root.winfo_children()[4].winfo_children()[0].winfo_children()[0].configure(state='disabled')

        def table_values(self):
            return [(data.winfo_children()[1]._text, data.winfo_children()[2]._text, data.winfo_children()[3]._text, data.winfo_children()[4].winfo_children()[0].get(), data.winfo_children()[5]._text ) for data in self.client_treeview.data_frames]
            
        def update_new_total(self):
            totals = ([price_format_to_float(remove_special_char(data.winfo_children()[5]._text, ['₱'])) for data in self.client_treeview.data_frames])   
            self.new_total_label.configure(text=f"₱{format_price(sum(totals))}")
            self.status_check()
            
        def set_values(self):
            [self.labels[i].configure(text=f"{self.transact_info[i]}") for i in range(len(self.labels))]
            self.original_total_label.configure(text=f"₱{self.item_total}")
            self.new_total_label.configure(text=f"₱{self.item_total}")
            
            
        def set_table(self):
            self.table_data = [(tuple(item[0].split(" ",1)) + (f'₱{format_price(item[2])}', item[1], f'₱{format_price(item[3])}'))for item in self.items]
            temp  = [(item[0], item[1], item[2], item[4]) for item in self.table_data]
            self.client_treeview.update_table(temp)
            #self.update_new_total()
            spinners = [spinner.winfo_children()[4].winfo_children()[0] for spinner in self.client_treeview.data_frames]
            item_ids = [database.fetch_data(sql_commands.get_item_id_by_name_unit, split_unit(item.winfo_children()[2]._text))[0][0] if len(split_unit(item.winfo_children()[2]._text)) == 2
                    else database.fetch_data(sql_commands.get_item_id_by_name_null_unit, split_unit(item.winfo_children()[2]._text))[0][0] for item in self.client_treeview.data_frames]
            #get_stocks_by_id
            for item in range(len(spinners)):
                spinners[item].configure(val_range = (0,database.fetch_data(sql_commands.get_stocks_by_id, (item_ids[item],))[0][0] or self.items[item][1]))
                spinners[item].configure(value = self.items[item][1])
            
                spinners[item].winfo_children()[0].bind("<Button-1>", self.row_values)
                
                
                if not database.fetch_data(sql_commands.get_stocks_by_id, (item_ids[item],))[0][0]:
                    spinners[item].winfo_children()[2].configure(state='disabled')
                else:
                    spinners[item].winfo_children()[2].bind("<Button-1>", self.row_values)
                spinners[item].set_entry_state('disabled')
                
        def update_table_buttons(self):
            self.update_new_total()
            spinners = [spinner.winfo_children()[4].winfo_children()[0] for spinner in self.client_treeview.data_frames]
            for item in range(len(spinners)):
                spinners[item].winfo_children()[0].bind("<Button-1>", self.row_values)
                spinners[item].winfo_children()[2].bind("<Button-1>", self.row_values)
                spinners[item].set_entry_state('disabled')
                
        def place(self, info, items, **kwargs):
            try:
                self.transact_info = database.fetch_data(sql_commands.get_sales_record_info, (info,))[0]
                self.item_total = format_price(database.fetch_data(sql_commands.get_item_total_by_id, (info,))[0][0])
                self.service_total = format_price(database.fetch_data(sql_commands.get_service_total_by_id, (info,))[0][0] or 0)
                
                
                self.items = [(item[0], int(item[1].split()[0]), item[2], item[3]) for item in items]
                
                self.set_values()
                self.set_table()
                return super().place(**kwargs)
            finally:
                item_ids = [database.fetch_data(sql_commands.get_item_id_by_name_unit, split_unit(items[0][0].split(' ', 1)[1]))[0][0] if len(split_unit(items[0][0].split(' ', 1)[1])) == 2
                    else database.fetch_data(sql_commands.get_item_id_by_name_null_unit, split_unit(items[0][0].split(' ', 1)[1]))[0][0] for item in items]
             
                temp = [database.fetch_data(sql_commands.get_stocks_by_id, (ids,))[0][0] or 0 for ids in item_ids]
                #print(temp)
                if 0 in temp:
                    messagebox.showinfo("Replacement ","An item in this record is currently out of stock and cannot be replaced", parent = self)
        
        def place_forget(self, **kwargs):
            self.replace_item_btn.configure(text=f"Replaced Items (0)")
            self.replaced_items.clear()
            self.status_check()
            return super().place_forget(**kwargs)
            
            
            
    return change_order(master, info)

def confirm_removal(master, info:tuple, command_callback:callable = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback:callable):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            super().__init__(master, width * 0.5, height=height*0.45, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            #self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            self.result = None
            self._command_callback = command_callback
            
            def reset():
                self.result = 0
                self.reason_option.set('')
                self.place_forget()
                if self._command_callback is not None:
                    self._command_callback((self.result,))
            
            def confirm():
                if self.reason_option.get() == "":
                    messagebox.showerror("Missing Field","Please select a reason for the item replacement")
                else:
                    self.result = 1
                    self.place_forget()
                    if self._command_callback is not None: 
                        self._command_callback((self.result, self.data+(self.reason_option.get(),)))
                
                    self.reason_option.set('')
            
            self.reasons = ['Defective/Damaged', 'Expired']

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure((1), weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('view_receipt_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="CONFIRM ITEM REPLACEMENT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
           
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky='nsew', padx=(width*0.005), pady=(width*0.005))
            self.content_frame.grid_columnconfigure(1, weight=1)
            
            self.item_code_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06, width=width*0.2)
            self.item_code_frame.grid(row=0, column=0,  padx=width*0.005, pady=(width*0.005))
            self.item_code_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_code_frame, text="Item Code: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.item_code_label = ctk.CTkLabel(self.item_code_frame, text="", font=("DM Sans Medium", 14))
            self.item_code_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005)) 
            
            self.item_brand_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06, width=width*0.185)
            self.item_brand_frame.grid(row=0, column=1, sticky='nsew',padx=(0, width*0.005), pady=(width*0.005))
            self.item_brand_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_brand_frame, text="Item Brand: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.item_brand_label = ctk.CTkLabel(self.item_brand_frame, text="", font=("DM Sans Medium", 14))
            self.item_brand_label.pack(side="left",padx=(width*0.005)) 
            
            self.item_desc_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06, width=width*0.185)
            self.item_desc_frame.grid(row=1, column=0, columnspan=2, sticky='nsew',padx=(width*0.005), pady=(0,width*0.005))
            self.item_desc_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_desc_frame, text="Item Description: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.item_desc_label = ctk.CTkLabel(self.item_desc_frame, text="", font=("DM Sans Medium", 14))
            self.item_desc_label.pack(side="left", padx=(width*0.005))
            
            
            ctk.CTkLabel(self.content_frame, text="Reason: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="w").grid(row=3, column=0, padx=(width*0.005), pady=(width*0.005,0), sticky="nsew")
            self.reason_option= ctk.CTkOptionMenu(self.content_frame, values=self.reasons, anchor="center", font=("DM Sans Medium", 14), height=height*0.055 , dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            self.reason_option.grid(row=4, column=0, columnspan=2, padx=(width*0.005), pady=(width*0.005), sticky="nsew")
            self.reason_option.set('') 
             
            self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5, width=width*0.215, height=height*0.065)
            self.action_frame.grid(row=2, column=0, columnspan=1, sticky='nsew', padx=(width*0.005), pady=(0,width*0.005))
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.085, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left", padx=(width*0.005,0), pady=(width*0.005)) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm',
                                         command=confirm)
            self.add_btn.pack(side="right",padx=(width*0.005), pady=(width*0.005))
            
            #self.labels=[self.item_code_label, self.item_brand_label, self.item_desc_label]
          
        
          
        def place(self, data, **kwargs):
            self.item_brand_label.configure(text=data[0])
            self.item_desc_label.configure(text=data[1]) 
            self.data = data
            temp = split_unit(data[1])
            self.item_info = database.fetch_data(sql_commands.get_item_info, (temp)) if len(temp) == 2 else database.fetch_data(sql_commands.get_item_info_null_unit, (temp))
            
            #print(self.item_info)
            self.item_code_label.configure(text=self.item_info[0][0])
            return super().place(**kwargs)
            
            
            
    return instance(master, info, command_callback)

def removed_items(master, info:tuple, command_callback:callable = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback:callable):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            super().__init__(master, width*0.8, height=height*0.85, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            #self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            self.result = None
            self._command_callback = command_callback
            
            def reset():
                self.place_forget()
            
            self.reasons = ['Defective/Damaged', 'Expired']

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure((2), weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('view_receipt_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="REPLACED ITEMS", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            '''Client Frame'''
            self.client_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.client_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=width*0.005, pady=(width*0.005,0))
            
            self.or_label = ctk.CTkLabel(self.client_frame, text='', font=('DM Sans Medium', 14), fg_color=Color.White_Lotion, width=width*0.125, height=height*0.055, corner_radius=5)
            self.or_label.pack(side='left',padx=(width*0.005,0), pady=(width*0.005))
            
            '''Client Name Frame'''
            self.client_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.client_name_frame.pack(side="right", padx=(width*0.005), pady=(width*0.005))
            self.client_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.client_name_frame, text="Client: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.client_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
           
           
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=2, column=0, sticky='nsew', padx=(width*0.005), pady=(width*0.005))
            self.content_frame.grid_columnconfigure(1, weight=1)
            
            '''Treeview'''
            self.client_treeview_frame = ctk.CTkFrame(self.content_frame, corner_radius=0,fg_color=Color.White_Platinum)
            self.client_treeview_frame.pack(fill='both', expand=1, padx=(width*0.005), pady=(width*0.005))
            
            self.item_treeview = cctk.cctkTreeView(self.client_treeview_frame, data=[], width= width*0.775, height= height*0.595, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*.08)}-tl/ItemDescription:x-tl/UnitPrice:{int(width*.085)}-tr/QuantityPcs:{int(width*.1)}-tr/TotalPrice:{int(width*.085)}-tr/Reason:{int(width*.125)}-tl!33!35',
                                           bd_message="Are you sure want to remove this item?")
            self.item_treeview.pack()
            
            
             
            self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5, width=width*0.215, height=height*0.065)
            self.action_frame.grid(row=3, column=0, columnspan=1, sticky='nsew', padx=(width*0.005), pady=(0,width*0.005))
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.085, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 16), text='Close', command=reset)
            self.cancel_btn.pack(side="right", padx=(width*0.005), pady=(width*0.005)) 
            
            #self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm',
            #                             command=confirm)
            #self.add_btn.pack(side="right",padx=(width*0.005), pady=(width*0.005))
            
            #self.labels=[self.item_code_label, self.item_brand_label, self.item_desc_label]
          
        def set_table(self):
            self.or_label.configure(text=self.info[0])
            self.client_name_label.configure(text=self.info[1])
            data = sum_similar_elements([(data[0], data[1], data[2], data[4]) for data in self.data])
            self.item_treeview.update_table(data)
        
          
        def place(self, info, data, **kwargs):
            print(info, data)
            self.info = info
            self.data = data
            self.set_table()
            
            return super().place(**kwargs)

    return instance(master, info, command_callback)

def show_payment_proceed(master, info:tuple,):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            global width, height
            width = info[0]
            height = info[1]

            
            super().__init__(master,  width=width*0.815, height=height*0.875, corner_radius= 0, fg_color="transparent")

            #self.payment_icon = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(28,28))
                
            def close():
                self.place_forget()
                self.or_label.configure(text = '_')
                self.payment_entry.delete(0, ctk.END)
                self.payment_total.configure(text = "₱ --.--")
                self.change_total.configure(text = "--.--")
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.8155, height=height*0.885, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('payment_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="PAYMENT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=close).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            
            def confirm():
                #(161, 'I00002', 'Taglory Rope Dog Leash (100mg)', 5, 440.0, 0)
                replaced_items = self.info_list[0]
                required_items = self.info_list[1]
                transact_items = self.info_list[2]
                
                print(replaced_items)
                print(required_items)
                print(transact_items)
                
                
                items = ([(self.or_label._text, item[0], item[2], item[4], price_format_to_float(item[3][1:])) for item in transact_items])
                payment = float((self.payment_entry.get() or 0))
                
                #steps insert replacement record, update transaction record to replaced, update item transaction content to 2, insert new transaction content, subtract items used in inventory
                if messagebox.askyesno("Replacement Confirmation", "Are you sure you want to conntinue?\nThis will update the order record."):
                     
                    rep_id = generateId(initial='REP', length=10).upper()
                    database.exec_nonquery([
                            [sql_commands.set_replacement_record, (rep_id, self.or_label._text, price_format_to_float(self.new_total._text[1:]),  self.cashier_name._text)],
                            
                            [sql_commands.update_transaction_record_to_replaced, (price_format_to_float(self.new_total._text[1:]), self.or_label._text)],
                            
                            [sql_commands.update_item_transaction_content_to_replaced, (self.or_label._text,)]])
                            
                    for item in transact_items:
                        database.exec_nonquery([[sql_commands.record_item_transaction_content, (self.or_label._text, item[0], item[2], item[4], price_format_to_float(item[3][1:]),0)]])
                            
                    for record in replaced_items:
                        database.exec_nonquery([[sql_commands.set_replacement_items, (rep_id, record[0], record[2], price_format_to_float(record[3][1:]), record[4], record[6])],
                                                
                                                [sql_commands.set_expired_items_from_inventory, (generateId("DIS",6).upper(), None, record[0], record[2], record[4],  record[6], self.cashier_name._text)]])

                    for item in required_items:
                        does_expire = bool(database.fetch_data(sql_commands.check_item_if_it_expire_by_categ, (item[0], ))[0][0])
                        quantity_needed = item[3]
                        stocks = database.fetch_data(sql_commands.get_specific_stock_ordered_by_expiry if does_expire
                                                    else sql_commands.get_specific_stock_ordered_by_date_added, (item[0], ))
                        
                
                        for st in stocks:
                            if st[2] == quantity_needed and st == stocks[-1]:
                                database.exec_nonquery([[sql_commands.null_stocks_by_id, (st[0], )]])
                            elif st[2] > quantity_needed:
                                database.exec_nonquery([[sql_commands.deduct_stocks_by_id, (quantity_needed, st[0])]])
                                quantity_needed = 0
                                break
                            elif st[2] <= quantity_needed:
                                database.exec_nonquery([[sql_commands.delete_stocks_by_id, (st[0], )]])
                                quantity_needed -= st[2]


                    messagebox.showinfo("Success",f"Order {self.or_label._text} Successfully Changed.") #item_particulars, service_particulars
                    ppdfp.preview_pdf_popup(receipt=1, ornum=self.or_label._text, cashier=self.cashier_name._text, client=self.client_name._text, pet='s[1]', item=items, service=self.service_data, total=price_format_to_float(self.new_total._text[1:]), paid=payment, deduction=0,
                                        title="Transaction Receipt Viewer", is_receipt=1, is_replaced=True)
                    self.master.master.place_forget()
                    self.master.place_forget()
                    self.master.master.master.refresh()
                    close()
                
            
            def payment_callback(var, index, mode):
                if re.search(r'[0-9\.]$', self.payment_entry.get() or "") is None and self.payment_entry._is_focused and self.payment_entry.get():
                        l = len(self.payment_entry.get())
                        self.payment_entry.delete(l-1, l)
                        
                payment = 0 if self.payment_entry.get() == '' else self.payment_entry.get()
                
                self.payment_total.configure(text=f"{'₱{:0,.2f}'.format(float(payment))}")
                self.change_total.configure(text=f"₱0.00") if float(payment) - price_format_to_float(self.payable_amount._text[1:]) <= 0 else self.change_total.configure(text=f"{'₱{:0,.2f}'.format(float(payment) - price_format_to_float(self.payable_amount._text[1:]))}")
                
                if (float(payment) >= price_format_to_float(self.payable_amount._text[1:])):  
                    self.complete_button.configure(state='normal') 
                else: 
                    self.complete_button.configure(state='disabled')
                 
                    
            self.payment_var = ctk.StringVar()
            
            '''Transaction Info'''
            self.client_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=0, column=0,sticky="nsew", columnspan=2, padx=width*0.005, pady=height*0.01)
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            
            self.cashier_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05,)
            self.cashier_frame.grid(row=0, column=0, padx=(width*0.005,0), pady= height*0.007)
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01))
            self.cashier_name = ctk.CTkLabel(self.cashier_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.cashier_name.pack(side="left",padx=(0,width*0.005))
            
            self.time_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.time_frame.grid(row=0, column=3, padx=width*0.005, pady= height*0.007, sticky="nse")
            
            self.date_label = ctk.CTkLabel(self.time_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium", 14), text=date.today().strftime('%B %d, %Y'), width=width*0.1)
            self.date_label.pack(side="right", padx=(width*0.005))
            
            self.receipt_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.receipt_frame.grid(row=1, column=0, sticky="nsew",padx=width*0.005, pady=(0,height*0.01))
            self.receipt_frame.grid_rowconfigure(1, weight=1)
            self.receipt_frame.grid_columnconfigure(1,weight=1)
            
            self.or_label = ctk.CTkLabel(self.receipt_frame,  text="OR#: ___",  font=("DM Sans Medium", 14),  height=height*0.05, width=width*0.1, fg_color=Color.White_Lotion, corner_radius=5)
            self.or_label.grid(row=0, column=0, padx=width*0.005, pady= height*0.005)

            self.client_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= height*0.007)
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.client_name.pack(side="left") 
            
            self.receipt_table_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Platinum, corner_radius=0)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,width*0.005) )
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            '''TABLE SETUP'''
            self.particulars_treeview = cctk.cctkTreeView(self.receipt_table_frame, data=[], width= width*0.515, height= height*0.625, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Particulars:x-tl/Quantity:{int(width*.1)}-tr/TotalPrice:{int(width*.085)}-tr!30!35',
                                           bd_message="Are you sure want to remove this item?")
            self.particulars_treeview.pack()

            '''END TABLE SETUP'''
            self.receipt_total_frame = ctk.CTkFrame(self.receipt_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.grid(row=2, column=2, padx=(0,width*0.005), pady= (0,height*0.007), sticky="e")
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ 0.00",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
            
            self.payment_frame= ctk.CTkFrame(self.content_frame, width=width*0.275, fg_color=Color.White_Platinum)
            self.payment_frame.grid(row=1, column=1, sticky="nsew", padx=(0,width*0.005), pady=(0,height*0.01))
            self.payment_frame.grid_columnconfigure((0,1), weight=1)
            self.payment_frame.grid_rowconfigure(0, weight=1)
            self.payment_frame.grid_propagate(0)
            
            self.pay_frame = ctk.CTkFrame(self.payment_frame, fg_color=Color.White_Lotion)
            self.pay_frame.grid(row=0, column=0, columnspan=2, padx=(width*0.005), pady=(height*0.007,0), sticky="nsew")
            self.pay_frame.grid_columnconfigure(1, weight=1)
            self.pay_frame.grid_rowconfigure(6, weight=1)
            
            ctk.CTkLabel(self.pay_frame, text="Services: ", font=("DM Sans Medium",16),).grid(row=0, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.services_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.services_total.grid(row=0, column=2, padx=(width*0.01), pady=(height*0.025,0), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Items: ", font=("DM Sans Medium",16),).grid(row=1, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.items_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor= 'e')
            self.items_total.grid(row=1, column=2, padx=(width*0.01), pady=(height*0.005,height*0.01), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=2, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="New Total: ", font=("DM Sans Medium",16),).grid(row=3, column=0, padx=(width*0.01), pady=(height*0.015,0), sticky="w")
            self.new_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.new_total.grid(row=3, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Original Total: ", font=("DM Sans Medium",16),).grid(row=4, column=0, padx=(width*0.01), pady=(height*0.005,0), sticky="w")
            self.orig_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.orig_total.grid(row=4, column=2, padx=(width*0.01), pady=(height*0.005,), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=5, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.005, 0))
            
            ctk.CTkLabel(self.pay_frame, text="Payable: ", font=("DM Sans Medium",16),).grid(row=6, column=0, padx=(width*0.01), pady=(height*0.0025,0), sticky="nw")
            self.payable_amount = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.payable_amount.grid(row=6, column=2, padx=(width*0.01), pady=(height*0.0025,height*0.01), sticky = 'ne')
            
            self.ammount_tendered = ctk.CTkLabel(self.pay_frame, text="Amount Tendered: ", font=("DM Sans Medium",16),)
            
            self.payment_entry = ctk.CTkEntry(self.pay_frame, font=("DM Sans Medium",16), justify="right", height=height*0.055, textvariable=self.payment_var)
            
            self.payment_var.trace_add("write", callback=payment_callback)
                        
            ctk.CTkLabel(self.pay_frame, text="Payment: ", font=("DM Sans Medium",16),).grid(row=8, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.payment_total = ctk.CTkLabel(self.pay_frame, text="₱ --.--", font=("DM Sans Medium",16), anchor='e')
            self.payment_total.grid(row=8, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=9, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="Change: ", font=("DM Sans Medium",16),).grid(row=10, column=0, padx=(width*0.01), pady=(height*0.01,height*0.1), sticky="w")
            self.change_total = ctk.CTkLabel(self.pay_frame, text="₱ --.--", font=("DM Sans Medium",18))
            self.change_total.grid(row=10, column=2, padx=(width*0.01), pady=(height*0.005, height*0.1), sticky = 'e')
            self.change_total.focus()
            
            self.complete_button = ctk.CTkButton(self.payment_frame, text="Complete",font=("DM Sans Medium",16), command=confirm)
            self.complete_button.grid(row=2, column=1, sticky="nsew", padx=(width*0.005), pady=(height*0.007))
            
            self.cancel_button = ctk.CTkButton(self.payment_frame, text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip
                                               ,font=("DM Sans Medium",16), width=width*0.065, height=height*0.05)
            self.cancel_button.configure(command=self.reset)
            self.cancel_button.grid(row=2, column=0, sticky="nsew", padx=(width*0.005,0), pady=(height*0.007))
            
        def reset(self):
            if messagebox.askyesno("Exit Confirmation", "Are you sure you want to cancel this process?\nThis will discard all your changes."):
                self.or_label.configure(text = '_')
                self.payment_entry.delete(0, ctk.END)
                self.payment_total.configure(text = "₱ --.--")
                self.change_total.configure(text = "--.--")
                self.or_label.configure(text= "OR#: ___")
                self.master.place_forget()
                self.place_forget()

        def set_values(self):
            global width, height
            total = f"₱{format_price(price_format_to_float((self.item_total[1:])) + float(self.service_total))}"
            temp = self.service_data + [item for item in self.item_data if item[1] > 0]
            
            self.or_label.configure(text=self.or_number)
            self.client_name.configure(text=self.client_data)
            self.cashier_name.configure(text=self.cashier_data)
            
            self.particulars_treeview.update_table(temp)
            self.receipt_total_amount.configure(text=total)
        
            self.items_total.configure(text=self.item_total)
            self.services_total.configure(text= f"₱{format_price(float(self.service_total))}")
        
            self.new_total.configure(text=total)
            self.orig_total.configure(text=f"₱{format_price(self.original_total)}")
            self.payable_amount.configure(text=f"₱{format_price(price_format_to_float(total[1:]) - float(self.original_total))}")
            
            if price_format_to_float(total[1:]) - float(self.original_total) == 0:
                self.ammount_tendered.grid_forget()
                self.payment_entry.grid_forget()
                self.complete_button.configure(state= 'normal')
            else:
                self.complete_button.configure(state= 'disabled')
                self.ammount_tendered.grid(row=7, column=0, padx=(width*0.01), pady=(height*0.005,0), sticky="w")
                self.payment_entry.grid(row=7, column=2, padx=(width*0.01), pady=(height*0.025,height*0.01),)
                
        def place(self, info, items, info_lists, item_total, service_total, or_num, client, cashier, **kwargs):
            self.service_data = [(data[0], data[1], f"₱{format_price(data[3])}")for data in database.fetch_data(sql_commands.get_service_record, (info,))]
            self.original_total = database.fetch_data(sql_commands.get_transaction_total_by_id, (info,))[0][0]
            self.item_data = [(data[1], data[3], data[4]) for data in items]
            self.item_total = str(item_total)
            self.service_total = str(service_total)   
            self.or_number = or_num
            self.cashier_data = cashier
            self.client_data = client            
            self.info_list = info_lists
            self.set_values()
            
            return super().place(**kwargs)
    return instance(master, info)

def add_item(master, info:tuple, root_treeview: cctk.cctkTreeView, command_callback:callable = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, command_callback:callable):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            global IP_Address

            '''internal data'''
            self.total_transaction_count = 0
            self._command_callback = command_callback
            #self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

            def item_proceed(_: any = None):
                selected_item = self.item_treeview.get_selected_data()
                #print(selected_item)
                if selected_item:
                    items_in_billing = [s[0] for s in root_treeview._data]
                    if selected_item[1] in items_in_billing:
                        frame:cctk.ctkButtonFrame = root_treeview.data_frames[items_in_billing.index(selected_item[1])]
                        spinner: cctk.cctkSpinnerCombo = frame.winfo_children()[-2].winfo_children()[0]
                        spinner.change_value()
                    else:
                        root_treeview.add_data((selected_item[0], selected_item[1], selected_item[3], selected_item[3]))
                        children_frames = root_treeview.data_frames[-1].winfo_children()
                        children_frames[-2].winfo_children()[-1].configure(value = 1, val_range = (1, selected_item[2]))
                    
                    if command_callback: self._command_callback()
                    self.place_forget()
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.875, corner_radius=0,fg_color=Color.White_Color[3])
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='ADD ITEM', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0,columnspan=2, sticky="nsew", padx=width*0.005, pady=width*0.005)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)
                
            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color=Color.White_Platinum)
            self.item_frame.pack_propagate(0)
            self.item_frame.grid(row=0, column=0, sticky="nsew",padx=width*0.005, pady=width*0.005)
            
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.item_frame, data=self.data, height=height*0.8, width=width*0.795,double_click_command=item_proceed, 
                                                   column_format=f"/No:{int(width*.035)}-#r/ItemBrand:{int(width*.1)}-tl/ItemDescpription:x-tl/Stocks:{int(width*.075)}-tr/Price:{int(width*.115)}-tr!30!30",)
            self.item_treeview.pack()
            
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            count_temp = database.fetch_data("SELECT COUNT(*) FROM transaction_record")[0][0]
            if count_temp != self.total_transaction_count:
                self.update_items_stocks()
                self.total_transaction_count = count_temp

            return super().place(**kwargs)
        
        def update_items_stocks(self):
            data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.data = [(data[0], f"{data[1]} ({data[2]})") + data[3:] if data[2] else (data[0], data[1], ) + data[3:] for data in data]
            #print(self.data)
            self.item_treeview.update_table(self.data)
        
        def place_forget(self):
            if self.item_treeview.data_grid_btn_mng.active:
                self.item_treeview.data_frames[self.item_treeview._data.index(self.item_treeview.get_selected_data())].response()
            return super().place_forget()
            
    return instance(master, info, root_treeview,command_callback)

def view_removed_items(master, info:tuple, command_callback:callable = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback:callable):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            super().__init__(master, width*0.8, height=height*0.85, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            #self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            self.result = None
            self._command_callback = command_callback
            
            def reset():
                self.place_forget()
            
            self.reasons = ['Defective/Damaged', 'Expired']

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure((2), weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.get_image('view_receipt_icon', (28,28))).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="REPLACED ITEMS", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            '''Client Frame'''
            self.client_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.client_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=width*0.005, pady=(width*0.005,0))
            
            self.or_label = ctk.CTkLabel(self.client_frame, text='', font=('DM Sans Medium', 14), fg_color=Color.White_Lotion, width=width*0.125, height=height*0.055, corner_radius=5)
            self.or_label.pack(side='left',padx=(width*0.005,0), pady=(width*0.005))
            
            '''Client Name Frame'''
            self.client_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.215)
            self.client_name_frame.pack(side="right", padx=(width*0.005), pady=(width*0.005))
            self.client_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.client_name_frame, text="Client: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.client_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
           
           
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=2, column=0, sticky='nsew', padx=(width*0.005), pady=(width*0.005))
            self.content_frame.grid_columnconfigure(1, weight=1)
            
            '''Treeview'''
            self.client_treeview_frame = ctk.CTkFrame(self.content_frame, corner_radius=0,fg_color=Color.White_Platinum)
            self.client_treeview_frame.pack(fill='both', expand=1, padx=(width*0.005), pady=(width*0.005))
            
            self.item_treeview = cctk.cctkTreeView(self.client_treeview_frame, data=[], width= width*0.775, height= height*0.595, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*.08)}-tl/ItemDescription:x-tl/UnitPrice:{int(width*.085)}-tr/QuantityPcs:{int(width*.1)}-tr/TotalPrice:{int(width*.085)}-tr/Reason:{int(width*.125)}-tl!33!35',
                                           bd_message="Are you sure want to remove this item?")
            self.item_treeview.pack()
            
            self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, corner_radius=5, width=width*0.215, height=height*0.065)
            self.action_frame.grid(row=3, column=0, columnspan=1, sticky='nsew', padx=(width*0.005), pady=(0,width*0.005))
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.085, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 16), text='Close', command=reset)
            self.cancel_btn.pack(side="right", padx=(width*0.005), pady=(width*0.005)) 
            
          
        def set_table(self):
            print(self.data)
            self.or_label.configure(text=self.info[0])
            self.client_name_label.configure(text=self.info[1])
            self.item_treeview.update_table(self.data)
        
          
        def place(self, info, data, **kwargs):
            self.info = info
            self.data = data
            self.set_table()
            
            return super().place(**kwargs)

    return instance(master, info, command_callback)