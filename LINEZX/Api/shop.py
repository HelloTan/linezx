# -*- coding: utf-8 -*-
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from akad import ShopService
from akad.ttypes import *

class Shop(Config):
    client = None

    def __init__(self, authToken):
        Config.__init__(self)
        self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN, None, self.LINE_API_QUERY_PATH_FIR)
        self.transport.path = self.LINE_AUTH_QUERY_PATH
        self.transport.setCustomHeaders({
            "X-Line-Application" : self.APP_NAME,
            "User-Agent" : self.USER_AGENT,
            "X-Line-Access": authToken
        })
        self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
        self.client = ShopService.Client(self.protocol)
        self.transport.path = self.LINE_SHOP_QUERY_PATH
        self.transport.open()

    def getProduct(self, packageID, language='ID', country='ID'):
        return self.client.getProduct(packageID, language, country)
    
    def getActivePurchases(self, start, size, language='ID', country='ID'):
        return self.client.getNewlyReleasedPackages(start, size, language, country)

    def getDownloads(self, start=0, size=1000, language='ID', country='ID'):
        return self.client.getDownloads(start, size, language, country)

    def getCoinProducts(self, appStoreCode, country="ID", language="ID"):
        return self.client.getCoinProducts(appStoreCode, country, language)

    def getEventPackages(self, start, size, language='ID', country='ID'):
        return self.client.getEventPackages(start, size, language, country)

    def getPopularPackages(self, start, size, language='ID', country='ID'):
        return self.client.getPopularPackages(start, size, language, country)

    def notifyDownloaded(self, packageId, language='ID'):
        return self.client.notifyDownloaded(packageId, language)
