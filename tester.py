import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups
from decimal import Decimal

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        customer_info(self, self.screen, (1, 'admin', '2012-01-01'), None).place(relx = .5 , rely = .5, anchor = 'c')
        self.mainloop()

def customer_info(master, info:tuple, sales_info: tuple, sales_content: list) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, sales_info: tuple, sales_content: list):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0)
            self.pack_propagate(0)
            #basic inforamtion needed; measurement

            lbltst = ctk.CTkLabel(self, text='OR#: %s\nCashier: %s\ndate of transaction: %s' % sales_info, text_color='white')
            lbltst._label.configure(justify=ctk.LEFT, )
            lbltst.pack(anchor = 'w')

            self.treeview = cctk.cctkTreeView(self, width= width * .7, height= height *.7, column_format='/No:45-#l/Name:x-tl/Price:150-tr!50!30')
            self.treeview.pack(pady =(12, 0))

            #the actual frame, modification on the frame itself goes here

    return instance(master, info, sales_info, sales_content)

body()