from customtkinter import *
import tkinter as tk
import login_module 
import encryption_module
import os
import csv
import pyperclip
import configparser
        

#root class for the main application
class PasswordManager(tk.Tk):
    def __init__(self):
        super().__init__() 

        # Create the main frame
        self.container = CTkFrame(self)
        self.container.pack(fill='both', expand=True)
        self.geometry('424x500')
        self.title("🔐 Password Manager")
        
        # Getting UI config of user
        self.config_UI = configparser.ConfigParser()
        self.load_config()
        
        # Creating session object
        self.session = {}
        
        #Creating Menu bar
        self.configure_menu()

        # Create the login frame
        self.login_frame = LoginFrame(self.container, session=self.session)
        self.login_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Create the add user frame
        self.add_user_frame = AddUserFrame(self.container, session = self.session)
        self.add_user_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Show the login frame
        self.show_frame('add_user','login') 
    
    def configure_menu(self):
        
        # Creating a Menu Bar
        menu_bar = tk.Menu(self)
        
        # Create a Scale menu
        scale_menu = tk.Menu(menu_bar,tearoff=0)
        scale_menu.add_command(label="80%", command=lambda: self.set_scaling(0.8))
        scale_menu.add_command(label="90%", command=lambda: self.set_scaling(0.9))
        scale_menu.add_command(label="100%", command=lambda: self.set_scaling(1.0))
        scale_menu.add_command(label="120%", command=lambda: self.set_scaling(1.2))
        
        # change the apperance mode
        mode_menu = tk.Menu(menu_bar,tearoff = 0)
        mode_menu.add_command(label="Light", command=lambda: self.set_appearance("light"))
        mode_menu.add_command(label="Dark", command=lambda: self.set_appearance("dark"))
        mode_menu.add_command(label="System", command=lambda: self.set_appearance("system"))
        
        # Add the theme menu to the Menu Bar
        menu_bar.add_cascade(label="Scaling",menu=scale_menu)
        
        # Add the mode change to menu bar
        menu_bar.add_cascade(label="mode",menu=mode_menu)
        
        # Config the menu bar
        self.config(menu=menu_bar)
        
    def set_appearance(self,theme):
        self.mode = theme
        set_appearance_mode(theme)
        self.save_config() 
        
    # Function to resize window according to scaling    
    def set_scaling(self,scal):
        geo = ''
        match scal:
            case 0.8:
                self.geometry('340x500')
                geo = '340x500'
            case 0.9:
                self.geometry('386x500')
                geo = '386x500'
            case 1.0:
                self.geometry('424x500')
                geo='424x500'
            case 1.2:
                self.geometry('510x500')
                geo='510x500'  
        set_widget_scaling(scal)
        self.scale = scal
        self.geomet = geo
        
        self.save_config()

    # Loading the UI config file
    def load_config(self):
        try:
            self.config_UI.read('UI.ini')
            self.mode = self.config_UI.get("UI_configure", "mode")
            self.scale = float(self.config_UI.get("UI_configure", "scale"))
            self.geomet = self.config_UI.get("UI_configure", "geometry")
        except(configparser.Error, FileNotFoundError):
            self.scale = 1.0
            self.mode = 'dark'
            self.geomet = '424x500'
        set_appearance_mode(self.mode)
        self.geometry(self.geomet)
        set_widget_scaling(self.scale)
    
    def save_config(self):
        
        self.config_UI["UI_configure"] = {
            "mode": self.mode,
            "scale": self.scale,
            "geometry": self.geomet
        }
        
        # Saving the config 
        with open("UI.ini","w") as configfile:
            self.config_UI.write(configfile)

    
    def show_frame(self,hidd_frame, frame_name):
        #hidding the current frame
        h_frame = getattr(self, f'{hidd_frame}_frame')
        h_frame.pack_forget()
        # Raise the specified frame to the top
        frame = getattr(self, f'{frame_name}_frame')
        frame.tkraise()
    
    def show_table(self, frame_name):
        frame = getattr(self, f'{frame_name}_frame')
        
        # Creating password table frame
        self.password_table_frame = PasswordFrame(self.container, self.session['username'],self.session['passkey'])
        self.password_table_frame.pack(fill='both',padx=2, pady=2, expand = True)
        self.password_table_frame.place(relx = 0.0, rely = 0.0, relwidth=1.0, relheight=1.0, anchor = "nw")
        frame.destroy()
        self.password_table_frame.tkraise()
        

#login frame configration
class LoginFrame(CTkFrame):
    def __init__(self, parent, session):
        super().__init__(parent)
        
        # 
        self.session = session

        # Create the username entry
        self.username_label = CTkLabel(self, text='Username:')
        self.username_label.pack(side='top', pady=5)
        self.username_entry = CTkEntry(self)
        self.username_entry.pack(side='top', pady=5)

        # Create the password entry
        self.password_label = CTkLabel(self, text='Password:')
        self.password_label.pack(side='top', pady=5)
        self.password_entry = CTkEntry(self, show='*')
        self.password_entry.pack(side='top', pady=5)

        # Create the login button
        self.login_button = CTkButton(self, text='Login', command=self.login)
        self.login_button.pack(side='top', pady=5)

        # Create the add user button
        self.add_user_button = CTkButton(self, text='Add User', command=lambda: parent.master.show_frame('login','add_user'))
        self.add_user_button.pack(side='top', pady=5)
        
        #Create a login status label
        self.login_status_label = CTkLabel(self, text="")
        self.login_status_label.pack(side='top',pady=5)
        
        self.table_screen = parent.master
        
    def login(self):
        # Check the username and password
        user = self.username_entry.get()
        password = self.password_entry.get()
        if login_module.user_login(user, password) == True:
            self.login_status_label.configure(text="login in successfully", text_color="green") 
            self.session['username'] = user
            self.session['passkey'] = password
            self.table_screen.show_table('login')
        else:
            self.login_status_label.configure(text="login in unsuccessfully", text_color="red")

class AddUserFrame(CTkFrame):
    def __init__(self, parent, session):
        super().__init__(parent)
        
        self.session = session

        # Create the username entry
        self.username_label = CTkLabel(self, text='New Username:')
        self.username_label.pack(side='top', pady=5)
        self.username_entry = CTkEntry(self)
        self.username_entry.pack(side='top', pady=5)

        # Create the password entry
        self.password_label = CTkLabel(self, text='New Password:')
        self.password_label.pack(side='top', pady=5)
        self.password_entry = CTkEntry(self, show='*')
        self.password_entry.pack(side='top', pady=5)

        # Create the add user button
        self.add_user_button = CTkButton(self, text='Add User', command=self.adding_user)
        self.add_user_button.pack(side='top', pady=5)
        
        #Create a add user label
        self.add_user_status_label = CTkLabel(self, text="")
        self.add_user_status_label.pack(side='top',pady=5)

        # Create the back button
        self.back_button = CTkButton(self, text='Back', command=lambda: parent.master.show_frame('add_user','login'))
        self.back_button.pack(side='top', pady=5)
        
        self.table = parent.master

    def adding_user(self):
        # Add the user
        username = self.username_entry.get()
        password = self.password_entry.get()
        if len(password) > 16:
            self.add_user_status_label.configure(text='password exceeded 16 chr length',text_color='red')
            return None
        else:
            if len(password) < 16:
                password = password.ljust(16, '\x00')
            login_module.add_user(username,password)
            self.session['username'] = username
            self.session['passkey'] = password
            self.add_user_status_label.configure(text='User Created',text_color='green')
            self.table.show_table('add_user')
            
class PasswordFrame(CTkFrame):
    def __init__(self, parent, usern, passk):
        super().__init__(parent)
        
        # Making users, passkey useable across classes
        self.user =usern
        self.passkey = passk
        
        # Configuring the Grid
        self.grid_columnconfigure((0,1),weight=0)
        self.grid_rowconfigure((0,1,2),weight = 0)
        self.grid_rowconfigure(3, weight=1)
        
        #creating add password frame
        self.add_password_frame = CTkFrame(self)
        self.add_password_frame.grid(row=0,column=0,columnspan=3,rowspan=3,padx=5,pady=5,sticky='nsew')
        
        # Creating add password service entry filed
        self.password_service_entry = CTkEntry(self.add_password_frame, placeholder_text="Service Name")
        self.password_service_entry.grid(row = 0, column= 0,columnspan=3, padx=5, pady=5, sticky='nsew')
        
        #Creating add password entry field
        self.add_password_entry = CTkEntry(self.add_password_frame,placeholder_text="Set Password",show='*')
        self.add_password_entry.grid(row=1,column=0,columnspan=2,padx=5,pady=5, sticky='nsew')
        
        # Creating Add new password button
        self.add_password_button = CTkButton(self.add_password_frame,text='Add\n Password',width=140, command=self.addpassword_fun)
        self.add_password_button.grid(row=2, column=0,columnspan=1, padx=5, pady=5, sticky = 'nsew')
        
        # Creating a see password button
        self.see_password_button = CTkCheckBox(self.add_password_frame,text='👁',command=self.password_visib)
        self.see_password_button.grid(row=1,column=2,padx=5,pady=5,sticky='nsew')
        
        # Creating a add password label
        self.add_password_label = CTkLabel(self.add_password_frame, text='||             ||',height=40,width=105)
        self.add_password_label.grid(row=2, column=1,columnspan=1, padx=5, pady=5, sticky = 'nsew')
        
        # Creating Generate password button
        self.generate_password_button = CTkButton(self.add_password_frame, text='Create\n Password', command=lambda : self.add_password_entry.insert(0, encryption_module.generate_password()))
        self.generate_password_button.grid(row=2, column=2, padx=5, pady=5, sticky = 'nsew')
        
        # Creation of scrollable frame 
        self.scrollable_frame  = CTkScrollableFrame(self,label_text='Saved Passwords')
        self.scrollable_frame.grid(row=3,column=0,columnspan=3,rowspan=3,padx=5,pady=5,sticky='nsew')
        self.scrollable_frame.grid_columnconfigure((0,1,2),weight=0)
        
        self.password_filepath = f'password_manager-collage_proj--main\\password_manager-collage_proj--main\\data\\user_data\\{self.user}.csv'
        self.table_content(path=self.password_filepath)
        
    def table_content(self,path):
        
        self.scrollable_frame_button = []
        self.scrollable_frame_label = []
        self.scrollable_frame_status = []
        self.update_password = []
        try:
            with open(self.password_filepath,mode='r',newline='') as csvfile: #getting a reader for the file
                read = csv.reader(csvfile)
                next(read)
                reader = list(read)
            # Showing the password list in the table
            for index, entry in enumerate(reader):
                # Showing Services in the list
                password_service_label = CTkLabel(self.scrollable_frame, text=entry[0])
                password_service_label.grid(row=index,column=0, padx=5, pady=5)
                self.scrollable_frame_label.append(password_service_label)
                
                # Password status label
                status_label = CTkLabel(self.scrollable_frame, text='_ _ _ _ _ _ _ _ _',width=115)
                status_label.grid(row=index,column=1,padx=5,pady=5)
                self.scrollable_frame_status.append(status_label)
                
                # Showing the button
                password_copy_button = CTkButton(self.scrollable_frame,text='Copy',command=lambda iv=entry[1], password=entry[2], ind=index:self.decrypt_copy(initializer_vector=iv, encrypt_pass=password, row=ind))
                password_copy_button.grid(row=index,column=2,padx=5,pady=5)
                self.scrollable_frame_button.append(password_copy_button)
                
                # Show Update Button
                update_button = CTkButton(self.scrollable_frame, text='🔃',width=35, command=lambda ind=index:self.password_updating(index=ind))
                update_button.grid(row=index, column=3, padx=5, pady=5)
                self.update_password.append(update_button)
                
        except FileNotFoundError:
            # Will show No password banner when there are no password
            self.table_empty_window = CTkLabel(self.scrollable_frame, text="No Saved Passwords", font=CTkFont(size=15, weight="bold"))
            self.table_empty_window.grid(row=1,column=1)        
        
    # Creating entries inside the table    
    def addpassword_fun(self):
        service = self.password_service_entry.get()
        password = self.add_password_entry.get()
        if len(password) > 32:
            self.add_password_label.configure(text="Password excced\n 32 caracters", text_color='red')
            return None
        else:
            encryption_module.encrypt_password(user=self.user,service=service,key=self.passkey,password=password)
            self.add_password_label.configure(text="Password added\n successfully", text_color='green')
            
            # Removing the table content and rereading them
            self.table_content(path=self.password_filepath)
        
    
    # Logic for visibility option of the entered code        
    def password_visib(self):
        status=self.see_password_button.get()
        if status:
            self.add_password_entry.configure(show='')
        else:
            self.add_password_entry.configure(show='*')
    
    
    # Logic to decrypt and copy to clipboard
    def decrypt_copy(self,initializer_vector,encrypt_pass,row):
        
        decrypted_password = encryption_module.decrypt(self.passkey, initializer_vector, encrypt_pass)
        pyperclip.copy(decrypted_password)
        self.scrollable_frame_status[row].configure(text='copy successfully!', text_color='green')
    
    # Module which take new password and update entry
    def password_updating(self, index):
        
        # Creating input frame
        password = CTkInputDialog(text="Enter new Password: ",title='update password')
        encryption_module.update_password(file_path=self.password_filepath, index=index, passkey=self.passkey, new_password=password.get_input())
        self.table_content(path=self.password_filepath)


# Create the PasswordManager instance
app = PasswordManager()
# Start the event loop
app.mainloop()
