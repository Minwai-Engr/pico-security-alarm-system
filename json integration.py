import json


#security_levels [key : value
#                 key : value
#                 key : value
#                 key : value]


class Room:
    def __init__(self, room_number, building, opening_time, closing_time,
                 security_level):
        self.room_number = room_number
        self.building = building
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.open_hour_uids = set()
        self.closed_hour_uids = set()
        self.ocupied = False
        self.security_level = security_level
        room_details = {"Room Number": room_number, "Building": building, "Opening Time": opening_time,
                        "Closing Time": closing_time, "Ocupied": self.ocupied, "Security Level": security_level}
        json.dumps(room_details)
        print(str(room_details))
        with open("room_data.json", mode="w", encoding="utf-8") as write_file:
            json.dump(room_details, write_file)
    def print_room(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
    
    def add_open_uids(self, value):
        
        """ If a specific uid isn't currently an open_hour_uid, make it one"""
        if isinstance(value, (list, tuple)):
            for item in value:
                self.open_hour_uids.add(item) 
        else:
            self.open_hour_uids.add(value)
            
    def add_closed_uids(self, value):
        """If a specific uid or list of uids aren't currently a closed or open hour uid then make it one"""
        
        if isinstance(value, (list, tuple)):
            for item in value:
                self.closed_hour_uids.add(item)
                self.open_hour_uids.add(item)    
        else:
                self.closed_hour_uids.add(value)
                self.open_hour_uids.add(value)
        
    def remove_open_uids(self, value):
                
        """ If a specific uid is currently an open_hour_uid, remove it"""
        if isinstance(value, (list, tuple)):
            for item in value:
                self.open_hour_uids.remove(item) 
        else:
            self.open_hour_uids.remove(value)
        
    def remove_closed_uids(self, value):
        
        """If a specific uid or list of uids aren't currently a closed or open hour uid then make it one"""
        if isinstance(value, (list, tuple)):
            for item in value:
                self.closed_hour_uids.remove(item)
                self.open_hour_uids.remove(item)    
        else:
                self.closed_hour_uids.remove(value)
                self.open_hour_uids.remove(value)
        
    #def change_operating_hours(self, open_time, close_time):
    
    #def change_security_level(self, level):






class Uid:
    _registry = set()
    
    def __new__(cls, uid, first_name, last_name, position):
        if uid in cls._registry:
            return cls._registry
            print(ValueError(f"UID '{uid}' already exists."))
        

        uid_space = super().__new__(cls)
        cls._registry.add(uid)
        return uid_space
    def __init__(self, uid, first_name, last_name, position):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.position = position



        
roomA = Room("336B", "ELW", 7, 19, "lab")

bob = Uid(334, "bob", "bobby", "student")
jeremy = Uid(335, "jeremy", "jeremy", "student")
roomA.add_open_uids(bob.uid)
roomA.add_open_uids(jeremy.uid)

roomA.add_open_uids([13, 17])
roomA.add_closed_uids([15, 16, 17])
roomA.add_closed_uids(17)



roomA.print_room()


