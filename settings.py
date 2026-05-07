SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Breakout"

COLOR_BG      = (15, 15, 25)
COLOR_PADDLE  = (200, 200, 255)
COLOR_BALL    = (255, 255, 255)
COLOR_TEXT    = (255, 255, 255)

BRICK_COLORS = [
    (255,  80,  80),
    (255, 140,  40),
    (255, 220,  40),
    ( 80, 200,  80),
    ( 80, 180, 255),
    (140,  80, 255),
    (220,  80, 220),
]

PADDLE_WIDTH    = 100
PADDLE_HEIGHT   = 14
PADDLE_SPEED    = 7.0
PADDLE_Y_OFFSET = 50

BALL_RADIUS     = 8
BALL_SPEED_INIT = 4.0   # starting speed (GPT-2 era)
BALL_SPEED_MIN  = 4.0
BALL_SPEED_MAX  = 14.0  # peak speed (Claude Opus 4.6 era)
BALL_TRAIL_LEN  = 12

# Target play-time in frames (30 s × 60 fps).
# Speed reaches its maximum after this many active frames.
GAME_DURATION_FRAMES = 1800

# AI milestone labels that appear on the ball as it speeds up.
# Each entry: (min_speed, display_name, ball_rgb, glow_rgb)
# Ordered from slowest to fastest, mirroring the chart's Y-axis.
AI_MILESTONES = [
    ( 4.0, "GPT-2",         (150, 150, 155), ( 90,  90, 100)),
    ( 4.7, "GPT-3",         (175, 175, 185), (110, 110, 130)),
    ( 5.5, "GPT-3.5",       ( 60, 200, 175), ( 30, 145, 130)),
    ( 6.4, "GPT-4",         ( 60, 180,  70), ( 30, 130,  40)),
    ( 7.4, "o3",            (255, 140,  40), (200,  90,  10)),
    ( 8.6, "GPT-5",         (255, 210,  50), (200, 155,  15)),
    ( 9.8, "Claude 4.5",    (165,  80, 235), (110,  35, 185)),
    (10.8, "GPT-5.2",       ( 80, 235, 100), ( 35, 175,  50)),
    (11.8, "GPT-5.4",       (195, 210, 225), (140, 155, 170)),
    (12.8, "Claude 4.6",    (255,  85,  55), (200,  35,  15)),
]

BRICK_COLS       = 10
BRICK_ROWS       = 7
BRICK_WIDTH      = 70
BRICK_HEIGHT     = 22
BRICK_MARGIN_X   = 15
BRICK_MARGIN_TOP = 80
BRICK_GAP        = 4

HUD_HEIGHT  = 40
LIVES_START = 3

PARTICLE_COUNT    = 12
PARTICLE_LIFETIME = 35
PARTICLE_SPEED    = 4.0

SHAKY_DURATION     = 240   # frames a ball stays shaky after MA brick hit
PADDLE_WIDTH_BONUS = 25    # pixels added each time a WID brick is destroyed
PADDLE_SPEED_BONUS = 0.6   # added to speed_mult each time a SPD brick is destroyed

# Each entry: (is_good, RGB color, display label)
BRICK_DEFS = {
    'SPD':  (True,  ( 55, 210, 105), 'SPD'),   # good – faster pad
    'WID':  (True,  ( 55, 155, 245), 'WID'),   # good – wider pad
    'VPAD': (True,  (240, 190,  40), 'V+' ),   # good – vertical pad
    '+1':   (False, (215,  50,  50), '+1' ),   # bad  – duplicate ball
    'MA':   (False, (200,  90,  25), 'MA' ),   # bad  – shaky movement
    'GH':   (False, (140,  45, 195), 'GH' ),   # bad  – ghost duplicate
}

SCORE_TABLE = {
    'SPD':  30,
    'WID':  25,
    'VPAD': 50,
    '+1':    5,
    'MA':    5,
    'GH':   10,
}
