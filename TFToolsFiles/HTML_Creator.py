from yattag import Doc, indent

def createHTML(errorList):

    doc, tag, text, line = Doc().ttl()

    with tag('style'):
        doc.asis('enemies {color: red;}')
        doc.asis('mapa {color: orange;}')
        doc.asis('fuenteChula {font-family: courier}')

    with tag('h1'):
        text("Errores")
    with tag("fuenteChula"):
        with tag('enemies'):
            with tag('h2'):
                text('Enemigos:')
            with tag('body'):                    
                text('Error enemigo')

        with tag('mapa'):
            with tag('h2'):
                text('Mapa:')
            with tag('body'):                    
                text('Error mapa')

        with tag('direcciones'):
            with tag('h2'):
                text('Dir:')
            with tag('ul'):                    
                for e in errorList:
                    line('li',e)

    file = open('newsletter.html','w')

    file.write(indent(doc.getvalue()))

    print(doc.getvalue())

    file.close()

eList = ["topo", "alba", "adre", "pipo", "aaaa"]

createHTML(eList)