# -*- coding: utf-8 -*-
from akad.ttypes import ApplicationType
import re

class Config():
    LINE_HOST_DOMAIN                = 'https://legy-jp.line.naver.jp'
    LINE_OBS_DOMAIN                 = 'https://obs-sg.line-apps.com'
    LINE_TIMELINE_API               = 'https://legy-jp.line.naver.jp/mh/api'
    LINE_TIMELINE_MH                = 'https://legy-jp.line.naver.jp/mh'

    LINE_LOGIN_QUERY_PATH           = '/api/v4p/rs'
    LINE_AUTH_QUERY_PATH            = '/api/v4/TalkService.do'

    LINE_API_QUERY_PATH_FIR         = '/S4'
    LINE_POLL_QUERY_PATH_FIR        = '/P4'
    LINE_API_QUERY_PATH_SEC         = '/F4'
    LINE_POLL_QUERY_PATH_SEC        = '/E4'
    LINE_POLL_QUERY_PATH_THI        = '/H4'
    LINE_NORMAL_POLL_QUERY_PATH     = '/NP4'
    LINE_COMPACT_MESSAGE_QUERY_PATH = '/C5'
    LINE_CALL_QUERY_PATH            = '/V4'
    LINE_CERTIFICATE_PATH           = '/Q'
    LINE_CHAN_QUERY_PATH            = '/CH4'
    LINE_SQUARE_QUERY_PATH          = '/SQS1'
    LINE_SHOP_QUERY_PATH            = '/SHOP4'

    CHANNEL_ID = {
        'LINE_TIMELINE': '1341209950',
        'LINE_WEBTOON': '1401600689',
        'LINE_TODAY': '1518712866',
        'LINE_STORE': '1376922440',
        'LINE_MUSIC': '1381425814',
        'LINE_SERVICES': '1459630796'
    }

    APP_TYPE    = ApplicationType.WINPHONE
    APP_VER     = '8.8.1'
    CARRIER     = '51089, 1-0'
    SYSTEM_NAME = 'WaifuBOT' # I not like wibu, you know -_-
    SYSTEM_VER  = '11.2.5'
    IP_ADDR     = '8.8.8.8'
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self):
        self.APP_NAME = '%s\t%s\t%s\t%s' % (self.APP_TYPE, self.APP_VER, self.SYSTEM_NAME, self.SYSTEM_VER)
        self.USER_AGENT = 'LineBot/%s' % self.APP_VER
