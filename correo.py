from email.message import EmailMessage
import smtplib
remitente = "jfvasquez59@misena.edu.co"
destinatario = "juanfernandovazquezdiaz@gmail.com"
mensaje = "<h1>¡Hola, mundo!</h1>"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Correo de prueba"
email.set_content(mensaje, subtype='html')
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
smtp.login(remitente, "ekckjctqseuvppot")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()