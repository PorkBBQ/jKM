#!/home/biadmin/anaconda/bin/python

import json
import sys

digits=[str(_) for _ in range(1,101)]

def getReplaceList():
    replaceList=[]
    replaceList.append(['""', '"'])
    replaceList.append(['"craetedAt":', '"createdAt":'])
    replaceList.append(['"created_at":', '"createdAt":'])
    replaceList.append(['"session_id":', '"sessionID":'])
    replaceList.append(['"user_agent":', '"userAgent":'])
    replaceList.append(['"item_id":', '"itemId":'])
    return replaceList

def getDrillPaths():
    return {
        '/auth':0
        , '/createdAt':0
        , '/payload':1
        , '/refId':0
        , '/sessionID':0
        , '/type':1
        , '/user':0
        , '/userAgent':0
        , '/payload/itemId':0
        , '/payload/marker':0
        , '/payload/popular':1
        , '/payload/recent':0
        , '/payload/recommended':1
        , '/payload/recs/':1
        , '/payload/results':1
    }

def getSummaryTypes():    
    return {
        '/auth':'3'
        , '/createdAt':'date'
        , '/payload':'1'
        , '/refId':'3'
        , '/sessionID':'3'
        , '/type':'3'
        , '/user':'num'
        , '/userAgent':'1'
        , '/payload/itemId':'num'
        , '/payload/lengtg':'num'
        , '/payload/marker':'num'
        , '/payload/new':'freq10'
        , '/payload/old':'freq10'
        , '/payload/popular':'1'
        , '/payload/popular/':'freq10'
        , '/payload/rating':'freq10'
        , '/payload/recent':'3'
        , '/payload/recs':'3'
        , '/payload/recs/':'freq10'
        , '/payload/recommended':'3'
        , '/payload/recommended/':'freq10'
        , '/payload/results':'1'
        , '/payload/results/':'freq10'
    }   

