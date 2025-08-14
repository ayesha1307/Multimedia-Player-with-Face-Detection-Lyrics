# Multimedia Player with Face Detection and Lyrics Display

## Overview
This project is a fullscreen multimedia application developed in **Python** using **Pygame** and **OpenCV**.  
It provides an integrated interface for image slideshows, music playback, synchronized lyrics display, and intelligent pause/resume functionality through real-time face detection.

---

## Key Features
- **Image Slideshow**: Manual and automatic image transitions.
- **Music Playback**: Play, pause, and track navigation.
- **Lyrics Display**: Automatic loading of lyrics from `.txt` files matching the music file name.
- **Face Detection**: Pauses playback when no face is detected and resumes when a face is present.
- **Volume Control**: Adjustable via keyboard shortcuts.
- **Interactive Controls**: Mouse and keyboard input support.
- **Progress Indicator**: Displays song playback status.

## Folder Structure
![WhatsApp Image 2025-08-14 at 22 50 52_ab554a56](https://github.com/user-attachments/assets/39dc46dd-b890-46fb-bb8f-cf16978e9365)


Install dependencies: pip install pygame opencv-python mutagen

Usage:
Navigate to the code directory and execute:
- python multimedia_project.py

Controls
- Input	Action
→ / ←	Next / Previous image
- S	Toggle auto slideshow
- N / P	Next / Previous song
- SPACE	Pause / Resume music
- ↑ / ↓	Increase / Decrease volume
- Mouse Click	Pause / Resume music
- Scroll Wheel	Change images
- ESC	Exit application

- ##Technical Details
Pygame is used for graphical rendering, event handling, and audio playback.
OpenCV captures frames from the webcam for real-time face detection.
Mutagen retrieves metadata for music files.
The application overlays song lyrics and playback information on the display.
Face detection logic ensures media is paused when no user presence is detected.
