#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import os.path
import datetime
import requests
import ssl
from io import StringIO

#import html 
#Cabecera con estilo

html_temp = """
<style>.icon-button {display:none}</style>
<div style="background-color:{};padding:{}">
<h1 style="color:#044a9d;text-align:center;">RESPONSIVE EMAIL GENERATOR</h1>
<h3 style="color:orange;text-align:center;margin-top:5px;">Developed by Raúl Fernández</h3>
<p style="margin-top:25px; margin-bottom:40px">Cada vez que rellenes un campo, recuerda dar al enter.</p>
</div>
"""
st.markdown(html_temp,unsafe_allow_html=True)
st.text('¿Vas a importar el HTML de alguna página?')

yes = st.checkbox('Sí')
if yes:
    url = st.text_input("Introduce la URL donde está la newsletter:")
    page = requests.get(url)
    texto = page.text

nope = st.checkbox('No')
if nope:
    texto = st.text_area("Pega tu código html aquí:")

recipient_mail = st.text_input('¿A quién vas a enviar el mail?')

#recipient = st.text_input('¿A quién deseas enviar el mail?')
subject = st.text_input('Introduce el asunto:')
st.text('¿Quieres adjuntar algo?')
yes2 = st.checkbox('Claro')
if yes2:
    file = st.file_uploader("Selecciona tu archivo:")
    filenaming = os.path.basename(file.name)
    
        
nope2 = st.checkbox('Ahora no')
if nope2:
    file =''
    filenaming= ''
    
st.text('¿Qué proveedor de correo usas?')
gmail = st.checkbox('Gmail')
if gmail:
    smtp='smtp.gmail.com'
    port= 587

office365 = st.checkbox('Office365')
if office365:
    smtp='smtp.office365.com'
    port= 25

outlook = st.checkbox('Outlook')    
if outlook:
    smtp='smtp-mail.outlook.com'
    port= 587
    
mail = st.checkbox('Mail')
if mail:
    smtp='smtp.mail.com'
    port= 587

def send_email(recipient_mail,
               subject,
               texto,
               filepath):
    
    email_sender = st.text_input('Introduce tu cuenta de correo:')
    name = st.text_input('El nombre que quieres que aparezca en el correo:')
    password = st.text_input('Introduce tu contraseña:', type="password")
    msg = MIMEMultipart()
    msg['From'] = name 
    msg['To'] = recipient_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(texto, 'html'))
    # Open PDF file in binary mode
    if file != '':
        with open(filenaming, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment", filename=filenaming),
    

    # Add attachment to message and convert message to string
            msg.attach(part)
            text = msg.as_string()
    
    try:
        server = smtplib.SMTP(smtp, port)
        server.ehlo()
        server.starttls() # Secure the connection
        server.login(email_sender, password)
        text = msg.as_string()
        server.sendmail(email_sender, recipient_mail.split(","), text)
        st.write(f'Estás de suerte. Email enviado.')
        server.quit()
    except:
        st.write(f"SMPT server connection error")
    return True


send_email(recipient_mail,
            subject,
            texto+'<div style="background-color:white; padding-bottom: 25px;font-size:smaller; color:DeepSkyBlue;text-align:center">Automated and developed via Python by Raúl Fernández</div>',
            filenaming)


# In[ ]:




