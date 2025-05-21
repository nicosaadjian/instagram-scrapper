import customtkinter as ctk

class BuscarUsuarioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        label = ctk.CTkLabel(self, text="Buscar usuario a scrapear")
        label.pack(pady=20)
        # Agregaremos más widgets luego
