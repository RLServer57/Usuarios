from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from GUI.users_ui import *
from DB.CRUD import *

crud = CRUD()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.columnas = ["Id", "Nombre", "Apellido", "Edad", "Sexo"]
        self.setupUi(self)
        self.setWindowIcon(QIcon('/resources/img/Logo_Usuarios.png'))
        self.tblListaUsuarios.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.btnGuardar.clicked.connect(self.agregar_usuario)
        self.btnBuscarID.clicked.connect(self.buscar_usuario)
        self.btnActualizar.clicked.connect(self.actualizar_usuario)
        self.btnEliminar.clicked.connect(self.eliminar_usuario)
        self.tabla_usuarios()

    def agregar_usuario(self):
        try:
            nombre = self.txtNombre.text()
            apellido = self.txtApellido.text()
            edad = int(self.txtEdad.text())
            sexo = self.cbxSexo.currentText()
            if sexo == "-Seleccione-":
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Atención')
                msgBox.setText('Debe seleccionar un Sexo')
                msgBox.exec_()
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Atención')
                msgBox.setText(crud.crear(nombre,apellido,edad,sexo))
                msgBox.exec_()
                self.limpiar_entradas()
                self.tblListaUsuarios.resizeColumnsToContents()
                self.tabla_usuarios()
        except (ValueError) as e:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Atención')
            msgBox.setText(f'Entrada no válida: {e.__str__()}')
            msgBox.exec_()

    def tabla_usuarios(self):
        self.tblListaUsuarios.resizeColumnsToContents()
        try:
            data = crud.leer()
            row = len(data)
            col = len(data[0])
            self.tblListaUsuarios.setRowCount(row)
            self.tblListaUsuarios.setColumnCount(col)
            self.tblListaUsuarios.setHorizontalHeaderLabels(self.columnas)
            header_view = self.tblListaUsuarios.horizontalHeader()
            idx = header_view.count() - 1
            header_view.setSectionResizeMode(idx, QtWidgets.QHeaderView.ResizeToContents)
            for i in range(row):
                for j in range(col):
                    temp_data = data [i][j] # registros temporales, no se pueden insertar directamente en la tabla
                    data1 = QTableWidgetItem (str (temp_data)) # se puede insertar en la tabla después de la conversión
                    data1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled) # marcamos las celas como no editables
                    self.tblListaUsuarios.setItem(i, j, data1)
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Atención')
            msgBox.setText('Ocurrió un error de conexión❗❗❗')
            msgBox.exec_()

    def buscar_usuario(self):
        try:
            id = self.txtBuscarID.text()
            data = crud.buscar(int(id))
            if len(data) > 0:
                for row in data:
                    self.txtNombre.setText(row[1])
                    self.txtApellido.setText(row[2])
                    self.txtEdad.setText(str(row[3]))
                    self.cbxSexo.setCurrentText(row[4])
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Atención')
                msgBox.setText('Usuario no encontrado.')
                msgBox.exec_()
        except (ValueError) as e:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Atención')
            msgBox.setText(f'Entrada no válida: {e.__str__()}')
            msgBox.exec_()

    def actualizar_usuario(self):
        try:
            id = self.txtBuscarID.text()
            nombre = self.txtNombre.text()
            apellido = self.txtApellido.text()
            edad = int(self.txtEdad.text())
            sexo = self.cbxSexo.currentText()
            if sexo == "-Seleccione-":
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Atención')
                msgBox.setText('Debe seleccionar un sexo')
                msgBox.exec_()
            else:
                msgBox = QMessageBox()
                msgBox.setText(crud.actualizar(nombre,apellido,edad,sexo,id))
                msgBox.exec_()
                self.limpiar_entradas()
                self.tblListaUsuarios.resizeColumnsToContents()
                self.tabla_usuarios()
        except (ValueError) as e:
            msgBox = QMessageBox()
            msgBox.setText(f'Entrada no válida: {e.__str__()}')
            msgBox.exec_()

    def eliminar_usuario(self):
        ret = QMessageBox.warning(self, "Advertencia",
        '¿Desea eliminar el usuario?',
        QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.Yes:
            try:
                id = int(self.txtBuscarID.text())
                msgBox = QMessageBox()
                msgBox.setText(crud.eliminar(id))
                msgBox.exec_()
                self.limpiar_entradas()
                self.tblListaUsuarios.resizeColumnsToContents()
                self.tabla_usuarios()
            except (ValueError) as e:
                msgBox = QMessageBox()
                msgBox.setWindowTitle('Atención')
                msgBox.setText(f'Entrada no válida: {e.__str__()}')
                msgBox.exec_()

    def limpiar_entradas(self):
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtEdad.clear()
        self.cbxSexo.setCurrentText('-Seleccione-')
        self.txtBuscarID.clear()

    def closeEvent(self,event):
        reply = QMessageBox.question(self, "Atención", "¿Seguro quiere salir?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else: 
            event.ignore()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()