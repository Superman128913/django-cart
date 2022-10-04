#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 
#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 
#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 
#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 
#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 
#### this is a sample file it may not be function i just show as example how the checker background python script should work /// the real file will be done by you 


from csv import excel
import requests
from requests.exceptions import Timeout
import pprint
from threading import Thread
import threading
import pprint
import time
import mysql.connector
import json
from datetime import datetime
api = "http://65.20.69.221/API.php?"
def get_status(api, phonenumber, day, month, year, zipcode, gatelink):
    if checker_name == "checker 1":
        checker_name = "checker 1"
    elif checker_name == "checker 2":
        checker_name = "checker 2"
    elif checker_name == "checker 3":
        checker_name = "checker 3"

    pp = pprint.PrettyPrinter(indent=4)
    endpoint = str("phonenumber="+phonenumber+"&day="+day+"&month=" +
                   month+"&year="+year+"&zipcode="+zipcode+"&checker_name="+checker_name)
    endpoint = str(api + endpoint)
    pp.pprint(endpoint)

    content = "Timeout"
    try:
        content = requests.get(endpoint, timeout=120).content
    except Timeout:
        content = "Timeout"
    except:
        content = "Unknow Error"

    return content


def getData_Thread(api, user_id, price, id, phonenumber, day, month, year, zipcode, checker_name):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="]f3PW3[*@,F2d3oC",
            database='MyDatabase',
            auth_plugin='mysql_native_password'
        )
    except:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint("Error MyDB connect in getData_Thread")
    mycursor = mydb.cursor(buffered=True)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("GetData_Thread START")

    is_success = False
    for tries in list(range(10)):
        m_result = get_status(api, phonenumber, day, month,
                              year, zipcode, checker_name)

        if m_result == "Timeout":
            tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
            mycursor.execute(tmp, ("Error", int(id)))
            tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
            mycursor.execute(tmp, ("problem while checking your Phone Please try again or select a differant checker", int(id)))
            tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
            mycursor.execute(tmp, ("-", int(id)))
            tmp = "UPDATE shop_data SET checker_cost=%s WHERE id= %s"
            mycursor.execute(tmp, (0.0, int(id)))

            tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
            m_userID = int(user_id)
            mycursor.execute(tmp, (m_userID,))
            m_result = mycursor.fetchall()
            m_userBalance = float(m_result[0][0])
            m_userBalance = m_userBalance + float(price)
            tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
            mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

            mydb.commit()
            is_success = True
            break

        if (m_result == bytes("phone registered successfully", 'utf-8') or m_result == bytes("Registration success", 'utf-8')) or (m_result == bytes("Thank you for your Registration", 'utf-8')):
            pp.pprint("_________________Success__________________")
            pp.pprint(m_result)
            tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
            mycursor.execute(tmp, ("valid", int(id)))
            tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
            mycursor.execute(tmp, ("Valid Phone", int(id)))
            tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
            mycursor.execute(tmp, ("phone number is valid by checker", int(id)))
            
            tmp = "UPDATE shop_data SET checker_cost =%s WHERE id= %s"
            mycursor.execute(tmp, (float(price), int(id)))

            mydb.commit()
            is_success = True
            break

        elif (m_result == bytes("Phone Registration Fails .", 'utf-8') or m_result == bytes("Phone number is no more active.", 'utf-8')) or (m_result == bytes("Please check your phone number.", 'utf-8')):
            pp.pprint("_________________ERROR__________________")
            pp.pprint(m_result)
            tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
            mycursor.execute(tmp, ("Fail", int(id)))
            tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
            mycursor.execute(tmp, ("Invaid Phone number", int(id)))
            tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
            mycursor.execute(tmp, ("phone number is invalid", int(id)))
            tmp = "UPDATE shop_data SET checker_cost =%s WHERE id= %s"
            mycursor.execute(tmp, (0.00, int(id)))

            tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
            m_userID = int(user_id)
            mycursor.execute(tmp, (m_userID,))
            m_result = mycursor.fetchall()
            m_userBalance = float(m_result[0][0])
            m_userBalance = m_userBalance + float(price)
            tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
            mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

            mydb.commit()
            is_success = True
            break

        elif (m_result == bytes("Please try again ", 'utf-8') or m_result == bytes("Please try again later", 'utf-8')) or (m_result == bytes("Problem while processing your request. ", 'utf-8')):
            if tries == 10:
                pp.pprint("__________________ERROR1_________________")
                pp.pprint(m_result)
                tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
                mycursor.execute(tmp, ("error", int(id)))
                tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
                mycursor.execute(tmp, ("Please try again Later", int(id)))
                tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
                mycursor.execute(tmp, ("Please try again Later vcan not connect", int(id)))
                tmp = "UPDATE shop_data SET checker_cost =%s WHERE id= %s"
                mycursor.execute(tmp, (0.00, int(id)))

                tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
                m_userID = int(user_id)
                mycursor.execute(tmp, (m_userID,))
                m_result = mycursor.fetchall()
                m_userBalance = float(m_result[0][0])
                m_userBalance = m_userBalance + float(price)
                tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
                mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

                mydb.commit()

        elif(m_result == bytes("Can’t process your request at the moment", 'utf-8') or m_result == bytes("Service is over load please try again later", 'utf-8')):
            if tries == 10:
                pp.pprint("__________________ERROR1_________________")
                pp.pprint(m_result)
                tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
                mycursor.execute(tmp, ("error", int(id)))
                tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
                mycursor.execute(tmp, ("Please try again Later", int(id)))
                tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
                mycursor.execute(tmp, ("Please try again Later message", int(id)))
                tmp = "UPDATE shop_data SET checker_cost =%s WHERE id= %s"
                mycursor.execute(tmp, (0.00, int(id)))

                tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
                m_userID = int(user_id)
                mycursor.execute(tmp, (m_userID,))
                m_result = mycursor.fetchall()
                m_userBalance = float(m_result[0][0])
                m_userBalance = m_userBalance + float(price)
                tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
                mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

                mydb.commit()
        else:
            pp.pprint(m_result)
            tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
            mycursor.execute(
                tmp, ("Unknown error please contact support", int(id)))
            tmp = "UPDATE shop_data SET status=%s WHERE id= %s"
            mycursor.execute(tmp, (2, int(id)))

            tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
            m_userID = int(user_id)
            mycursor.execute(tmp, (m_userID,))
            m_result = mycursor.fetchall()
            m_userBalance = float(m_result[0][0])
            m_userBalance = m_userBalance + float(price)
            tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
            mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

            mydb.commit()
            is_success = True
            break

    if is_success == False:
        tmp = "UPDATE shop_data SET checker_status =%s WHERE id= %s"
        mycursor.execute(tmp, ("Please try again Later", int(id)))
        tmp = "UPDATE shop_data SET checker_response_text =%s WHERE id= %s"
        mycursor.execute(tmp, ("-", int(id)))
        tmp = "UPDATE shop_data SET checker_response_full =%s WHERE id= %s"
        mycursor.execute(tmp, ("-", int(id)))
        tmp = "UPDATE shop_data SET checker_cost=%s WHERE id= %s"
        mycursor.execute(tmp, (0.0, int(id)))

        tmp = "SELECT balance FROM home_balance WHERE user_id=%s"
        m_userID = int(user_id)
        mycursor.execute(tmp, (m_userID,))
        m_result = mycursor.fetchall()
        m_userBalance = float(m_result[0][0])
        m_userBalance = m_userBalance + float(price)
        tmp = "UPDATE home_balance SET balance =%s WHERE user_id= %s"
        mycursor.execute(tmp, (format(m_userBalance, ".2f"), m_userID))

        mydb.commit()

    tmp = "SELECT batch_id FROM shop_data WHERE id= %s"
    mycursor.execute(tmp, (int(id),))
    m_result = mycursor.fetchall()
    m_batchID = int(m_result[0][0])

    tmp = "SELECT status, checker_status FROM shop_data WHERE batch_id= %s"
    mycursor.execute(tmp, (m_batchID,))
    m_result = mycursor.fetchall()
    pp.pprint(m_batchID)
    pp.pprint("______________BATHID_GATE_STATUS____")
    m_inq = 0
    m_proc = 0
    m_fail = 0
    m_done = 0
    m_retry = 0

    for ii in m_result:
        if ii[0] == 0:
            m_inq += 1
        elif ii[0] == 1:
            m_proc += 1
        elif ii[0] == 2:
            # m_fail += 1
            m_retry += 1
        elif ii[0] == 3:
            if ii[1] == "Phone Registration Fails":
                m_fail += 1
            else:
                m_done += 1

    tmp = "UPDATE home_batch SET succeed=%s WHERE batch_id= %s"
    mycursor.execute(tmp, (int(m_done), m_batchID))
    tmp = "UPDATE home_batch SET done=%s WHERE batch_id= %s"
    m_fd = m_fail+m_done
    mycursor.execute(tmp, (int(m_fd), m_batchID))
    tmp = "UPDATE home_batch SET fail=%s WHERE batch_id= %s"
    mycursor.execute(tmp, (int(m_fail), m_batchID))
    tmp = "UPDATE home_batch SET remains=%s WHERE batch_id= %s"
    m_reamin = m_inq+m_proc+m_retry
    mycursor.execute(tmp, (int(m_reamin), m_batchID))

    tmp = "UPDATE home_batch SET retry=%s WHERE batch_id= %s"
    mycursor.execute(tmp, (int(m_retry), m_batchID))

    pp.pprint(m_inq)
    pp.pprint(m_proc)

    if m_inq == 0 and m_proc == 0:
        tmp = "UPDATE home_batch SET status=%s WHERE batch_id= %s"
        mycursor.execute(tmp, ("Finished", m_batchID))
        tmp = "UPDATE home_batch SET finish_time =%s WHERE batch_id= %s"
        mycursor.execute(tmp, (datetime.now(), m_batchID))

    mydb.commit()
    mycursor.close()
    mydb.close()
    pp.pprint("GetData_Thread END")

    return
