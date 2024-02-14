"""
The create_hotel method creates a new JSON file for the hotel.
The delete_hotel method deletes the JSON file of the hotel if it exists.
The display_hotel_info method reads and displays hotel information from the JSON file.
The modify_hotel_info method renames the JSON file of the hotel.
The reserve_room method adds a reservation to the JSON file of the hotel.
The cancel_reservation method removes a reservation from the JSON file of the hotel.
"""


import os
import json

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = {}
        self.reservations = []

    def create_hotel(self):
        if not os.path.exists("hotels"):
            os.makedirs("hotels")
        with open(f"hotels/{self.name}.json", "w") as file:
            json.dump({"name": self.name, "rooms": {}, "reservations": []}, file)

    @staticmethod
    def delete_hotel(name):
        file_path = f"hotels/{name}.json"
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{name} hotel has been deleted.")
        else:
            print(f"{name} hotel does not exist.")

    def display_hotel_info(self):
        file_path = f"hotels/{self.name}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                hotel_data = json.load(file)
                print(f"Hotel Name: {hotel_data['name']}")
                print("Rooms:")
                for room_number, room_type in hotel_data['rooms'].items():
                    print(f"   Room Number: {room_number}, Type: {room_type}")
                print("Reservations:")
                for reservation in hotel_data['reservations']:
                    print(f"   Guest Name: {reservation['guest_name']}, Room Number: {reservation['room_number']}, Start Date: {reservation['start_date']}, End Date: {reservation['end_date']}")
        else:
            print(f"{self.name} hotel does not exist.")

    def modify_hotel_info(self, new_name):
        file_path = f"hotels/{self.name}.json"
        new_file_path = f"hotels/{new_name}.json"
        if os.path.exists(file_path):
            os.rename(file_path, new_file_path)
            self.name = new_name
            print("Hotel information modified successfully.")
        else:
            print(f"{self.name} hotel does not exist.")

    def reserve_room(self, guest_name, room_number, start_date, end_date):
        file_path = f"hotels/{self.name}.json"
        if os.path.exists(file_path):
            with open(file_path, "r+") as file:
                hotel_data = json.load(file)
                if room_number in hotel_data['rooms']:
                    reservation = {"guest_name": guest_name, "room_number": room_number, "start_date": start_date, "end_date": end_date}
                    hotel_data['reservations'].append(reservation)
                    file.seek(0)
                    json.dump(hotel_data, file)
                    print("Room reserved successfully.")
                else:
                    print(f"Room number {room_number} does not exist in {self.name} hotel.")
        else:
            print(f"{self.name} hotel does not exist.")

    def cancel_reservation(self, guest_name, room_number, start_date, end_date):
        file_path = f"hotels/{self.name}.json"
        if os.path.exists(file_path):
            with open(file_path, "r+") as file:
                hotel_data = json.load(file)
                for reservation in hotel_data['reservations']:
                    if reservation['guest_name'] == guest_name and reservation['room_number'] == room_number and reservation['start_date'] == start_date and reservation['end_date'] == end_date:
                        hotel_data['reservations'].remove(reservation)
                        file.seek(0)
                        json.dump(hotel_data, file)
                        print("Reservation canceled successfully.")
                        return
                print("No matching reservation found.")
        else:
            print(f"{self.name} hotel does not exist.")
