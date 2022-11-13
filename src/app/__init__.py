import asyncio
import board
import displayio
import framebufferio
import rgbmatrix
import time

BIT_DEPTH = 5
FPS_TARGET = 60
NTP_INTERVAL = 60 * 60  # 1h
LOOP_DELAY = 0.002  # secs

displayio.release_displays()


class Manager:
    def __init__(self, theme, debug=False):
        print(f"MANAGER::INIT theme={theme} debug={debug}")
        # RGB Matrix
        self.matrix = rgbmatrix.RGBMatrix(
            width=64,
            height=64,
            bit_depth=BIT_DEPTH,
            rgb_pins=[board.R0, board.G0, board.B0, board.R1, board.G1, board.B1],
            addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D, board.ROW_E],
            clock_pin=board.CLK,
            latch_pin=board.LAT,
            output_enable_pin=board.OE,
        )
        # Display Buffer
        self.display = framebufferio.FramebufferDisplay(self.matrix, auto_refresh=True)
        # Networking
        # self.network = Network(status_neopixel=board.NEOPIXEL, debug=debug)
        # Theme
        self.theme = theme(display=self.display)

    def run(self):
        while True:
            try:
                asyncio.run(self.loop())
            finally:
                print("asyncio crash, restarting")
                asyncio.new_event_loop()

    def refresh_display(self):
        self.display.refresh(
            minimum_frames_per_second=0, target_frames_per_second=FPS_TARGET
        )

    async def loop(self):
        await self.theme.setup()
        while True:
            await self.theme.loop()
            # self.refresh_display()
            # time.sleep(LOOP_DELAY)
