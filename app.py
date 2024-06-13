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
st.set_page_config(page_title="AUTO GENERAL INTEGRATION", page_icon="")

#://returnxdigital.leadbyte.co.uk/api/submit.php?returnjson=yes&campid=FUNERAL-COVER&sid=24845&testmode=yes&email=test@test.com&firstname=Test&lastname=Test&phone1=0613394600&optinurl=http://url.com&optindate=INSERTVALUEyes&grossmonthlyincome=INSERTVALUE&acceptterms=true&offer_id=2512


def floatify(value):

 
    if pd.isna(value) ==True:
        return ""
    if ":" in str(value):
        return 0.0
    else:
   
        float_= value.replace(' ','')
        return float(float_.replace(',','.'))
not_found_order =[]
not_found_invoiced =[]
not_found_return =[]
time_out =[]
#----------User AUth----------
names = ["Simphiwe Fakude", "Jean-Pierre Myburg"]
usernames = ["simphiwef", "JP"]
file_path  = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"aspol", "abcdef", cookie_expiry_days=30 )# cookie
name, authentication_status, username = authenticator.login('Please Login', 'main')


if authentication_status == False:
    st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')
elif authentication_status:
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
        st.title("AUTO GENERAL INTEGRATION")
        st.subheader("NB, make sure the file is type XLSX:")
        data_file = st.file_uploader("[Leads]",type=['xlsx'])
        campaign = st.radio(
"Select Campaign",
["BUDGET-BDM", "DIALDIRECT-DDMP3", "AUTO_GENERAL-AGPI", "FIRST_WOMAN-FDMP3"],
index=None,
)

        st.write("You selected:", campaign)
        successful_responses = []

        if st.button("Process" ):
            if campaign == None:
                st.error("Please Select Campaign")
            else:
                
                if data_file is not None:
                    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}

                    df_leads = read_file(data_file)
    
                    
                
                    latest_iteration = st.empty()
                    print("-----------------------Leads------------------")
                    len_df_leads =len(df_leads.index)
                    
    

                    for i, j in df_leads.iterrows():
                        email = j[2]
                        if len_df_leads - i == 1:
                            latest_iteration.text('Done Loading Leads')
                        else:
                            latest_iteration.text(f'Leads: {len_df_leads - i} records left - {j[2]}')
                        if pd.isna(email) ==True:
                            break
                        else:
                        
                            
                            firstname=  j[0]
                            lastname =  j[1]
                            email = str(j[2])
                            id_number =  str(j[4])
        
                            comments  =str(j[5])
                            phone1= str(j[3])
                            if phone1[0] !="0":
                                phone1= "0"+str(j[3])
    
                            sid ="99786998"
                            
                            if campaign =="BUDGET-BDM":
                                campid = "ALPHA-TLSRBDGT-WARM"
                            # if campaign =="DIALDIRECT-DDMP3":
                            #     campid = "ALPHA-TLSR-DIAL-WARM"
                            # if campaign =="AUTO_GENERAL-AGPI":
                            #     campid = "ALPHA-TLSRBDGT-WARM"
                            # if campaign =="FIRST_WOMAN-FDMP3":
                            #     campid = "ALPHA-TLSRBDGT-WARM"
                            


                        
                            current_datetime = datetime.now()
                            current_date_time = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                        
                            url = "https://icon.leadbyte.co.uk/restapi/v1.3/leads?campid="+campid+"&sid="+sid+"&email="+email+"&firstname="+firstname+"&lastname="+lastname+"&phone1="+phone1+"&id_number="+id_number+"&comments"+comments
                            
                            
                            headers = {"X_KEY": "42d9b732862a56c33ed59dca9f2b43b1", "Content-Type": "application/json"}
                            response = requests.post(url = url, headers=headers)
                            print("Leads- ",response.content, phone1)
                            if response.status_code == 200: 
                                status_ = "Success"
                            else:
                                    status_ = "Fail"
                            rep= response.content
                            response_data = json.loads(rep)
                            error_message = response_data.get('message', None)
                            # Extract errors array
                            errors = response_data.get('errors', None)
                            successful_responses.append({ 'Status': status_  , "Warning/Errors": errors,'Name': firstname,   'Last Name': lastname , 'Email': email, 'Phone': phone1, 'Id Number': id_number, 'Comments': comments })

                        
                        
                    if successful_responses:
                        df_successful_responses = pd.DataFrame(successful_responses)
                        st.write(df_successful_responses)
                    else:
                        st.write("No successful responses found.")  
                    st.markdown("<h2 style='text-align: center; color: white;'>Data Upload completed!</h2>", unsafe_allow_html=True)
                
                    print("-----------------------------------------------")
        
    
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


