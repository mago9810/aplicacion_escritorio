
# bibliotecas para trabajar con tkinter
from tkinter import ttk
from tkinter import *
from tkinter.tix import TEXT

# coneccion con la base de datos
import sqlite3

from setuptools import Command

# creacion del objeto produc
# creamos el constructor de la clase
# aplicamos el metodo title a la propiedad wind 
# row = fila  colum = columna columnspan = colunas que se crean sin nada para espaciar el frame y se valla un poco a la derecha
# finalmente pady para que los elementos no se vean tan juntos hay padx tambien 
# este proceso se hace para configurar la posicion en la grilla y como se va a separar de otros elementos 

# 1 - creo un label o etiqueta que estara dentro del frame, tendra un texto (Text=) 
# 2 - Para crear una caja de texto usamos el metodo Entry y que este dentro del frame, para poder manipularla como una propiedad
#     posteriormente la guardo en una varible 
# 3 - Luego puedo de esta propiedad usar sus metodos como grid para ubicarla espacialmente y focus para que luego de creada se ubique el
#       cursor al abrir la aplicacion
# 4 - fianlmente ubico el input(entry) en la fila 1 col 1


class produc():
#     try:
#         mi_conexion = sqlite3.connect("data_base.sqllite3")   
#         cursor = mi_conexion.cursor()
#         cursor.execute("SELECT * FROM productos")
#         rows = cursor.fetchall()
#         for row in rows:
#             print(row)
#     except Exception as ex:
#         print(ex)

# Se ejecuta desde la estructura del objeto


    def __init__(self, window) -> None:
        self.wind = window  
        self.wind.title('APLICACION PARA MANEJO DE PRODUCTOS')

        # crear el contenedor         
        frame = LabelFrame(self.wind, text= 'Register a new  product')
        frame.grid(row = 0,column = 0, columnspan = 3, pady = 20)
        # frame.pack(pady=20)
        # Name input
        Label(frame, text = 'Name: ').grid(row = 1, column =  0)    #1
        self.name = Entry(frame) #2
        self.name.focus() #3
        self.name.grid(row = 1, column = 1)     #3
        #price
        Label(frame, text = 'Price: ').grid(row = 2, column =  0)    
        self.Price = Entry(frame) 
        self.Price.grid(row = 2, column = 1) 
        #provedor
        Label(frame, text = 'Provedor: ').grid(row = 3, column =  0)    
        self.Provedor = Entry(frame) 
        self.Provedor.grid(row = 3, column = 1)

        #boton agregar producto   command liga a el cotos con una funcion o tarea
        ttk.Button(frame,text = "Guardar producto",command = self.adicionar_productos).grid(row = 4, columnspan = 3, sticky = W + E)
        ttk.Button(frame,text = "Borrar",command = self.borrar_producto).grid(row = 6, column =   0, sticky = W + E)
        ttk.Button(frame,text = "Editar",command =self.borrar_producto).grid(row = 6, column =   1, sticky = W + E)        
        
        #Mensaje de salida de informacion
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 4,column = 0, columnspan = 2, sticky = W + E)

        # #table
            #scrollbar

        self.tree= ttk.Treeview(height = 30, columns = ("col1","col2" ))
        self.tree.grid(row =4, column = 0, columnspan = 2)

        # sb = Scrollbar(frame, orient=VERTICAL)
        # sb.pack(side=RIGHT, fill=Y)

        # self.tree.config(frame,yscrollcommand=sb.set)
        # sb.config(command=self.tree.yview)


        self.tree.place(relx = 0.1, rely = 0.12, width = 100, height = 100)
        self.tree.grid(row = 2, column = 0, columnspan = 1)

        self.tree.column("#0",width = 200, anchor = CENTER )
        self.tree.column("#1",width = 80, anchor = CENTER)
        self.tree.column("#2",width = 200, anchor = CENTER)

        self.tree.heading("#0", text = "Producto", anchor= CENTER)
        self.tree.heading("#1", text = "Precio", anchor= CENTER)
        self.tree.heading("#2", text = "Provedor", anchor= CENTER)

        #me trae los datos consultados al formulario
        self.get_products()   

    def run_query(self, query, parameters = ()):
        # print(parameters)
        mi_conexion = sqlite3.connect("data_base.sqllite3")   #creo la conexion con la base de datos
        cursor = mi_conexion.cursor()                         #Creo el cursor de la base de datos para que retorne fila a fila la informacion resultante de la consulta
        result = cursor.execute(query, parameters)  #la funcion execute me permite ejecutar las query a la DB
        # for fila in result:
        #     print(fila)
        mi_conexion.commit()   #hace permanentes o da el ok a los cambios generados en la tabla
   
        for row in result:   # recorre el resultado de la consulta genardo por rl vector 
            self.tree.insert('', 0, text = row[1], values = (row[2],row[3]))  #me va a insentar la informacion en la tabla
                                                                            #text es el nombre del objeto y el resto son las caracteristicas
                                                                            #o valores propios 

    def adicionar_productos(self):
        if self.validacion():
            query = 'INSERT INTO productos VALUES (NULL, ?, ?, ?)'
            parameters = (self.name.get(),self.Price.get(), self.Provedor.get())
            self.run_query(query,parameters)
            self.mensaje['text'] = 'producto: {}. Guardado satisfactoriamente'.format(self.name.get())
            print ('datos guardados')
            self.get_products()
            # print(self.name.get())
            # print(self.Price.get())
            # print(self.Provedor.get())
        else:
            self.mensaje['text'] = "Nombre y precio requerido"
            print("Nombre y precio requerido")

    def get_products(self):   # funcion que crea el query para la consulta a la db 
        query = 'SELECT * FROM  productos ORDER BY Name DESC '  #consulta a la base de datos
        db_rows = self.run_query(query) #envia la query a la funcion run_query y recibe el resultado
        # print(db_rows)

    def validacion(self):
        return len(self.name.get()) != 0 and len(self.Price.get()) != 0 and len(self.Provedor.get()) != 0  

    def borrar_producto(self):
        print(self.tree.item(self.tree.selection()))
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecione un item'
        return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM productos WHERE name = ?'
        self.run_query(query, (name) )
        self.mensaje['text'] =  'El elemento borrado'
        self.get_products()


        
# tk me devuelve una ventana, en este caso es la ventana principal de la aplicacion
# le enviamos a product la ventana creada 
# 3 Hasta aqui la ventana esta creada 

if __name__ =='__main__':
    window = Tk()    
    window.geometry('490x520')
    application = produc(window) 
    window.mainloop()


