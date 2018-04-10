bl_info = {
    "name": "apaza610",
    "author": "Homar Richard Orozco Apaza",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Objeto > Propiedades",
    "description": "Extiende la clase objeto de Blender con enlaces",
    "warning": "",
    "wiki_url": "",
    "category": "mapas mentales",
    }
	
import bpy
import webbrowser
import subprocess, sys
import os

###############################################################################################################
# extender la clase base de Blender con las propiedades:  OJO: nuca mas cambiar nombres o perderas TOOOODOOOOO
###############################################################################################################
#bpy.types.Object.miFlotante = bpy.props.IntProperty(name="miFlotante", default=1, update=miFloat_cambio)
#bpy.types.Object.miBoolLINK1 = bpy.props.BoolProperty(name="linkInterno", default = False) 
bpy.types.Object.esVideo = bpy.props.BoolProperty(name="esVideo", default=False)
bpy.types.Object.enlaceDISK = bpy.props.StringProperty(name="enlaceDISK", default="")   # dentro esta maquina
bpy.types.Object.enlaceNET = bpy.props.StringProperty(name="enlaceNET", default="")     # hacia la web
bpy.types.Object.enlaceLOC = bpy.props.StringProperty(name="enlaceLOC", default="")     # dentro Blender
bpy.types.Object.tiempoINI = bpy.props.StringProperty(name="tiempoINI", default="")     # tiempo HH:MM:SS  
bpy.types.Object.tiempoFIN = bpy.props.StringProperty(name="tiempoFIN", default="")

########################################################################
# funcion de apoyo, arregla STRINGs para que funcionen en GNU/linux
########################################################################

from pathlib import Path
raizGNU ='/mnt/'                   	 						# punto de montaje de los discos en GNU
raicesDIC = {'DISCO2':'D:','DISCO3':'E:','DISCO4':'F:','DISCO5':'G:','DISCO6':'L:'}

appsGNU = {'.txt':'gedit'  ,'.odt':'libreoffice','.mp4':'vlc','.mpg':'vlc','.flv':'vlc'}
appsWIN = {'.txt':'notepad','.odt':'libreoffice','.mp4':'vlc','.mpg':'vlc','.flv':'vlc'}

estasEnWIN = os.getenv("OS") == 'Windows_NT'

def cadenaGNUWIN(direccion, tiempoINI, tiempoFIN):        	# saca cadena util para GNU
    
    cadenaPATH = Path(direccion)                			# es agnostica al OS

    #------------averiguar el programa a ser invocado--------------------------------
    extension = cadenaPATH.suffix  
        
    if estasEnWIN:
        aplicacion = appsWIN[extension]
    else:
        aplicacion = appsGNU[extension]

    #------------arreglar la direccion segun el OS-----------------------------------
    if estasEnWIN:
        nombreDISCO = direccion.split('/')[0]          # extrae de la cadena nombres de discos: DISCO2, DISCO3, etc...
        comando = direccion.replace(nombreDISCO,raicesDIC[nombreDISCO])    
        comando = comando.replace('/','\\')              
    
    else:
        comando = raizGNU + direccion
    
    #------ una coletita si es Video-------------------------------
    if tiempoINI != '':    
        temporal = tiempoINI.split(':')            
        tiempo1 = " --start-time " + str(3600*int(temporal[0]) + 60*int(temporal[1]) + int(temporal[2]))
    else:
        tiempo1 = ''
    
    if tiempoFIN !='':
        temporal = tiempoFIN.split(':')
        tiempo2 = " --stop-time " + str(3600*int(temporal[0]) + 60*int(temporal[1]) + int(temporal[2])) + " --loop"
    else:
        tiempo2 = ''
    
    #------------armar la cadena final--------------------------------
    comando =  aplicacion + ' "' + comando + '"' + tiempo1 + tiempo2

    print("_______________________________________________: " + comando)    
    return comando

#################################################################################################################
class apazaPanel(bpy.types.Panel):
    """creacion de la GUI"""
    bl_label = "Panel de objetos mejorados"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'  
    bl_context = "object"  
    
    def draw(self, context):
        objetoSLCTD = context.object        # el objeto actualmente seleccionado
        
        row = self.layout.row()
        row.label(text="use formato UNIX ej: DISCO2/cosas/SilentHill.mp4",icon='WORLD_DATA')
        
        row = self.layout.row()
        row.prop(objetoSLCTD, "enlaceDISK")
        row = self.layout.row()
        row.prop(objetoSLCTD, "enlaceNET")
    
        row = self.layout.row()

        row.operator("apaza.boton", text="en DISCO").indice=1
        row.operator("apaza.boton", text="en SCENE").indice=2
        row.operator("apaza.boton", text="en WEB").indice=3      
            
        row = self.layout.row()
        row.prop(objetoSLCTD, "enlaceLOC")

        row = self.layout.row()
        row.prop(objetoSLCTD, "tiempoINI")
        row.prop(objetoSLCTD, "tiempoFIN")
        
class apazaBoton(bpy.types.Operator):
    """el ID y el NOMBRE del operador son: """
    bl_idname = "apaza.boton"
    bl_label = " solo son botones "
    print("........................")
    
    indice = bpy.props.IntProperty()
    esVideo = bpy.props.BoolProperty()
    enlaceEXT = bpy.props.StringProperty()
    
    def execute(self, context):
        objetoSLCTD = context.object        # el objeto actualmente seleccionado
        
        #---------------------enlace en esta MAQUINA------------------
        if self.indice == 1:                
            comando = cadenaGNUWIN(objetoSLCTD.enlaceDISK, objetoSLCTD.tiempoINI, objetoSLCTD.tiempoFIN)
            os.system(comando)

            print('.....presionaste boton: ' + str(self.indice))    
    
        #---------------------enlace en SCENE de este BLEND file-------
        elif self.indice == 2:              
            objetoSLCTD.select = False
            bpy.data.objects[objetoSLCTD.enlaceLOC].select = True                    
            
        #---------------------enlade a un servidor WEB----------------
        elif self.indice == 3:
            webbrowser.open(objetoSLCTD.enlaceNET)
            print('.....presionaste boton: ' + str(self.indice))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(apazaBoton)
    bpy.utils.register_class(apazaPanel)

def unregister():
    bpy.utils.unregister_class(apazaBoton)
    bpy.utils.unregister_class(apazaPanel)

if __name__ == "__main__":
    register()