import yaml

class IMap:
    def __init__(self, data, tile_size) -> None:
        self.data = data
        self.height = len(data)
        self.width = len(data[0])
        self.tile_size = tile_size

instance: IMap = None