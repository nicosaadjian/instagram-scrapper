import customtkinter as ctk

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label_title = ctk.CTkLabel(self, text="Iniciar sesión", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10)

        self.button_login = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        usuario = self.entry_user.get()
        password = self.entry_pass.get()
        
        if usuario == "admin" and password == "123":  # Validación dummy
            self.master.switch_frame(lambda master: BuscarUsuarioFrame(master))  # Carga el siguiente frame
        else:
            ctk.CTkMessagebox(title="Error", message="Credenciales incorrectas")  # Podés cambiar esto

# ⚠️ IMPORTACIÓN para evitar error circular (se puede refactorizar después)
from frames.buscar_usuario_frame import BuscarUsuarioFrame
