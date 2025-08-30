import flet as ft

def main(page: ft.Page):
    page.title = "Test UI"
    page.add(ft.Text("Hello from Flet!"))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)