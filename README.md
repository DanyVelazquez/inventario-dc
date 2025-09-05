Sistema de Inventario DC
Sistema de gestión de inventario desarrollado con Flask y SQLite.

📦 Requisitos Previos
Python 3.8+

pip

🚀 Instalación Rápida
1. Clonar el repositorio
bash
git clone -b proyecto-inventario https://github.com/DanyVelazquez/inventario-dc.git
cd inventario-dc
2. Crear entorno virtual e instalar dependencias
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
3. Configurar la aplicación
bash
cp .env.example .env
Editar .env con:

text
SECRET_KEY=tu-clave-secreta-aqui
4. Inicializar base de datos
bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
5. Ejecutar la aplicación
bash
flask run
Abre tu navegador en: http://localhost:5000
