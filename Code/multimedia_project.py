import pygame
import os
import time
import random
import cv2
import threading

pygame.init()
pygame.mixer.init()

# Paths for images, music, and lyrics
IMAGE_FOLDER = "C:/Users/ayesh/OneDrive/Desktop/multimedia_project/images"
MUSIC_FOLDER = "C:/Users/ayesh/OneDrive/Desktop/multimedia_project/music"
LYRICS_FOLDER = "C:/Users/ayesh/OneDrive/Desktop/multimedia_project/lyrics"

IMAGE_FILES = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
AUDIO_FILES = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]

if not IMAGE_FILES or not AUDIO_FILES:
    print("Missing image or music files!")
    exit()

# Display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
font = pygame.font.SysFont("arial", 30)
clock = pygame.time.Clock()

# Music
song_index = 0
volume = 0.5
pygame.mixer.music.set_volume(volume)

def play_song(index):
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, AUDIO_FILES[index]))
    pygame.mixer.music.play()
    return time.time()

# Initialize music and face detection status
music_paused = False
face_detected = False
image_index = 0
auto_slideshow = False
slideshow_interval = 3  # seconds
last_switch_time = time.time()

# Load thumbnails
thumb_size = 80
thumbs = []
for img_file in IMAGE_FILES:
    img = pygame.image.load(os.path.join(IMAGE_FOLDER, img_file))
    img = pygame.transform.scale(img, (thumb_size, thumb_size))
    thumbs.append(img)

def show_image(index):
    img_path = os.path.join(IMAGE_FOLDER, IMAGE_FILES[index])
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(img, (0, 0))

def draw_overlay(lyrics):
    overlay = pygame.Surface((SCREEN_WIDTH, 120))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Song info
    song_text = font.render(f"Song: {AUDIO_FILES[song_index]}", True, (255, 255, 255))
    image_text = font.render(f"Image: {IMAGE_FILES[image_index]}", True, (255, 255, 255))
    screen.blit(song_text, (20, 10))
    screen.blit(image_text, (20, 50))

    # Volume
    vol_text = font.render(f"Volume: {int(volume * 100)}%", True, (255, 255, 255))
    screen.blit(vol_text, (SCREEN_WIDTH - 200, 10))

    # Progress bar
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        duration = 180  # Assume 3 min for simplicity (or use mutagen)
        bar_width = SCREEN_WIDTH - 40
        fill_width = int((current_time / duration) * bar_width)
        pygame.draw.rect(screen, (100, 100, 100), (20, 90, bar_width, 10))
        pygame.draw.rect(screen, (0, 200, 0), (20, 90, fill_width, 10))

        # Face detection status
    if face_detected:
        face_status = "Face Detected"
        face_color = (0, 255, 0)  # Green
    else:
        face_status = "Face Not Detected"
        face_color = (255, 0, 0)  # Red

    face_text = font.render(face_status, True, face_color)
    screen.blit(face_text, (SCREEN_WIDTH - 250, 50))

    # Display lyrics
    draw_lyrics(lyrics)

def draw_lyrics(lyrics):
    y_offset = 90
    for line in lyrics:
        lyrics_text = font.render(line.strip(), True, (255, 255, 255))
        screen.blit(lyrics_text, (20, y_offset))
        y_offset += 30  # Move to next line

def load_lyrics(song_index):
    # Assuming each song has a corresponding .txt file in the lyrics folder
    lyrics_path = os.path.join(LYRICS_FOLDER, AUDIO_FILES[song_index].replace('.mp3', '.txt'))
    if os.path.exists(lyrics_path):
        with open(lyrics_path, 'r') as file:
            return file.readlines()
    return []

def detect_face():
    global face_detected, music_paused
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Check face detection
        if len(faces) > 0:
            if not face_detected:  # If face was not previously detected, unpause music
                face_detected = True
                if music_paused:
                    pygame.mixer.music.unpause()
                    music_paused = False
        else:
            if face_detected:  # If face is lost, pause the music
                face_detected = False
                if not music_paused:
                    pygame.mixer.music.pause()
                    music_paused = True

    cap.release()

# Ask the user to select a song to play
print("\nAvailable Songs:")
for i, song in enumerate(AUDIO_FILES):
    print(f"{i + 1}. {song}")

while True:
    try:
        choice = int(input("\nEnter the number of the song to play: ")) - 1
        if 0 <= choice < len(AUDIO_FILES):
            song_index = choice
            play_song(song_index)
            break
        else:
            print("Invalid choice. Try again!")
    except ValueError:
        print("Please enter a valid number!")

# Start face detection in a separate thread
threading.Thread(target=detect_face, daemon=True).start()

# Initial display
show_image(image_index)
lyrics = load_lyrics(song_index)
draw_overlay(lyrics)
pygame.display.flip()

running = True
while running:
    screen.fill((0, 0, 0))
    if auto_slideshow and time.time() - last_switch_time > slideshow_interval:
        image_index = (image_index + 1) % len(IMAGE_FILES)
        last_switch_time = time.time()

    show_image(image_index)
    draw_overlay(lyrics)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                image_index = (image_index + 1) % len(IMAGE_FILES)
                last_switch_time = time.time() 
            elif event.key == pygame.K_LEFT:
                image_index = (image_index - 1) % len(IMAGE_FILES)
                last_switch_time = time.time() 
            elif event.key == pygame.K_SPACE:
                if music_paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                music_paused = not music_paused
            elif event.key == pygame.K_UP:
                volume = min(volume + 0.1, 1.0)
                pygame.mixer.music.set_volume(volume)
            elif event.key == pygame.K_DOWN:
                volume = max(volume - 0.1, 0.0)
                pygame.mixer.music.set_volume(volume)
            elif event.key == pygame.K_s:
                auto_slideshow = not auto_slideshow
                last_switch_time = time.time()
            elif event.key == pygame.K_n:
                song_index = (song_index + 1) % len(AUDIO_FILES)
                play_song(song_index)
                music_paused = False
            elif event.key == pygame.K_p:
                song_index = (song_index - 1) % len(AUDIO_FILES)
                play_song(song_index)
                music_paused = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to pause/play
                if music_paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                music_paused = not music_paused
            elif event.button == 4:  # Scroll up
                image_index = (image_index - 1) % len(IMAGE_FILES)
            elif event.button == 5:  # Scroll down
                image_index = (image_index + 1) % len(IMAGE_FILES)

    pygame.display.flip()
    clock.tick(5)

pygame.quit()