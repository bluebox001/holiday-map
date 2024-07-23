import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    exif_data = {}
    try:
        exif_info = image._getexif()
        if exif_info:
            for tag, value in exif_info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for gps_tag in value:
                        sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_decoded] = value[gps_tag]
                    exif_data['GPSInfo'] = gps_data
                exif_data[decoded] = value
            # Dodajemy czas z metadanych EXIF
            if 'DateTime' in exif_data:
                exif_data['timestamp'] = exif_data['DateTime']
            else:
                print("Brak daty i czasu w danych EXIF dla obrazu")
    except AttributeError:
        print("Nie znaleziono danych EXIF.")
    return exif_data

def get_photo_location(exif_data):
    """Parsuje dane GPS z danych EXIF i zwraca szerokość i długość geograficzną."""
    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        latitude = gps_info.get(2)  # Tuple (stopnie, minuty, sekundy)
        longitude = gps_info.get(4) # Tuple (stopnie, minuty, sekundy)

        if latitude and longitude:
            # Konwersja stopni, minut i sekund na wartość dziesiętną
            lat_decimal = latitude[0] + (latitude[1] / 60.0) + (latitude[2] / 3600.0)
            lon_decimal = longitude[0] + (longitude[1] / 60.0) + (longitude[2] / 3600.0)

            # Uwzględnienie kierunku N/S i E/W
            if gps_info.get(1) == 'S':
                lat_decimal = -lat_decimal
            if gps_info.get(3) == 'W':
                lon_decimal = -lon_decimal

            return {'latitude': lat_decimal, 'longitude': lon_decimal}
    return None

def scan_photos(directory):
    photos = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            with Image.open(filepath) as img:
                exif_data = get_exif_data(img)
                if 'timestamp' not in exif_data:
                    print(f"Brak timestamp dla {filename}")
                    continue
                location = get_photo_location(exif_data)
                if location:
                    location['timestamp'] = exif_data['timestamp']
                    photos.append(location)
                    print(f"Dodano lokalizację: {location}")  # Wydruk kontrolny
    return photos


def display_first_photo_info(directory):
    """Wyświetla informacje o pierwszym pliku JPG w podanym katalogu."""
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpg"):
            filepath = os.path.join(directory, filename)
            print(f"Nazwa pliku: {filename}")
            try:
                with Image.open(filepath) as img:
                    exif_data = get_exif_data(img)
                    print("Dane EXIF:")
                    for key, value in exif_data.items():
                        print(f"{key}: {value}")
            except IOError:
                print("Nie można otworzyć obrazu.")
            break  # Zatrzymujemy po pierwszym znalezionym pliku JPG

