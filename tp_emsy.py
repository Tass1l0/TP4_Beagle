#-----------------------------------------------------
# Importing libraries and modules
#-----------------------------------------------------
import datetime                                                             # Library for date and time related stuff
import math                                                                 # Library for math stuff
import csv                                                                  # Library for csv handling stuff
import smtplib

from sensirion_i2c_driver import I2cConnection                              # Sensor driver
from sensirion_i2c_sht.sht4x import Sht4xI2cDevice                          # Sensor driver
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver  # Sensor driver

#-----------------------------------------------------
# Declaring the sensor object
#-----------------------------------------------------
sht40 = Sht4xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-2')))
                                                       
#-----------------------------------------------------
# Declaring functions
#-----------------------------------------------------
def read_sensor():
    try:
        t, rh = sht40.single_shot_measurement()
        # Watch out! t and rh are variable that contain not only the values but also the units.
        # You can print the values with the units (print(t)) or you can also recover only the value
        # by specifying which one: t.degrees_celsius or rh.percent_rh
    except Exception as ex:
        print("Error while recovering sensor values:", ex)
    else:
        return t, rh
    return 0 # In case something went wrong



def send_email(receiver, subject, message):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("ETML.ES.EMSY@gmail.com","cely neve caly akjz")
        sender = "ETML.ES.EMSY@gmail.com"

        headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Disposition': 'inline',
            'Content-Transfer-Encoding': '8bit',
            'From': sender,
            'To':receiver,
            'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
            'X-Mailer': 'python',
            'Subject': subject
        }
        # create the message
        msg = ''
        for key, value in headers.items():
            msg += "%s: %s\n" % (key, value)

        # add contents
        msg += "\n%s\n" % (message)

        try:
            server.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
            server.quit()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong.", ex)


def save_to_csv(filename, date, time, temperature, humidity, dew_point):
    with open(filename,'a') as file:
       writer = csv.writer(file)
       writer.writerow([date, time, temperature, humidity, dew_point])

#-----------------------------------------------------
# Main script 
#-----------------------------------------------------

if __name__ == "__main__":  # Runs only if called as a script but not if imported
    print("Hello and welcome to EMSY")
    # Calcul du Point de rosee
    COEFF1 = 17.62               #  BETA
    COEFF2 = 243.12              #  GAMA
    t, rh = read_sensor()        # Appel de la focntion read_sensor()
    rh_value = rh.percent_rh     # Recupere la valeur de l'humidite relative du capteur en pourcentage .
    t_value = str(t)             # Convertit la valeur de temperature en chaine de caracteres.
    t_value =t_value.split()     # Divise la chaine de caracteres qui contient la valeur de temperature 
    t_value =float(t_value[0])   # Convertit la premiere partie de la chaine divisee en un nombre flottant.
    # Calcul partie du numerateur
    part1 = COEFF2 * (math.log(rh_value / 100) + COEFF1 * t_value / (COEFF2 + t_value))
    # Calcul partie du denominateur
    part2 = COEFF1 - (math.log(rh_value / 100) + COEFF1 * t_value / (COEFF2 + t_value))
    # Divise les deux parties
    Prosee = part1 / part2 
    print("Temperature:", t_value, "°C")               # Affiche la temperature 
    print("Humidite relative:", rh_value, "%")         #Affiche la valeur de l'Humidite relative
    print("Point de Rosee:", round(Prosee, 2), "°C")   # Affiche Point de Rosee et l'arrondie 2 decimales


    system_datetime = datetime.datetime.now()               # Obtient l'heure et la date actuelles du systeme
    current_date = system_datetime.strftime("%d.%m.%Y")     # Prend l'heure actuelle au format jour/mois/annee
    current_time = system_datetime.strftime("%H:%M")        # Prend l'heure actuelle au format heure/minute
    print("Heure:", current_time)                           # Affiche l'heure
    print("Date", current_date)                             # Affiche la date
    #Engeristrer les donnees dans un fichier csv qui se trouve dans le chemin /home/debian/TempLog.csv
    save_to_csv('/home/debian/TempLog.csv', current_date, current_time, t_value,round(rh_value, 2), round(Prosee, 2))   


    # Controler si la temperature deppase la limite et envoyer le mail
    temperature_limite = 28.0
    if t_value > temperature_limite:                                # Si la temperature depasse 28°C
        print("Temperature limite depasse! ENVOI D'ALARME")
        subject = "Alarme de Temperature"
        message = f"La temperature a depasse la limite de {temperature_limite}°C. La temperature actuelle est de {t_value}°C."
        send_email("luis.pucuji@etml-es.ch", subject, message)      #Envoi du mail avec l'alarme
    else:
        print("Temperature dans la plage de securite :)")           # Si la temperature <= à 28°C afficher le texte...
