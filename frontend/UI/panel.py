from typing import Optional, Tuple, Union
import customtkinter as ctk
import tkinter as tk
import os
import json
from datetime import datetime

class Panel(ctk.CTk):
    
    def __init__(self, rootDir, *args, **kwargs):
        # print(core.loaded_profiles)
        super().__init__(*args, **kwargs)
        self.geometry(f"{800}x{450}")
        self.title(f"Panel: User")
        self.rootDir = rootDir
       # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebarFrame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, sticky="nsw")
        self.sidebarFrame.grid_columnconfigure(0, weight=1)
        self.sidebarFrame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebarFrame, text="Shamir", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.browseRequestsButton = ctk.CTkButton(self.sidebarFrame, text="Access browser", command=self.access_browser_callback)
        self.browseRequestsButton.grid(row=1, column=0, padx=20, pady=10)
        self.newRequestButton = ctk.CTkButton(self.sidebarFrame, text="Request Access", command=self.request_access_callback)
        self.newRequestButton.grid(row=2, column=0, padx=20, pady=10)
        self.manageRequests = ctk.CTkButton(self.sidebarFrame, text="Manage Requests", command=self.manage_requests_callback)
        self.manageRequests.grid(row=3, column=0, padx=20, pady=10)
        self.logoutButton = ctk.CTkButton(self.sidebarFrame, text="Logout", command=self.logout_callback)
        self.logoutButton.grid(row=5, column=0, padx=20, pady=10, sticky="s")
        
        accessBrowser = self.print_access_browser()
        accessBrowser.grid(row=0, column=1, sticky="nswe", padx=10)
        self.mainloop()
    
    def access_browser_callback(self):
        obj = self.print_access_browser()
        obj.grid(row=0, column=1, sticky="nwse", padx=10)

    def request_access_callback(self):
        obj = self.print_resources()
        obj.grid(row=0, column=1, sticky="nwse", padx=10)

    def manage_requests_callback(self):
        obj = self.print_manager()
        obj.grid(row=0, column=1, sticky="nwse", padx=10)

    def print_access_browser(self):
        result = ctk.CTkTabview(self)
        result.add("Active")
        result.add("Pending")
        result.add("Expired")
        result.add("Denied")
        activeScrollableFrame = ctk.CTkScrollableFrame(result.tab("Active"), bg_color="transparent", fg_color="transparent")
        pendingScrollableFrame = ctk.CTkScrollableFrame(result.tab("Pending"), bg_color="transparent", fg_color="transparent")
        expiredScrollableFrame = ctk.CTkScrollableFrame(result.tab("Expired"), bg_color="transparent", fg_color="transparent")
        deniedScrollableFrame = ctk.CTkScrollableFrame(result.tab("Denied"), bg_color="transparent", fg_color="transparent")
        activeScrollableFrame.grid(row=0, column=0, sticky="nwse")
        pendingScrollableFrame.grid(row=0, column=0, sticky="nwse")
        expiredScrollableFrame.grid(row=0, column=0, sticky="nwse")
        deniedScrollableFrame.grid(row=0, column=0, sticky="nwse")
        activeScrollableFrame.columnconfigure(0, weight=1)
        pendingScrollableFrame.columnconfigure(0, weight=1)
        expiredScrollableFrame.columnconfigure(0, weight=1)
        deniedScrollableFrame.columnconfigure(0, weight=1)
        result.tab("Active").grid_columnconfigure(0, weight=1)
        result.tab("Active").grid_rowconfigure(0, weight=1)
        result.tab("Pending").grid_columnconfigure(0, weight=1)
        result.tab("Pending").grid_rowconfigure(0, weight=1)
        result.tab("Expired").grid_columnconfigure(0, weight=1)
        result.tab("Expired").grid_rowconfigure(0, weight=1)
        result.tab("Denied").grid_columnconfigure(0, weight=1)
        result.tab("Denied").grid_rowconfigure(0, weight=1)
        data = self.mock_get_browser()
        iActive = 1
        iPending = 1
        iExpired = 1
        iDenied = 1
        for item in data:
            if item["Status"] == 'Approved' and not is_expired(item["ExpiryTimestamp"]):
                tempframe = ctk.CTkFrame(activeScrollableFrame, bg_color="transparent", fg_color="transparent")
                tempframe.grid(row=2*iActive, column=0, padx=10, pady=(10, 0), sticky="ew")
                no = ctk.CTkLabel(tempframe, text=iActive)
                no.grid(row=0, column=0, padx=10, pady=(10, 10))
                DN = ctk.CTkLabel(tempframe, text=item["resource"]["resourceDN"])
                DN.grid(row=0, column=1, padx=10, pady=(10, 10))
                timestamp = ctk.CTkLabel(tempframe, text=decode_timestamp(item["ExpiryTimestamp"]))
                timestamp.grid(row=0, column=2, padx=10, pady=(10, 10))
                tempframe.columnconfigure(3, weight=1)
                separator = tk.ttk.Separator(tempframe, orient="horizontal")
                separator.grid(row=(2*iActive)-1, column=0, columnspan=4, sticky="ew", padx=10 )
                tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
                tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
                tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight

                iActive = iActive + 1

            elif item["Status"] == 'Pending':
                tempframe = ctk.CTkFrame(pendingScrollableFrame, bg_color="transparent", fg_color="transparent")
                tempframe.grid(row=2*iPending, column=0, padx=10, pady=(10, 0), sticky="ew")
                no = ctk.CTkLabel(tempframe, text=iPending)
                no.grid(row=0, column=0, padx=10, pady=(10, 10))
                DN = ctk.CTkLabel(tempframe, text=item["resource"]["resourceDN"])
                DN.grid(row=0, column=1, padx=10, pady=(10, 10))
                VIH = ctk.CTkLabel(tempframe, text=format_hours(item["ValidityInHours"]))
                VIH.grid(row=0, column=2, padx=10, pady=(10, 10))
                ratio = ctk.CTkLabel(tempframe, text=f"{item['sharesAmount']}/{item['resource']['MinSharesRequired']}")
                ratio.grid(row=0, column=3, padx=10, pady=(10, 10))
                tempframe.columnconfigure(4, weight=1)
                separator = tk.ttk.Separator(tempframe, orient="horizontal")
                separator.grid(row=(2*iPending)-1, column=0, columnspan=5, sticky="ew", padx=10 )
                tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
                tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
                tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight
                tempframe.grid_columnconfigure(3, weight=0)                


                iPending = iPending + 1

            elif item["Status"] == 'Approved' and is_expired(item["ExpiryTimestamp"]):
                tempframe = ctk.CTkFrame(expiredScrollableFrame, bg_color="transparent", fg_color="transparent")
                tempframe.grid(row=2*iExpired, column=0, padx=10, pady=(10, 0), sticky="ew")
                no = ctk.CTkLabel(tempframe, text=iExpired)
                no.grid(row=0, column=0, padx=10, pady=(10, 10))
                DN = ctk.CTkLabel(tempframe, text=item["resource"]["resourceDN"])
                DN.grid(row=0, column=1, padx=10, pady=(10, 10))
                timestamp = ctk.CTkLabel(tempframe, text=decode_timestamp(item["ExpiryTimestamp"]))
                timestamp.grid(row=0, column=2, padx=10, pady=(10, 10))
                tempframe.columnconfigure(3, weight=1)
                separator = tk.ttk.Separator(tempframe, orient="horizontal")
                separator.grid(row=(2*iExpired)-1, column=0, columnspan=4, sticky="ew", padx=10 )
                tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
                tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
                tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight

                iExpired = iExpired + 1
            elif item["Status"] == 'Denied':
                tempframe = ctk.CTkFrame(deniedScrollableFrame, bg_color="transparent", fg_color="transparent")
                tempframe.grid(row=2*iDenied, column=0, padx=10, pady=(10, 0), sticky="ew")
                no = ctk.CTkLabel(tempframe, text=iDenied)
                no.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="wns")
                DN = ctk.CTkLabel(tempframe, text=item["resource"]["resourceDN"])
                DN.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="wns")
                VIH = ctk.CTkLabel(tempframe, text=format_hours(item["ValidityInHours"]))
                VIH.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="wns")
                reasoningButton = ctk.CTkButton(tempframe, width=50, height=20, text='read', command=lambda arg=item['reasoning']: show_text_in_new_window(arg))
                reasoningButton.grid(row=0, column=3, padx=10, sticky="ens")
                separator = tk.ttk.Separator(tempframe, orient="horizontal")
                separator.grid(row=(2*iDenied)-1, column=0, columnspan=4, sticky="ew", padx=10 )
                tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
                tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
                tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight
                tempframe.grid_columnconfigure(3, weight=1)  

                iDenied = iDenied + 1
        if activeScrollableFrame.winfo_children():
            tempframe = ctk.CTkFrame(activeScrollableFrame, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            no = ctk.CTkLabel(tempframe, text="No.")
            no.grid(row=0, column=0, padx=10, pady=(10, 10))
            DN = ctk.CTkLabel(tempframe, text="Resource name")
            DN.grid(row=0, column=1, padx=10, pady=(10, 10))
            timestamp = ctk.CTkLabel(tempframe, text="Expiration date")
            timestamp.grid(row=0, column=2, padx=10, pady=(10, 10))
            tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=1)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1)   # Columns for buttons and last label with no weight
            tempframe.grid_columnconfigure(3, weight=0)

            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)

        if pendingScrollableFrame.winfo_children():
            tempframe = ctk.CTkFrame(pendingScrollableFrame, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            no = ctk.CTkLabel(tempframe, text="No.")
            no.grid(row=0, column=0, padx=10, pady=(10, 10))
            DN = ctk.CTkLabel(tempframe, text="Resource name")
            DN.grid(row=0, column=1, padx=10, pady=(10, 10))
            VIH = ctk.CTkLabel(tempframe, text="Validity")
            VIH.grid(row=0, column=2, padx=10, pady=(10, 10))
            ratio = ctk.CTkLabel(tempframe, text="Shares")
            ratio.grid(row=0, column=3, padx=10, pady=(10, 10))
            tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight
            tempframe.grid_columnconfigure(3, weight=1)
            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)
        if expiredScrollableFrame.winfo_children():
            tempframe = ctk.CTkFrame(expiredScrollableFrame, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            no = ctk.CTkLabel(tempframe, text="No.")
            no.grid(row=0, column=0, padx=10, pady=(10, 10))
            DN = ctk.CTkLabel(tempframe, text="Resource name")
            DN.grid(row=0, column=1, padx=10, pady=(10, 10))
            timestamp = ctk.CTkLabel(tempframe, text="Expiration date")
            timestamp.grid(row=0, column=2, padx=10, pady=(10, 10))
            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)
            tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight
            tempframe.grid_columnconfigure(3, weight=1)  
        if deniedScrollableFrame.winfo_children():
            tempframe = ctk.CTkFrame(deniedScrollableFrame, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            no = ctk.CTkLabel(tempframe, text="No.")
            no.grid(row=0, column=0, padx=10, pady=(10, 10))
            DN = ctk.CTkLabel(tempframe, text="Resource name")
            DN.grid(row=0, column=1, padx=10, pady=(10, 10))
            VIH = ctk.CTkLabel(tempframe, text="Validity")
            VIH.grid(row=0, column=2, padx=10, pady=(10, 10))
            reasoning = ctk.CTkLabel(tempframe, text="Reasoning")
            reasoning.grid(row=0, column=3, padx=10, pady=(10, 10))
            

            tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight
            tempframe.grid_columnconfigure(3, weight=1)  
            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)
        return result
    


    def print_resources(self):
        result = ctk.CTkScrollableFrame(self)
        result.columnconfigure(0, weight=1)
        data = self.mock_get_resources()
        if len(data) > 0:
            tempframe = ctk.CTkFrame(result, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            no = ctk.CTkLabel(tempframe, text="Resource name")
            no.grid(row=0, column=0, padx=10, pady=(10, 10))
            DN = ctk.CTkLabel(tempframe, text="Min. secrets")
            DN.grid(row=0, column=1, padx=10, pady=(10, 10))
            timestamp = ctk.CTkLabel(tempframe, text="Validity time")
            timestamp.grid(row=0, column=2, padx=10, pady=(10, 10))
            tempframe.grid_columnconfigure(0, weight=1)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=0)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1)   # Columns for buttons and last label with no weight
            tempframe.grid_columnconfigure(3, weight=0)

            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10)
        else: return
        i = 1
        for item in data:
            tempframe = ctk.CTkFrame(result, bg_color="transparent", fg_color="transparent")
            tempframe.grid(row=2*i, column=0, padx=10, pady=(10, 0), sticky="ew")
            DN = ctk.CTkLabel(tempframe, text=item["resourceDN"])
            DN.grid(row=0, column=0, padx=10, pady=(10, 10))
            msn = ctk.CTkLabel(tempframe, text=item["MinSharesRequired"])
            msn.grid(row=0, column=1, padx=10, pady=(10, 10))
            validityOptionMenu = ctk.CTkOptionMenu(tempframe, values=["2h", "24h", "7d", "30d", "permanent"])
            validityOptionMenu.grid(row=0, column=2, padx=10)
            requestButton = ctk.CTkButton(tempframe, width=50, height=20, text='request', command=lambda arg=[to_hours(validityOptionMenu.get()), item["id"]]: request_access(arg))
            requestButton.grid(row=0, column=3, padx=10, sticky="ens")
            tempframe.columnconfigure(3, weight=1)
            separator = tk.ttk.Separator(tempframe, orient="horizontal")
            separator.grid(row=(2*i)-1, column=0, columnspan=4, sticky="ew", padx=10)
            tempframe.grid_columnconfigure(0, weight=0)   # Make the column with the first label expand
            tempframe.grid_columnconfigure(1, weight=1, minsize=50)   # Empty space column, no weight to keep it minimal
            tempframe.grid_columnconfigure(2, weight=1, minsize=50)   # Columns for buttons and last label with no weight

            i = i + 1

        return result 

    def print_manager(self):
        result = ctk.CTkScrollableFrame(self)

        return result

    def hello_world(self):
        print("hello world!")
    
    def request_access(self, args):
        VIH = args[0]
        resourceID = args[1]
        #TODO

    def mock_get_browser(self):
        file_path = f"{self.rootDir}/Data/requests_browser.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    def mock_get_resources(self):
        file_path = f"{self.rootDir}/Data/resources.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    def logout_callback(self):
        from UI.login import Login
        self.destroy()
        login = Login(self.rootDir)

    # def print_list(self):
    #     for widget in self.grid_slaves():
    #             if widget.grid_info()['row'] > 0:
    #                 widget.destroy()
    #     self.core.load_profiles()
    #     if self.core.loaded_profiles == []:
    #         label = ctk.CTkLabel(self, text="No profiles! Add a profile to start...")
    #         label.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nswe")
    #         return
    #     self.core.check_running_processes()

    #     if self.searchText == "":
    #         searchRes = self.core.loaded_profiles
    #     else:
    #         searchRes = self.get_search_results()
    #         if searchRes == []:
    #             label = ctk.CTkLabel(self, text="Invalid search query!")
    #             label.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nswe")
    #             return

    #     self.mainFrame = ctk.CTkScrollableFrame(self, bg_color="transparent", fg_color="transparent")
    #     self.mainFrame.grid(row=1, column=0, sticky="news")
    #     self.mainFrame.columnconfigure(0, weight=1)
    #     self.mainFrame.columnconfigure(0, weight=1)
    #     for i, profile, in enumerate(searchRes):
    #         # self.profile_frames.update({profile.name: ctk.CTkFrame(self, height=50)})
    #         # profile_frame.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="new")
            
    #         profile_frame = ctk.CTkFrame(self.mainFrame, height=50)
    #         profile_frame.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="new")
            
    #         label = ctk.CTkLabel(profile_frame, text=profile.name)
    #         label.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")
    #         # TODO: fix button reference
    #         # if profile.name not in self.core.active_processes:
    #         #     startButton = ctk.CTkButton(profile_frame,
    #         #                                   fg_color='green', width=30, height=30, text="▶️",
    #         #                                     command=lambda arg=profile: self.run_profile_callback(arg))
    #         # else:
    #         #     startButton = ctk.CTkButton(profile_frame,
    #         #                                 fg_color='red', width=30, height=30, text="⏹️",
    #         #                                         command=lambda arg=profile: self.stop_profile_callback(arg))
    #         startButton = ctk.CTkButton(profile_frame,
    #                                           fg_color='green', width=30, height=30, text="▶️",
    #                                             command=lambda arg=profile: self.run_profile_callback(arg))
    #         editButton = ctk.CTkButton(profile_frame,
    #                                           fg_color='blue', width=30, height=30, text="✏️",
    #                                             command=lambda arg=profile: self.edit_profile_callback(arg))
    #         # editButton = ctk.CTkButton(profile_frame,
    #         #                                   fg_color='blue', width=30, height=30, text="✏️",
    #         #                                     command=print(f"EDIT: {profile.name}"))
    #         deleteButton = ctk.CTkButton(profile_frame,
    #                                           fg_color='red', width=30, height=30, text="🗑️",
    #                                             command=lambda arg=profile: self.delete_profile_callback(arg))
    #         sizeLabel = ctk.CTkLabel(profile_frame,
    #                                  text = utils.get_folder_size(self.core.get_profile_path(profile)))
        
    #         startButton.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="wse")
    #         editButton.grid(row=0, column=3, padx=10, pady=(10, 10), sticky="wse")
    #         deleteButton.grid(row=0, column=4, padx=10, pady=(10, 10), sticky="wse")
    #         sizeLabel.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="wse")
    #         profile_frame.grid_columnconfigure(0, weight=1)   # Make the column with the first label expand
    #         profile_frame.grid_columnconfigure(1, weight=0, minsize=50)   # Empty space column, no weight to keep it minimal
    #         profile_frame.grid_columnconfigure(2, weight=0)   # Columns for buttons and last label with no weight
    #         profile_frame.grid_columnconfigure(3, weight=0)
    #         profile_frame.grid_columnconfigure(4, weight=0)
    #         profile_frame.grid_columnconfigure(5, weight=0)
    #         # self.start_buttons.update({profile.name: startButton})
    #         # self.edit_buttons.update({profile.name: editButton})
    #         # self.delete_buttons.update({profile.name: deleteButton})
    #     #print(self.core.active_processes)



def decode_timestamp(timestamp):
    # Format wejściowego timestampu
    input_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    # Format wyjściowy
    output_format = "%d.%m.%Y %H:%M"

    # Parsowanie wejściowego timestampu
    dt = datetime.strptime(timestamp, input_format)
    # Formatowanie do formatu wyjściowego
    formatted_timestamp = dt.strftime(output_format)

    return formatted_timestamp

def is_expired(timestamp):
    # Parsowanie timestampu
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    # Pobranie aktualnego czasu systemowego
    current_time = datetime.now()
    
    # Sprawdzenie, czy timestamp jest przed aktualnym czasem
    return dt < current_time

def format_hours(hours):
    if hours == 9999999:
        return "permanent"
    elif hours < 24:
        return f"{hours} h"
    else:
        days = hours // 24
        return f"{days} d"

def show_text_in_new_window(text):
    # Tworzenie nowego okna typu Toplevel
    new_window = tk.Toplevel()

    # Tworzenie etykiety z podanym tekstem
    label = tk.Label(new_window, text=text)
    label.pack(padx=20, pady=20)

    # Uruchomienie pętli głównej dla okna
    new_window.mainloop()

def to_hours(text):
    if text == "2h":
        return 2
    if text == "24h":
        return 24
    if text == "7d":
        return 168
    if text == "30d":
        return 720
    if text == "permanent":
        return 9999999