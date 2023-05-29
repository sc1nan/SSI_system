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

        self.val = 0
        btn = ctk.CTkButton(self, text='click', command = lambda:print(self.val))
        btn.pack()

        self.bind('<Return>', lambda _: customer_info(self, self.screen, self.val).place(relx = .5, rely = .5, anchor = 'c'))

        self.mainloop()

def customer_info(master, info:tuple, val) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, _val):
            width = info[0]
            height = info[1]
            self._val = _val
            #basic inforamtion needed; measurement

            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0)
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def change_val():
                self._val = 10
                self.destroy()

            #From here
            self.left_frame = ctk.CTkFrame(self, bg_color='#c3c3c3')
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.pet_info_lbl = ctk.CTkLabel(self.left_frame, text='Pet Info',font=("Poppins", 45))
            self.pet_info_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            #Name label
            self.Name_lbl = ctk.CTkLabel(self.left_frame, text='Name:',font=("Poppins", 25))
            self.Name_lbl.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name entry
            self.services_entry = ctk.CTkEntry(self.left_frame, placeholder_text='Required', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.services_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            #Breed and Animal Type label
            self.animal_breed_lbl = ctk.CTkLabel(self.left_frame, text='Breed and Animal Type:',font=("Poppins", 25))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.left_frame, placeholder_text='Required', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            #calendar and note frame
            self.middle_frame = ctk.CTkFrame(self.left_frame, bg_color='#D9D9D9', fg_color='#D9D9D9')
            self.middle_frame.grid(row=5, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #sched service frame
            self.schedule_service_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.schedule_service_frame.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #Scheduled service label
            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text='Scheduled Service:',font=("Poppins", 25))
            self.scheduled_service_lbl.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="nw")
            #Scheduled service entry
            self.scheduled_service_entry = ctk.CTkEntry(self.schedule_service_frame, placeholder_text='Required', height=height*0.09, width=width*0.285, font=("Poppins", 25))
            self.scheduled_service_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="ns")
            #note frame
            self.note_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.note_frame.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nsw")
            #note label
            self.note_lbl = ctk.CTkLabel(self.note_frame, text='Note:',font=("Poppins", 25))
            self.note_lbl.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nw")
            #note entry
            self.note_entry = ctk.CTkEntry(self.note_frame, placeholder_text='Optional', height=height*0.25, width=width*0.445, font=("Poppins", 25))
            self.note_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ns")




            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=height*0.78, width=width*0.312, fg_color='white')

            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=change_val, width=270, font=("Poppins-Bold", 45))

            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')


            self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=change_val, width=270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")


            #on out

    return instance(master, info, val)

body()