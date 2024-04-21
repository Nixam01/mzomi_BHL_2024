import customtkinter as ctk
from copy import copy
from PIL import Image, ImageTk
class Login(ctk.CTk):
    def __init__(self, rootDir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("260x180")
        self.title("Login")
        self.rootDir=rootDir
        self.grid_columnconfigure(0, weight=1)
        im = Image.open(f'{rootDir}/img/lock.png')
        photo = ImageTk.PhotoImage(im)
        self.wm_iconphoto(True, photo)

        self.mainFrame = ctk.CTkFrame(self, width=300, height=120)
        self.mainFrame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="new")
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)

        self.usernameLabel = ctk.CTkLabel(self.mainFrame, text="Username: ")
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")
        self.usernameEntry = ctk.CTkEntry(self.mainFrame)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="ew")
        self.passwordLabel = ctk.CTkLabel(self.mainFrame, text="Password: ")
        self.passwordLabel.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="w")
        self.passwordEntry = ctk.CTkEntry(self.mainFrame, show="•")
        self.passwordEntry.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="ew")
       # self.mainFrame.columnconfigure(0, weight=1)

        self.changesFrame = ctk.CTkFrame(self, height=50)
        self.changesFrame.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nwse")
        self.loginButton = ctk.CTkButton(self.changesFrame, text="Login", command=self.login_callback)
        self.loginButton.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nwse")
        self.changesFrame.columnconfigure(0, weight=1)
        self.mainloop()

    def login_callback(self):
        from UI.panel import Panel
        role = "user"
        self.destroy()
        #TODO: uwierzytelnienie
        if role == "user":
            panel = Panel(self.rootDir)
        else:
            Exception("No such role")
        
        
        