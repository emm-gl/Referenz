class Room:
    def __init__(self, room_number, room_type):
        self.room_number = room_number
        self.room_type = room_type

    def __str__(self):
        return f"Room Number: {self.room_number}, Type: {self.room_type}"

class Reservation:
    def __init__(self, guest_name, room, start_date, end_date):
        self.guest_name = guest_name
        self.room = room
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Reservation for {self.guest_name}, Room: {self.room.room_number}, Type: {self.room.room_type}, Start Date: {self.start_date}, End Date: {self.end_date}"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_room(self, room_number, room_type):
        room = Room(room_number, room_type)
        self.rooms.append(room)

    def make_reservation(self, guest_name, room_number, start_date, end_date):
        for room in self.rooms:
            if room.room_number == room_number:
                reservation = Reservation(guest_name, room, start_date, end_date)
                return reservation
        return None

# Example usage:
hotel = Hotel("Example Hotel")
hotel.add_room(101, "Single")
hotel.add_room(102, "Double")
hotel.add_room(103, "Suite")

reservation1 = hotel.make_reservation("John Doe", 101, "2024-02-14", "2024-02-16")
print(reservation1)

reservation2 = hotel.make_reservation("Jane Smith", 102, "2024-02-18", "2024-02-20")
print(reservation2)
