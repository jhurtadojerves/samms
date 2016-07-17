# -*- coding: utf-8 -*-

from suds.client import Client
from suds.sax.element import Element
import metodos

def infoGeneral():
    #Definimos URLs de Acceso a los Webservices
    urlGeneral = 'http://academico.espoch.edu.ec/OAS_Interop/Infogeneral.wsdl'
    clienteGeneral = Client(urlGeneral)
    #Definimos el nombre de usuario
    user = Element('acad:username').setText('webmail')

    #Definimos la contraseña
    pwd = Element('acad:password').setText('webmail')
    #Creamos el elemento padre, y el espacio de nombres
    reqsoapheader = Element('acad:credentials', ns=['acad','http://academico.espoch.edu.ec/'])
    #agregamos usuario y contraseña al padre
    reqsoapheader.children = [user, pwd]
    clienteGeneral.set_options(soapheaders=reqsoapheader)
    return clienteGeneral

#Definimos URLs de Acceso a los Webservices
def infoCarrera():
    #Definimos URLs de Acceso a los Webservices
    urlCarrera = 'http://academico.espoch.edu.ec/OAS_Interop/Infocarrera.wsdl'
    #Creamos el clientes
    clienteCarrera = Client(urlCarrera)
    #Definimos el nombre de usuario
    user = Element('acad:username').setText('webmail')
    #Definimos la contraseña
    pwd = Element('acad:password').setText('webmail')
    #Creamos el elemento padre, y el espacio de nombres
    reqsoapheader = Element('acad:credentials', ns=['acad','http://academico.espoch.edu.ec/'])
    #agregamos usuario y contraseña al padre
    reqsoapheader.children = [user, pwd]
    #Seteamos los soapheaders con las credenciales de login
    clienteCarrera.set_options(soapheaders=reqsoapheader)
    return clienteCarrera





