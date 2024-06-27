import json
import paho.mqtt.client as mqtt

# Détails du broker MQTT
broker = "localhost"
port = 1883
topic = "go-wallbox-lux"

# Chemin du fichier JSON
json_file_path = "file.json"

def read_json(file_path):
    with open(file_path, mode='r') as file:
        data = json.load(file)
    return data

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT !")
    else:
        print(f"Échec de la connexion, code de retour {rc}")

def on_publish(client, userdata, mid):
    print("Données publiées")

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker, port)
client.loop_start()  # Démarrer la boucle pour traiter le trafic réseau et les callbacks

# Lire le fichier JSON
json_data = read_json(json_file_path)

# Publier les données JSON sur le broker MQTT
message = json.dumps(json_data)
result = client.publish(topic, message)

# État du résultat
status = result.rc
if status == mqtt.MQTT_ERR_SUCCESS:
    print(f"Données envoyées au topic `{topic}`")
else:
    print(f"Échec de l'envoi du message au topic {topic}")

# Déconnexion du broker
client.loop_stop()  # Arrêter la boucle
client.disconnect()
