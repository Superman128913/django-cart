import sys
import requests
from datetime import datetime
from requests.exceptions import Timeout

import mysql.connector
import cryptography.fernet
from django.core.exceptions import ImproperlyConfigured


def parse_key(key):
    """
    If the key is a string we need to ensure that it can be decoded
    :param key:
    :return:
    """
    return cryptography.fernet.Fernet(key)
    

def get_crypter():
    configured_keys = 'VmREnqyJTsRtQt7x0OHRm0e_LwYMf2EVJrIsoYJIhWo='

    if configured_keys is None:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY must be defined in settings')

    try:
        # Allow the use of key rotation
        if isinstance(configured_keys, (tuple, list)):
            keys = [parse_key(k) for k in configured_keys]
        else:
            # else turn the single key into a list of one
            keys = [parse_key(configured_keys), ]
    except Exception as e:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY defined incorrectly: {}'.format(str(e)))

    if len(keys) == 0:
        raise ImproperlyConfigured('No keys defined in setting FIELD_ENCRYPTION_KEY')

    return cryptography.fernet.MultiFernet(keys)


CRYPTER = get_crypter()


def decrypt_str(t):
    # be sure to decode the bytes to a string
    return CRYPTER.decrypt(t.encode('utf-8')).decode('utf-8')

api = 'https://hardcore-varahamihira.78-141-193-11.plesk.page/API.php'


def checker_api(phonenumber, day, month, year, zipcode, gatelink):
    api_url = api + '?' + \
        'phonenumber=' + phonenumber + '&' + \
        'day=' + day + '&' + \
        'month=' + month + '&' + \
        'year=' + year + '&' + \
        'zipcode=' + zipcode + '&' + \
        'gatelink=' + gatelink

    result = requests.get(api_url)

    return result.text
    
def check(product_id, checker_id, user_id):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='MyDatabase',
            # password="]f3PW3[*@,F2d3oCx",
            # database='MyDatabase-andrew',
            auth_plugin='mysql_native_password'
        )
    except:
        return "Error MyDB connect in getData_Thread"

    mycursor = mydb.cursor(buffered=True)

    tmp = "SELECT Phone, Exp_day, Exp_month, Exp_year, Zipcode, Price FROM cart_shop_data WHERE id=%d" % (product_id)
    mycursor.execute(tmp)
    product_obj = mycursor.fetchall()[0]

    tmp = "SELECT Name, Cost FROM cart_checker WHERE id=%d" % (checker_id)
    mycursor.execute(tmp)
    checker_obj = mycursor.fetchall()[0]

    phonenumber =   decrypt_str(str(product_obj[0]))
    day =           str(product_obj[1])
    month =         str(product_obj[2])
    year =          str(product_obj[3])
    zipcode =       str(product_obj[4])
    price =         float(product_obj[5])
    gatelink =      str(checker_obj[0])
    checker_price = float(checker_obj[1])

    for each in range(10):
        m_result = checker_api(phonenumber, day, month, year, zipcode, gatelink)
        
        if (m_result == "phone registered successfully" or m_result == "Registration success" or m_result == "Thank you for your Registration"):
            # print("_________________DONE__________________")
            checker_response_text = m_result
            checker_response_full = "Phone Registered Successfully"
            check_status = "Done"
            break

        elif (m_result == "Phone Registration Fails ." or m_result == "Phone number is no more active." or m_result == "Please check your phone number."):
            # print("_________________FAIL__________________")
            checker_response_text = m_result
            checker_response_full = "Phone Registration Fails"
            check_status = "Fail"
            break

        elif (m_result == "Please try again " or m_result == "Please try again later" or m_result == "Problem while processing your request. " or m_result == "Can’t process your request at the moment" or m_result == "Service is over load please try again later"):
            if each == 9:
                # print("__________________ERROR_________________")
                checker_response_text = m_result
                checker_response_full = "Please try again Later"
                check_status = "Error"

        else:
            # print("__________________UNKOWN ERROR_________________")
            checker_response_text = m_result
            checker_response_full = "Unknown error please contact support"
            check_status = "Error"
            break
    #? #################################################

    if check_status == 'Done':        
        tmp = "INSERT INTO cart_order_history (User_id, Product_id, Checker_id, Checker_status, Checker_response_text, Checker_response_full, Checker_date) VALUES (%d, %d, %d, '%s', '%s', '%s', '%s')" % (user_id, product_id, checker_id, 'Done', checker_response_text, checker_response_full, str(datetime.now()))
        mycursor.execute(tmp)
        tmp = "UPDATE cart_shop_data SET Sold_unsold='%s', Sold_date='%s' WHERE id=%d" % ('SOLD', str(datetime.now()), product_id)
        mycursor.execute(tmp)
        tmp = "SELECT balance FROM home_balance WHERE user_id=%d" % (user_id)
        mycursor.execute(tmp)
        m_result = mycursor.fetchall()
        m_userBalance = float(m_result[0][0])
        m_userBalance = round(m_userBalance - checker_price, 2)
        tmp = "UPDATE home_balance SET balance=%f WHERE user_id=%d" % (m_userBalance, user_id)
    elif check_status == 'Fail':     
        tmp = "INSERT INTO cart_order_history (User_id, Product_id, Checker_id, Checker_status, Checker_response_text, Checker_response_full, Checker_date) VALUES (%d, %d, %d, '%s', '%s', '%s', '%s')" % (user_id, product_id, checker_id, 'Fail', checker_response_text, checker_response_full, str(datetime.now()))
        mycursor.execute(tmp)
        tmp = "UPDATE cart_shop_data SET Sold_unsold='%s', Sold_date='%s' WHERE id=%d" % ('REFUND', str(datetime.now()), product_id)
        mycursor.execute(tmp)
        tmp = "SELECT balance FROM home_balance WHERE user_id=%d" % (user_id)
        mycursor.execute(tmp)
        m_result = mycursor.fetchall()
        m_userBalance = float(m_result[0][0])
        m_userBalance = round(m_userBalance + price - checker_price, 2)
        tmp = "UPDATE home_balance SET balance=%f WHERE user_id=%d" % (m_userBalance, user_id)
        mycursor.execute(tmp)

    mydb.commit()
    mycursor.close()
    mydb.close()
    return check_status

if __name__ == '__main__':
    product_id = int(sys.argv[1])
    checker_id = int(sys.argv[2])
    user_id = int(sys.argv[3])
    result = check(product_id, checker_id, user_id)
    print(result)