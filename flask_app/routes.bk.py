from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.models import Equipo, db

import csv
import io
import pandas as pd
from flask import send_file, flash
from werkzeug.utils import secure_filename



main = Blueprint('main', __name__)

# Página principal con lista de equipos
@main.route('/')
def home():
    equipos = Equipo.query.all()
    return render_template('equipos/index.html', equipos=equipos)

# Formulario para agregar equipo (GET para mostrar, POST para guardar)
@main.route('/nuevo', methods=['GET', 'POST'])
def form_equipo():
    if request.method == 'POST':
        nuevo_equipo = Equipo(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            modelo=request.form['modelo'],
            numero_serial=request.form['numero_serial'],
            datacenter=request.form['datacenter'],
            estado=request.form['estado']
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        flash('Equipo agregado con éxito', 'success')
        return redirect(url_for('main.home'))

    return render_template('equipos/form.html')

# Eliminar equipo
@main.route('/delete/<int:id>', methods=['POST'])
def delete_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado', 'danger')
    return redirect(url_for('main.home'))

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipo(id):
    equipo = Equipo.query.get_or_404(id)

    if request.method == 'POST':
        equipo.nombre = request.form['nombre']
        equipo.descripcion = request.form['descripcion']
        equipo.modelo = request.form['modelo']
        equipo.numero_serial = request.form['numero_serial']
        equipo.datacenter = request.form['datacenter']
        equipo.estado = request.form['estado']

        db.session.commit()
        flash('Equipo actualizado con éxito', 'success')
        return redirect(url_for('main.home'))

    return render_template('equipos/edit.html', equipo=equipo)

@main.route('/export_excel')
def export_excel():
    equipos = Equipo.query.all()
    data = [{
        'Nombre': e.nombre,
        'Descripción': e.descripcion,
        'Modelo': e.modelo,
        'Número de Serie': e.numero_serial,
        'Datacenter': e.datacenter,
        'Estado': e.estado
    } for e in equipos]

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventario')

    output.seek(0)
    return send_file(output, as_attachment=True, download_name="inventario.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




@main.route('/import_csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        flash('No se subió ningún archivo', 'danger')
        return redirect(url_for('main.home'))

    file = request.files['file']
    if file.filename == '':
        flash('Nombre de archivo inválido', 'danger')
        return redirect(url_for('main.home'))

    try:
        # Check file extension
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension == 'xlsx' or file_extension == 'xls':
            # Handle Excel files
            import pandas as pd
            df = pd.read_excel(file, engine='openpyxl')
            csv_data = df.to_dict('records')
        else:
            # Handle CSV files with different encodings
            file_content = file.stream.read()
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-8-sig']
            csv_data = None
            
            for encoding in encodings:
                try:
                    stream = io.StringIO(file_content.decode(encoding), newline=None)
                    csv_input = csv.DictReader(stream)
                    csv_data = list(csv_input)
                    break
                except UnicodeDecodeError:
                    continue
            
            if csv_data is None:
                flash('No se pudo leer el archivo con ningún encoding', 'danger')
                return redirect(url_for('main.home'))

        required_cols = {'nombre', 'descripcion', 'modelo', 'numero_serial', 'datacenter', 'estado'}
        
        if not csv_data:
            flash("El archivo está vacío o no se pudo leer", "danger")
            return redirect(url_for('main.home'))

        # Normaliza las claves del primer registro
        columnas_archivo = set(k.strip().lower() for k in csv_data[0].keys())
        print(f"📋 Columnas detectadas: {columnas_archivo}")

        if not required_cols.issubset(columnas_archivo):
            faltantes = required_cols - columnas_archivo
            flash(f"Faltan columnas: {', '.join(faltantes)}", "danger")
            return redirect(url_for('main.home'))


        for row in csv_data:
            equipo = Equipo(
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                modelo=row['modelo'],
                numero_serial=row['numero_serial'],
                datacenter=row['datacenter'],
                estado=row['estado']
            )
            db.session.add(equipo)


        db.session.commit()
        flash('Equipos importados con éxito ✅', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar: {str(e)}', 'danger')

    return redirect(url_for('main.home'))



