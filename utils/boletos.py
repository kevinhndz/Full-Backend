import os
from dotenv import load_dotenv
from datetime import datetime, timedelta  
from jose import jwt, JWTError    
             
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")        
         
def crear_boleto(usuario_id: int, usuario: str):  
    expira_en = datetime.utcnow() + timedelta(minutes=30)  
    
    datos = {                             
        "user_id": usuario_id,
        "user": usuario,
        "exp": expira_en
    }
    
    boleto = jwt.encode(  datos, 
                          SECRET_KEY, 
                         algorithm="HS256"
                         
                         )  
    
    return boleto                         


def verificar_boleto(token: str):
    try:
        
        datos = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return datos  
    
    except JWTError:
        
        return None