import os
import sys
import pygame
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import *
from tkinter import filedialog, messagebox, ttk

# This code is not complete. If you have any improvements or suggestions, I would appreciate it if you could share them with me.

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.minsize(600, 580)
        self.root.resizable(False, False)
        mixer.init()

        self.track = StringVar()
        self.status = StringVar()
        self.songs_list = []
        self.song = None
        self.pause_situation = False
        self.stopped = False

        self.create_frames()
        self.create_widgets()

        # Process command-line arguments
        if len(sys.argv) > 1:
            self.add_to_playlist(sys.argv[1:])
            self.play_file(sys.argv[1:])

    def create_frames(self):
        # Create Frames
        self.track_frame = LabelFrame(self.root, text="Song Track", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5)
        self.track_frame.place(x=0, y=0, width=600, height=100)

        self.song_frame = LabelFrame(self.root, text="Song Controls", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5)
        self.song_frame.place(x=0, y=100, width=600, height=100)

        self.playlist_frame = LabelFrame(self.root, text="Playlist", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5)
        self.playlist_frame.place(x=0, y=200, width=600, height=220)

        self.info_frame = LabelFrame(self.root, text="Info", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5)
        self.info_frame.place(x=0, y=450, width=600, height=110)

    def create_widgets(self):
        # Track Label
        track_label = Label(self.track_frame, textvariable=self.track, width=20, font=("times new roman", 24, "bold"), bg="grey", fg="white")
        track_label.grid(row=0, column=0, padx=10, pady=5)

        # Status Label
        status_label = Label(self.track_frame, textvariable=self.status, font=("times new roman", 24, "bold"), bg="grey", fg="white")
        status_label.grid(row=0, column=1, padx=10, pady=5)

        # Song Listbox
        self.song_box = Listbox(self.root, height=7, width=52, selectmode=SINGLE, font=("times new roman", 14, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        self.song_box.bind('<Double-1>', lambda event: self.play())
        self.song_box.place(x=6, y=230)

        # Volume Control
        self.volume_scale = ttk.Scale(self.playlist_frame, length=170, command=self.set_volume, from_=100, to_=0, orient=VERTICAL)
        self.volume_scale.set(70)
        pygame.mixer.music.set_volume(0.7)
        self.volume_scale.place(x=550, y=5)

        # Create Status Bar
        self.status_bar = Label(self.root, text="", bd=1, relief=GROOVE, anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, pady=2)

        # Create a Slider
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=590, value=0, command=self.slide)
        self.slider.place(x=0, y=420)

        # Create Buttons
        play_button = Button(self.root, text="play", command=self.play, width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        play_button.place(x=10, y=135)

        pause_button = Button(self.root, text="pause", command=lambda: self.pause(self.pause_situation), width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        pause_button.place(x=105, y=135)

        stop_button = Button(self.root, text="stop", command=self.stop, width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        stop_button.place(x=205, y=135)

        next_button = Button(self.root, text="next", command=self.next_song, width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        next_button.place(x=305, y=135)

        previous_button = Button(self.root, text="previous", command=self.previous_song, width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        previous_button.place(x=405, y=135)

        open_button = Button(self.root, text="open", command=self.browse_files, width=6, height=1, font=("times new roman", 16, "bold"), fg="white", bg="blue")
        open_button.place(x=505, y=135)

        # Info Label
        info_label = Label(self.info_frame, width=60, height=4, text="Asad Music Player is possibly the lightest free music player available.\nIf you appreciate my work and would like to see more of it,\nplease consider making a donation to support my efforts.\nMy contacts: alirezasadg@gmail.com", font=("times new roman", 11, "bold"), bg="grey", fg="white")
        info_label.place(x=30, y=0)

    def browse_files(self):
        files = filedialog.askopenfilenames(initialdir="c:/Users/ali/Downloads/Music",
                                            title="Choose Songs", filetypes=(("mp3 File", "*.mp3"),))
        if files:
            self.add_to_playlist(files)

    def add_to_playlist(self, file_paths):
        for item in file_paths:
            if item not in self.songs_list:
                self.songs_list.append(item)
                song_name = os.path.basename(item)
                self.song_box.insert(END, song_name)

    def play(self):
        try:
            selected_song = self.song_box.get(ACTIVE)
            self.song = self.get_full_path(selected_song)
            self.track.set(selected_song)
            self.status.set("-Playing")
            self.stopped = False
            mixer.music.load(self.song)
            mixer.music.play(loops=0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play song: {e}")

    def play_file(self, file_paths):
        try:
            if isinstance(file_paths, str):
                file_paths = [file_paths]
            self.add_to_playlist(file_paths)
            self.song = file_paths[0]
            self.track.set(os.path.basename(self.song))
            self.status.set("-Playing")
            self.stopped = False
            mixer.music.load(self.song)
            mixer.music.play(loops=0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play file: {e}")

    def stop(self):
        self.status.set("-Stopped")
        mixer.music.stop()
        self.song_box.selection_clear(ACTIVE)
        self.stopped = True

    def set_volume(self, x):
        mixer.music.set_volume(self.volume_scale.get() / 100)

    def slide(self, x):
        try:
            mixer.music.load(self.song)
            mixer.music.play(loops=0, start=int(self.slider.get()))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to slide: {e}")

    def pause(self, is_paused):
        if is_paused:
            mixer.music.unpause()
            self.status.set("-Playing")
        else:
            mixer.music.pause()
            self.status.set("-Paused")
        self.pause_situation = not is_paused

    def next_song(self):
        try:
            next_one = self.song_box.curselection()[0] + 1
            self.song_box.selection_clear(0, END)
            self.song_box.activate(next_one)
            self.song_box.selection_set(next_one)
            self.play()
        except IndexError:
            pass

    def previous_song(self):
        try:
            previous_one = self.song_box.curselection()[0] - 1
            self.song_box.selection_clear(0, END)
            self.song_box.activate(previous_one)
            self.song_box.selection_set(previous_one)
            self.play()
        except IndexError:
            pass

    def get_full_path(self, song_name):
        for item in self.songs_list:
            if os.path.basename(item) == song_name:
                return item
        return None


if __name__ == "__main__":
    root = Tk()
    MusicPlayer(root)
    root.mainloop()
