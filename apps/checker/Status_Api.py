

import requests
import pprint
from threading import Thread
import threading
import pprint
import time
import mysql.connector
import json
from datetime import datetime
from api_module import getData_Thread
#import socketio
#from aiohttp import web


class main_Thread(Thread):
    api = "https://hardcore-varahamihira.78-141-193-11.plesk.page/API.php?"
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("Start main_Thread ")
    info = True

    while info:
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="]f3PW3[*@,F2d3oCx",
                database='MyDatabase-andrew',
                auth_plugin='mysql_native_password'
            )
        except:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint("Error MyDB connect")
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute(
            "SELECT * FROM home_gate WHERE status = 0 ORDER BY id")
        myresult_gate = mycursor.fetchall()
        rtn_data = {}
        if myresult_gate == []:
            pp.pprint("Finished Set Result Api")
            time.sleep(3)
            continue
        # pp.pprint(myresult_gate)
        tmp = "SELECT id FROM auth_user WHERE username=%s"
        mycursor.execute(tmp, (str(myresult_gate[0][24]),))
        m_result = mycursor.fetchall()
        pp.pprint(m_result[0][0])
        tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
        m_userID = int(m_result[0][0])
        mycursor.execute(tmp, (m_userID,))
        m_result = mycursor.fetchall()
        m_userBalance = float(m_result[0][0])
        pp.pprint(m_userBalance)
        tmp = "SELECT Link_price FROM home_gate_link WHERE Link_Name=%s"
        mycursor.execute(tmp, (str(myresult_gate[0][22]),))
        m_result = mycursor.fetchall()
        m_LinkPrice = float(m_result[0][0])
        if m_userBalance < m_LinkPrice:
            pp.pprint("Balance Error")
            tmp = "UPDATE home_gate SET result1=%s, status=2 WHERE id= %s"
            mycursor.execute(
                tmp, ("Your Balance is too low please Deposit Funds", int(myresult_gate[0][0])))
            mydb.commit()
            time.sleep(3)
            continue

        m_ba = m_userBalance-m_LinkPrice
        tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
        mycursor.execute(tmp, (format(m_ba, ".2f"), m_userID))
        mydb.commit()

        ##Batch Status Update___RUNNIG(1) ######################################

        tmp = "SELECT batch_id FROM home_gate WHERE id= %s"
        mycursor.execute(tmp, (int(myresult_gate[0][0]),))
        m_result = mycursor.fetchall()
        m_batchID = int(m_result[0][0])

        tmp = "UPDATE home_batch SET status =%s WHERE batch_id= %s"
        mycursor.execute(tmp, ("Running", m_batchID))
        ##Gate Status Update___RUNNIG(1) ######################################
        tmp = "UPDATE home_gate SET status =%s WHERE id= %s"
        mycursor.execute(tmp, (1, int(myresult_gate[0][0])))
        mydb.commit()
        pp.pprint(m_LinkPrice)
        rtn_data['api'] = api
        rtn_data['user_id'] = m_userID
        rtn_data['price'] = m_LinkPrice
        rtn_data['id'] = myresult_gate[0][0]
        rtn_data['phonenumber'] = str(myresult_gate[0][1])
        rtn_data['day'] = str(myresult_gate[0][2])
        rtn_data['month'] = str(myresult_gate[0][3])
        rtn_data['year'] = str(myresult_gate[0][4])
        rtn_data['zipcode'] = str(myresult_gate[0][5])
        rtn_data['gatelink'] = str(myresult_gate[0][22])
        t1 = threading.Thread(target=getData_Thread, args=rtn_data.values())
        t1.start()
        pp.pprint("TIME SLEEP START")
        time.sleep(3)
        pp.pprint("TIME SLEEP END")
       # pp.pprint(myresult)
