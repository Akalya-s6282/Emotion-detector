import flet as ft
import threading
import time

class BlinkKeyboardApp:
    def __init__(self, page: ft.Page, blink_queue):
        self.page = page
        self.blink_queue = blink_queue

        self.keyboard_rows = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            list("ZXCVBNM") + ["SPACE", "BACKSPACE"]
        ]
        self.current_row = 0
        self.current_col = 0
        self.key_buttons = []

        self.output = ft.TextField(
            label="Typed Text",
            value="",
            read_only=True,
            width=500,
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_radius=8,
            border_color="#444444",
            focused_border_color="#9500ff",
            bgcolor="#0d0d0d",
            color="white",
            cursor_color="#9500ff",
            hint_text="Type here...",
            hint_style=ft.TextStyle(color="#bbbbbb"))
        
        self.display = ft.Container(
            content=ft.Text(
            value="",
            size=16,
            color="white",
            weight="bold",
            text_align="center",
            ),
            width=200,
            bgcolor="#00000080",
            border_radius=8,
            padding=10,
            visible=True
        )
        
        self.camera_image = ft.Image(
            src_base64="",
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=10,)

        self.pause_highlight = threading.Event()

        self.build_ui()
        self.page.update()

        threading.Thread(target=self.listen_blink_queue, daemon=True).start()
        threading.Thread(target=self.blink_loop, daemon=True).start()

    def build_ui(self):
        layout = []
        for row in self.keyboard_rows:
            row_buttons = []
            for key in row:
                btn = ft.ElevatedButton(
                    text=key,
                    bgcolor="#D3D3D3",
                    # on_click=self.on_key_press,
                    width=80 if key in ["SPACE", "BACKSPACE"] else 50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation={"": 2, "hovered": 6},
                    ),
                    on_click=self.on_key_press
                )
                row_buttons.append(btn)
                self.key_buttons.append(btn)
            layout.append(ft.Row(row_buttons, alignment=ft.MainAxisAlignment.CENTER))

        self.page.controls.append(
        ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text("Live Camera Feed", size=20),
                self.camera_image,
                self.display,
            ], expand=1, alignment=ft.MainAxisAlignment.START, spacing=15),

            ft.Column([
                ft.Text("Blink Keyboard", size=24),
                self.output,
                *layout
            ], expand=2, alignment=ft.MainAxisAlignment.START, spacing=20)
        ], spacing=30),
        expand=True,                          # fill entire window
        padding=20,
        image=ft.DecorationImage(
            src="background.png",   # <-- put your violet/black background file path here
            fit=ft.ImageFit.COVER 
                )         # COVER = full screen, CONTAIN = fit inside
    )
)

    def on_key_press(self, e):
        key = e.control.text
        self.handle_key_input(key)

    def handle_key_input(self, key):
        if key == "SPACE":
            self.output.value += " "
        elif key == "BACKSPACE":
            self.output.value = self.output.value[:-1]
        else:
            self.output.value += key
        time.sleep(1.0)
        self.page.update()

    def blink_loop(self):
        while True:
            if not self.pause_highlight.is_set():
                self.current_col += 1
                if self.current_col >= len(self.keyboard_rows[self.current_row]):
                    self.current_col = 0  # Wrap to beginning of same row
                self.update_highlight()
                time.sleep(1.0)

    def update_highlight(self):
        # Reset all buttons
        for btn in self.key_buttons:
            btn.bgcolor = "#D3D3D3"
            btn.color = "#000000"
            btn.style = ft.ButtonStyle(
                elevation={"": 2}
            )

        try:
            btn_index = sum(len(row) for row in self.keyboard_rows[:self.current_row]) + self.current_col
            btn = self.key_buttons[btn_index]
            btn.bgcolor = "#9500FF"
            btn.color = "#FFFFFF"
            btn.style = ft.ButtonStyle(
                elevation={"": 8},
                shadow_color={"": "#460080"}
            )
        except IndexError:
            pass

        self.page.update()

    def listen_blink_queue(self):
        while True:
            if not self.blink_queue.empty():
                msg = self.blink_queue.get()

                if msg == "LEFT":
                    self.current_row = (self.current_row + 1) % len(self.keyboard_rows)
                    self.current_col = 0
                    self.display.content.value = "Right blink detected"
                    self.pause_highlight.set()
                    self.page.update()
                    time.sleep(2.2)
                    self.pause_highlight.clear()
                    self.display.content.value = ""


                # elif msg == "RIGHT":
                #     self.current_row = 0
                #     self.current_col = 0
                #     self.display.value = "Right blink detected"
                #     self.pause_highlight.set()
                #     self.page.update()
                #     time.sleep(2.2)
                #     self.pause_highlight.clear()
                #     self.display.value = ""


                elif msg == "BLINK":
                    try:
                        key = self.keyboard_rows[self.current_row][self.current_col]
                        self.handle_key_input(key)
                    except IndexError:
                        pass

                    self.display.content.value = "Blink detected"
                    self.pause_highlight.set()
                    self.page.update()
                    time.sleep(1.2)
                    self.pause_highlight.clear()
                    self.display.content.value = ""

                self.update_highlight()

    def update_camera_image(self, img_base64):
        self.camera_image.src_base64 = img_base64
        self.page.update()
