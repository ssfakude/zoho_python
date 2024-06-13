import pickle
from pathlib import Path
from argon2 import hash_password
import streamlit_authenticator as stauth
names = ["Simphiwe Fakude", "Robert joubert","Jean-Pierre Myburg"]
usernames = ["simphiwef", "JP"]
passwords = ["sleepingdog" ,"2Birds1Stone"]
hashed_passwords = stauth.Hasher(passwords).generate() # bycrat algor
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
