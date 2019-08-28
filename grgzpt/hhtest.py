# -*- coding:utf-8 -*-
import requests
import string
import HttpLibrary
import urllib3
import struct
import socket
import uuid
import random
import os
import re
import time
import urllib
import json
import base64
import logging
import HttpLibrary
from robot.libraries import BuiltIn
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# session=requests.Session()
start = time.clock()
class hhtest(object):
    def hhpost(self, url, body):
        print type(body)
        print url
        headers = {}
        headers['content-type'] = 'application/json'
        headers['Accept'] = 'application/json'
        body = body.encode('utf-8')
        resp = requests.post(url, body, headers, verify=False)
        print "response text:" + resp.text.encode('utf-8')
        print resp.status_code
        return resp

    def hhget(self, uri):
        print "uri:" + str(uri)
        headers = {}
        headers['content-type'] = 'text/html'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml'
        print headers
        resp = requests.get(uri, headers, verify=False)
        print "response text:" + resp.text.encode('utf-8')
        print resp.status_code
        str1 = resp.text.encode('utf-8').replace('\xc3\xaf\xc2\xbb\xc2\xbf\xc3\xaf\xc2\xbb\xc2\xbf', '')
        print str1
        return str1

    def hhgethead(self, url, ip8088):
        body = {
            'username': 'admin',
            'password': 'e10adc3949ba59abbe56e057f20f883e'
        }
        rq = requests.session()
        purl = url + '/sys/user/loginSubmit'
        headers1 = {}
        headers1['content-type'] = 'application/json'
        headers1['Origin'] = ip8088
        headers1['Referer'] = ip8088+'/'
        headers1['Accept'] = 'application/json'
        #r = requests.session().post(purl, data=body, headers=headers1, verify=False)
        print purl
        print body
        bodyjson = json.dumps(body)
        print bodyjson
        r = rq.post(url=purl, data=bodyjson, headers=headers1)
        print r
        hjson = json.loads(r.text)
        print hjson
        sessionId1 = hjson['sessionId']
        print sessionId1
        #print str(r.cookies)
        res = rq.get(ip8088)
        print res
        header = res.request.headers
        # header = {}
        header['content-type'] = 'application/json'
        header['Accept'] = 'application/json, text/plain, */*'
        header['Origin'] = ip8088
        header['Referer'] = ip8088+'/'
        header['token'] = sessionId1
        return header

    def pic64(self, pic):
        dir = pic
        print dir
        f = open(dir, 'rb')
        ls_f = base64.b64encode(f.read())
        f.close()
        return ls_f

    def paramjson(self, jsonData):
        body = json.dumps(jsonData, ensure_ascii=False)
        print(type(body))
        body = body.encode('utf-8')
        return body

    def queryCasesByPolygon(self, url, header):
        #查询
        print header
        urlfax = "/lawcase/police/queryCasesByPolygon"
        fullurl = url + urlfax
        body = {}
        body["polygon"] = "112.92147299438474:28.215918666445262,113.00764700561524:28.215918666445262,113.00764700561524:28.181538568323404,112.92147299438474:28.181538568323404"
        # body["extInfo"] = "1122"
        bodyjson = json.dumps(body)
        print fullurl
        print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        bodyjson1 = "polygon=112.92147299438474:28.215918666445262,113.00764700561524:28.215918666445262,113.00764700561524:28.181538568323404,112.92147299438474:28.181538568323404"
        req = requests.post(url=fullurl, data=bodyjson1, headers=header1, verify=False)
        #str1 = req.text.encode('utf-8').replace('\xc3\xaf\xc2\xbb\xc2\xbf\xc3\xaf\xc2\xbb\xc2\xbf', '')
        print req.text
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print hjson
        if hjson['state'] == True:#如果返回失败，返回-1给前台，返回成功时将ID返回前台
            return hjson['cases'][0]['lawcaseId']
        else:
            return "-1"

    def queryCasesByPolygon1(self, url, header):
        #查询所有案件
        urlfax = "/lawcase/police/queryCasesByPolygon"
        fullurl = url + urlfax
        body = {}
        # body["name"] = ""
        # body["pageNo"] = 1
        # body["pageSize"] = 10
        bodyjson = json.dumps(body)
        print fullurl
        print bodyjson
        req = requests.get(url=fullurl, data=bodyjson, headers=header, verify=False)
        #str1 = req.text.encode('utf-8').replace('\xc3\xaf\xc2\xbb\xc2\xbf\xc3\xaf\xc2\xbb\xc2\xbf', '')
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print hjson
        if hjson['state'] == "true":#如果查询没结果，返回失败
            total = hjson['content']['getRegistLib']['total']
            for i in range(0, total):#遍历所有人像库，找到自己创建的人像库，如果有直接删除，如果没有返回成功
                print i
                if hjson['content']['getRegistLib']['records'][i]['name'] == '1122':#判断是否已经添加，如果已经添加，先删除
                    delresult = self.faceGroupdelete(url, hjson['content']['getRegistLib']['records'][i]['id'], header)
                    return delresult
            return "0"
        else:
            return "-1"

    def queryMotorVehiclesByHour(self, url, header):
        #根据时间查询机动车数量
        urlfax = "/video/dataLive/queryMotorVehiclesByHour"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['lineDataList'])
        else:
            return "-1"

    def queryMotorVehiclesNow(self, url, header):
        #查询当前时间机动车数量
        urlfax = "/video/dataLive/queryMotorVehiclesNow"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['motorVehiclesNum'])
        else:
            return "-1"

    def queryNonMotorVehiclesNow(self, url, header):
        #查询当前时间非机动车数量
        urlfax = "/video/dataLive/queryNonMotorVehiclesNow"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['nonMotorVehiclesNum'])
        else:
            return "-1"

    def queryFacesPersonsNow(self, url, header):
        #查询当前时间人脸人形数量
        urlfax = "/video/dataLive/queryFacesPersonsNow"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['facesNum'])
        else:
            return "-1"

    def queryNonMotorVehiclesByHour(self, url, header):
        #根据时间查询非机动车数量
        urlfax = "/video/dataLive/queryNonMotorVehiclesByHour"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['lineDataList'])
        else:
            return "-1"

    def queryFacesPersonsByHour(self, url, header):
        #根据时间查询人脸和人形数量
        urlfax = "/video/dataLive/queryFacesPersonsByHour"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['personsDataList'])
        else:
            return "-1"

    def getDataLiveVideoPerson(self, url, header):
        #获取人形数量
        urlfax = "/video/dataLive/getDataLiveVideoPerson"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['personsTotal'])
        else:
            return "-1"

    def getDataLiveVideoFace(self, url, header):
        #获取人脸数量
        urlfax = "/video/dataLive/getDataLiveVideoFace"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['facesTotal'])
        else:
            return "-1"

    def getDataLiveVideoMotor(self, url, header):
        #获取机动车数量
        urlfax = "/video/dataLive/getDataLiveVideoMotor"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['motorVehiclesTotal'])
        else:
            return "-1"

    def getDataLiveVideoNonMotor(self, url, header):
        #获取非机动车数量
        urlfax = "/video/dataLive/getDataLiveVideoNonMotor"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['nonMotorVehiclesTotal'])
        else:
            return "-1"

    def getDataLiveLawcase(self, url, header):
        #获取案件数量
        urlfax = "/lawcase/police/getDataLiveLawcase"
        fullurl = url + urlfax
        body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['lawcaseTotal'])
        else:
            return "-1"

    def queryTasksByPolygon(self, url, header):
        #获取当前分析任务
        urlfax = "/video/u2sTask/queryTasksByPolygon"
        fullurl = url + urlfax
        # body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1 = "polygon=102.24772208917582:27.884378394040866,102.2871369241735:27.884353022234603,102.28713709730222:27.878851499664968,102.24772226085335:27.8788768715334"
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return req.text
        else:
            return "-1"

    def queryResultsByPage(self, url, header, cameraId, serialNumber):
        #获取当前分析点位图片
        urlfax = "/video/dataLive/queryResultsByPage"
        fullurl = url + urlfax
        # body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1 = {"pageNum":1 ,"pageSize": 12, "cameraId": cameraId, "serialNumber": serialNumber}
        print body1
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def getCameraByAddress(self, url, header, address):
        #通过CAMERAid获取信息
        urlfax = "/lawcase/camera/getCameraByAddress"
        fullurl = url + urlfax
        # body = {}
        # body["age"] = ""
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1 = {"address":address}
        print body1
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['camera']['id'])
        else:
            return "-1"

    def queryPoints(self, url, header):
        #查询点位
        urlfax = "/lawcase/camera/queryPoints"
        fullurl = url + urlfax
        # body = {}
        # body["polygon"] = "102.24772208917582:27.884378394040866,102.2871369241735:27.884353022234603,102.28713709730222:27.878851499664968,102.24772226085335:27.8788768715334"
        # body["image"] = image
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        # bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        bodyjson1 = "polygon=112.92147299438474:28.215918666445262,113.00764700561524:28.215918666445262,113.00764700561524:28.181538568323404,112.92147299438474:28.181538568323404"
        req = requests.post(url=fullurl, data=bodyjson1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['cameras'][0]['id'])
        else:
            return "-1"

    def queryTmpClueByUser(self, url, header):
        #查询临时线索库
        urlfax = "/lawcase/clue/queryTmpClueByUser"
        fullurl = url + urlfax
        body = {}
        body["pageNum"] = 1
        body["pageSize"] = 10
        # body["name"] = "1122"
        # body["regId"] = regId
        # body["sex"] = ""
        bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        bodyjson1 = {"pageNum":1, "pageSize":10}
        req = requests.post(url=fullurl, data=bodyjson1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        #print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['records'])
        else:
            return "-1"

    def queryPoliceHomeDataByPage(self, url, header):
        #获取案件（案件库）
        print header
        urlfax = "/lawcase/police/queryPoliceHomeDataByPage?pageNum=1&pageSize=10&type=&keyWord="
        fullurl = url + urlfax
        body = {}
        body["caseName"] = ""
        body["categoryValue"] = ""
        body["categoryValueLevel"] = ""
        body["keyWord"] = ""
        body["pageNum"] = "1"
        body["pageSize"] = "10"
        body["recieveCode"] = ""
        body["type"] = ""
        body["verifyingStatus"] = ""
        bodyjson = json.dumps(body)
        print fullurl
        # print bodyjson
        header['content-type'] = 'application/json'
        req = requests.post(url=fullurl, data=bodyjson, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['records'])
        else:
            return "-1"

    def addImageSearchTask(self, url, header, objType, imgUrl):
        #添加以图搜图任务
        urlfax = "/video/realtimeTrace/addImageSearchTask"
        fullurl = url + urlfax
        # body = {}
        # body["startTime"] = "2019-06-12 00:00:00"
        # body["endTime"] = "2019-07-31 00:00:00"
        # # body["imgUrl"] = "http://192.168.0.228/img/PIC/body/body1.jpg"
        # body["imgUrl"] = imgUrl
        # body["objType"] = objType
        # bodyjson = json.dumps(body)
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1={"startTime": "2019-06-12 00:00:00", "endTime": "2019-07-31 00:00:00", "imgUrl": imgUrl, "objType": objType, "tradeOff":"10"}
        print fullurl
        print body1
        # print bodyjson
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        # print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return json.dumps(hjson['serialNumber'])
        else:
            return "-1"

    def queryImageSearchTop(self, url, header, serialNumberid):
        #查询以图搜图结果
        urlfax = "/video/realtimeTrace/queryImageSearchTop"
        fullurl = url + urlfax
        # body = {}
        # body["startTime"] = "2019-06-12 00:00:00"
        # body["endTime"] = "2019-07-31 00:00:00"
        # # body["imgUrl"] = "http://192.168.0.228/img/PIC/body/body1.jpg"
        # body["imgUrl"] = imgUrl
        # body["objType"] = objType
        # bodyjson = json.dumps(body)
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1 = {"serialNumber": serialNumberid}
        print fullurl
        print body1
        # print bodyjson
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        # print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def getAnalysisInitData(self, url, header):
        #获取分析数据
        urlfax = "/video/u2sAnalysisNew/getAnalysisInitData"
        fullurl = url + urlfax
        body = {}
        # body["startTime"] = "2019-06-12 00:00:00"
        # body["endTime"] = "2019-07-31 00:00:00"
        # body["imgUrl"] = "http://192.168.0.228/img/PIC/body/body1.jpg"
        # body["imgUrl"] = "http://192.168.0.80:8088/ftp/imagesearch/2019/6/20/201906200942362633214214.jpg"
        # body["objType"] = "1"
        # bodyjson = json.dumps(body)
        # header1 = header
        # header1["Content-Type"] = "application/x-www-form-urlencoded"
        # body1={"serialNumber":serialNumberid}
        # print fullurl
        # print bodyjson
        req = requests.post(url=fullurl, data=body, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def querySemanticTop(self, url, header, type):
        #查询语义搜结果
        urlfax = "/video/realtimeTrace/querySemanticTop"
        fullurl = url + urlfax
        body = {}
        body["startTime"] = "2019-06-12 00:00:00"
        body["endTime"] = "2019-07-31 00:00:00"
        body["pageNo"] = "1"
        body["pageSize"] = "10"
        # body["sex"] = "1"
        body["type"] = type
        bodyjson = json.dumps(body)
        # header1 = header
        # header1["Content-Type"] = "application/x-www-form-urlencoded"
        # body1={"endTime": "2019-07-31 00:00:00",
        # "pageNo": 1,
        # "pageSize": 10,
        # "sex": "1",
        # "startTime": "2019-06-17 00:00:00",
        # "type": "person"}
        print fullurl
        print bodyjson
        req = requests.post(url=fullurl, data=bodyjson, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def querySemanticGroupData(self, url, header, type):
        #查询语义搜结果分组
        urlfax = "/video/realtimeTrace/querySemanticGroupData"
        fullurl = url + urlfax
        body = {}
        body["startTime"] = "2019-06-12 00:00:00"
        body["endTime"] = "2019-07-31 00:00:00"
        body["pageNo"] = "1"
        body["pageSize"] = "10"
        # body["sex"] = "1"
        body["type"] = type
        bodyjson = json.dumps(body)
        # header1 = header
        # header1["Content-Type"] = "application/x-www-form-urlencoded"
        # body1={"endTime": "2019-07-31 00:00:00",
        # "pageNo": 1,
        # "pageSize": 10,
        # "sex": "1",
        # "startTime": "2019-06-17 00:00:00",
        # "type": "person"}
        print fullurl
        print bodyjson
        req = requests.post(url=fullurl, data=bodyjson, headers=header)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def getImageDetails(self, url, header, pic1):
        #查询图片结构化
        urlfax = "/video/u2sTask/getImageDetails"
        fullurl = url + urlfax
        # body = {}
        # body["startTime"] = "2019-06-12 00:00:00"
        # body["endTime"] = "2019-07-31 00:00:00"
        # body["pageNo"] = "1"
        # body["pageSize"] = "10"
        # body["sex"] = "1"
        # body["base64Str"] = self.pic64(pic1)
        # bodyjson = json.dumps(body)
        # header1 = header
        # header1["Content-Type"] = "application/x-www-form-urlencoded"
        # body1={"endTime": "2019-07-31 00:00:00",
        # "pageNo": 1,
        # "pageSize": 10,
        # "sex": "1",
        # "startTime": "2019-06-17 00:00:00",
        # "type": "person"}
        print fullurl
        # print bodyjson
        header1 = header
        # print header1
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1={"base64Str": self.pic64(pic1)}
        # print body1
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        # print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return 1
        else:
            return "-1"

    def structPicture1(self, url, header, imgurl):
        #自动框选图片
        urlfax = "/video/imageSearch/structPicture"
        fullurl = url + urlfax
        print fullurl
        body = {}
        body["imgurl"] = imgurl
        header1 = header
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        print header1
        print body
        req = requests.post(url=fullurl, data=body, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return hjson['xywhs']
        else:
            return "-1"

    def editImageByXYWH(self, url, header, imgurl):
        #手动框选图片
        urlfax = "/lawcase/ftp/editImageByXYWH"
        fullurl = url + urlfax
        print fullurl
        # print bodyjson
        header1 = header
        # print header1
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        body1={"imgUrl": imgurl, 'width': 265, 'height': 741, 'x': 129, 'y': 39}
        print body1
        req = requests.post(url=fullurl, data=body1, headers=header1)
        hjson = json.loads(req.text)#因为平台解析失败，在后台获取对应JSON
        # print req.text
        #return req.text
        print hjson
        if hjson['state'] == True:
            return hjson['data']['fileUrl']
        else:
            return "-1"

    def aa(self):
        header=self.hhgethead(	"http://192.168.0.80:5555/sys/user/loginSubmit")
        print header
        return 1

    aa = pic64("", "D:\\HH\\Media\\PIC\\driver\\1.jpg")
    print aa