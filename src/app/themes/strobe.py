import random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from displayio import Group, Palette
from app.themes._base import BaseSprite, BaseTheme
from app.utils import load_sprites_brightness_adjusted

LARGE_CIRCLE_ROW = 2
PANEL_WIDTH = 64
PITCH_SPEED = 0.1  # RPM per tick


class StrobeTheme(BaseTheme):
    def __init__(self, display):
        super().__init__(display)
        # Display & Resources
        self.display = display
        self.rpm = float(33.0)
        self.rpm_target = float(33.0)

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
        # Labels
        group_labels = Group()
        self.label_rpm = RPMLabel(1, 3, font_bitocra)
        group_labels.append(self.label_rpm)
        self.group_root.append(group_labels)
        self.display.show(self.group_root)

    async def loop(self):
        # self.circle8px.tick(self.frame)
        # Call base loop at end of function (to increment frame index etc)
        for actor in self.group_rows:
            actor.tick(self.frame)
        self.pitch_to_target()
        if self.frame % 800 == 0:
            self.set_rpm_target(self.get_next_rpm_target())
        self.label_rpm.text = "{0:.1f}".format(self.rpm)
        # print(f"rpm: {self.rpm}")
        await super().loop()

    def set_rpm_target(self, rpm_target=33):
        print(f"RPM target set: {rpm_target}")
        self.rpm_target = rpm_target

    def get_next_rpm_target(self):
        next_target = None
        while next_target is None or abs(next_target - int(self.rpm)) < 5:
            next_target = random.randint(33, 45)
        return next_target

    def pitch_to_target(self):
        if round(self.rpm) != self.rpm_target:
            self.rpm += PITCH_SPEED if self.rpm_target > self.rpm else -PITCH_SPEED
        else:
            self.rpm = round(self.rpm)


(
    bitmap_circle5px,
    _,
) = load_sprites_brightness_adjusted("/app/themes/circle-5px.bmp", transparent_index=0)

(
    bitmap_circle8px,
    _,
) = load_sprites_brightness_adjusted("/app/themes/circle-8px.bmp", transparent_index=0)

palette = Palette(2)
palette.make_transparent(0)
palette[0] = 0x000000
palette[1] = 0x090000

palette_alt = Palette(2)
palette_alt.make_transparent(0)
palette_alt[0] = 0x000000
palette_alt[1] = 0x120000

font_bitocra = bitmap_font.load_font("/bitocra7.bdf")

# VELOCITIES = [60, 30, 1, -30]
DISTANCE = 7
MULTIPLIER = 16


class CircleBaseSprite(BaseSprite):
    _name = "circlebase"

    def tick(self, frame, rpm=33):
        # print("tick", frame, rpm)
        move_amount = (-DISTANCE * MULTIPLIER) * (self.row + 1) * (rpm / 45)
        self.x_float += move_amount
        if self.x_float < -(PANEL_WIDTH * MULTIPLIER):
            self.x_float = PANEL_WIDTH * MULTIPLIER
        if self.x_float > (PANEL_WIDTH * MULTIPLIER):
            self.x_float = -(PANEL_WIDTH * MULTIPLIER)
        self.x = round(self.x_float / MULTIPLIER)
        # self.pixel_shader = palette if frame % 2 == 0 else palette_alt


class Circle5pxSprite(CircleBaseSprite):
    _name = "circle5px"

    def __init__(self, row, x, y):
        super().__init__(
            bitmap=bitmap_circle5px,
            palette=palette,
            x=x,
            y=y,
            default_tile=0,
            tile_width=64,
            tile_height=5,
        )
        self.x_float = float(x * MULTIPLIER)
        self.row = row


class Circle8pxSprite(CircleBaseSprite):
    _name = "circle8px"

    def __init__(self, row, x, y):
        super().__init__(
            bitmap=bitmap_circle8px,
            palette=palette,
            x=x,
            y=y,
            default_tile=0,
            tile_width=64,
            tile_height=8,
        )
        self.x_float = float(x * MULTIPLIER)
        self.row = row


class RPMLabel(Label):
    def __init__(self, x, y, font, color=0x999999):
        super().__init__(text="00.0", font=font, color=color)
        self.x = x
        self.y = y

    def tick(self, frame):
        pass
