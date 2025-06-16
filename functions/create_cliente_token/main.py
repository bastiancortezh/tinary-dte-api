import logging
import zcatalyst_sdk
import uuid
from datetime import date
from flask import make_response, jsonify

def handler(request):
    now = None
    try:
        app = zcatalyst_sdk.initialize()
        datastore = app.datastore()
        clientes = datastore.table("ClientesAPI")

        # Soporte para JSON y formulario
        content_type = request.headers.get("Content-Type", "")
        if "application/json" in content_type:
            data = request.get_json()
        else:
            data = request.form

        nombre = data.get("nombre_empresa")
        rut = data.get("rut_empresa")

        if not nombre or not rut:
            return make_response(jsonify({
                "status": "error",
                "message": "Faltan campos requeridos"
            }), 400)

        token = str(uuid.uuid4())
        now = date.today().isoformat()

        row_data = {
            "nombre_empresa": nombre,
            "rut_empresa": rut,
            "token_api": token,
            "estado": "activo",
            "fecha_creacion": now,
            "ultima_actividad": now
        }

        clientes.insert_row(row_data)

        return make_response(jsonify({
            "status": "success",
            "token_api": token
        }), 200)

    except Exception as e:
        return make_response(jsonify({
            "status": "error",
            "message": str(e),
            "fecha_creacion_debug": str(now) if now else "now no definido"
        }), 500)
