import re     # module for regular expression
import os
import time
import pytube
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, StringVar, IntVar, Entry



# Graphical User Input(GUI)*********************************************************************************************

class GUI:
    def __init__(self, window, canvas) -> None:
        self.window = window
        self.canvas = canvas
    

    def create_GUI_layout(self):

        def modify_folder():
            down_dir = filedialog.askdirectory(initialdir="/", parent=self.window)
            folder_text.set(down_dir)

        def initiate_downloads():
            # extract the inputs from the dialogs and checkboxes
            down_link = entry_link.get()
            down_dir = download_entry.get()
            audio = audio_var.get()
            video = video_var.get()
            video_only = video_only_var.get()
            #do the download
            initiate_download(down_link, down_dir, audio, video, video_only)

        def display_about():
            messagebox.showinfo("ABOUT",
                                'Youtube Downloader built with Python!')

        def display_help():
            messagebox.showinfo("HELP",
                                'Hi! Welcome to Youtube Downloader v1.0.\n\n'
                                '1. Add the video URL \n'
                                '2. Select the download format. \n'
                                '3. Select the destination. \n'
                                '4. Sit back and relax. \n'
                                )

        # Main title label
        title = tk.Label(self.window, text="YouTube Downloader", font=('Arial Bold', 20), fg='black')
        title.place(x=385, y=20, anchor="center")

        # Display about button
        display_help_button = tk.Button(self.window, text='About ?', font=("Arial Bold", 10),command=display_about)
        display_help_button.place(x=15, y=455)

        # Shop help button
        display_help_file_button = tk.Button(self.window, text="Show help", font=("Arial Bold", 10),command=display_help)
        display_help_file_button.place(x=650, y=455)

        # Label for Youtube link
        link_label = tk.Label(self.window, text=" Enter video URL here: ", font=("Arial Bold", 10))
        link_label.place(x=300, y=75)

        down_link_text = StringVar()
        entry_link = Entry(self.window, width=55, textvariable=down_link_text) #textbox for user entry
        entry_link.pack()
        entry_link.focus_set()  # moves the keyboard input to the textbox
        entry_link.place(x=150, y=100)

        # audio and video checkboxes
        option_label = tk.Label(self.window, text="Download options available:", font=("Arial Bold", 10))
        option_label.place(x=285, y=175)

        audio_var = IntVar()
        option_button_audio = tk.Checkbutton(self.window, text="MP3 Audio Track", font=("Arial Bold", 10), variable=audio_var)
        option_button_audio.place(x=190, y=200)

        video_var = IntVar()
        option_button_video = tk.Checkbutton(self.window, text="720p Video", font=("Arial Bold", 10), variable=video_var)
        option_button_video.place(x=331, y=200)

        video_only_var = IntVar()
        option_button_video_only = tk.Checkbutton(self.window, text="720p Video(no audio)", font=("Arial Bold", 10), variable=video_only_var)
        option_button_video_only.place(x=435, y=200)

        # output folder selection
        download_folder_label = tk.Label(self.window, text="Select your download folder:", font=("Arial Bold", 10))
        download_folder_label.place(x=285, y=255)

        folder_text = StringVar()
        download_entry = Entry(self.window, width=55, textvariable=folder_text)
        desktop_address = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')  #gets the address of the user's desktop
        folder_text.set(desktop_address)
        download_entry.pack()
        download_entry.place(x=150, y=280)

        modify_folder_button = tk.Button(self.window,text="Select Folder",font=("Arial Bold", 10),command=modify_folder)
        modify_folder_button.place(x=330, y=305)

        # download button - triggers data extraction and download actions
        download_button = tk.Button(self.window, text="Start Download", font=("Arial Bold", 20), command=initiate_downloads)
        download_button.place(x=265, y=350)


        # DOWNLOAD *******************************************************************************************************
        def initiate_download(down_link, down_dir, audio, video, video_only):
            start = time.time()

            # create input warnings
            if len(down_link) == 0:
                messagebox.showinfo("Warning !", 'You have not provided a link for download.\nPlease paste or enter a YouTube link')
            elif audio + video + video_only == 0:
                messagebox.showinfo("Warning !", 'You have not selected a file type to download.\nPlease select atleast one of the options to download')

            # proceed if no input warnings are required
            else:
                print("Link being operated: ", down_link)
                print("Download directory: ", down_dir)

                
                # processing the link given
                print("Attempting to download:", down_link)
                individual_link_count = 0
                total_files_to_download = (audio + video + video_only)

                get_label = tk.Label(self.window, text="Getting stream info (takes 10 sec)", font=("Arial Bold", 20))
                get_label.place(x=260, y=250)
                self.canvas.update_idletasks()

                yt = pytube.YouTube(down_link) # time: 10 secs for connecting to Youtube
                # yt.register_on_progress_callback(display_progress)  #_progress_callback to run the display_progress function at each trifle

                stream = []
                if audio == 1:
                    all_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').all()
                    stream.append(all_audio_streams[0])
                if video == 1:
                    all_video_streams = yt.streams.filter(subtype='mp4', progressive=True).all()
                    stream.append(all_video_streams[0])
                if video_only == 1:
                    all_video_only_streams = yt.streams.filter(subtype='mp4', only_video=True).order_by('resolution').all()
                    stream.append(all_video_only_streams[0])

                end = time.time()
                print("Current Runtime:", end - start, "seconds")
                get_label.destroy()
                self.canvas.update()  # destroy canvas object using .update()

                for item in stream:
                    individual_link_count += 1
                    print("Downloading:", item)
                    items_label = tk.Label(self.window, text="Downloading file " + str(individual_link_count) + " of " + str(total_files_to_download), font=("Arial Bold", 20))
                    items_label.place(x=260, y=290)
                    self.canvas.update_idletasks()

                    # naming files differently to avoid overwrite
                    filename = str(item.default_filename) + " - YTD-Download"

                    item.download(down_dir, filename)
                    print("\nDownload complete")
                    end = time.time()
                    elapsed = float(round((end - start), 2))
                    items_label.destroy()
                    download_complete_label = tk.Label(self.window, text=f"Downloaded in {elapsed} secs", font=("Arial Bold", 20))
                    download_complete_label.place(x=260, y=290)
                    self.canvas.update_idletasks()
                    print("Time Elapsed:", end - start, "seconds")
    
        self.window.mainloop()



if __name__ == "__main__":
    window = tk.Tk()
    canvas = Canvas()
    gui = GUI(window, canvas)