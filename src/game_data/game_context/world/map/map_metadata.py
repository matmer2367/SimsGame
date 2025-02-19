class MapMetaData:
    def __init__(self,
                 tile_size = 0,
                 tile_columns = 0,
                 tile_rows = 0):
        self.width = tile_columns 
        self.height = tile_rows
        self.tile_size = tile_size