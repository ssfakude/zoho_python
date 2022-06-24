import pickle
from pathlib import Path
from argon2 import hash_password
import streamlit_authenticator as stauth
names = ["Simphiwe Fakude", "Robert Jacobs", "Robert joubert","Jean-Pierre Myburg","Paul Oosthuizen", "Lee Douglas Webster", "Nazley Miranda", "Cindy Santamaria","Natasha Naidoo", "Carla kolbe",  "RC Admin"]
usernames = ["simphiwef", "robertj","robert", "jp","paulo","leew","nazleym","cindys","natashan","carla",  "rcadmin"]
passwords = ["sleepingdog","Boom@123","master","doubleclick", "justdoit","tryme", "letmein","hello","master", "letmein" ,"2Birds1Stone"]
hashed_passwords = stauth.Hasher(passwords).generate() # bycrat algor
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
