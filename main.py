from client import student,types
from dotenv import load_dotenv
import os

load_dotenv()
user=student(tckn=os.getenv("TCKN"),passwd=os.getenv("PASSWD"),show=True)
user.login()
user.go(types.go.dersler("Matematik"))
user.go(types.go.dersler("Fen Bilimleri"))
