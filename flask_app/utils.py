import csv
from io import StringIO
from flask import Response


def export_csv_response(equipos):
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow([
        "id", "nombre", "descripcion", "modelo", "numero_serial",
        "datacenter", "estado", "fecha_registro"
    ])
    for e in equipos:
        writer.writerow([
            e.id, e.nombre, e.descripcion or "", e.modelo, e.numero_serial,
            e.datacenter, e.estado, e.fecha_registro.isoformat()
        ])
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=equipos.csv"}
    )
