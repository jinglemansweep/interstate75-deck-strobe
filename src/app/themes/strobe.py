from displayio import Group
from app.themes._base import BaseSprite, BaseTheme
from app.utils import load_sprites_brightness_adjusted

LARGE_CIRCLE_ROW = 2
PANEL_WIDTH = 64


class StrobeTheme(BaseTheme):
    def __init__(self, display):
        super().__init__(display)
        # Display & Resources
        self.display = display

    async def setup(self):
        # Call base setup
        await super().setup()
        # Primitives
        self.group_root = Group()
        # Actors
        group_actors = Group()
        self.group_rows = Group()
        for idx_row in range(4):
            is_large = idx_row == LARGE_CIRCLE_ROW
            sprite_cls = Circle8pxSprite if is_large else Circle5pxSprite
            row_sprite = sprite_cls(
                row=idx_row,
                x=0,
                y=16 + (idx_row * 8) + (3 if idx_row == LARGE_CIRCLE_ROW + 1 else 0),
            )
            self.group_rows.append(row_sprite)
            row_sprite_next = sprite_cls(
                row=idx_row,
                x=PANEL_WIDTH,
                y=16 + (idx_row * 8) + (3 if idx_row == LARGE_CIRCLE_ROW + 1 else 0),
            )
            self.group_rows.append(row_sprite_next)
        group_actors.append(self.group_rows)
        self.group_root.append(group_actors)
        self.display.show(self.group_root)

    async def loop(self, button=None):
        # self.circle8px.tick(self.frame)
        # Call base loop at end of function (to increment frame index etc)
        for actor in self.group_rows:
            actor.tick()
        await super().loop()


(
    bitmap_circle5px,
    palette_circle5px,
) = load_sprites_brightness_adjusted("/app/themes/circle-5px.bmp", transparent_index=0)

(
    bitmap_circle8px,
    palette_circle8px,
) = load_sprites_brightness_adjusted("/app/themes/circle-8px.bmp", transparent_index=0)


VELOCITIES = [60, 30, 1, -30]


class CircleBaseSprite(BaseSprite):
    _name = "circlebase"

    def tick(self):
        # print("tick", self.row)

        self.x_float += VELOCITIES[self.row]
        if self.x_float < -(PANEL_WIDTH * PANEL_WIDTH):
            self.x_float = PANEL_WIDTH * PANEL_WIDTH
        if self.x_float > (PANEL_WIDTH * PANEL_WIDTH):
            self.x_float = -(PANEL_WIDTH * PANEL_WIDTH)
        self.x = round(self.x_float / PANEL_WIDTH)


class Circle5pxSprite(CircleBaseSprite):
    _name = "circle5px"

    def __init__(self, row, x, y):
        super().__init__(
            bitmap=bitmap_circle5px,
            palette=palette_circle5px,
            x=x,
            y=y,
            default_tile=0,
            tile_width=64,
            tile_height=5,
        )
        self.x_float = float(x * PANEL_WIDTH)
        self.row = row


class Circle8pxSprite(CircleBaseSprite):
    _name = "circle8px"

    def __init__(self, row, x, y):
        super().__init__(
            bitmap=bitmap_circle8px,
            palette=palette_circle8px,
            x=x,
            y=y,
            default_tile=0,
            tile_width=64,
            tile_height=8,
        )
        self.x_float = float(x * PANEL_WIDTH)
        self.row = row
