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


def topo1():

    logger.info('Entro en topo1')


    form = SQLFORM.factory(
        Field('points', requires=IS_NOT_EMPTY()),
        Field('basis', requires=IS_NOT_EMPTY()))
    if form.process(onvalidation=form_processing_es_una_base).accepted:
        response.flash = 'form accepted'
        session.points = form.vars.points
        session.basis = form.vars.basis
        redirect(URL('topo4'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    logger.info('Salgo de topo1')
    return dict(form=form)


def form_processing_es_una_base(form):
    # Comprobamos si nos han dado una base topológica
    logger.info('Entro en form_processing_es_una_base')


    puntos1 = form.vars.points
    base1 = form.vars.basis

    if not tiene_pinta_de_puntos(puntos1):
        form.errors.points = 'Does not seems to be a list of points'
        return
    if not tiene_pinta_de_base(base1):
        form.errors.basis = 'Does not seems to be a list of open sets'
        return

    if not es_base(puntos1, base1):
        form.errors.basis = 'This set is not a topological basis'
    else:
        form.vars.basis = de_lista_a_llaves(base1)
    logger.info('Salgo de form_processing_es_una_base')
    return


def topo4():
    logger.info('Entro en topo4')
    logger.info('Salgo de topo4')
    return dict(pagina=HTML(BODY(IMG(_src=URL('prueba1')))))


def prueba1():
    logger.info('Entro en prueba1')
    response.headers['Content-Type']='image/png'
    logger.info('Salgo de prueba1')
    return my_hasse1(session.points, session.basis)









# Funciones de web2py. No tocar de momento.

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
