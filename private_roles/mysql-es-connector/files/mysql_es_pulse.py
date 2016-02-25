#! /usr/bin/env python
from elasticsearch import Elasticsearch
import mysql.connector
import datetime
import traceback
import argparse
import requests
import json
import urllib3
import logging
logging.basicConfig()
urllib3.disable_warnings()

"""
Simple utility to pull ad data from a mysql database and load into elastic search. It can handle three doc_types. If executed from
command line it will loop over the three doc_types, execute a query for each, and update Elasticsearch accordingly. A user submits
the *interval* to test. For example, if --interval=5 then any rows added or updated within the last 5 minutes will be added/updated
in Elasticsearch

"""

doc_types = ['question_responses', 'outgoing', 'deploy']


# ELASTIC SEARCH HELPER METHODS


def get_rows(doc_type, interval, cursor,build, db_prefix):
    if doc_type == 'question_responses':
        columns = [ 
           "survey_instance",
           "response_id",
           "answer_id",
           "question_id",
           "survey_id",
           "contact_id",
           "contact_num",
           "question_responses_text",
           "translation",
           "is_ignored",
           "gateway_id",
           "device_id",
           "created_by",
           "updated_by",
           "question_responses_created_ts",
           "updated_ts",
           "question_title",
           "survey_title",
           "gateway_name",
           "gateway_name2",
           "question_type",
           "answer_line_id",
           "survey_archived",
           "survey_status",
           "location_name",
           "location_lat",
           "location_long"
        ]

        if build == 'all':
            sql = "SELECT b.survey_instance, b.response_id, b.answer_id, b.question_id, b.survey_id, b.contact_id, b.contact_num, b.text AS question_responses_text, b.translation, b.is_ignored, b.gateway_id, c.device_id, b.created_by, b.updated_by, b.created_ts AS question_responses_created_ts, b.updated_ts, a.text AS question_title, d.NAME AS survey_title, c.name AS gateway_name, c.device_name AS gateway_name2, a.question_type AS question_type, e.answer_line_id, d.archived as survey_archived, d.status as survey_status, d.location_name, d.location_lat, d.location_long FROM " + db_prefix + "_sms_survey_question_responses b LEFT JOIN " + db_prefix + "_sms_survey_questions a ON a.question_id = b.question_id LEFT JOIN " + db_prefix + "_sms_survey_question_answers e ON b.answer_id = e.answer_id LEFT JOIN " + db_prefix + "_sms_surveys d ON d.survey_id = b.survey_id LEFT JOIN " + db_prefix + "_gateways c ON b.gateway_id = c.gateway_id;"
        else:
            sql = "SELECT b.survey_instance, b.response_id, b.answer_id, b.question_id, b.survey_id, b.contact_id, b.contact_num, b.text AS question_responses_text, b.translation, b.is_ignored, b.gateway_id, c.device_id, b.created_by, b.updated_by, b.created_ts AS question_responses_created_ts, b.updated_ts, a.text AS question_title, d.NAME AS survey_title, c.name AS gateway_name, c.device_name AS gateway_name2, a.question_type AS question_type, e.answer_line_id, d.archived as survey_archived, d.status as survey_status, d.location_name, d.location_lat, d.location_long FROM " + db_prefix + "_sms_survey_question_responses b LEFT JOIN " + db_prefix + "_sms_survey_questions a ON a.question_id = b.question_id LEFT JOIN " + db_prefix + "_sms_survey_question_answers e ON b.answer_id = e.answer_id LEFT JOIN " + db_prefix + "_sms_surveys d ON d.survey_id = b.survey_id LEFT JOIN " + db_prefix + "_gateways c ON b.gateway_id = c.gateway_id WHERE b.updated_ts > DATE_SUB(NOW() , INTERVAL " + str(interval) + " MINUTE);"

    elif doc_type == 'outgoing':
        columns = [
            "survey_instance",
            "outgoing_id",
            "question_id",
            "survey_id",
            "contact_id",
            "contact_num",
            "outgoing_text",
            "device_id",
            "created_by",
            "updated_by",
            "outgoing_created_ts",
            "updated_ts",
            "gateway_id",
            "survey_title",
            "question_title",
            "location_name",
            "location_lat",
            "location_long"
        ]
        if build == 'all':
            sql = "SELECT a.survey_instance, a.outgoing_id, a.question_id, a.survey_id, a.contact_id, a.contact_num, a.text as outgoing_text, b.device_id, a.created_by, a.updated_by, a.created_ts as outgoing_created_ts, a.updated_ts, a.gateway_id, c.name AS survey_title, d.text as question_title, c.location_name, c.location_lat, c.location_long FROM " + db_prefix + "_sms_survey_outgoing a LEFT JOIN " + db_prefix + "_sms_surveys c ON a.survey_id = c.survey_id LEFT JOIN " + db_prefix + "_sms_survey_questions d ON d.question_id = a.question_id LEFT JOIN " + db_prefix + "_gateways b ON a.gateway_id = b.gateway_id;"
        else:        
            sql = "SELECT a.survey_instance, a.outgoing_id, a.question_id, a.survey_id, a.contact_id, a.contact_num, a.text as outgoing_text, b.device_id, a.created_by, a.updated_by, a.created_ts as outgoing_created_ts, a.updated_ts, a.gateway_id, c.name AS survey_title, d.text as question_title, c.location_name, c.location_lat, c.location_long FROM " + db_prefix + "_sms_survey_outgoing a LEFT JOIN " + db_prefix + "_sms_surveys c ON a.survey_id = c.survey_id LEFT JOIN " + db_prefix + "_sms_survey_questions d ON d.question_id = a.question_id LEFT JOIN " + db_prefix + "_gateways b ON a.gateway_id = b.gateway_id WHERE a.updated_ts > DATE_SUB(NOW() , INTERVAL " + str(interval) + " MINUTE);"
            
    elif doc_type == 'deploy':
        columns = [  
           "survey_id",
           "project_id",
           "template_id",
           "survey_title",
           "description",
           "optin_text",
           "status",
           "sample_size",
           "begin_date",
           "end_date",
           "archived",
           "created_by",
           "updated_by",
           "created_ts",
           "updated_ts",
           "location_name",
           "location_lat",
           "location_long"           
           ]

        if build == 'all':
            sql = "SELECT survey_id, project_id, template_id, name as survey_title, description, optin_text, status, sample_size, begin_date, end_date, archived, created_by, updated_by, created_ts, updated_ts, location_name, location_lat, location_long FROM " + db_prefix + "_sms_surveys;"
        else:
            sql = "SELECT survey_id, project_id, template_id, name as survey_title, description, optin_text, status, sample_size, begin_date, end_date, archived, created_by, updated_by, created_ts, updated_ts, location_name, location_lat, location_long FROM " + db_prefix + "_sms_surveys WHERE updated_ts > DATE_SUB(NOW() , INTERVAL " + str(interval) + " MINUTE);"

    cursor.execute(sql)
    rows = cursor.fetchall()
    timestamp = datetime.datetime.now()

    data_items = []
    for row in rows:
        data = {}
        ignoreThisRow = False
        for i in range(len(columns)):
                if row[i] is None or row[i] == 'null':
                    continue
                datarow = row[i]
                if isinstance(datarow, bytearray):
                    datarow = str(datarow)
                if isinstance(datarow, datetime.datetime) or isinstance(datarow, datetime.date):
                    datarow = datarow.isoformat()
                data[columns[i]] = datarow

        if doc_type == 'deploy':
            survey_id = data['survey_id']

            survey_json = get_survey_json(survey_id, cursor, db_prefix)
            data['survey_json'] = survey_json
            
            survey_questions = get_survey_questions(survey_id, cursor, db_prefix)
            data['survey_questions'] = survey_questions
            
            survey_question_answers = get_survey_question_answers(survey_id, cursor, db_prefix)
            data['survey_question_answers'] = survey_question_answers

        if doc_type == 'question_responses':
            # Check to make sure this row shouldn't be intentionally ignored
            if data.has_key('contact_id')and data.has_key('survey_archived') and data.has_key('survey_status') and shouldThisContactBeIgnored(data['contact_id'], data['survey_archived'], data['survey_status'], cursor, db_prefix) == True:
                ignoreThisRow = True

            # Group multiple choice question responses under their first-oridinal answer grouping
            if data.has_key('question_type') and data['question_type'] == 'select1':
                survey_question_answers = get_survey_question_answers(data['survey_id'], cursor, db_prefix)
                data['question_responses_text'] = get_norm_question_response(data['answer_line_id'], cursor, db_prefix)

        data['log_time'] = data['updated_ts']

        # Properly format location field
        try:
            data = get_location(data)
        except:
            pass

        if ignoreThisRow != True:
            data_items.append(data)
    
    return data_items


def getES(conn):
    es = Elasticsearch(conn)
    return es


def get_cnx(user,password,host,database):
    return mysql.connector.connect(user=user, password=password, host=host, database=database)


def get_id(doc_type, body):
    if doc_type == 'question_responses':
        doc_id = body['response_id']
    elif doc_type == 'outgoing':
        doc_id = body['outgoing_id']
    elif doc_type == 'deploy':
        doc_id = body['survey_id']
    return doc_id


def get_location(body):
    lat = body.pop('location_lat')
    lon = body.pop('location_long')
    try:
        location = str(lat) + ',' + str(lon)
        body['location'] = location
    except: 
        pass
    return body


def addToES(es,index,doc_type,item):
    try:
        doc_id = get_id(doc_type,item)   
        body = json.dumps(item)
        res = es.index(index=index, doc_type=doc_type, id=doc_id, body=body)
        if res['created'] == True:
            out = {'response': 'INDEXED', 'doc_type':doc_type, 'doc_id':doc_id}
        elif res['created'] == False:
            res = es.update(index=index, doc_type=doc_type, id=doc_id, body={'doc':body})
            if res['_index'] == index:
                out = {'response': 'UPDATED', 'doc_type':doc_type, 'doc_id':doc_id}
        else:
            out = {'response': 'ERROR', 'doc_type':doc_type, 'doc_id':doc_id}
    except Exception:
        out = {'response': 'FATAL', 'doc_type':doc_type, 'doc_id':doc_id}
    return out


def shouldThisContactBeIgnored(contact_id_to_check, survey_archived_to_check, survey_status_to_check, cursor, db_prefix):
    shouldIgnore = False

    sql = "SELECT is_blocked from " + db_prefix + "_contacts WHERE contact_id = '" + str(contact_id_to_check) + "';"
    cursor.execute(sql)
    is_blocked = cursor.fetchone()

    if str(is_blocked) == "(1,)":
        shouldIgnore = True

    if str(survey_archived_to_check) != "0":
        shouldIgnore = True

    if str(survey_status_to_check) != "1":
        shouldIgnore = True

    return shouldIgnore

def get_survey_json(s_id, cursor, db_prefix):
    s_id = str(s_id)
    sql = "SELECT survey_json FROM " + db_prefix + "_sms_surveys WHERE survey_id = '" + s_id + "' ;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    survey_json = str(rows[0][0])
    return survey_json


def get_survey_questions(s_id, cursor, db_prefix):
    
    columns = [         
         "question_id",
         "survey_id",
         "rank",
         "text",
         "comments",
         "is_ignored",
         "question_type",
         "title",
         "media_id",
         "created_by",
         "updated_by",
         "created_ts",
         "updated_ts"
         ]

    sql = "SELECT * from " + db_prefix + "_sms_survey_questions WHERE survey_id = '" + str(s_id) + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()

    question_list = []
    for row in rows:
        data = {}
        for i in range(len(columns)):
            if row[i] is None or row[i] == 'null':
                continue
            datarow = row[i]
            if isinstance(datarow, bytearray):
                datarow = str(datarow)
            if isinstance(datarow, datetime.datetime):
                datarow = datarow.isoformat()
            data[columns[i]] = datarow

        question_list.append(data)
        
    return question_list



def get_survey_question_answers(s_id, cursor, db_prefix):
    
    columns = [
         "answer_id",
         "question_id",
         "survey_id",
         "answer_line_id",
         "next_question_id",
         "rank",
         "text",
         "comments",
         "is_ignored",
         "odk_answer",
         "created_by",
         "updated_by",
         "created_ts",
         "updated_ts"
         ]

    sql = "SELECT * from " + db_prefix + "_sms_survey_question_answers WHERE survey_id = '" + str(s_id) + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    question_list = []
    for row in rows:
        data = {}
        for i in range(len(columns)):
            if row[i] is None or row[i] == 'null':
                continue
            datarow = row[i]
            if isinstance(datarow, bytearray):
                datarow = str(datarow)
            if isinstance(datarow, datetime.datetime):
                datarow = datarow.isoformat()
            data[columns[i]] = datarow

        question_list.append(data)
        
    return question_list


def get_norm_question_response(answer_line_id, cursor, db_prefix):
    sql = "SELECT text from " + db_prefix + "_sms_survey_question_answers WHERE answer_line_id = '" + str(answer_line_id) + "' AND odk_answer = 1;"
    cursor.execute(sql)
    return cursor.fetchone()


def run_update(dbhost,dbuser,dbpassword,db,es,index,doc_type,interval,build,db_prefix):
    logfile = open(LOG_FILE,'a')
    cnx = get_cnx(dbuser,dbpassword,dbhost,db)
    cursor = cnx.cursor()
    try:
        rows = get_rows(doc_type, interval, cursor,build, db_prefix)
        print str(len(rows)) + ' rows found for ' + doc_type
    except:
        rows = []

    if len(rows) > 0:
        es_conn = getES(es)
        for item in rows:
            out = addToES(es_conn,index,doc_type,item)
            if out.get('response','') == 'INDEXED':
                logfile.write(str(datetime.datetime.now())+'\t INDEXED doc with ' + doc_type + ' id:'+ str(out.get('doc_id',''))+'\n')
            elif out.get('response','') == 'UPDATED':
                logfile.write(str(datetime.datetime.now())+'\t UPDATED doc with ' + doc_type + ' id:'+ str(out.get('doc_id',''))+'\n')
            elif out.get('response','') == 'ERROR':
                logfile.write(str(datetime.datetime.now())+'\t ERROR for doc with ' + doc_type + ' id:'+ str(out.get('doc_id',''))+'\n')
            elif out.get('response','') == 'FATAL':
                logfile.write(str(datetime.datetime.now())+'\t FATAL for doc with ' + doc_type + ' id:'+ str(out.get('doc_id',''))+'\n')
            else:
                logfile.write(str(datetime.datetime.now())+'\t UNKNOWN ERROR for doc with ' + doc_type + ' id:'+ str(out.get('doc_id',''))+'\n')                
    else:
        logfile.write(str(datetime.datetime.now()) + '\t no db query results for '+ doc_type + '\n')
    
    logfile.close()
    cnx.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull ads in sequence from a database and load into elasticsearch')
    parser.add_argument('--dbhost',dest='dbhost',required=True,help='database hostname. required')
    parser.add_argument('--dbuser',dest='dbuser',required=True,help='database username. required')
    parser.add_argument('--pw',dest='password',required=True,help='database password. required')
    parser.add_argument('--db',dest='db',default='joka_brandon_test',help='database to use. default=joka_brandon_test')
    parser.add_argument('--interval',dest='interval',default='5',help='interval to pull rows from db. default=5')
    parser.add_argument('--es',dest='es',required=True,help='elasticsearch ip:port. required.')
    parser.add_argument('--index',dest='index',default='test',help='elasticsearch index. default=test')
    parser.add_argument('--logfile',dest='LOGFILE',default='out.log',help='logfile path. default=out.log')
    parser.add_argument('--build',dest='build',default='incremental',help='if build=all then rebuilds entire index. default=incremental')
    parser.add_argument('--mapping',dest='mapping',default='{}',help='if build=all then provide path to mapping')
    parser.add_argument('--db_prefix',dest='db_prefix',default='pulse',help='set the db_prefix, default=pulse')

    start = datetime.datetime.now()

    args = parser.parse_args()

    LOG_FILE = args.LOGFILE

    if args.build == 'all':
        es_conn = getES(args.es)
        if es_conn.indices.exists(args.index):
            print 'deleting index ' + args.index + '...'
            es_conn.indices.delete(index=args.index)

        with open(args.mapping, 'r') as fp:
            mapping = json.loads(fp.read())
            fp.close()
            
        es_conn.indices.create(index=args.index, body=json.dumps(mapping))
        print 'created index ' + args.index + '.'


    for doc_type in doc_types:
        run_update(args.dbhost,args.dbuser,args.password,args.db,args.es,args.index,doc_type,args.interval,args.build,args.db_prefix)

    end = datetime.datetime.now()

    total_time = end - start
    print 'Took ' + str(total_time)