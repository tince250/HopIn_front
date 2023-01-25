import googlemaps
import datetime
import polyline
import requests
from random import randrange

gmaps = googlemaps.Client(key="AIzaSyADf7wmEupGmb08OGVJR1eNhvtvF6KYuiM")

taxi_stops = [
    (45.265254, 19.830832),   # Stajaliste na Z stanici
    (45.253574, 19.862451),   # Stajaliste na djavi
    (45.235773, 19.827446),   # Stajaliste Ive Andrica Telep
    (45.259048, 19.837329),   # Stajaliste na Zitnom trgu
    (45.246540, 19.849282)    # Stajaliste kod menze
]

taxi_stop_waiting_in_seconds = 15


class VehicleInRide():

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.wait_on_taxi_stop_counter = 0

        if self.is_vehicle_in_ride():
            return 
        else:
            random_taxi_stop_index = randrange(0, len(taxi_stops))
            self.previous_taxi_stop_index = random_taxi_stop_index
            random_taxi_stop = taxi_stops[random_taxi_stop_index]

            self.driving_to_start_point = False
            self.driving_the_route = False
            self.driving_to_taxi_stop = True

            self.departure = self.vehicle.get_coordinates()
            self.destination = random_taxi_stop
            self.get_new_coordinates()


    def is_vehicle_in_ride(self):
        response = requests.get("http://localhost:4321/api/ride/driver/" + str(self.vehicle.driver_id) + "/accepted-started")
        print(response.status_code)
        if response.status_code == 200:
            return True
        return False

    def decide(self):
        self.update_vehicle_coordinates()

    def update_vehicle_coordinates(self):
        if len(self.coordinates) > 0:
            new_coordinates = self.coordinates.pop(0)
            requests.put("http://localhost:4321/api/vehicle/" + str(self.vehicle.vehicle_id) + "/location", json={
                'address': "random", 
                'latitude': new_coordinates[0],
                'longitude': new_coordinates[1]
            })
            self.vehicle.current_location.latitude = new_coordinates[0]
            self.vehicle.current_location.longitude = new_coordinates[1]
        elif len(self.coordinates) == 0 and self.driving_to_start_point:
            self.departure = self.destination
           # while (self.departure[0] == self.destination[0]):
            #    self.destination = start_and_end_points.pop(randrange(0, len(start_and_end_points)))
            self.get_new_coordinates()
            self.driving_to_start_point = False
            self.driving_the_route = True
        elif len(self.coordinates) == 0 and self.driving_the_route:
            random_taxi_stop = taxi_stops[randrange(0, len(taxi_stops))]
            #start_and_end_points.append(self.departure)
            self.departure = self.destination
            self.destination = random_taxi_stop
            self.get_new_coordinates()
            self.driving_the_route = False
            self.driving_to_taxi_stop = True
        elif len(self.coordinates) == 0 and self.driving_to_taxi_stop:
            random_taxi_stop_index = randrange(0, len(taxi_stops))
            if random_taxi_stop_index == self.previous_taxi_stop_index:
                random_taxi_stop_index = (random_taxi_stop_index + 1) % len(taxi_stops)
            random_taxi_stop = taxi_stops[random_taxi_stop_index]
            #start_and_end_points.append(self.departure)
            # self.departure = random_taxi_stop
            if self.is_wait_on_taxi_stop_finished():
                self.departure = self.vehicle.get_coordinates()
                self.destination = random_taxi_stop
                self.get_new_coordinates()

                #obrni posle
                self.driving_to_taxi_stop = True
                self.driving_to_start_point = False


    def get_new_coordinates(self):
        departure_to_string = ', '.join(str(coordinate) for coordinate in self.departure)
        destination_to_string = ', '.join(str(coordinate) for coordinate in self.destination)
    

        directions_result = gmaps.directions(departure_to_string,
                                            destination_to_string,
                                            mode="transit",
                                            arrival_time=datetime.datetime.now() + datetime.timedelta(minutes=5))

        decoded_polyline = polyline.decode(directions_result[0]["legs"][0]["steps"][0]['polyline']["points"], 5)
        self.coordinates = []
        for coordinate in decoded_polyline:
            self.coordinates.append(coordinate)

    def is_wait_on_taxi_stop_finished(self):
        self.wait_on_taxi_stop_counter += 1
        if self.wait_on_taxi_stop_counter == taxi_stop_waiting_in_seconds:
            self.wait_on_taxi_stop_counter = 0
            return True
        return False
