from datetime import datetime

def sort_photos_by_time(photo_data):
    """Sortuje dane zdjęć po czasie od najstarszego do najmłodszego."""
    return sorted(photo_data, key=lambda x: datetime.strptime(x['timestamp'], '%Y:%m:%d %H:%M:%S'))

def generate_route(photo_data):
    """Generuje trasę na podstawie przesortowanych danych zdjęć."""
    sorted_photos = sort_photos_by_time(photo_data)
    print(f"Liczba posortowanych punktów: {len(sorted_photos)}")  # Wydruk kontrolny
    route = []
    for photo in sorted_photos:
        location = {
            'timestamp': photo['timestamp'],
            'latitude': photo['latitude'],
            'longitude': photo['longitude']
        }
        route.append(location)
        print(f"Trasa punkt: {location}")  # Wydruk kontrolny
    return route


