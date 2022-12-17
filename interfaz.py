

from tkinter import *
from tkinter import ttk
from query import *


class Grafico:

    #Nombres
    enunciado= ["serial", "producto", "marca", "precio", "estado", "ubicacion", "observacion"]
    
    #Ventana
    window = Tk () 
    wind=window
    wind.title('INVENTARIO C&Z') 


    #Container for add product    
    frame= LabelFrame(wind, text= 'Registro de producto')
    frame.grid(row=0, column=0, columnspan=3, pady=20)

    #output messages
    message = Label (text= '', fg='red')
    message.grid (row=3, column=0, columnspan=2, sticky=W+E)

    #table
    tree =ttk.Treeview (height=20, columns = ('#0','#1','#2','#3','#4','#5'))
    tree.grid (row=5, column=0, columnspan=2)
    tree.heading ('#0', text = 'SERIAL', anchor= CENTER)
    tree.heading ('#1', text= 'PRODUCTO', anchor=CENTER)
    tree.heading ('#2', text = 'MARCA', anchor= CENTER)
    tree.heading ('#3', text= 'PRECIO', anchor= CENTER)
    tree.heading ('#4', text = 'ESTADO', anchor=CENTER)
    tree.heading ('#5', text= 'UBICACION', anchor=CENTER)
    tree.heading ('#6', text= 'OBSERVACION', anchor=CENTER)

    #variable for serial validation
    output=[]
    bolean=False
    preciobolean=False
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #Query
    db_name= '/Users/moisescampos/Desktop/Python/Inventario/database.db'
    query = 'SELECT * FROM product ORDER BY precio ASC'

    def run_query (self, query, parameters = ()):
        with sqlite3.connect (self.db_name) as conn:
            cursor1 = conn.cursor ()
            result= cursor1.execute(query, parameters)
            conn.commit ()
        return result
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    def __init__(self):
        
        #show values
        for i in range(7):

            Label (Grafico.frame, text= Grafico.enunciado [i]).grid (row=i, column=0)
        
 
        self. entradas()
        self.get_products ()

        #Buttons
        ttk.Button(Grafico.frame, text ='Guardar', command=self.add_product).grid(row =8, columnspan= 2)
        ttk.Button (text = 'BORRAR', command=self.delete_product).grid ( row=21, column=0, sticky=W+E)
        ttk.Button (text = 'EDITAR', command= self.edit_product).grid ( row=21, column=1, sticky=W+E)
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #Inputs
    def entradas (self):
        
        # Input
        self.serial=Entry (Grafico.frame)
        self.serial.focus ()
        self.serial.grid (row=0, column=1)

        self.producto=Entry (Grafico.frame)
        self.producto.grid (row=1, column=1)
  
        self.marca=Entry (Grafico.frame)
        self.marca.grid (row=2, column=1)
   
        self.precio=Entry (Grafico.frame)
        self.precio.grid (row=3, column=1)
  
        self.estado_selecionado= StringVar ()
        self.estado_selecionado.set ("Nuevo")
        options = ("Nuevo","Usado","Mal Estado", "Semi Nuevo")
        self.estado = OptionMenu (Grafico.frame, self.estado_selecionado, *options)
        self.estado.grid (row=4, column=1,sticky=W+E)
 
        self.ubicacion=Entry (Grafico.frame)
        self.ubicacion.grid (row=5, column=1)
 
        self.observacion=Entry (Grafico.frame)
        self.observacion.grid (row=6, column=1)
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #clean the label
    def clean_label (self):
        self.serial.delete (0,END)
        self.producto.delete (0,END)
        self.marca.delete (0,END)
        self.precio.delete (0,END)
        self.estado_selecionado.set("Nuevo")
        self.ubicacion.delete (0,END)
        self.observacion.delete (0,END)
    #----------------------------------------------------------------------------------------------------#               
   
    #----------------------------------------------------------------------------------------------------#
    #making the call  
    def get_products (self):

        #cleaning table
        records=Grafico.tree.get_children ()
        for element in records:
            Grafico.tree.delete(element)
        
        #Get the data
        query = 'SELECT * FROM product ORDER BY precio ASC'
        db_rows= self.run_query(query)

        #filling table
        for row in db_rows:    
            Grafico.tree.insert ('',0,text=row[1],values= (row[2], row[3], row[4],row[5],row[6], row[7]))
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#  
    #Validation for add product
    def validation(self):
        return len (self.serial.get ()) !=0 and len(self.producto.get())!=0 and len (self.precio.get ()) !=0 and len (self.ubicacion.get ()) !=0 and len(self.observacion.get ())!=0
    #----------------------------------------------------------------------------------------------------#               
    
    #----------------------------------------------------------------------------------------------------#  
    def serial_validation (self):
    # making the query for the serial data
        self.message ['text']=''
        query = 'SELECT serial FROM product'
        db_rows= self.run_query(query)
        serials=[]
                
    #insert the serials into a array
        for i in db_rows:
            serials.append(i)
    
    #making the tuple into a string
        values = ','.join([str(i) for i in serials])
        characters = "( )"

        for x in range(len(characters)):
            values = values.replace(characters[x],"")

    #depurate the string
        values=values.replace(",,"," ")
        values=values.replace(",","")
        values=values.replace("'","")
        Grafico.output=values.split(' ') 
        #print (type(Grafico.output))

       #change the bolean value 
        if self.serial.get() in Grafico.output:
            Grafico.bolean=True
    #----------------------------------------------------------------------------------------------------#  

    #----------------------------------------------------------------------------------------------------#
    #Add product
    def add_product(self):
        if self.validation (): 
            if  self.precio.get().isnumeric():
                    
                self.serial_validation()


                #if the serial are repeat
                if (Grafico.bolean==True):
                    self.message ['text']= 'Serial repetido, porfavor ingrese uno valido'
                    Grafico.bolean=False
                    
                else: 
                    query = 'INSERT INTO product VALUES (NULL,? ,?, ?, ?, ?, ?,?)'
                    parameters = (self.serial.get(), self.producto.get(), self.marca.get(), self.precio.get(),self.estado_selecionado.get(),self.ubicacion.get(), self.observacion.get())
                    self.run_query (query, parameters)
                    self.get_products()
                    self.message ['text']= 'El producto {} ha sido agregado satifactoriamente'.format (self.producto.get())
                    self.clean_label ()
            else:
                self.message ['text']= 'Precio invalido, ingrese solo numeros'
           
        # if the data are incomplete
        else:

            self.message ['text']= 'Hace falta datos para agregar el producto'

        self.get_products()
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #Delte a product
    def delete_product (self):

        self.message ['text']=''
        try:
            Grafico.tree.item (Grafico.tree.selection ()) ['values'] [0]
            
        except IndexError as e:
            Grafico.message ['text']= 'Porfavor seleccione un producto'
            return
        
     
        Grafico.message ['text']=''
        serial= Grafico.tree.item (Grafico.tree.selection ()) ['text'] 
        name=Grafico.tree.item (Grafico.tree.selection ()) ['values'] [0]
        query= 'DELETE FROM product WHERE serial= ?'
        self.run_query (query, (serial,))
        self.message ['text']='El siguiente producto {} ha sido eliminado'.format (name)  

        print (name)
        self.get_products ()

    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #Query for Edit a Product
    
    def edit_records (self, new_serial, old_serial, new_name, new_marca, new_precio, nestado_selecionado,  new_ubicacion, new_observacion,precio_bolean ):
        if new_serial== "" and new_name=="" and new_marca=="" and new_precio=="" and nestado_selecionado=="Nuevo" and new_ubicacion=="" and new_observacion=="":
            self.edit_wind.destroy()
            
        else:
            #if the serial are repeat
            self.serial_validation()
            
            if (new_serial in Grafico.output):
                self.message ['text']= 'Serial repetido, porfavor ingrese uno valido'
        
                    
            else: 

                if precio_bolean==True or new_precio=="":
                #Olds and New Inputs
                    old_serial= self.tree.item (self.tree.selection ()) ['text'] 

                    #Taking the old data
                    old_data=[old_serial]
                    for i in range (6):
                        old_data.append(self.tree.item (self.tree.selection ()) ['values'] [i])

                    #Making the new data array
                    new_data=[new_serial,new_name, new_marca, new_precio, nestado_selecionado,  new_ubicacion, new_observacion]
                    for i in range (7):
                        if new_data[i]== "":
                            new_data[i]=old_data[i]
                        
                    new_data.append(old_serial)
                        
                    #This is the query
                    query = 'UPDATE product SET serial = ?, producto = ?, marca = ?, precio = ?, estado = ?, ubicacion = ?, observacion = ? WHERE serial = ?'
                            
                    parameters=new_data
                            
                    self.run_query(query, parameters)
                    self.edit_wind.destroy()
                    old_name=Grafico.tree.item (Grafico.tree.selection ()) ['values'] [0]
                    self.message['text'] = 'El producto {} ha sido actualizado satisfactoriamente'.format (old_name)
                    self.get_products()
                else:
                    self.message ['text']= 'Precio invalido, ingrese solo numeros'
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    def edit_product(self):

        self.message ['text']=''
        try:
            self.tree.item (self.tree.selection ()) ['values'] [0]       
        except IndexError as e:
            self.message ['text']= 'Porfavor seleccione un producto'
            return

        #Making the new window
        self.edit_wind = Toplevel()
        self.edit_wind.title= 'Edit Product'

        #Olds and New Inputs
        old_serial= self.tree.item (self.tree.selection ()) ['text'] 

        #Taking the old data
        old_data=[old_serial]
        for i in range (6):
            old_data.append(self.tree.item (self.tree.selection ()) ['values'] [i])
  
        #Show values
        for i in range(0,7):
            Label (self.edit_wind, text= Grafico.enunciado [i]).grid (row=i, column=0)
            Label (self.edit_wind, text= old_data [i]).grid (row=i, column=2)
        
        #New Data
            Label (self.edit_wind, text= "Nuevo "+Grafico.enunciado [i]).grid (row=i, column=3)

        #Entry for the new data
        new_serial=Entry (self.edit_wind)
        new_serial.grid(row=0,column=4)
        
        new_name=Entry (self.edit_wind)
        new_name.grid(row=1,column=4)
        
        new_marca=Entry (self.edit_wind)
        new_marca.grid(row=2,column=4)

        new_precio=Entry (self.edit_wind)
        new_precio.grid(row=3,column=4)

        if new_precio.get().isnumeric():
            Grafico.preciobolean=True

        self.nuevoestado_selecionado= StringVar ()
        self.nuevoestado_selecionado.set ("Nuevo")
        options = ("Nuevo","Usado","Mal Estado", "Reparado")
        nuevoestado_selecionado = OptionMenu (self.edit_wind, self.nuevoestado_selecionado, *options)
        nuevoestado_selecionado.grid (row=4, column=4, sticky=W+E)
        
        new_ubicacion=Entry (self.edit_wind)
        new_ubicacion.grid(row=5,column=4)

        new_observacion=Entry (self.edit_wind)
        new_observacion.grid(row=6,column=4)
        
        #Validation for edit product
        Button(self.edit_wind, text='ACTUALIZAR',command=lambda: self.edit_records(new_serial.get(),old_serial, new_name.get(), new_marca.get(),new_precio.get(),self.nuevoestado_selecionado.get(),  new_ubicacion.get(), new_observacion.get(),new_precio.get().isnumeric())).grid(row=10, column=2, sticky=W)        
    #----------------------------------------------------------------------------------------------------#               
     
    #----------------------------------------------------------------------------------------------------#
    #making the search
    #def serial_validation(self):
  
    
        #query = ' SELECT * FROM tasks WHERE priority=? '

          
   
    #----------------------------------------------------------------------------------------------------#



    
