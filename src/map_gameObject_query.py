import game_data

from GameObject import GameObject
from typing import List

# game object setup
class Map_GameObject_Query:
    def __init__(self, game_objects: List[GameObject]) -> None:
        self.game_objects = game_objects
        self.map = game_data.SMap.instance
        self.transform = game_data.SIsometricTransform.instance

        self.object_query_tree: dict = {}
    
    def get_object_list_at(self, x, y) -> List:
        query = self.object_query_tree.get((x,y))
        if query == None:
            return []
        else:
            return query

    def update(self):
        self.object_query_tree.clear()
        for o in self.game_objects:
            x, y = o.getPivotPos()
            key = x//self.map.tile_size, y//self.map.tile_size
            if self.object_query_tree.get(key) == None:
                self.object_query_tree[key] = []
            self.object_query_tree[key].append(o)
            self.object_query_tree[key].sort(key=lambda o: o.get_transformed_isometric_screen_pivot_coordinate()[1])