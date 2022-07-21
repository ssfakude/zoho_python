from __future__ import print_function
from imaplib import _Authenticator
from itertools import count
import json
import pickle
from pathlib import Path
from unicodedata import name
import streamlit_authenticator as stauth
from re import X
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import numpy as np
import requests
import timeit
import altair as alt
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import datetime as dt
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta # to add days or years
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

start = timeit.default_timer()
st.set_page_config(page_title="1 Nav sync Zoho", page_icon="rc_logo.ico")


CLIENT_ID = '1000.0G3DK4Y761UL7AHEKYKIMHQLTXWJLO'
CLIENT_SECRET = '7752cf983497614b4144c1fa482b21fd378db6a0fa'
ZOHO_DATA = {
    "access_token": "1000.cc8e2f20b4b26629fd81166df1c745e5.e223cc6c2d4f877eff83c24eaaaca5ab",
    "refresh_token": "1000.5b482d0f8da0e2aa6773b97f0cc9d7f9.29b3cbfd1dc7314dc3a4ec12394434b1",
    "api_domain": "https://www.zohoapis.com",
    "token_type": "Bearer",
    "expires_in": 3600
}

def refresh_auth():

    url = "https://accounts.zoho.com/oauth/v2/token?refresh_token=1000.5b482d0f8da0e2aa6773b97f0cc9d7f9.29b3cbfd1dc7314dc3a4ec12394434b1&client_id=1000.0G3DK4Y761UL7AHEKYKIMHQLTXWJLO&client_secret=7752cf983497614b4144c1fa482b21fd378db6a0fa&grant_type=refresh_token"
    r = requests.post(url)
    data = json.loads(r.text)
    if 'access_token' in data:
        ZOHO_DATA['access_token'] = data['access_token']

    return data['access_token']


access_token = refresh_auth()

not_found_order =[]
not_found_invoiced =[]
not_found_return =[]
time_out =[]
#----------User AUth----------
names = ["Simphiwe Fakude", "Robert Jacobs", "Robert joubert","Jean-Pierre Myburg","Paul Oosthuizen", "Lee Douglas Webster", "Nazley Miranda", "Cindy Santamaria","Natasha Naidoo", "Carla kolbe",  "RC Admin"]
usernames = ["simphiwef", "robertj","robert", "jp","paulo","leew","nazleym","cindys","natashan","carla",  "rcadmin"]
file_path  = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"rc_dashboard", "abcdef", cookie_expiry_days=30 )# cookie
name, authentication_status, username = authenticator.login('Please Login', 'main')


if authentication_status == False:
    st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')
elif authentication_status:
   
    def load_lottieurl(url: str): #load from the web
       
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    st.write(f'Welcome  *{name}*')
    lottie_dog=load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_xBGyhl.json")
    with st_lottie_spinner(lottie_dog, width= 300, key="dog"):

        @st.cache()
        def read_file(data_file):
            #st.write(file_details)
            xls = pd.ExcelFile(data_file)
            
            try:
                df_Order = pd.read_excel(xls, 'Open Released')
            except Exception as e:
                st.error("Incorect Sheet name for Open Released:(")
                st.stop()
            try:
                df_Invoiced = pd.read_excel(xls, 'Posted Invoices')
            except Exception as e:
                st.error("Incorect Sheet name for Posted Invoices:(")
                st.stop() 
            try:
                df_Return = pd.read_excel(xls, 'SRT')
            except Exception as e:
                st.error("Incorect Sheet name for SRT:(")
                st.stop()
            return df_Order, df_Invoiced, df_Return




        #time.sleep(4)
        def main():
            st.title("1 Nav + Zoho Integration")
            st.subheader("The file should contain this 3 sheets:")
            data_file = st.file_uploader("[Open Released, Posted Invoices ,SRT]",type=['xlsx'])
            # lottie_nodata=load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_5awivhzm.json")
            # st_lottie(lottie_nodata, key="load", width=600)
            if st.button("Process"):

                if data_file is not None:
                    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}

                    df_Order = read_file(data_file)[0]
                    df_Invoiced = read_file(data_file)[1]
                    df_Return =read_file(data_file)[2]
                    
                    # st.write(file_details)
                    # df = pd.read_csv(data_file)
                    # left_column, middle_column, right_column  = st.columns(3)
                    # with left_column:
                    #     st.dataframe(df_Order)
                    # with middle_column:
                    #     st.dataframe(df_Invoiced)
                    # with right_column:
                    #     st.dataframe(df_Return)

                    
                    headers = {"Authorization" : "Zoho-oauthtoken "+access_token, "orgId": "725575894"}
                    latest_iteration = st.empty()
                    print("-----------------------Open Released-------------------")
                    len_df_Order =len(df_Order.index)
                    for i, j in df_Order.iterrows():
                        so_number = j[1]
                        if len_df_Order - i == 1:
                            latest_iteration.text('Done updating Open Released spreadsheet')
                        else:
                            latest_iteration.text(f'Open Released: {len_df_Order - i} records left - {j[1]}')
                        if pd.isna(so_number) ==True:
                            break
                        else:
                            
                            so_number = so_number[5:]
                            dateTime= str(j[2])
                            dateTime = dateTime.replace(" ", "T")
                            dateTime = dateTime[:19]+".000Z"
                            cf_1nav_customer_name= j[4]
                            nav_overdue_bal = j[6]
                            nav_credit_hold =j[5]
                            cf_1nav_cus_price_grp =j[8]
                            cf_1nav_sales_resp = j[9]
                            cf_1nav_net_weight = j[11]
                            cf_1nav_amount = j[18]
                            cf_1nav_location_code = j[10]
                            now = datetime.now()
    
                         
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            sync_date=dt_string.replace(" ", "T")+ ".000Z"
                            status_ = j[0]
                            if status_ == "Open":
                                #desk_status = "Approval Rejected"
                                desk_status = "Pending - finance query"
                            else:
                                desk_status = "Pending - awaiting shipment"

                            
                            if nav_overdue_bal  <1 or str(nav_overdue_bal) =="FALSE" :
                                cf_1nav_overdue_bal = "false"
                        
                            else:
                                cf_1nav_overdue_bal= "true"



                            if  nav_credit_hold <1 or str(nav_credit_hold) =="FALSE" :
                                cf_1nav_credit_hold = "false"
                            else:
                                cf_1nav_credit_hold ="true"


                            URL = "https://desk.zoho.com/api/v1/tickets/search?limit=1&customField1=cf_s_o_number:"+so_number
                            



                            try:
                                req = requests.get(url = URL, headers= headers)
                
                            except:
                                print("Connection refused by the server..")
                                print("Let me sleep for 5 seconds")
                                print("ZZzzzz...")
                                time.sleep(2)
                                print("Was a nice sleep, now let me continue...")
                    
                        
                            
                            if req.status_code == 200:
                                data_respo = json.loads(req.text)
                                ticket_id = data_respo['data'][0]['id']
                                # So Number founf then update fields
                                url = "https://desk.zoho.com/api/v1/tickets/"+ticket_id
                                data ={ "status":desk_status,
                                    "cf":{
                                    "cf_1_nav_sync":"true",
                                    "cf_1nav_status":status_,
                                    "cf_1nav_customer_name":cf_1nav_customer_name,
                                    "cf_1nav_cus_price_grp":cf_1nav_cus_price_grp,
                                    "cf_1nav_sales_resp":cf_1nav_sales_resp,
                                    "cf_1nav_date_time":dateTime,
                                    "cf_1nav_amount":cf_1nav_amount,
                                    "cf_1nav_net_weight":cf_1nav_net_weight,
                                    "cf_1nav_overdue_bal":cf_1nav_overdue_bal,
                                    "cf_1nav_credit_hold":cf_1nav_credit_hold,
                                    "cf_1nav_location_code": cf_1nav_location_code,
                                    "cf_1nav_sync_time": sync_date,

                                    "cf_added_by": name
                                    }
                                }	
                                try:
                                    r = requests.patch(url, headers=headers, json=data)
                                except:
                                    print("Connection refused by the server..")
                                    print("Let me sleep for 5 seconds")
                                    print("ZZzzzz...")
                                    time_out.append(so_number)
                                    time.sleep(3)
                                    print("Was a nice sleep, now let me continue...")
                                
                            
                            else:
                                not_found_order.append(so_number)
                            print("Search: ", req.status_code, " Update: ",req.status_code, " - ", so_number)
                    
                    print("-----------------------Invoiced-------------------")
                    latest_iteration = st.empty()
                    len_df_Invoiced =len(df_Invoiced.index)
                    for i, j in df_Invoiced.iterrows():
                        if len_df_Invoiced - i == 1:
                            latest_iteration.text('Done updating Invoiced spreadsheet')
                        else:
                            latest_iteration.text(f'Invoiced: {((len_df_Invoiced - i))} records left - {j[6]}')
                        so_number = j[6]
                        if pd.isna(so_number) ==True:
                            break
                        else:
                            
                            so_number = so_number[5:]
                            cf_1nav_customer_name= j[2]
                            #cf_1nav_cus_price_grp =j[8]
                            cf_1nav_sales_resp = j[7]
                            cf_1nav_net_weight = j[9]
                            cf_1nav_amount = j[3]
                            cf_1nav_location_code = j[8]
                            cf_1nav_req_del_date = str(j[5])[:10]
                            cf_1nav_shipping_date = str(j[11])[:10]
                            cf_1nav_doc_date =str(j[10])[:10]
                            now = datetime.now()
    
                         
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            sync_date = dt_string.replace(" ", "T")+ ".000Z"
                        
                        
                            URL = "https://desk.zoho.com/api/v1/tickets/search?limit=1&customField1=cf_s_o_number:"+so_number
                            headers = {"Authorization" : "Zoho-oauthtoken "+access_token, "orgId": "725575894"}
                            

                            try:
                                req = requests.get(url = URL, headers= headers)
                               
                            except:
                                print("Connection refused by the server..")
                                print("Let me sleep for 3 seconds")
                                print("ZZzzzz...")
                                time.sleep(3)
                                print("Was a nice sleep, now let me continue...")
                            

                            if req.status_code == 200:
                                data_resp = json.loads(req.text)
                                ticket_id = data_resp['data'][0]['id']
                                url = "https://desk.zoho.com/api/v1/tickets/"+ticket_id
                                # So Number founf then update fields
                                data ={
                    "cf":{"status": "Closed",
                        "cf_1_nav_sync":"true",
                        "cf_1nav_status":"Invoiced",
                        "cf_1nav_customer_name":cf_1nav_customer_name,
                        "cf_1nav_sales_resp":cf_1nav_sales_resp,
                        "cf_1nav_amount":cf_1nav_amount,
                        "cf_1nav_net_weight":cf_1nav_net_weight,
                        "cf_1nav_req_del_date":cf_1nav_req_del_date,
                        "cf_1nav_shipping_date":cf_1nav_shipping_date,
                        "cf_1nav_location_code": cf_1nav_location_code,
                          "cf_1nav_doc_date": ,
                        "cf_1nav_overdue_bal":"false",
                        "cf_1nav_credit_hold":"false",
                        "cf_1nav_sync_time": sync_date,
                         "cf_added_by": name
                    }
                    }		
                                try:
                                    r = requests.patch(url, headers=headers, json=data)
                                
                                except:
                                    print("Connection refused by the server..")
                                    print("Let me sleep for 3 seconds")
                                    print("ZZzzzz...")
                                    time.sleep(3)
                                    time_out.append(so_number)
                                    print("Was a nice sleep, now let me continue...")
                            
                            
                            else:
                                not_found_invoiced.append(so_number)
                            print("Search: ", req.status_code, " Update: ",req.status_code, " - ", so_number)
                    

                    print("-----------------------SRT-------------------")
                    len_df_Return =len(df_Return.index)
                    for i, j in df_Return.iterrows():
                        so_number = j[0]
                        if len_df_Return - i == 1:
                            latest_iteration.text('Done updating SRT spreadsheet ')
                        else:
                            latest_iteration.text(f'SRT: {len_df_Return - i} records left - {j[0]}')
                        if pd.isna(so_number) ==True:
                            break
                        else:
                            
                            cf_1nav_customer_name = j[2]
                            cf_1nav_sales_resp = j[3]
                            so_number = so_number[6:]
                            cf_1nav_location_code =j[4]
                            cf_1nav_doc_date =str(j[8])[:10]
                            now = datetime.now()
    
                         
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            sync_date = dt_string.replace(" ", "T")+ ".000Z"
                            
                            URL = "https://desk.zoho.com/api/v1/tickets/search?limit=1&customField1=cf_s_o_number:"+so_number
                            headers = {"Authorization" : "Zoho-oauthtoken "+access_token, "orgId": "725575894"}
                            
                            
                            try:
                                req = requests.get(url = URL, headers= headers)
                                
                            except:
                                print("Connection refused by the server..")
                                print("Let me sleep for 3 seconds")
                                print("ZZzzzz...")
                                time.sleep(3)
                                print("Was a nice sleep, now let me continue...")


                            if req.status_code == 200:
                                data_resp = json.loads(req.text)
                                ticket_id = data_resp['data'][0]['id']
                                # So Number founf then update fields
                                url = "https://desk.zoho.com/api/v1/tickets/"+ticket_id
                            
                                data ={
                                    "cf":{
                        "cf_1nav_status":"Processed",
                        "cf_1_nav_sync":"true",
                        "cf_1nav_customer_name":cf_1nav_customer_name,
                        "cf_1nav_sales_resp":cf_1nav_sales_resp,
                        "cf_1nav_location_code": cf_1nav_location_code,
                        "cf_1nav_doc_date": cf_1nav_doc_date,
                        "cf_1nav_overdue_bal":"false",
                        "cf_1nav_credit_hold":"false",
                        "cf_1nav_sync_time": sync_date,
                         "cf_added_by": name

                            }
                            }
                                try:
                                    r = requests.patch(url, headers=headers, json=data)
                                
                                except:
                                    print("Connection refused by the server..")
                                    print("Let me sleep for 5 seconds")
                                    print("ZZzzzz...")
                                    time.sleep(5)
                                    time_out.append(so_number)
                                    print("Was a nice sleep, now let me continue...")
                                
                            else:
                                not_found_return.append(so_number)
                            print("Search: ", req.status_code, " Update: ",req.status_code, " - ", so_number)
                    stop = timeit.default_timer()
                    execution_time = stop - start
                    c = """<html>
                    <head></head>
                    <body><p>Hi Naz and Cindy, <br><br></p></body>
                    </html>"""
                    space= """<html>
                    <br><br>
                    </html>"""
                    content = c+"Here is the lists of all the SO Number that are not on Zoho Desk, but in 1 Nav: " + space +"""<html>
                    <head></head><body><p>------------------ <strong>Open Released</strong>------------------- <br> </p></body>
                    </html>"""+str(not_found_order)+"""<html>
                    <head></head>
                    <br>
                    <body><p>---------------------<strong>Posted Invoices</strong>--------------------- <br></p></body>
                    </html>"""+ str(not_found_invoiced)+"""<html>
                    <head></head>
                    <br>
                    <body><p>-----------------------<strong>SRT</strong>---------------------------- <br></p></body>
                    </html>"""+ str(not_found_return)+"""<html>
                    <head></head>
                    <br>
                    <body><p>-----------------------<strong>Time Out</strong>---------------------------- <br></p></body>
                    </html>"""+ str(time_out)
                    
            


                    email_body = """<html>
                    <head></head>
                    <body><p>Hi, <br><br></p> The Integration has been completed<br><br> </body>
                    </html>""" +"Runtime: "+ str(round(execution_time,2))+" seconds."

                    url = "https://desk.zoho.com/api/v1/tickets"
                    data ={ "subject":"SO Number not Found in CRM",
                        "departmentId":"541303000000434081",

                "status" : "Open",
                "teamId":"541303000031453272",
                        "contactId":"541303000024559001",
                    "description":content, 
    
                    "cf":{
                    "cf_ticket_type":"1Nav error",
                    }
                    }
                    r = requests.post(url, headers=headers, json=data)
                    
                    url = 'https://mail.zoho.com/api/accounts/6014958000000008002/messages'
                
                    data = {
                    "fromAddress":"simphiwef@boomerangsa.co.za",
                    "toAddress": username+"@boomerangsa.co.za",
                    "ccAddress": "simphiwef@boomerangsa.co.za",
                    "bccAddress": "",
                    "subject": "Zoho Desk Integration completed",
                    "content": email_body,
                    "askReceipt": "no"
                    }
                    headers = {
                        'Authorization': 'Zoho-oauthtoken ' + ZOHO_DATA['access_token']
                    }
                    r = requests.post(url, headers=headers, json=data)

                   



                    st.markdown("<h2 style='text-align: center; color: white;'>Synchronization completed!</h2>", unsafe_allow_html=True)
                    lottie_nodata=load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_rjqwaenm.json")
                    st_lottie(lottie_nodata, key="done", width=270)
                    print("-----------------------------------------------")

                    print (f"Run Time: {execution_time:.2f} Seconds")
                    st.subheader(f"Run Time: {execution_time:.2f} Seconds")
                    


        if __name__ == '__main__':
            main()




    # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """2218146
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #title {
                text-align: center
                </style>
                """
        
st.markdown(hide_st_style, unsafe_allow_html=True)


