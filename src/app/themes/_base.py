from displayio import TileGrid


class BaseTheme:
    def __init__(self, display):
        self.display = display
        self.frame = 0

    async def setup(self):
        pass

    async def loop(self):
        self.frame += 1


class BaseSprite(TileGrid):
    _name = "sprite"

    def __init__(
        self,
        bitmap,
        palette,
        x,
        y,
        width=1,
        height=1,
        default_tile=0,
        tile_width=8,
        tile_height=8,
    ):
        super().__init__(
            bitmap=bitmap,
            pixel_shader=palette,
            x=x,
            y=y,
            width=width,
            height=height,
            default_tile=default_tile,
            tile_width=tile_width,
            tile_height=tile_height,
        )
        self.x_orig = x
        self.y_orig = y

    def tick(self, frame):
        pass
