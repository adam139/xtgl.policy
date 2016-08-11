#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
 
from xtgl.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedBlobImage,NamedBlobFile,NamedImage
import os
from Products.CMFPlone.utils import safe_unicode
def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
# 公路动态
        portal.invokeFactory('Folder', 'gongludongtai',
                             title=u"公路动态",description="demo productfolder")         

# 新闻中心
        portal.invokeFactory('Folder', 'xinwenzhongxin',
                             title=u"新闻中心",description="demo productfolder") 
        portal['xinwenzhongxin'].invokeFactory('Folder', 'guanligongzuodongtai',
                             title=u"管理工作动态",description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('Folder', 'shehuizuzhifengcai',
                             title=u"社会组织风采",description="demo productfolder")
        portal['xinwenzhongxin'].invokeFactory('Folder', 'jingyanjiaoliu',
                             title=u"经验交流",description="demo productfolder")        
        portal['gongludongtai'].invokeFactory('my315ok.products.productfolder', 'tupianxinwen',
                             title=u"图片新闻",description="demo productfolder")
        portal['gongludongtai']['tupianxinwen'].invokeFactory('my315ok.products.product', 'tupianxinwen1',
                             title=u"图片新闻1",description="demo productfolder")
        data = getFile('image.jpg').read()
        item = portal['gongludongtai']['tupianxinwen']['tupianxinwen1']
        item.image = NamedBlobImage(data, 'image/jpg', u'image.jpg')
        item.text = u"图片新闻1"
        
        portal['xinwenzhongxin']['guanligongzuodongtai'].invokeFactory('Document', 'guanligongzuodongtai1',
                             title=u"管理工作动态1",description="demo productfolder")
        portal['xinwenzhongxin']['jingyanjiaoliu'].invokeFactory('Document', 'jingyanjiaoliu1',
                             title=u"经验交流1",description="demo productfolder")
        portal['xinwenzhongxin']['shehuizuzhifengcai'].invokeFactory('Document', 'shehuizuzhifengcai1',
                             title=u"社会组织风采1",description="demo productfolder")                                                           

#信息公开 
        portal.invokeFactory('Folder', 'xinxigongkai',
                             title=u"信息公开",description="demo productfolder")       
        portal['xinxigongkai'].invokeFactory('Folder', 'tongzhigonggao',
                             title=u"通知公告",description="demo productfolder") 
        portal['xinxigongkai'].invokeFactory('Folder', 'zhengcefagui',
                             title=u"政策法规",description="demo productfolder")
        portal['xinxigongkai'].invokeFactory('Folder', 'xingzhengchufagonggao',
                             title=u"行政处罚公告",description="demo productfolder")
        portal['xinxigongkai']['tongzhigonggao'].invokeFactory('Document', 'guanligotongzhigonggao1',
                             title=u"通知公告1",description="demo productfolder")        
        portal['xinxigongkai']['zhengcefagui'].invokeFactory('Document', 'zhengcefagui1',
                             title=u"政策法规1",description="demo productfolder")
        portal['xinxigongkai']['xingzhengchufagonggao'].invokeFactory('Document', 'xingzhengchufagonggao',
                             title=u"行政处罚公告1",description="demo productfolder")
#查询集 
        portal.invokeFactory('Folder', 'sqls',
                             title=u"查询集",description="demo productfolder")
        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'Document',
}]
        portal['sqls'].invokeFactory('Collection', 'gongzuodongtai',
                             title=u"通知公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'jicengdongtai',
                             title=u"社会组织动态",query=query)
        portal['sqls'].invokeFactory('Collection', 'zonghexinxi',
                             title=u"工作动态",query=query)
        portal['sqls'].invokeFactory('Collection', 'tongzhigonggao',
                             title=u"互动交流",query=query)
        portal['sqls'].invokeFactory('Collection', 'gonglujianbao',
                             title=u"政策法规",query=query) 
        portal['sqls'].invokeFactory('Collection', 'zhengwugongkai',
                             title=u"服务信息",query=query) 
        portal['sqls'].invokeFactory('Collection', 'qunzhongluxianshijian',
                             title=u"行政许可公告",query=query) 
        portal['sqls'].invokeFactory('Collection', 'chaoxianchaozai',
                             title=u"年检结果公告",query=query) 
        portal['sqls'].invokeFactory('Collection', 'dangtuanjianshe',
                             title=u"查处结果公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'gongluwenhua',
                             title=u"查处结果公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'falvzhengce',
                             title=u"查处结果公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'gonglujianshe',
                             title=u"查处结果公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'gongluyanghu',
                             title=u"查处结果公告",query=query)
        portal['sqls'].invokeFactory('Collection', 'gongluzhifa',
                             title=u"查处结果公告",query=query)                                                                                                        
                                           
        self.portal = portal
    
    def test_homepage_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@index.html'        

        browser.open(obj)
 
        outstr = safe_unicode(u"政策法规1").encode('utf-8')
        
        self.assertTrue(outstr in browser.contents)          
        
   