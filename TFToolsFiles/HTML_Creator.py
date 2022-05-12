from yattag import Doc, indent
from Error import *

def createHTML(errorDict):

    doc, tag, text, line = Doc().ttl()

    with tag('style'):
        doc.asis('colorRed {color: red;}')
        doc.asis('colorGreen {color: green;}')
        doc.asis('mapa {color: orange;}')
        doc.asis('body {background: #191919; color: #FAFAFA}')
        doc.asis('divErrores {font-family: courier;}')

    with tag('h1'):
        if(len(errorDict)):
            line('colorRed', 'Se encontraron los siguientes errores:')
        else:
            line('colorGreen', 'No se encontaron errores. Nice!')
    with tag("divErrores"):
        for key, value in errorDict.items():
            with tag('h2'):
                line(str(key), str(key)+":")  # Enemigos:
            with tag('ul'):
                for errorInfo in value:  # Cada error
                    with tag(str(key)):
                        with tag('li'):
                            text(str(errorInfo.errCode), " en ", errorInfo.file, " : ", errorInfo.message)

    file = open('newsletter.html', 'w')

    file.write(indent(doc.getvalue()))

    print(doc.getvalue())

    file.close()

E = Error(ERRCODE.ENEMY_NAME_DUPLICATED, "FILE.PNG", "HOLA")

errDict = {"enemigos": [E],
            "mapa": [E,E]}

createHTML(errDict)
