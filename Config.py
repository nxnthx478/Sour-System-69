from json import load, dump
VERSION = '1.07'
MY_COLOR = 'deeppurpleaccent100'
URL_CHANNEL = 'https://instagram.com/SrcSys69'
CONFIG_NAME = 'config.json'

# Theme colors
# Deep dark background for cyber/ glass look
DARK_BG = '#0f0f0f'
DARK_TEXT = '#E6E6F0'
LIGHT_BG = '#F6F5EF'  # soft off-white (kept)
LIGHT_TEXT = '#222222'  # dark gray for less contrast

# Accent (neon / cyberpunk)
# Default: neon purple
ACCENT_FILL = '#8A2BE2'  # neon purple accent (fill)
ACCENT_STROKE = '#2b0057'  # darker stroke for contrast

# Palette presets (soft variants)
# Cyberpunk / soft palettes
PALETTES = {
    'magenta': {'fill': '#FF42A1', 'stroke': '#3b0033'}
}

# Default palette
DEFAULT_PALETTE = 'magenta'

# Custom font support: place TTF at Core/assets/CustomFont.ttf
CUSTOM_FONT_PATH = 'Core/assets/CustomFont.ttf'
# prefer modern sans; if custom font exists, will be used, otherwise fallbacks apply
CUSTOM_FONT_NAME = 'Inter'

def check_config():
    while True:
        try:
            with open(CONFIG_NAME) as f:
                return load(f)
        except:
            with open(CONFIG_NAME, 'w') as f:
                f.write('{"theme": "dark", "feedback": "False", "type_attack": "SMS", "attack": "False", "key": "", "color": "purple"}')



def change_config(key, value):
    config = check_config()
    config[key] = f'{value}'
    with open(CONFIG_NAME, 'w') as f:
        dump(config, f)


