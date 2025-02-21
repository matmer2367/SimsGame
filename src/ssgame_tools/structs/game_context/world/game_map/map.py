from .map_metadata import MapMetaData


class Map:
    def __init__(self,
                 data = [[]],
                 tile_size = 0):
        self.data = data
        self.meta_data = MapMetaData(tile_size=tile_size, tile_rows=len(data), tile_columns=len(data[0]))