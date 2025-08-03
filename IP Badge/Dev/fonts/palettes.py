# --- LED Color Palettes (GRB Order) ---
# Note: LEDs use GRB, display uses RGB. Display versions are prefixed with FONT_

# Vibrant alien green tones
ALIEN_GREEN = [
    (255, 0, 64),    # Neon green
    (200, 0, 40),    # Dull neon
    (255, 64, 128),  # Bright lime
    (255, 0, 0),     # Standard green
    (255, 32, 96),   # Soft lime
    (180, 0, 60),    # Organic green
    (255, 80, 60),   # Yellow-green
    (240, 16, 100),  # Fluorescent jade
    (160, 0, 80),    # Magenta shift
    (255, 48, 0),    # Amber-tint green
]

# Muted/dark alien greens - darker tones with wider variation
DARK_ALIEN_GREEN = [
    (40, 0, 10),      # Shadow moss
    (32, 8, 16),      # Dried olive
    (24, 0, 12),      # Faint jade
    (36, 12, 20),     # Shaded algae
    (28, 4, 14),      # Dusty leaf
    (20, 0, 10),      # Murky green
    (18, 6, 12),      # Brown-green mix
    (48, 16, 24),     # Deep dusk
    (60, 24, 30),     # Heavy soil
    (44, 12, 22),     # Rotten wood
    (50, 20, 10),     # Earth bark
    (38, 10, 18),     # Dead fern
]

# Neon pinks and purples for cyberpunk
CYBERPUNK_VIOLET = [
    (0, 128, 255),    # Vivid violet
    (0, 255, 255),    # Hot pink
    (0, 180, 255),    # Orchid
    (40, 200, 255),   # Ultraviolet
    (64, 255, 200),   # Bubblegum pink
    (0, 160, 160),    # Purple
    (32, 255, 128),   # Punchy pink
    (0, 220, 180),    # Plasma
    (0, 100, 255),    # Deep blue violet
    (80, 255, 180),   # Cyan pink
]

# Muted letter colors for dark fonts
DARK_LETTERS = [
    (48, 48, 48),     # Dim gray
    (32, 64, 16),     # Olive brown
    (40, 40, 80),     # Navy shade
    (64, 32, 32),     # Moss
    (48, 64, 0),      # Mustard olive
    (30, 30, 30),     # Shadow
    (20, 50, 40),     # Steel green
    (50, 20, 60),     # Ink blue
    (64, 64, 64),     # Fog gray
    (72, 60, 48),     # Bark
]

# Earthy but bold, dimmed primary tones
DIMMED_BOLD = [
    (200, 80, 80),    # Leafy green
    (180, 100, 100),  # Calm emerald
    (180, 60, 100),   # Jade
    (200, 120, 80),   # Burnished gold
    (160, 80, 120),   # Desert sage
    (128, 64, 64),    # Stone moss
    (180, 90, 80),    # Muddy gold
    (140, 100, 60),   # Rustic yellow
    (220, 140, 100),  # Red ochre
    (180, 160, 90),   # Aged bronze
]

# Lighting: IP-themed gold range (original, not GRB flipped)
IP_GOLD = [
    (255, 251, 0),     # Anchor: Neon yellow
    (255, 223, 0),     # Goldenrod
    (240, 230, 140),   # Khaki gold
    (255, 236, 139),   # Soft yellow gold
    (212, 175, 55),    # Rich metallic gold
    (192, 192, 192),   # Silver highlight
    (255, 215, 0),     # Trophy gold
    (230, 204, 128),   # Muted golden beige
]

ALIEN_GREEN_EXTREME = [
    (180, 255, 180),
    (192, 255, 64),
    (128, 255, 128),
    (200, 255, 100),
    (255, 255, 128),
    (255, 255, 255),
    (255, 255, 160),
    (180, 255, 120),
    (140, 255, 80),
    (100, 255, 64),
    (255, 255, 100),
    (220, 255, 200),
]

GHOST_GLITCH = [
    (40, 40, 40),
    (80, 80, 80),
    (120, 120, 120),
    (200, 200, 200),
    (255, 255, 255),
    (255, 0, 80),
    (0, 255, 180),
    (255, 240, 180),
    (180, 255, 255),
    (255, 100, 0),
    (0, 220, 180),
    (120, 255, 120),
]

HOT_PINK_NEONS = [
    (255, 64, 160),
    (255, 100, 180),
    (255, 128, 192),
    (255, 80, 120),
    (200, 64, 255),
    (255, 128, 255),
    (255, 0, 128),
    (255, 255, 255),
    (255, 220, 200),
    (180, 0, 120),
]

NEON_BLUE_TEAL = [
    (0, 128, 255),
    (0, 180, 255),
    (32, 200, 255),
    (80, 240, 255),
    (180, 255, 255),
    (0, 255, 255),
    (255, 64, 64),
    (255, 0, 128),
    (0, 255, 180),
    (100, 255, 240),
    (220, 100, 100),
]

# --- Font-safe RGB versions for Display ---
FONT_ALIEN_GREEN = [
    (180, 255, 180),   # radioactive mint
    (192, 255, 64),    # neon chartreuse
    (255, 255, 255),   # white-hot flash
    (128, 255, 128),   # searing lime
    (200, 255, 100),   # lemon-lime laser
    (150, 255, 150),   # soft green-white
    (255, 255, 128),   # LED yellow burst
    (220, 255, 200),   # pastel overload
    (255, 100, 255),   # pink-violet pulse
    (160, 240, 255),   # cyan glitch
]

FONT_DARK_ALIEN_GREEN = [
    (120, 180, 120),   # dark lime mist
    (140, 200, 100),   # jade fog
    (110, 180, 110),   # moss plasma
    (100, 160, 140),   # sea glitch
    (150, 220, 100),   # forest flash
    (130, 200, 130),   # muted bright green
    (160, 230, 160),   # ghost vine
    (180, 240, 180),   # bright mist
    (200, 255, 200),   # plasma fade
    (180, 255, 150),   # lemon fade
    (255, 255, 160),   # glare wash
    (200, 255, 120),   # jungle static
]

FONT_CYBERPUNK_VIOLET = [
    (128, 0, 255), (255, 0, 255), (180, 0, 255),
    (200, 40, 255), (255, 64, 200), (160, 0, 160),
    (255, 32, 128), (220, 0, 180), (255, 100, 0), (180, 255, 80),
]

FONT_DARK_LETTERS = [
    (48, 48, 48), (64, 32, 16), (40, 40, 80),
    (32, 64, 32), (64, 48, 0), (30, 30, 30),
    (50, 20, 40), (20, 50, 60), (64, 64, 64), (48, 60, 72),
]

FONT_DIMMED_BOLD = [
    (80, 200, 80), (100, 180, 100), (60, 180, 100),
    (120, 200, 80), (80, 160, 120), (64, 128, 64),
    (90, 180, 80), (100, 140, 60), (100, 140, 220), (90, 160, 180),
]

FONT_ALIEN_GREEN_EXTREME = [
    (180, 255, 180), (192, 255, 64), (128, 255, 128), (200, 255, 100),
    (255, 255, 128), (255, 255, 255), (255, 255, 160), (180, 255, 120),
    (140, 255, 80), (100, 255, 64), (255, 255, 100), (220, 255, 200),
]

FONT_GHOST_GLITCH = [
    (40, 40, 40),     # dark gray base
    (80, 80, 80),     # mid gray
    (120, 120, 120),  # light gray
    (200, 200, 200),  # bright gray
    (255, 255, 255),  # white burst
    (255, 0, 80),     # hot glitch pink
    (0, 255, 180),    # teal punch
    (255, 240, 180),  # warm pale gold
    (180, 255, 255),  # cyan ghost
    (255, 100, 0),    # fire red accent
    (0, 220, 180),    # glowing teal
    (120, 255, 120),  # muted green
]

FONT_HOT_PINK_NEONS = [
    (255, 64, 160),   # neon magenta
    (255, 100, 180),  # punchy hot pink
    (255, 128, 192),  # bubblegum
    (255, 80, 120),   # cherry blast
    (200, 64, 255),   # pink-violet
    (255, 128, 255),  # soft neon pink
    (255, 0, 128),    # glitch pink
    (255, 255, 255),  # CRT white pop
    (255, 220, 200),  # pale glow
    (180, 0, 120),    # deep retro
]

FONT_NEON_BLUE_TEAL = [
    (0, 128, 255),    # bright blue
    (0, 180, 255),    # pure neon cyan
    (32, 200, 255),   # turquoise blast
    (80, 240, 255),   # light ice blue
    (180, 255, 255),  # sky white
    (0, 255, 255),    # full cyan
    (255, 64, 64),    # hot red splash
    (255, 0, 128),    # pink glitch
    (0, 255, 180),    # aqua green
    (100, 255, 240),  # teal neon
    (220, 100, 100),  # glitch burn red
]

FONT_IP_GOLD = [
    (255, 251, 0),     # Anchor: Neon yellow
    (255, 223, 0),     # Goldenrod
    (240, 230, 140),   # Khaki gold
    (255, 236, 139),   # Soft yellow gold
    (212, 175, 55),    # Rich metallic gold
    (192, 192, 192),   # Silver highlight
    (255, 215, 0),     # Trophy gold
    (230, 204, 128),   # Muted golden beige
]

PALETTES = {
    # Original / legacy palettes
    "ALIEN_GREEN": ALIEN_GREEN,
    "DARK_ALIEN_GREEN": DARK_ALIEN_GREEN,
    "CYBERPUNK_VIOLET": CYBERPUNK_VIOLET,
    "DARK_LETTERS": DARK_LETTERS,
    "DIMMED_BOLD": DIMMED_BOLD,
    "IP_GOLD": IP_GOLD,

    # Display RGB versions
    "FONT_ALIEN_GREEN": FONT_ALIEN_GREEN,
    "FONT_DARK_ALIEN_GREEN": FONT_DARK_ALIEN_GREEN,
    "FONT_CYBERPUNK_VIOLET": FONT_CYBERPUNK_VIOLET,
    "FONT_DARK_LETTERS": FONT_DARK_LETTERS,
    "FONT_DIMMED_BOLD": FONT_DIMMED_BOLD,
    "FONT_IP_GOLD": FONT_IP_GOLD,

    # New ultra-bright LED palettes
    "ALIEN_GREEN_EXTREME": ALIEN_GREEN_EXTREME,
    "GHOST_GLITCH": GHOST_GLITCH,
    "HOT_PINK_NEONS": HOT_PINK_NEONS,
    "NEON_BLUE_TEAL": NEON_BLUE_TEAL,

    # New display RGB versions of the above
    "FONT_ALIEN_GREEN_EXTREME": FONT_ALIEN_GREEN_EXTREME,
    "FONT_GHOST_GLITCH": FONT_GHOST_GLITCH,
    "FONT_HOT_PINK_NEONS": FONT_HOT_PINK_NEONS,
    "FONT_NEON_BLUE_TEAL": FONT_NEON_BLUE_TEAL,
}