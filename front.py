import customtkinter as ctk
from frames.login_frame import LoginFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Instagram Photo Scraper")
        self.geometry("500x400")
        self.resizable(False, False)

        self.current_frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        """Destruye el frame actual y carga uno nuevo"""
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # "light", "dark", "system"
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
