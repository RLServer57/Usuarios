from DB.Conexion import conectar
import mysql.connector

class CRUD:
    def crear(self,nombre,apellido,edad,sexo):
        try:
            conexion=conectar()
            try:
                cursor=conexion.cursor()
                sql="insert into Usuario(nombre,apellido,edad,sexo) values (%s,%s,%s,%s);"
                cursor.execute(sql, (nombre, apellido,edad,sexo))
                conexion.commit()
                return "El usuario se ha registrado ✅"
            finally:
                conexion.close()
        except (mysql.connector.Error) as e:
            return f"Ocurrió un error ❌:{e}"

    def leer(self):
        try:
            conexion=conectar()
            try:
                cursor=conexion.cursor()
                sql="SELECT * FROM Usuario;"
                cursor.execute(sql)
                usuarios = cursor.fetchall()
                return usuarios
            finally:
                conexion.close()
        except (mysql.connector.Error) as e:
            return e

    def actualizar(self,nombre,apellido,edad,sexo,id):
        try:
            conexion=conectar()
            try:
                cursor=conexion.cursor()
                sql="UPDATE Usuario SET Nombre = %s,Apellido = %s,Edad = %s,Sexo = %s WHERE id = %s;"
                cursor.execute(sql, (nombre,apellido,edad,sexo,id))
                conexion.commit()
                return "El usuario se ha modificado ✅"
            finally:
                conexion.close()
        except (mysql.connector.Error) as e:
            return f"Ocurrió un error ❌:{e}"

    def eliminar(self,id):
        try:
            conexion=conectar()
            try:
                cursor=conexion.cursor()
                sql="DELETE FROM Usuario WHERE id = %s;"
                cursor.execute(sql,(id,))
                conexion.commit()
                return "El usuario se ha eliminado ❗❗❗"
            finally:
                conexion.close()
        except (mysql.connector.Error) as e:
            return f"Ocurrió un error ❌:{e}"

    def buscar(self,id):
        try:
            conexion=conectar()
            try:
                cursor=conexion.cursor()
                sql="SELECT * FROM Usuario WHERE id = %s;"
                cursor.execute(sql,(id,))
                usuario = cursor.fetchall()
                return usuario
            finally:
                conexion.close()
        except (mysql.connector.Error) as e:
            return e