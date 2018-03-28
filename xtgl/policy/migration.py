# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
import os
import re
import datetime
from cStringIO import StringIO
from PIL import Image
from plone.app.contenttypes.interfaces import IFolder
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.interfaces import IImage
from my315ok.products.product import Iproduct
from bs4 import BeautifulSoup 


id = set()
save_path = "/home/plone/exports"
created = []
def cropText(text, length):
        """Crop text on a word boundary
        """
        if not length:
            return text
        converted = False
        if not isinstance(text, unicode):
            text = utils.safe_unicode(text)
            converted = True
        if len(text) > length:
            text = text[:length]
            l = text.rfind(' ')
            if l > length / 2:
                text = text[:l + 1]
        if converted:
            # encode back from unicode
            text = text.encode('utf-8')
        return text
def mkdirs(context):
    "in order to the origin site's directory structure,build directory tree in file system"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IFolder.__identifier__,"sort_on":"created","sort_order":"reverse"}
    bns = pc(query)
#     bns = filter(isExisted,bns)
    finished = map(mkdir,bns)

def isExisted(bn):
    path = bn.getPath()
    if path in created:
        return True
    else:
        created.append(path)
        return False
def mkdir(bn):
    "create dir in filesystem"
    path = bn.getPath()
    path= "%s/%s" % (save_path,path)
    try:
        os.mkdirs(path)
    except:
        pass
## start export contents
def export_document(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IDocument.__identifier__,"sort_on":"created","sort_order":"reverse"}
    bns = pc(query)
#     bns = filter(nashuiren_is_repeat,bns)
    finished = map(write_html,bns) 

    
def write_html(brain):
    template = """
    <!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-cn" xml:lang="zh-cn">
  <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>%s</title>
    <link rel="stylesheet" href="../xtgl/css/bootstrap336.min.css" /> 
    <link href="../xtgl/css/custom.minv7.css" rel="stylesheet" />
    </head>
    <body>
    <div class="container">
    <div class="row">
    <div class="col-xs-12 col-sm-12">
    <article id="content">
    <header>    
    <h1 class="text-center">%s</h1>
    </header>
    <section id="content-core">
    <div id="parent-fieldname-text">%s
    </div>
    </section>
    </article>
    </div>
    </div>
    <div>
    </body>
    </html>
    """
    
#     filename = brain.id
    title = brain.Title
    try:
        richtext = brain.getObject().text.output
    except:
        richtext = brain.getObject().text
    output = template % (title,title,richtext)
    output = BeautifulSoup(output)
    srcs = output.find_all(src=re.compile("^http://localhost:8080/xtgl/"))
    for src in srcs:
        src['src'] = "../xtgl/images/%s" % src['src'].split('/')[-1]
    
#     import pdb
#     pdb.set_trace()
    output = output.prettify()
    if isinstance(output, unicode):
        output = output.encode('utf-8')
    
    bname = cropText(title,16)
    filename = "/home/plone/xtgl/%s.html" % bname
    with open(filename,'w') as outfile:
        outfile.write(output)

## end export contents
def export_image(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IImage.__identifier__}
    bns = pc(query)
#     import pdb
#     pdb.set_trace()
#     bns = filter(nashuiren_is_repeat,bns)
    finished = map(image2fs,bns)

def image2fs(brain):

    filename = brain.id
    title = brain.Title
    obj = brain.getObject()

#     imgsubstr = "http://localhost:8080/xtgl/gongludongtai/redianxinwen/qingsanba-xiangtanshigonglujuzuzhijubandengshanbisai/@@images/"
#     newstr = "../images/"
#     if imgsubstr in richtext:
#         richtext.replace(imgsubstr,newstr)
    image = obj.image
    imgdata = image.data
#     import pdb
#     pdb.set_trace()    
    # image data
    virf = StringIO(imgdata)
    imgobj = Image.open(virf)
#     imgtype = image.contentType
    imgname = image.filename
#     suffix = imgname[-4:]
#     bname = imgname[:-4]
#     bname = cropText(bname,16)
#     imgname = "%s%s" % (bname,suffix) 
    if "." not in filename:
        filename = imgname
    imgfilename = "/home/plone/xtgl/images/%s" % filename
#     imgsrc = "../xtgl/images/%s" % imgname
    try:
        imgobj.save(imgfilename)
        imgobj.close()
    except:
        print imgfilename
        pass
    
 

def export_product(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Iproduct.__identifier__,"path":"/xtgl/gongludongtai/redianxinwen"}
    bns = pc(query)
#     import pdb
#     pdb.set_trace()
#     bns = filter(nashuiren_is_repeat,bns)
    finished = map(product2html,bns) 

def product2html(brain):
    template = """
    <!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-cn" xml:lang="zh-cn">
  <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>%s</title>
    <link rel="stylesheet" href="../xtgl/css/bootstrap336.min.css" /> 
    <link href="../xtgl/css/custom.minv7.css" rel="stylesheet" />
    </head>
    <body>
    <div class="container">
    <div class="row">
    <div class="col-xs-12 col-sm-12">
    <article id="content">
    <header>    
    <h1 class="text-center">%s</h1>
    </header>
    <section id="content-core">
    <div class="mainphoto">
    <img src="%s" alt="%s" />
    </div>
    <div class="details">%s
    </div>
    </section>
    </article>
    </div>
    </div>
    <div>
    </body>
    </html>
    """
#     filename = brain.id
    title = brain.Title
    obj = brain.getObject()
    try:
        richtext = obj.text.output
    except:
        richtext = obj.text
#     imgsubstr = "http://localhost:8080/xtgl/gongludongtai/redianxinwen/qingsanba-xiangtanshigonglujuzuzhijubandengshanbisai/@@images/"
#     newstr = "../images/"
#     if imgsubstr in richtext:
#         richtext.replace(imgsubstr,newstr)
    image = obj.image
    imgdata = image.data
#     import pdb
#     pdb.set_trace()    
    # image data
    virf = StringIO(imgdata)
    imgobj = Image.open(virf)
    imgtype = image.contentType
    imgname = image.filename
    suffix = imgname[-4:]
    bname = imgname[:-4]
    bname = cropText(bname,16)
    imgname = "%s%s" % (bname,suffix) 
    
    imgfilename = "/home/plone/xtgl/images/%s" % imgname
    imgsrc = "../xtgl/images/%s" % imgname
    imgobj.save(imgfilename)
    
    output = template % (title,title,imgsrc,title,richtext)

    if isinstance(output, unicode):
        output = output.encode('utf-8')
    
    filename = "/home/plone/xtgl/%s.html" % title
    with open(filename,'w') as outfile:
        outfile.write(output)  
    


