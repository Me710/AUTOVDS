import pywhatkit
import schedule
import time
from datetime import datetime
import csv
import os

current_image_number = 1


def send_image(phone_number, image_folder, caption=""):
    global current_image_number
    try:
        # Construire le nom du fichier image
        image_filename = f"{current_image_number}_{get_next_image_name(image_folder)}"
        image_path = os.path.join(image_folder, image_filename)

        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            print(f"L'image {image_path} n'existe pas. Réinitialisation à 1.")
            current_image_number = 1
            image_filename = f"{get_next_image_name(image_folder)}"
            image_path = os.path.join(image_folder, image_filename)

        pywhatkit.sendwhats_image(phone_number, image_path, caption, 10, True, 10)
        print(f"Image {image_filename} envoyée à {phone_number}")
        time.sleep(15)
        print("Onglets fermés")

        # Incrémenter pour la prochaine image
        current_image_number += 1
    except Exception as e:
        print(f"Erreur lors de l'envoi : {str(e)}")

def get_next_image_name(folder):
    files = [f for f in os.listdir(folder) if f.startswith(f"{current_image_number}_")]
    return files[0] if files else None

def schedule_posts(schedule_list):
    for item in schedule_list:
        schedule.every().day.at(item['time']).do(send_image, item['phone'], item['image'], item['caption'])
def load_schedule_from_csv(filename):
    schedule_list = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            schedule_list.append(row)
    return schedule_list

if __name__ == '__main__':
    # Configuration
    # Charger la configuration depuis le fichier CSV
    csv_filename = 'csv/schedule.csv'
    schedule_list = load_schedule_from_csv(csv_filename)

    # Planifier les publications
    schedule_posts(schedule_list)

    # Boucle principale
    while True:
        schedule.run_pending()
        time.sleep(20)
