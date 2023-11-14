import pygame

class World():
    def __init__(self, data,  map_img) -> None:
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_img

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for object in layer["objects"]:
                    waypoint_data = object["polyline"]
                    self.process_waypoints(waypoint_data)
    
    def process_waypoints(self, data ):
        for point in data:
             temp_x = point.get("x")
             temp_y = point.get("y")
             self.waypoints.append((temp_x, temp_y  ))


    def draw(self, screen):
        screen.blit(self.image, (0,0))