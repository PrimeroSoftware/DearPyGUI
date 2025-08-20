import screeninfo as scr

def getPositionX(xPosition = 100, **kwargs):
    ''' 
        Devuelve la posición en X de la ventana.
        Permitiendo ajustar la posición en múltiples monitores.

        numberDisplay : Si se coloca esta parametro, se utilizara el ancho del monitor correspondiente.
    '''
    display = scr.get_monitors()
    if len(display) > 1:
        if 'numberDisplay' in kwargs:
            return display[kwargs['numberDisplay']].width + xPosition
        else:
            return display[1].width + xPosition
    return xPosition