import os
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURACIÓN ===

# Usuario objetivo
usuario = "francolapinto"  # Cambiá por el que quieras

# Credenciales (idealmente deberías encriptarlas o ponerlas en variables de entorno)
USER = "francolapinto"
PASS = "aguantenlascarreras"

# Selector de imágenes
img_selector = 'img.x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3'

# Ruta de Brave
options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# options.add_argument("--headless=new")  # Descomentar si querés modo invisible

# Inicializar driver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# === LOGIN ===

driver.get("https://www.instagram.com")
wait.until(EC.presence_of_element_located((By.NAME, "username")))

driver.find_element(By.NAME, "username").send_keys(USER)
driver.find_element(By.NAME, "password").send_keys(PASS)

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
login_button.click()

time.sleep(10)  # Espera extra para login + popups

# === NAVEGAR A LA CUENTA ===

driver.get(f"https://www.instagram.com/{usuario}/")
time.sleep(5)

# === SCROLL Y DESCARGA DE IMÁGENES ===

visited_srcs = set()
last_count = 0
scrolls = 0
max_scrolls = 30  # Evita loops infinitos

print("🔍 Comenzando el scroll...")

while scrolls < max_scrolls:
    # Scroll hasta el fondo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Obtener imágenes actuales
    imgs = driver.find_elements(By.CSS_SELECTOR, img_selector)

    for img in imgs:
        src = img.get_attribute("src")
        if src and src not in visited_srcs:
            visited_srcs.add(src)

    print(f"🖼️ Iteración {scrolls + 1}: total imágenes únicas encontradas: {len(visited_srcs)}")

    # Salir si ya no aparecen nuevas
    if len(visited_srcs) == last_count:
        print("✅ No se detectaron imágenes nuevas, fin del scroll.")
        break

    last_count = len(visited_srcs)
    scrolls += 1

# === GUARDAR IMÁGENES ===

# Crear carpeta si no existe
output_dir = "imagenes"
os.makedirs(output_dir, exist_ok=True)

print(f"💾 Guardando {len(visited_srcs)} imágenes en la carpeta '{output_dir}'...")

for i, src in enumerate(visited_srcs):
    try:
        response = requests.get(src)
        if response.status_code == 200:
            filename = os.path.join(output_dir, f"imagen_{i+1}.jpg")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Imagen guardada: {filename}")
        time.sleep(1)  # Evita pisarse
    except Exception as e:
        print(f"⚠️ Error al descargar {src}: {e}")

input("\n🛑 Presioná Enter para cerrar...")
driver.quit()
