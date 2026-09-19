# API RESTful con FastAPI en AWS EC2 (Usuarios y Libros)

Esta es una API sencilla desarrollada con **FastAPI** y **SQLModel** (SQLite) que implementa operaciones CRUD para las entidades **Usuarios** y **Libros**. Está lista para ser desplegada en una instancia **AWS EC2** y gestionada con **PM2**.

---

##  Estructura del Proyecto

```text
Fastapi on EC2/
│
├── main.py            # Código completo de la API (modelos, base de datos y endpoints)
├── requirements.txt   # Dependencias de Python necesarias
├── .gitignore         # Archivos ignorados por Git
└── README.md          # Instrucciones paso a paso
```

---

##  1. Ejecución en Local

### Paso 1.1: Crear y activar entorno virtual
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux / Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 1.2: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 1.3: Ejecutar la API
```bash
uvicorn main:app --reload --port 8000
```

### Paso 1.4: Probar la API
Abre en tu navegador:
- **Documentación Swagger interactiva:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentación Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 2. Subir el Proyecto a GitHub / GitLab

Desde la carpeta del proyecto en tu terminal:

```bash
git init
git add .
git commit -m "API inicial con FastAPI y SQLModel para EC2"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

---

## 3. Despliegue en AWS EC2

### Paso 3.1: Crear la Instancia EC2
1. Ve a la consola de AWS -> **EC2** -> **Lanzar instancia**.
2. **Nombre:** `FastAPI-Server` (o el que gustes).
3. **AMI:** Ubuntu 22.04 LTS o 24.04 LTS (o Amazon Linux).
4. **Tipo de instancia:** `t2.micro` (Apta para la capa gratuita).
5. **Par de claves:** Crea o selecciona un par de claves `.pem` para conectarte por SSH.

### Paso 3.2: Configurar el Security Group (¡Muy Importante!)
En las reglas de entrada (**Inbound Rules**):
- **SSH** (Puerto 22): Desde tu IP o Anywhere (0.0.0.0/0).
- **Regla personalizada TCP** (Puerto **8000**):
  - Tipo: `Custom TCP`
  - Puerto: `8000`
  - Origen: `Anywhere-IPv4` (`0.0.0.0/0`)

### Paso 3.3: Conectarte a la instancia por SSH
```bash
ssh -i "tu-llave.pem" ubuntu@<IP_PUBLICA_EC2>
```

### Paso 3.4: Instalar Python, Git, Node.js y PM2 en la EC2
Ejecuta en la consola de la EC2:
```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python, pip y venv
sudo apt install -y python3-pip python3-venv git

# Instalar Node.js y PM2 para mantener la API siempre corriendo
sudo apt install -y nodejs npm
sudo npm install -g pm2
```

### Paso 3.5: Clonar el Repositorio y Configurar la API
```bash
# Clonar tu repositorio
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd "TU_REPOSITORIO"

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 3.6: Ejecutar la API con PM2
Dentro de la carpeta del proyecto y con el entorno virtual activado:
```bash
pm2 start "venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000" --name "fastapi-app"
```

Guardar la configuración de PM2 para que inicie automáticamente si la máquina se reinicia:
```bash
pm2 save
pm2 startup
```

---

## 4. Probar la API en Producción

Accede desde cualquier navegador a la IP pública de tu instancia EC2:

- **Inicio:** `http://<IP-PUBLICA>:8000/`
- **Documentación Swagger interactiva:** `http://<IP-PUBLICA>:8000/docs`
- **Endpoints de Usuarios:** `http://<IP-PUBLICA>:8000/usuarios/`
- **Endpoints de Libros:** `http://<IP-PUBLICA>:8000/libros/`

---

## 5. Endpoints Disponibles

### Usuarios:
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/usuarios/` | Crear un nuevo usuario |
| `GET` | `/usuarios/` | Listar todos los usuarios |
| `GET` | `/usuarios/{usuario_id}` | Obtener un usuario por ID |
| `PUT` | `/usuarios/{usuario_id}` | Actualizar un usuario existente |
| `DELETE`| `/usuarios/{usuario_id}` | Eliminar un usuario |

### Libros:
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/libros/` | Crear un nuevo libro |
| `GET` | `/libros/` | Listar todos los libros |
| `GET` | `/libros/{libro_id}` | Obtener un libro por ID |
| `PUT` | `/libros/{libro_id}` | Actualizar un libro existente |
| `DELETE`| `/libros/{libro_id}` | Eliminar un libro |
