import logging
#from flask import Request, make_response, jsonify
import zcatalyst_sdk
import uuid
from datetime import date
'''
Execute below command to install SDK in global for enabling code suggestions
-> python3 -m pip install zcatalyst-sdk
'''

#def handler(request: Request):
    # app = zcatalyst_sdk.initialize()
    # logger = logging.getLogger()
    # if request.path == "/":
    #     response = make_response(jsonify({
    #         'status': 'success',
    #         'message': 'Hello from main.py'
    #     }), 200)
    #     return response
    # elif request.path == "/cache":
    #     default_segment = app.cache().segment()

    #     insert_resp = default_segment.put('Name', 'DefaultName')
    #     logger.info('Inserted cache : ' + str(insert_resp))
    #     get_resp = default_segment.get('Name')

    #     return jsonify(get_resp), 200
    # else:
    #     response = make_response('Unknown path')
    #     response.status_code = 400
    #     return response
def handler(request):
    now = None
    try:
        app = zcatalyst_sdk.initialize()
        datastore = app.datastore()
        clientes = datastore.table("ClientesAPI")

        data = request.get_json()
        nombre = data.get("nombre_empresa")
        rut = data.get("rut_empresa")

        if not nombre or not rut:
            return {
                "status":"error",
                "message":"Faltan campos requeridos"
            }
        
        token = str(uuid.uuid4())
        now = date.today().isoformat()

        
        row_data = {
            "nombre_empresa":nombre,
            "rut_empresa":rut,
            "token_api":token,
            "estado":"activo",
            "fecha_creacion": now,
            "ultima_actividad":now
        }

        clientes.insert_row(row_data)
        return {
            "status":"success",
            "token_api": token
        }

    except Exception as e:
        return {
            "status":"error",
            "message":str(e),
            "fecha_creacion_debug": str(now) if 'now' in locals() else "now no definido"
        }
