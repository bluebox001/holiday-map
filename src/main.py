from photo_scanner import scan_photos, display_first_photo_info
from route_generator import generate_route

def main():
    # Ścieżka do folderu ze zdjęciami
    photos_path = 'data/photos/'
    

    display_first_photo_info(photos_path)


    # Skanowanie zdjęć i ekstrakcja metadanych
    photo_data = scan_photos(photos_path)
    
    # Generowanie trasy na podstawie metadanych zdjęć
    route = generate_route(photo_data)
    
    # Wypisanie wynikowej trasy (lub innego sposobu prezentacji)
    print("Wygenerowana trasa:")
    for point in route:
        print(f"{point['timestamp']} - Lokalizacja: {point['latitude']},{point['longitude']}")

if __name__ == "__main__":
    main()
