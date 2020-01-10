from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import pymysql
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/usuarios/*": {"origins": "*"}})

class Usuarios(Resource):
    def get(self):        
        db = pymysql.connect("localhost","root","julio3017","compras")       
        cursor = db.cursor()
        cursor.execute("select * from usuarios")
        results = cursor.fetchall()
        db.close()
        
        return {'Usuarios': [i[0] for i in results]}  # Se obtiene la primera columna que es UsuariosID
    def post(self):
        db = pymysql.connect("localhost","root","julio3017","compras")       
        cursor = db.cursor()
        usuario = request.json['usuario']
        nombre = request.json['nombre']        
        clave = request.json['clave']
        rol=request.json['rol']
        id_ofi=request.json['id_ofi']
        id_user=request.json['id']
        cursor.execute("insert into usuarios values('{0}','{1}','{2}','{3}', \
                             '{4}','{5}')".format(id_user, usuario, clave, nombre, rol, id_ofi))
        #results = cursor.fetchall()
        db.close()       
        return {'status': 'Nuevo Usuario añadido'}

class DatosUsuario(Resource):
    def get(self, id_usuario):
        db=pymysql.connect("localhost","root","julio3017","compras")
        cursor=db.cursor()
        cursor.execute("select * from usuarios where id =%d " % int(id_usuario))
        result=cursor.fetchall()
        row_headers=[x[0] for x in cursor.description]
        db.close()
        json_data=[]
        for res in result:
                json_data.append(dict(zip(row_headers,res)))
        return jsonify(json_data)

class UpdateUsuario(Resource):
    def put(self, id_usuario):
        db=pymysql.connect("localhost","root","julio3017","compras")
        cursor=db.cursor()
        usuario = request.json['usuario']
        nombre = request.json['nombre']        
        clave = request.json['clave']
        rol=request.json['rol']
        id_ofi=request.json['id_ofi']
        id_user=id_usuario
        cursor.execute("update usuarios set user='{1}', password='{2}', nombre='{3}', \
                             rol='{4}', id_ofi='{5}' where id={0}".format(id_user, usuario, clave, nombre, rol, id_ofi))
        #results = cursor.fetchall()
        db.close()       
        return {'status': 'Usuario Actualizado'}

class DeleteUsuario(Resource):
    def delete(self, id_usuario):
        db=pymysql.connect("localhost","root","julio3017","compras")
        cursor=db.cursor()
        cursor.execute("delete from usuarios where id={0}".format(id_usuario))
        return {'status': 'Usuario Eliminado'}


       
api.add_resource(Usuarios, '/usuarios/')  # Route_1
api.add_resource(DatosUsuario, '/usuarios/<id_usuario>')  # Route_2
api.add_resource(UpdateUsuario, '/updateusuarios/<id_usuario>')  # Route_3
api.add_resource(DeleteUsuario, '/deleteusuarios/<id_usuario>')  # Route_4
if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5000')