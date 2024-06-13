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

#://returnxdigital.leadbyte.co.uk/api/submit.php?returnjson=yes&campid=FUNERAL-COVER&sid=24845&testmode=yes&email=test@test.com&firstname=Test&lastname=Test&phone1=0613394600&optinurl=http://url.com&optindate=INSERTVALUEyes&grossmonthlyincome=INSERTVALUE&acceptterms=true&offer_id=2512






@st.cache_data
def read_file(data_file):

    xls = pd.ExcelFile(data_file)

    try:
        df_leads = pd.read_excel(xls, 'Leads')
    except Exception as e:
        st.error("Incorect Sheet name for Leads:(")
        st.stop()

    return df_leads




#time.sleep(4)
def main():
    st.title("JP- Integration")
    st.subheader("testtttt:")
    data_file = st.file_uploader("[Leads]",type=['xlsx'])
    # lottie_nodata=load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_5awivhzm.json")
    # st_lottie(lottie_nodata, key="load", width=600)
    if st.button("Process"):

        if data_file is not None:
            file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}

            df_Order = read_file(data_file)[0]

            
            
            latest_iteration = st.empty()
            print("-----------------------Leads------------------")
            len_df_leads =len(df_leads.index)
            for i, j in df_leads.iterrows():
                so_number = j[1]
                if len_df_Order - i == 1:
                    latest_iteration.text('Done Loading Leads')
                else:
                    latest_iteration.text(f'Leads: {len_df_leads - i} records left - {j[1]}')
                if pd.isna(so_number) ==True:
                    break
                else:

                    email = j[0]
                    firstname=  j[1]
                    lastname =  j[3]
                    dateTime =  j[4]
                    phone1= j[5]
                    optindate = j[6]
                    nav_credit_hold =j[7]
                    testmode =j[8]
                    grossmonthlyincome = j[9]
                    acceptterms = j[10]
                    offer_id = j[11]
                    
                    url = "https://returnxdigital.leadbyte.co.uk/api/submit.php?returnjson=yes&campid=FUNERAL-COVER&sid=24845&testmode=yes&email=test@test.com&firstname=Test&lastname=Test&phone1=0613394600&optinurl=http://url.com&optindate=INSERTVALUEyes&grossmonthlyincome=INSERTVALUE&acceptterms=true&offer_id=2512"
                    
                    #dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                    # sync_date=dt_string.replace(" ", "T")+ ".000Z"
                    
                    
                    
                    #response = requests.post(url = url)
                    #print("Leads - ",response.status_code)
                    
            st.markdown("<h2 style='text-align: center; color: white;'>Synchronization completed!</h2>", unsafe_allow_html=True)
            #lottie_nodata=load_lottieurl("https://lottie.host/?file=e686c78b-e554-498d-aaa1-e045ea2e2df9/iZMW2qsupf.json")
            lottie_nodata=load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_rjqwaenm.json")
            #st_lottie(lottie_nodata, key="done", width=270) https://lottie.host/?file=e686c78b-e554-498d-aaa1-e045ea2e2df9/iZMW2qsupf.json
            st.balloons()
            print("-----------------------------------------------")

            print (f"Run Time: {execution_time:.2f} Seconds")
            st.subheader(f"Run Time: {execution_time:.2f} Seconds")
                        


            if __name__ == '__main__':
                main()




    # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                #title {
                text-align: center
                </style>
                """
        
st.markdown(hide_st_style, unsafe_allow_html=True)


