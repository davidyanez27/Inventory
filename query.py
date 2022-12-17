
import sqlite3
from tkinter import *
from interfaz import *



class Query:
    
    db_name= '/Users/moisescampos/Desktop/Inventario/database.db'

    def run_query (self, query, parameters = ()):
        with sqlite3.connect (self.db_name) as conn:
            cursor1 = conn.cursor ()
            result= cursor1.execute(query, parameters)
            conn.commit ()
        return result
    
        
     
 

    

    
 




       
 
        
