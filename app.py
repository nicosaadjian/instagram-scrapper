import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Abstraer el LOGIN

# 3. Obtener el token CSRF si existe
#csrf_token = soup.find("input", {"name": "csrf_token"})
#csrf_value = csrf_token["value"] if csrf_token else ""

#username = response
#password = response

### Get imagenes deseadas
#Primero hay que pegarle al usuario del cual queremos descargar las fotos
#ig_account = input("Ingresa cuenta de la queres descargar fotos: ")
#Este ig_account no va a ser necesario tenerlo como input, sino como un text porque vamos a scrapear el text.value de ahi y despues encajarselo a la url que querramos

### Fin del Get imagenes

#Guardar imagenes fetcheadas en una carpeta 


# Opciones del navegador ---> Apuntar al ejecutable de Brave
options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # ⚠️ Asegurate de que esta ruta exista
#options.add_argument("--headless=new")  # ✅ Modo oculto --> Sirve para ahorrarnos el levantar una instancia de Brave cada vez que corremos la app

# Ruta al chromedriver que está en la misma carpeta que app.py
service = Service(executable_path="./chromedriver.exe")

# Inicializar el driver
driver = webdriver.Chrome(service=service, options=options)

#Este get testea si el driver te levanta Chrome efectivamente, para ver si el driver esta instalado ok y andando
#Ademas si lo dejamos levantado, vamos a ver que escribe las credenciales e inicia sesion correctamente
driver.get("https://www.instagram.com")

# Esperar que cargue el input de login
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

#Apuntamos al sitio de login de Instagram
driver.find_element(By.NAME, "username").send_keys("usuario")
driver.find_element(By.NAME, "password").send_keys("contraseña")

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
)
login_button.click()

#Le damos una espera de 10 segundos para que termine de iniciar sesion Instagram con las credenciales que pasemos
time.sleep(10)

#Definimos de que cuenta queremos guardar las imagenes
usuario = "francolapinto"  # o el que quieras buscar
driver.get(f"https://www.instagram.com/{usuario}/")

#Mensajes
url_msg = "https://www.instagram.com/direct/inbox/"
#driver.get(url_msg)


#Partes claves del scraper

#Instanciamos un WebDriverWait para reutilizarlo con la carga de contenido html 
wait = WebDriverWait(driver, 10)

#Trupla: 3-uplas (a.k.a. divs que tienen 3 elementos)
div_contenedor_truplas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._ac7v.xat24cr.x1f01sob.xcghwft.xzboxd6')))

for i in div_contenedor_truplas:
    #Primero bancamos que cargue el div que tiene cada imagen individual
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x11i5rnm.x1ntc13c.x9i3mqj.x2pgyrj')))
    #Despues bancamos que cargue el img que contiene el src de la imagen que queremos descargar
    imgs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')))
    src = [img.get_attribute("src") for img in imgs]
    #Por cada link en la lista de src...
    for s in src:
        print("Imagen del facha: ", s)
        response = requests.get(s)
        #Si el response esta ok, escribimos la imagen
        if response.status_code == 200:
            filename = f"imagen_{int(time.time())}.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
        #Le damos un time.sleep(4) para que no procese todo de una, sino trae siempre las mismas imagenes porque se pisa todo
        time.sleep(4)


input("Presioná Enter para cerrar...")
driver.quit()