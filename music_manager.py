import pygame
import os
import random
from collections import deque

class MusicManager:
    def __init__(self, music_folder):
        self.music_folder = os.path.join(os.path.dirname(__file__), music_folder)
        self.songs = []
        self.queue = []
        self.current_index = 0
        self.is_muted = False
        self.song_history = deque(maxlen=5)
        self.load_songs()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Custom end event

    def load_songs(self):
        if not os.path.isdir(self.music_folder):
            print(f"Music folder not found: {self.music_folder}. Create it and add .mp3 files.")
            return
        for file_name in os.listdir(self.music_folder):
            if file_name.lower().endswith('.mp3'):
                full_path = os.path.join(self.music_folder, file_name)
                self.songs.append(full_path)
        if not self.songs:
            print(f"No .mp3 files found in {self.music_folder}. Add some to play music.")
            return
        self.queue = self.songs[:]
        random.shuffle(self.queue)

    def play_next(self):
        if not self.queue:
            self.load_songs()
            if not self.queue:
                return
        song = self.queue.pop(0)
        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.song_history.append(song)
        except Exception as e:
            print(f"Error playing {song}: {e}")
            self.play_next()  # Skip bad file

    def mute(self):
        self.is_muted = not self.is_muted
        volume = 0 if self.is_muted else 1.0
        pygame.mixer.music.set_volume(volume)

    def skip(self):
        pygame.mixer.music.stop()
        self.play_next()

    def play_previous(self):
        if self.song_history:
            song = self.song_history[-1]
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.song_history.append(song)
            except Exception as e:
                print(f"Error playing previous {song}: {e}")
                self.play_next()
        else:
            self.play_next()

    def update(self):
        for event in pygame.event.get([pygame.USEREVENT + 1]):
            if event.type == pygame.USEREVENT + 1:
                self.play_next()

