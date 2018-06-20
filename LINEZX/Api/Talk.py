# -*- coding: utf-8 -*-
import json, requests, rsa

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from akad import TalkService, AuthService
from akad.ttypes import *
con = Config()
_session = requests.session()

def getJson(url, headers=None):
    if headers is None:
        return json.loads(_session.get(url).text)
    else:
        return json.loads(_session.get(url, headers=headers).text)

def defaultCallback(str):
    print(str)

def createTransport(path=None, update_headers=None, service=None):
    Headers = {
        'User-Agent': con.USER_AGENT,
        'X-Line-Application': con.APP_NAME,
        "x-lal": "in_ID",
    }
    Headers.update({"x-lpqs" : path})
    if(update_headers is not None):
        Headers.update(update_headers)
    transport = THttpClient.THttpClient(con.LINE_HOST_DOMAIN + path)
    transport.setCustomHeaders(Headers)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = service(protocol)
    return client

class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def QrUrl(self, url, showQr=True):
        self.callback(url)
        
    def PinVerified(self, pin):
        self.callback("Masukan kode pin berikut '" + pin + "' di smartphone anda")

    def default(self, str):
        self.callback(str)

class Talk(Config):
  client = None


  authToken = None
  cert = None

  def __init__(self):
    Config.__init__(self)
    self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN,None, self.LINE_API_QUERY_PATH_FIR)
    self.transport.setCustomHeaders({
      "X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT})
    self.transport.open()
    self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
    self.client = TalkService.Client(self.protocol)
    
  def ready(self,moji):
    r = moji.split(",")
    self.cert = r[0]
    self.authToken = r[1]
    self.transport.setCustomHeaders({
      "X-Line-Application" : self.APP_NAME,
      "User-Agent" : self.USER_AGENT,
      "X-Line-Access" : r[1]
      })
    self.transport.path = self.LINE_API_QUERY_PATH_FIR

  def TokenLogin(self, authToken):
    headers = {"X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT,"X-Line-Access" : authToken}
    self.transport.setCustomHeaders(headers)
    self.authToken = authToken
    self.headers = headers
    self.transport.path = self.LINE_API_QUERY_PATH_FIR
    
  def login(self, mail, passwd, cert=None):
    self.userid = mail
    self.password = passwd
    self.certificate = cert

    self.transport.path = self.LINE_AUTH_QUERY_PATH
    r = self.client.getRSAKeyInfo(IdentityProvider.LINE)

    data = (chr(len(r.sessionKey)) + r.sessionKey
            + chr(len(self.userid)) + self.userid
            + chr(len(self.password)) + self.password)

    pub = rsa.PublicKey(int(r.nvalue, 16), int(r.evalue, 16))
    cipher = rsa.encrypt(data, pub).encode('hex')

    login_request = LoginRequest()
    login_request.type = 0
    login_request.identityProvider = IdentityProvider.LINE
    login_request.identifier = r.keynm
    login_request.password = cipher
    login_request.keepLoggedIn = 1
    login_request.accessLocation = self.IP_ADDR
    login_request.systemName = self.SYSTEM_NAME
    login_request.certificate = self.certificate
    login_request.e2eeVersion = 1
    
    client = createTransport(self.LINE_LOGIN_QUERY_PATH, None, AuthService.Client)

    self.transport.path = self.LINE_LOGIN_QUERY_PATH
    r = client.loginZ(login_request)

    if r.type == LoginResultType.SUCCESS:
        self.TokenLogin(r.authToken)
        print(r.certificate)
    elif r.type == LoginResultType.REQUIRE_QRCODE:
        pass
    elif r.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
        tos = LineCallback(defaultCallback)
        tos.PinVerified(r.pinCode)
        verifier = _session.get(url=self.LINE_HOST_DOMAIN + self.LINE_CERTIFICATE_PATH, headers={"X-Line-Access": r.verifier}).json()["result"]["verifier"].encode("utf-8")
        verifier_request = LoginRequest()
        verifier_request.type = 1
        verifier_request.verifier = verifier
        verifier_request.e2eeVersion = 1
        r = client.loginZ(verifier_request)
        #self.TokenLogin(r.authToken)
        #print("Your certificate " + r.certificate)
        self.ready('{},{}'.format(r.certificate, r.authToken))
    else:
        print("Eror {}".format(r.type))

  def qrLogin(self,keepLoggedIn=True, systemName=None):
        if systemName is None:
            systemName=self.SYSTEM_NAME
        client = createTransport(self.LINE_AUTH_QUERY_PATH, None, TalkService.Client)

        qr = client.getAuthQrcode(keepLoggedIn, systemName)
        uri = "line://au/q/" + qr.verifier
        clb = LineCallback(defaultCallback)
        clb.QrUrl(uri, 1)
        header = {
                'User-Agent': self.USER_AGENT,
                'X-Line-Application': self.APP_NAME,
                "x-lal" : "in_ID",
                "x-lpqs" : self.LINE_LOGIN_QUERY_PATH,
                'X-Line-Access': qr.verifier
        }
        getAccessKey = getJson(self.LINE_HOST_DOMAIN + self.LINE_CERTIFICATE_PATH, header)

        client = createTransport(self.LINE_LOGIN_QUERY_PATH, None, AuthService.Client)
        req = LoginRequest()
        req.type = 1
        req.verifier = qr.verifier
        req.e2eeVersion = 1
        res = client.loginZ(req)
        client = createTransport(self.LINE_API_QUERY_PATH_FIR, {'X-Line-Access':res.authToken}, TalkService.Client)
        self.TokenLogin(res.authToken)
        return res.authToken
    

  def __crypt(self, mail, passwd, RSA):
    message = (chr(len(RSA.sessionKey)) + RSA.sessionKey +
                   chr(len(mail)) + mail +
                   chr(len(passwd)) + passwd).encode('utf-8')

    pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
    crypto = rsa.encrypt(message, pub_key).encode('hex')

    return crypto
