# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################




def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to topolab.org")
    return dict(message=T('Estamos en la versión 13'))


from modulo53 import *





def topo1():

    form1 = FORM(INPUT(_name='entrada1', requires=IS_NOT_EMPTY()),
                 INPUT(_name='entrada2', requires=IS_NOT_EMPTY()),
                 INPUT(_type='submit'))
    if form1.process().accepted:
        session.entrada1 = [form1.vars.entrada1, form1.vars.entrada2]
        print session.entrada1
        exec 'puntos = ' + session.entrada1[0]
        exec 'base_min = ' + session.entrada1[1]
        print 'le paso = ', puntos, ' y ', base_min
        print type(puntos)
        figura = pinta_hasse_diagrama(puntos, base_min)
        redirect(URL('topo4'))
    return dict(form1=form1)

# def topo1():
#     form1 = FORM(INPUT(_name='entrada1', requires=IS_NOT_EMPTY()), INPUT(_type='submit'))
#     if form1.process().accepted:
#         session.entrada1 = form1.vars.entrada1
#
#         redirect(URL('topo3'))
#     return dict(form1=form1)

# Los datos entre funciones se pasan como variables de session
# En este caso se está pasando session.entrada1



def topo3():
    salida1 = session.entrada1
    html_salida1 = H2(salida1)
    return dict(html_salida1=html_salida1)

def topo4():
    return HTML(BODY(
        IMG(_src=URL('prueba1'))))

def prueba1():
    response.headers['Content-Type']='image/png'
    return my_hasse1()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
