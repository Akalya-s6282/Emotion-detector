import flet as ft
import threading
import queue
from keyboard import BlinkKeyboardApp
from gray_img import blink

blink_queue = queue.Queue()

def main(page: ft.Page):
    app = BlinkKeyboardApp(page, blink_queue)

    # Start blink detection + send frames to Flet
    threading.Thread(
        target=blink,
        args=(blink_queue, app.update_camera_image),
        daemon=True
    ).start()

ft.app(target=main)
