import os, sys, math, json, time, random, socket, threading, traceback, struct, io
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
CRASH_FILE = os.path.join(BASE_DIR, "crash_report_cs0.3.txt")
SAVE_FILE = os.path.join(BASE_DIR, "pycs_save_v5.json")

def custom_excepthook(exc_type, exc_value, exc_tb):
    err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        with open(CRASH_FILE, "w", encoding="utf-8") as f:
            f.write(err_msg)
    except Exception:
        pass
    try:
        if not pygame.get_init():
            pygame.init()
        scr = pygame.display.set_mode((800, 450), pygame.FULLSCREEN | pygame.SCALED)
        fnt = pygame.font.SysFont("sans-serif", 14, bold=True)
        t_end = time.time() + 15
        while time.time() < t_end:
            for e in pygame.event.get():
                if e.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    pygame.quit()
                    sys.exit(1)
            scr.fill((95, 14, 22))
            y = 18
            scr.blit(fnt.render("CRITICAL ERROR (Saved to crash_report_cs0.3.txt):", True, (255, 230, 90)), (18, y))
            y += 24
            for line in err_msg.splitlines()[-18:]:
                scr.blit(fnt.render(line[:92], True, (255, 255, 255)), (18, y))
                y += 18
            pygame.display.flip()
            time.sleep(0.05)
    except Exception:
        pass
    pygame.quit()
    sys.exit(1)

sys.excepthook = custom_excepthook

pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()
W, H = 800, 450
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("PyCS 0.5 Ultimate")
clock = pygame.time.Clock()

def get_smooth_font(size, bold=True):
    for name in ("Roboto", "DejaVuSans", "Arial", "sans-serif"):
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, size)

font_xs = get_smooth_font(13, True)
font_sm = get_smooth_font(16, True)
font_md = get_smooth_font(20, True)
font_lg = get_smooth_font(28, True)
font_xl = get_smooth_font(40, True)

LANG_STR = {
    "RU": {
        "HOME": "ГЛАВНАЯ", "INV": "СКИНЫ", "MP": "ОНЛАЙН", "STAT": "ПРОФИЛЬ", "SET": "НАСТРОЙКИ",
        "PLAY": "ИГРАТЬ", "SELECT_MAP": "ВЫБОР КАРТЫ И РЕЖИМА", "START_MATCH": "ЗАПУСТИТЬ КАТКУ",
        "CHOOSE_TEAM": "ВЫБЕРИТЕ КОМАНДУ ДЛЯ ВХОДА В БОЙ",
        "TEAM_CT": "СПЕЦНАЗ (CT) — Защита и разминирование",
        "TEAM_T": "ТЕРРОРИСТЫ (T) — Атака и закладка C4",
        "OPEN_CASE": "ОТКРЫТЬ КЕЙС (600 М)", "EQUIPPED": "НАДЕТО", "OWNED": "КУПЛЕНО (Надеть)",
        "CUSTOM_HUD": "РЕДАКТОР КНОПОК HUD", "SAVE_HUD": "СОХРАНИТЬ",
        "SIZE": "Размер", "ALPHA": "Прозр.", "ALL_ALPHA": "Ко всем", "CLOSE": "ЗАКРЫТЬ",
        "SHOP_TITLE": "МАГАЗИН СНАРЯЖЕНИЯ", "KEVLAR": "Броня + Шлем ($1000)",
        "DEFUSE": "Набор сапера 2x ($400)", "NADES": "Комплект гранат ($300)",
        "GFX": "Качество текстур", "LANG": "Язык / Language: RU",
        "GFX_0": "НИЗКОЕ", "GFX_1": "НОРМАЛЬНОЕ", "GFX_2": "ВЫСОКОЕ",
        "MODE_DEFUSE": "ЗАКЛАДКА C4", "MODE_ARMS_RACE": "ГОНКА ОРУЖИЯ",
        "MODE_ZOMBIE": "ЗОМБИ РЕЖИМ", "MODE_WINGMAN": "ДУЭЛЬ 1x1", "MODE_TRAINING": "ТРЕНИРОВКА",
        "PAUSE": "ПАУЗА", "RESUME": "ПРОДОЛЖИТЬ БОЙ", "TO_MENU": "ВЫЙТИ В МЕНЮ",
        "BOT_AI": "Поведение ботов", "AI_0": "МИРНЫЕ (СТОЯТ)", "AI_1": "ТОЛЬКО НОЖИ", "AI_2": "ОБЫЧНЫЕ", "AI_3": "ХАРДКОР",
        "DROP": "БРОСИТЬ", "TAKE": "ВЗЯТЬ", "HEADSHOT": "★ ХЕДШОТ! ★", "DAILY": "БОНУС ДНЯ: +750 МОНЕТ!"
    },
    "EN": {
        "HOME": "HOME", "INV": "SKINS", "MP": "ONLINE", "STAT": "PROFILE", "SET": "SETTINGS",
        "PLAY": "PLAY", "SELECT_MAP": "SELECT MAP & GAME MODE", "START_MATCH": "LAUNCH MATCH",
        "CHOOSE_TEAM": "CHOOSE YOUR TEAM TO DEPLOY",
        "TEAM_CT": "COUNTER-TERRORIST (CT) — Defend & Defuse",
        "TEAM_T": "TERRORIST (T) — Attack & Plant C4",
        "OPEN_CASE": "OPEN CASE (600 C)", "EQUIPPED": "EQUIPPED", "OWNED": "OWNED (Equip)",
        "CUSTOM_HUD": "CUSTOMIZE HUD BUTTONS", "SAVE_HUD": "SAVE HUD",
        "SIZE": "Size", "ALPHA": "Alpha", "ALL_ALPHA": "Apply All", "CLOSE": "CLOSE",
        "SHOP_TITLE": "TACTICAL ARMORY SHOP", "KEVLAR": "Kevlar + Helmet ($1000)",
        "DEFUSE": "Defuse Kit 2x ($400)", "NADES": "Full Grenade Pack ($300)",
        "GFX": "Texture Quality", "LANG": "Language / Язык: EN",
        "GFX_0": "LOW", "GFX_1": "NORMAL", "GFX_2": "HIGH",
        "MODE_DEFUSE": "DEFUSE C4", "MODE_ARMS_RACE": "ARMS RACE",
        "MODE_ZOMBIE": "ZOMBIE INFECT", "MODE_WINGMAN": "WINGMAN 1v1", "MODE_TRAINING": "TRAINING",
        "PAUSE": "PAUSE", "RESUME": "RESUME MATCH", "TO_MENU": "EXIT TO MENU",
        "BOT_AI": "Bot Behavior", "AI_0": "PASSIVE (IDLE)", "AI_1": "KNIVES ONLY", "AI_2": "NORMAL", "AI_3": "HARDCORE",
        "DROP": "DROP", "TAKE": "PICKUP", "HEADSHOT": "★ HEADSHOT! ★", "DAILY": "DAILY BONUS: +750 COINS!"
    }
}

SFX = {}
def build_sfx():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(22050, -16, 1, 512)
        sr = 22050
        def make_wav(samples):
            buf = io.BytesIO()
            n = len(samples)
            buf.write(b'RIFF' + struct.pack('<I', 36 + n * 2) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16) + b'data' + struct.pack('<I', n * 2))
            buf.write(struct.pack('<' + 'h' * n, *samples))
            buf.seek(0)
            return pygame.mixer.Sound(file=buf)
        rng = random.Random(99)
        SFX["shoot"] = make_wav([int((rng.uniform(-1, 1) * 0.7 + math.sin(i * 0.12) * 0.3) * 26000 * ((1 - i / 2400) ** 2)) for i in range(2400)])
        SFX["awp"] = make_wav([int((rng.uniform(-1, 1) * 0.8 + math.sin(i * 0.06) * 0.4) * 30000 * ((1 - i / 5500) ** 1.6)) for i in range(5500)])
        SFX["knife"] = make_wav([int(rng.uniform(-1, 1) * 16000 * math.sin((i / 1400) * math.pi)) for i in range(1400)])
        SFX["hit"] = make_wav([int(math.sin(i * 0.55) * 24000 * (1 - i / 950)) for i in range(950)])
        SFX["headshot"] = make_wav([int(math.sin(i * 0.90) * 29000 * (1 - i / 1700)) for i in range(1700)])
        SFX["reload"] = make_wav([int(math.sin(i * 0.25) * 14000) if (i < 600 or 1400 < i < 2000) else 0 for i in range(2400)])
        SFX["boom"] = make_wav([int(rng.uniform(-1, 1) * 30000 * ((1 - i / 8000) ** 1.4)) for i in range(8000)])
        SFX["beep"] = make_wav([int(math.sin(i * 0.55) * 22000) for i in range(1100)])
        SFX["click"] = make_wav([int(math.sin(i * 0.65) * 15000 * (1 - i / 450)) for i in range(450)])
    except Exception:
        pass

build_sfx()

def play_sfx(name, vol=0.7):
    if name in SFX:
        try:
            SFX[name].set_volume(max(0.0, min(1.0, vol)))
            SFX[name].play()
        except Exception:
            pass

DEFAULT_LAYOUT = {
    "joy":     {"x": 110, "y": 335, "r": 58, "s": 1.0, "a": 115},
    "fire":    {"x": 695, "y": 320, "r": 50, "s": 1.0, "a": 135},
    "reload":  {"x": 585, "y": 390, "r": 27, "s": 1.0, "a": 115},
    "zoom":    {"x": 590, "y": 270, "r": 27, "s": 1.0, "a": 115},
    "jump":    {"x": 745, "y": 200, "r": 27, "s": 1.0, "a": 115},
    "crouch":  {"x": 670, "y": 195, "r": 27, "s": 1.0, "a": 115},
    "shop":    {"x": 145, "y": 42,  "r": 25, "s": 1.0, "a": 145},
    "inspect": {"x": 515, "y": 390, "r": 24, "s": 1.0, "a": 105},
    "drop":    {"x": 450, "y": 390, "r": 24, "s": 1.0, "a": 105},
    "grenade": {"x": 655, "y": 120, "r": 27, "s": 1.0, "a": 120},
    "c4_btn":  {"x": 400, "y": 325, "r": 32, "s": 1.0, "a": 140}
}

DEFAULT_SAVE = {
    "lang": "RU", "gfx": 2,
    "coins": 5000, "kills": 0, "deaths": 0, "headshots": 0, "wins": 0, "bombs": 0,
    "shots_fired": 0, "shots_hit": 0, "play_time": 0.0, "weapon_kills": {},
    "last_daily": "", "inv": ["Default"], "equipped": {},
    "sens": 1.0, "fov": 1.05, "btn_alpha": 115,
    "xhair": {"col": 0, "len": 9, "thick": 2, "dot": True, "dyn": True},
    "layout": DEFAULT_LAYOUT
}

def load_save():
    data = json.loads(json.dumps(DEFAULT_SAVE))
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            for k, v in loaded.items():
                if k == "layout" and isinstance(v, dict):
                    for bk, bv in DEFAULT_LAYOUT.items():
                        if bk in v and isinstance(v[bk], dict):
                            data["layout"][bk].update(v[bk])
                elif k == "xhair" and isinstance(v, dict):
                    data["xhair"].update(v)
                else:
                    data[k] = v
        except Exception:
            pass
    for bk, bv in DEFAULT_LAYOUT.items():
        if bk not in data["layout"]:
            data["layout"][bk] = dict(bv)
        data["layout"][bk].setdefault("s", 1.0)
        data["layout"][bk].setdefault("a", 115)
    return data

def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)
    except Exception:
        pass

save_data = load_save()

def tr(key):
    return LANG_STR.get(save_data.get("lang", "RU"), LANG_STR["RU"]).get(key, key)

RANKS = [
    (0, "Silver I", (160, 170, 180)), (10, "Silver Elite", (185, 195, 205)),
    (25, "Gold Nova", (235, 195, 50)), (50, "Master Guardian", (65, 165, 245)),
    (90, "Legendary Eagle", (190, 95, 245)), (150, "Supreme", (235, 75, 95)),
    (250, "Global Elite", (255, 215, 0))
]

def get_player_rank():
    score = save_data.get("kills", 0) + save_data.get("wins", 0) * 3 + save_data.get("headshots", 0)
    cur = RANKS[0]
    for r in RANKS:
        if score >= r[0]:
            cur = r
    return cur[1], cur[2], score

WEAPONS = {
    "Knife":   {"price": 0,    "dmg": 55,  "rate": 0.38, "clip": 0,  "res": 0,  "spread": 0.01, "recoil": 0.00, "range": 2.3,  "auto": False, "slot": 0, "pen": 0.0},
    "USP-S":   {"price": 200,  "dmg": 36,  "rate": 0.18, "clip": 12, "res": 36, "spread": 0.012,"recoil": 0.03, "range": 22.0, "auto": False, "slot": 1, "pen": 0.35},
    "Deagle":  {"price": 700,  "dmg": 68,  "rate": 0.34, "clip": 7,  "res": 35, "spread": 0.018,"recoil": 0.08, "range": 24.0, "auto": False, "slot": 1, "pen": 0.70},
    "MP5":     {"price": 1500, "dmg": 29,  "rate": 0.08, "clip": 30, "res": 90, "spread": 0.032,"recoil": 0.03, "range": 19.0, "auto": True,  "slot": 2, "pen": 0.40},
    "M3":      {"price": 1700, "dmg": 26,  "rate": 0.70, "clip": 8,  "res": 32, "spread": 0.075,"recoil": 0.10, "range": 14.0, "auto": False, "slot": 2, "pen": 0.30, "pellets": 6},
    "AK-47":   {"price": 2700, "dmg": 44,  "rate": 0.095,"clip": 30, "res": 90, "spread": 0.022,"recoil": 0.05, "range": 28.0, "auto": True,  "slot": 2, "pen": 0.78},
    "M4A1-S":  {"price": 2900, "dmg": 38,  "rate": 0.085,"clip": 25, "res": 75, "spread": 0.014,"recoil": 0.03, "range": 28.0, "auto": True,  "slot": 2, "pen": 0.70},
    "AWP":     {"price": 4750, "dmg": 125, "rate": 1.00, "clip": 10, "res": 30, "spread": 0.001,"recoil": 0.14, "range": 36.0, "auto": False, "slot": 2, "pen": 0.95, "scope": True}
}
WEAPON_ORDER = ["Knife", "USP-S", "Deagle", "MP5", "M3", "AK-47", "M4A1-S", "AWP"]
ARMS_RACE_ORDER = ["MP5", "M3", "AK-47", "M4A1-S", "AWP", "Deagle", "USP-S", "Knife"]

SKINS = {
    "Default":   {"price": 0,    "rarity": "Common",     "c1": (88, 94, 104),  "c2": (46, 50, 58),   "acc": (165, 172, 182)},
    "Asiimov":   {"price": 1200, "rarity": "Rare",       "c1": (242, 242, 248),"c2": (238, 108, 22), "acc": (34, 38, 45)},
    "CyberNeon": {"price": 1400, "rarity": "Classified", "c1": (28, 228, 248), "c2": (218, 28, 188), "acc": (255, 250, 95)},
    "Gold":      {"price": 1500, "rarity": "Classified", "c1": (238, 195, 48), "c2": (155, 115, 18), "acc": (255, 242, 155)},
    "Ruby":      {"price": 1800, "rarity": "Covert",     "c1": (205, 24, 52),  "c2": (98, 12, 25),   "acc": (255, 120, 135)},
    "Emerald":   {"price": 1800, "rarity": "Covert",     "c1": (24, 190, 88),  "c2": (12, 84, 40),   "acc": (135, 255, 180)},
    "IceDragon": {"price": 2200, "rarity": "Special",    "c1": (165, 225, 255),"c2": (48, 110, 200), "acc": (245, 252, 255)}
}

MAPS = {
    "Mirage Palace": {
        "sky_top": (52, 84, 155), "sky_bot": (225, 190, 155), "floor": (148, 124, 96),
        "grid": [
            [7,7,1,1,1,7,7,1,1,1,7,7,1,1,7,7],
            [7,0,0,0,0,7,4,4,0,0,1,0,0,0,0,7],
            [1,0,2,5,0,7,4,4,0,2,1,0,5,6,0,1],
            [1,0,0,6,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,7,7,0,2,0,0,2,0,7,7,0,1,1],
            [1,0,0,0,0,0,8,8,5,5,0,0,0,0,0,1],
            [1,0,2,0,1,0,8,8,6,6,0,1,0,2,0,1],
            [7,0,0,0,1,0,0,0,0,0,0,1,0,0,0,7],
            [7,0,0,0,1,0,2,0,0,2,0,1,0,0,0,7],
            [1,0,5,0,0,0,0,8,8,0,0,0,0,5,0,1],
            [1,0,6,0,7,1,0,1,1,0,1,7,0,6,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,4,4,0,0,2,0,0,2,0,0,0,2,0,1],
            [7,0,4,4,0,1,0,0,5,6,1,0,0,0,0,7],
            [7,0,0,0,0,1,0,0,0,0,1,0,0,0,0,7],
            [7,7,1,1,1,7,7,1,1,1,7,7,1,1,7,7]
        ]
    },
    "Dust2 Remake": {
        "sky_top": (42, 82, 148), "sky_bot": (185, 205, 230), "floor": (162, 140, 105),
        "grid": [
            [7,1,1,1,1,1,7,7,1,1,1,1,1,1,7,7],
            [1,0,0,0,2,0,0,7,4,4,5,5,0,0,0,7],
            [1,0,2,0,0,0,0,1,4,4,6,2,0,8,8,1],
            [1,0,0,0,5,6,0,0,0,0,0,0,0,8,8,1],
            [1,0,0,7,1,1,0,1,1,0,1,7,1,0,0,1],
            [1,8,8,1,0,0,0,0,0,0,0,0,1,0,0,1],
            [1,2,0,0,0,5,5,0,0,2,0,0,0,0,2,1],
            [1,0,0,1,0,6,0,8,8,0,0,1,1,0,0,1],
            [1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,1],
            [1,0,5,7,1,0,0,1,1,0,5,7,0,2,0,1],
            [1,0,6,0,0,0,0,0,0,0,6,0,0,0,0,1],
            [1,0,0,0,2,0,1,7,1,0,0,0,5,6,0,1],
            [7,0,4,4,0,0,1,0,0,0,2,0,0,0,0,1],
            [7,5,4,4,0,0,0,0,5,6,0,0,2,0,0,1],
            [7,6,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [7,7,1,1,1,1,1,7,7,1,1,1,1,1,7,7]
        ]
    },
    "Cyber Bunker": {
        "sky_top": (12, 18, 34), "sky_bot": (34, 54, 88), "floor": (50, 56, 68),
        "grid": [
            [3,3,3,7,7,3,3,3,3,3,3,7,7,3,3,3],
            [3,0,0,0,3,4,4,0,0,0,3,0,0,0,0,3],
            [3,0,2,0,3,4,4,0,5,0,3,0,2,0,0,3],
            [3,0,0,0,0,0,0,0,6,0,0,0,0,0,0,3],
            [3,0,3,3,0,3,3,0,0,3,3,0,3,3,0,3],
            [3,0,3,0,0,8,8,8,8,8,8,0,0,3,0,3],
            [3,0,0,0,5,6,8,2,2,8,6,5,0,0,0,3],
            [7,3,0,3,0,8,8,0,0,8,8,0,3,0,3,7],
            [7,3,0,3,0,8,8,0,0,8,8,0,3,0,3,7],
            [3,0,0,0,5,6,8,2,2,8,6,5,0,0,0,3],
            [3,0,3,0,0,8,8,8,8,8,8,0,0,3,0,3],
            [3,0,3,3,0,3,3,0,0,3,3,0,3,3,0,3],
            [3,0,0,0,0,0,0,0,6,0,0,0,0,0,0,3],
            [3,0,2,0,3,0,0,0,5,4,4,0,2,0,0,3],
            [3,0,0,0,3,0,0,0,0,4,4,0,0,0,0,3],
            [3,3,3,7,7,3,3,3,3,3,3,7,7,3,3,3]
        ]
    }
}
MAP_NAMES = list(MAPS.keys())

TEX_SIZE = 64
WALL_TEXTURES = {}

def generate_realistic_textures():
    global TEX_SIZE
    gfx = save_data.get("gfx", 2)
    TEX_SIZE = 32 if gfx == 0 else (48 if gfx == 1 else 64)
    rng = random.Random(42)
    for code in range(1, 9):
        for side in (0, 1):
            surf = pygame.Surface((TEX_SIZE, TEX_SIZE))
            dark = pygame.Surface((TEX_SIZE, TEX_SIZE))
            shade = 1.0 if side == 0 else 0.74
            bh_step = max(8, TEX_SIZE // 4)
            for y in range(TEX_SIZE):
                for x in range(TEX_SIZE):
                    n = rng.randint(-10, 10) if gfx >= 1 else 0
                    if code in (1, 7):
                        row = y // bh_step
                        bx, by = (x + (row % 2) * bh_step) % (bh_step * 2), y % bh_step
                        if by < 2 or bx < 2:
                            r, g, b = 105 + n, 102 + n, 96 + n
                        else:
                            v = ((row * 7 + (x // (bh_step * 2)) * 13) % 20) - 10
                            base_r = 188 if code == 1 else 155
                            base_g = 148 if code == 1 else 132
                            base_b = 110 if code == 1 else 108
                            r, g, b = base_r + n + v, base_g + n + v, base_b + n + v
                            if by == 2 or bx == 2:
                                r, g, b = min(255, r + 24), min(255, g + 22), min(255, b + 18)
                            if code == 7 and (bh_step <= x % (bh_step * 2) <= bh_step + 4) and (4 <= by <= bh_step - 4):
                                r, g, b = 45, 65, 95
                    elif code in (2, 5):
                        bdr = max(3, TEX_SIZE // 12)
                        if x < bdr or x >= TEX_SIZE - bdr or y < bdr or y >= TEX_SIZE - bdr or abs(x - y) < bdr:
                            r, g, b = 112 + n, 76 + n, 38 + n
                        else:
                            grain = int(math.sin(y * 0.7) * 10) if gfx == 2 else 0
                            r, g, b = 166 + n + grain, 118 + n + grain, 68 + n + grain
                            if y % bh_step == 0:
                                r, g, b = 78, 50, 24
                        if (x < bdr + 2 and y < bdr + 2) or (x > TEX_SIZE - bdr - 3 and y < bdr + 2):
                            r, g, b = 180, 185, 195
                    elif code == 3:
                        if x in (0, TEX_SIZE - 1) or y in (0, TEX_SIZE - 1) or y == TEX_SIZE // 2:
                            r, g, b = 36 + n, 42 + n, 52 + n
                        elif abs(y - TEX_SIZE // 2) <= 2:
                            r, g, b = 20, 215, 255
                        else:
                            r, g, b = 86 + n, 96 + n, 114 + n
                    elif code == 4:
                        if TEX_SIZE // 4 <= y <= (TEX_SIZE * 3) // 4:
                            r, g, b = (240, 195, 20) if ((x + y) // max(4, TEX_SIZE // 8)) % 2 == 0 else (28, 30, 34)
                        else:
                            r, g, b = 132 + n, 126 + n, 118 + n
                    elif code == 6:
                        st = y % max(6, TEX_SIZE // 5)
                        r, g, b = (220 + n, 190 + n, 135 + n) if st < 2 else ((152 + n, 126 + n, 86 + n) if st < 5 else (72, 60, 40))
                    elif code == 8:
                        row = y // max(6, TEX_SIZE // 6)
                        r, g, b = (72 + n, 68 + n, 62 + n) if (x + row * 7) % 12 < 2 or y % 8 == 0 else (98 + n, 90 + n, 80 + n)
                    ao = 0.82 + 0.18 * math.sin((y / TEX_SIZE) * math.pi)
                    r = max(0, min(255, int(r * shade * ao)))
                    g = max(0, min(255, int(g * shade * ao)))
                    b = max(0, min(255, int(b * shade * ao)))
                    surf.set_at((x, y), (r, g, b))
                    dark.set_at((x, y), (int(r * 0.54), int(g * 0.54), int(b * 0.58)))
            WALL_TEXTURES[(code, side, 0)] = surf
            WALL_TEXTURES[(code, side, 1)] = dark

generate_realistic_textures()

def can_move_to(nx, ny, pz, grid, is_bot=False):
    rad = 0.22 if is_bot else 0.25
    for dx, dy in ((-rad, -rad), (rad, -rad), (-rad, rad), (rad, rad), (0.0, 0.0)):
        ix, iy = int(nx + dx), int(ny + dy)
        if ix < 1 or ix >= 15 or iy < 1 or iy >= 15:
            return False
        cell = grid[iy][ix]
        if cell in (1, 2, 3, 7):
            return False
        if cell == 5 and pz < 0.36:
            return False
    return True

def draw_operator_sprite(surf, cx, cy, h, team, is_crouch=False, flash_blind=False, weapon="AK-47", hp_ratio=1.0):
    if h < 10:
        return
    if is_crouch:
        cy += int(h * 0.16)
        h = int(h * 0.78)
    w = max(10, int(h * 0.48))
    x0, y0 = cx - w // 2, cy - h // 2
    if team == "ZOMBIE":
        c_suit, c_vest, c_helm = (48, 92, 42), (32, 56, 28), (64, 120, 48)
    elif team == "CT":
        c_suit, c_vest, c_helm = (40, 68, 108), (22, 34, 52), (30, 52, 84)
    else:
        c_suit, c_vest, c_helm = (120, 88, 54), (54, 40, 26), (38, 32, 32)
    pygame.draw.ellipse(surf, (10, 12, 16), (cx - w // 2, y0 + h - max(4, h // 14), w, max(4, h // 10)))
    lw, ly, lh = max(3, int(w * 0.32)), y0 + int(h * 0.54), int(h * 0.40)
    pygame.draw.rect(surf, c_suit, (cx - int(w * 0.36), ly, lw, lh), border_radius=3)
    pygame.draw.rect(surf, (int(c_suit[0]*0.72), int(c_suit[1]*0.72), int(c_suit[2]*0.72)), (cx - int(w * 0.14), ly, lw // 2, lh), border_radius=2)
    pygame.draw.rect(surf, c_suit, (cx + int(w * 0.04), ly, lw, lh), border_radius=3)
    pygame.draw.rect(surf, (int(c_suit[0]*0.72), int(c_suit[1]*0.72), int(c_suit[2]*0.72)), (cx + int(w * 0.24), ly, lw // 2, lh), border_radius=2)
    pygame.draw.rect(surf, (18, 20, 24), (cx - int(w * 0.38), y0 + int(h * 0.88), lw + 3, max(3, int(h * 0.12))), border_radius=2)
    pygame.draw.rect(surf, (18, 20, 24), (cx + int(w * 0.04), y0 + int(h * 0.88), lw + 3, max(3, int(h * 0.12))), border_radius=2)
    sh_w = max(3, int(w * 0.18))
    pygame.draw.rect(surf, c_suit, (cx - int(w * 0.54), y0 + int(h * 0.24), sh_w, int(h * 0.28)), border_radius=4)
    pygame.draw.rect(surf, c_suit, (cx + int(w * 0.36), y0 + int(h * 0.24), sh_w, int(h * 0.28)), border_radius=4)
    pygame.draw.rect(surf, c_suit, (cx - int(w * 0.42), y0 + int(h * 0.22), int(w * 0.84), int(h * 0.35)), border_radius=5)
    pygame.draw.rect(surf, c_vest, (cx - int(w * 0.36), y0 + int(h * 0.25), int(w * 0.72), int(h * 0.28)), border_radius=4)
    hr = max(4, int(h * 0.135))
    hx, hy = cx, y0 + int(h * 0.14)
    pygame.draw.circle(surf, c_helm, (hx, hy), hr)
    if team == "CT":
        pygame.draw.rect(surf, (45, 215, 255), (hx - int(hr * 0.8), hy - int(hr * 0.28), int(hr * 1.6), max(2, int(hr * 0.46))), border_radius=2)
    elif team == "ZOMBIE":
        pygame.draw.circle(surf, (255, 35, 35), (hx - max(1, hr // 3), hy - 1), max(1, hr // 4))
        pygame.draw.circle(surf, (255, 35, 35), (hx + max(1, hr // 3), hy - 1), max(1, hr // 4))
    else:
        pygame.draw.rect(surf, (215, 35, 35), (hx - hr, hy - int(hr * 0.6), hr * 2, max(2, int(hr * 0.35))))
        pygame.draw.rect(surf, (215, 175, 140), (hx - int(hr * 0.55), hy - int(hr * 0.15), int(hr * 1.1), max(2, int(hr * 0.35))))
    gy = y0 + int(h * 0.36)
    if team == "ZOMBIE":
        pygame.draw.line(surf, c_helm, (cx - int(w * 0.35), gy), (cx - int(w * 0.68), gy - int(h * 0.08)), max(2, w // 6))
        pygame.draw.line(surf, c_helm, (cx + int(w * 0.35), gy), (cx + int(w * 0.68), gy - int(h * 0.08)), max(2, w // 6))
    else:
        pygame.draw.rect(surf, (24, 26, 32), (cx - int(w * 0.20), gy, int(w * 0.88), max(3, int(h * 0.065))), border_radius=2)
    if flash_blind:
        pygame.draw.circle(surf, (255, 255, 190), (hx, hy - hr - 6), max(3, hr // 2))
    if hp_ratio < 0.99 and h > 22:
        bw = max(18, int(w * 0.95))
        pygame.draw.rect(surf, (20, 22, 28), (cx - bw // 2, y0 - 8, bw, 4), border_radius=2)
        pygame.draw.rect(surf, (40, 230, 85) if hp_ratio > 0.4 else (235, 45, 45), (cx - bw // 2, y0 - 8, int(bw * max(0.0, hp_ratio)), 4), border_radius=2)

def draw_fp_weapon(surf, weapon, skin_name, team, recoil_t, walk_t, is_zoomed, inspect_t=0.0, reload_t=0.0):
    w_w, w_h = surf.get_size()
    if is_zoomed and weapon == "AWP":
        pygame.draw.circle(surf, (12, 14, 18), (w_w // 2, w_h // 2), 205, 150)
        pygame.draw.circle(surf, (32, 38, 48), (w_w // 2, w_h // 2), 201, 3)
        pygame.draw.line(surf, (18, 22, 28), (0, w_h // 2), (w_w, w_h // 2), 1)
        pygame.draw.line(surf, (18, 22, 28), (w_w // 2, 0), (w_w // 2, w_h), 1)
        pygame.draw.circle(surf, (255, 35, 35), (w_w // 2, w_h // 2), 3)
        return
    sk = SKINS.get(skin_name, SKINS["Default"])
    c1, c2, acc = sk["c1"], sk["c2"], sk["acc"]
    bob_x = int(math.cos(walk_t * 7.0) * 6)
    bob_y = int(abs(math.sin(walk_t * 7.0)) * 5)
    rec_x, rec_y = int(recoil_t * 16), int(recoil_t * 24)
    insp_x = int(math.sin(inspect_t * math.pi * 2) * 30) if inspect_t > 0 else 0
    insp_y = int(- abs(math.sin(inspect_t * math.pi)) * 20) if inspect_t > 0 else 0
    rel_y = int(math.sin(reload_t * math.pi) * 58) if reload_t > 0 else 0
    bx = w_w - 170 + bob_x + rec_x - insp_x
    by = w_h - 65 + bob_y + rec_y + insp_y + rel_y
    tx = w_w // 2 + 40 + bob_x // 2 - insp_x // 2
    ty = w_h // 2 + 34 + bob_y // 2 - rec_y // 2 + insp_y + rel_y
    sleeve = (38, 64, 102) if team == "CT" else (115, 86, 52)
    glove = (26, 30, 36)
    skin_tone = (210, 168, 135)
    pygame.draw.polygon(surf, sleeve, [(w_w // 2 - 48, w_h + 10), (w_w // 2 + 4, w_h + 10), (tx + 24, ty + 30), (tx, ty + 24)])
    pygame.draw.circle(surf, skin_tone, (tx + 14, ty + 22), 9)
    pygame.draw.circle(surf, glove, (tx + 16, ty + 18), 12)
    if weapon == "Knife":
        kx, ky = w_w - 190 + bob_x - insp_x, w_h - 90 + bob_y + insp_y - rec_y
        pygame.draw.polygon(surf, sleeve, [(w_w - 55, w_h + 10), (w_w, w_h + 10), (kx + 18, ky + 38), (kx - 8, ky + 42)])
        pygame.draw.circle(surf, glove, (kx + 4, ky + 30), 13)
        pygame.draw.rect(surf, c2, (kx - 6, ky + 6, 13, 28), border_radius=3)
        pygame.draw.polygon(surf, c1, [(kx - 4, ky + 6), (kx - 15, ky - 48), (kx + 8, ky - 32), (kx + 8, ky + 6)])
        pygame.draw.line(surf, acc, (kx - 13, ky - 44), (kx + 5, ky - 30), 2)
        return
    if recoil_t > 0.52:
        pygame.draw.circle(surf, (255, 225, 100), (tx - 16, ty - 7), random.randint(12, 20))
        pygame.draw.circle(surf, (255, 255, 225), (tx - 16, ty - 7), random.randint(5, 9))
    blen = 48 if weapon in ("AWP", "AK-47", "M4A1-S", "M3") else 22
    pygame.draw.line(surf, (28, 32, 40), (tx + 8, ty + 4), (tx - blen, ty - int(blen * 0.28)), 6 if weapon != "M3" else 9)
    if weapon in ("USP-S", "M4A1-S"):
        pygame.draw.line(surf, (44, 48, 56), (tx - 4, ty), (tx - blen - 16, ty - int((blen + 16) * 0.28)), 9)
    body_pts = [(bx + 42, by + 16), (bx + 52, by - 12), (tx + 6, ty - 12), (tx - 2, ty + 10)]
    pygame.draw.polygon(surf, c1, body_pts)
    pygame.draw.polygon(surf, c2, [(bx + 32, by + 5), (bx + 38, by - 6), (tx + 10, ty - 6), (tx + 6, ty + 5)])
    pygame.draw.line(surf, acc, (bx + 44, by - 9), (tx + 6, ty - 9), 3)
    pygame.draw.polygon(surf, (18, 22, 28), body_pts, 2)
    if weapon in ("AK-47", "M4A1-S", "MP5"):
        mag_pts = [(tx + 20, ty + 6), (tx + 36, ty + 8), (tx + 26, ty + 48), (tx + 10, ty + 44)]
        pygame.draw.polygon(surf, c2 if weapon == "AK-47" else (28, 32, 38), mag_pts)
        pygame.draw.polygon(surf, acc, mag_pts, 1)
    if weapon == "AWP":
        pygame.draw.line(surf, (20, 24, 30), (bx + 14, by - 20), (tx + 8, ty - 22), 8)
        pygame.draw.circle(surf, (40, 210, 255), (bx + 16, by - 20), 5)
    pygame.draw.polygon(surf, sleeve, [(w_w - 22, w_h + 10), (w_w + 15, w_h - 22), (bx + 30, by + 6), (bx + 6, by + 22)])
    pygame.draw.circle(surf, skin_tone, (bx + 22, by + 14), 9)
    pygame.draw.circle(surf, glove, (bx + 18, by + 10), 13)

def blit_wall_column(surf, tex, tx_i, sx, col_w, y_top, y_bot, w_h, v_frac=1.0):
    wh = y_bot - y_top
    if wh < 2 or y_bot <= 0 or y_top >= w_h or not tex:
        return
    src_h = max(1, int(TEX_SIZE * v_frac))
    if y_top >= 0 and y_bot <= w_h and wh <= 900:
        col_s = pygame.transform.scale(tex.subsurface((tx_i, 0, 1, src_h)), (col_w, wh))
        surf.blit(col_s, (sx, y_top))
    else:
        cy_top = max(0, y_top)
        cy_bot = min(w_h, y_bot)
        c_h = cy_bot - cy_top
        if c_h <= 0:
            return
        t_start = int(((cy_top - y_top) / max(1, wh)) * src_h)
        t_end = int(((cy_bot - y_top) / max(1, wh)) * src_h)
        t_start = max(0, min(src_h - 1, t_start))
        t_len = max(1, min(src_h - t_start, t_end - t_start))
        col_s = pygame.transform.scale(tex.subsurface((tx_i, t_start, 1, t_len)), (col_w, c_h))
        surf.blit(col_s, (sx, cy_top))

def render_game_3d(surf, p_x, p_y, p_z, p_angle, p_pitch, current_map_name, decals, dropped_weapons, smokes, fires, c4_obj):
    map_cfg = MAPS[current_map_name]
    grid = map_cfg["grid"]
    sky_top, sky_bot, floor_col = map_cfg["sky_top"], map_cfg["sky_bot"], map_cfg["floor"]
    w_w, w_h = surf.get_size()
    horizon = max(20, min(w_h - 20, w_h // 2 + int(p_pitch * 180)))
    for y in range(0, horizon, 4):
        f = y / max(1, horizon)
        c = (int(sky_top[0] * (1 - f) + sky_bot[0] * f), int(sky_top[1] * (1 - f) + sky_bot[1] * f), int(sky_top[2] * (1 - f) + sky_bot[2] * f))
        pygame.draw.rect(surf, c, (0, y, w_w, 4))
    for y in range(horizon, w_h, 4):
        f = min(1.0, ((y - horizon) / max(1, w_h - horizon)) ** 0.75)
        c = (int(floor_col[0] * (0.45 + 0.55 * f)), int(floor_col[1] * (0.45 + 0.55 * f)), int(floor_col[2] * (0.45 + 0.55 * f)))
        pygame.draw.rect(surf, c, (0, y, w_w, 4))

    fov = save_data.get("fov", 1.05) * (0.42 if is_zoomed and current_weapon == "AWP" else 1.0)
    num_rays = 200 if save_data.get("gfx", 2) == 2 else (140 if save_data.get("gfx", 2) == 1 else 100)
    col_w = w_w // num_rays
    half_fov = (math.pi / 3.0) * fov * 0.5
    z_buffer = [999.0] * w_w
    eye_z = 0.52 + p_z - (0.20 if is_crouching else 0.0)
    proj_scale = w_h * 0.92

    for i in range(num_rays):
        ray_a = p_angle - half_fov + (i / num_rays) * (half_fov * 2.0)
        cos_a, sin_a = math.cos(ray_a), math.sin(ray_a)
        if abs(cos_a) < 1e-6: cos_a = 1e-6
        if abs(sin_a) < 1e-6: sin_a = 1e-6
        map_x, map_y = int(p_x), int(p_y)
        delta_x, delta_y = abs(1.0 / cos_a), abs(1.0 / sin_a)
        step_x = 1 if cos_a > 0 else -1
        side_x = (map_x + 1.0 - p_x) * delta_x if cos_a > 0 else (p_x - map_x) * delta_x
        step_y = 1 if sin_a > 0 else -1
        side_y = (map_y + 1.0 - p_y) * delta_y if sin_a > 0 else (p_y - map_y) * delta_y
        
        low_hits = []
        full_hit = None
        for _ in range(28):
            if side_x < side_y:
                exit_d = side_x
                side_x += delta_x; map_x += step_x; side = 0
            else:
                exit_d = side_y
                side_y += delta_y; map_y += step_y; side = 1
            if map_x < 0 or map_x >= 16 or map_y < 0 or map_y >= 16:
                break
            cell = grid[map_y][map_x]
            if cell > 0:
                raw_d = exit_d
                wx = (p_y + raw_d * sin_a) if side == 0 else (p_x + raw_d * cos_a)
                wx -= math.floor(wx)
                corr_d = max(0.06, raw_d * math.cos(ray_a - p_angle))
                next_raw_d = min(side_x, side_y)
                corr_exit_d = max(corr_d + 0.04, next_raw_d * math.cos(ray_a - p_angle))
                if cell in (5, 6, 8):
                    low_hits.append((corr_d, corr_exit_d, cell, side, wx))
                else:
                    full_hit = (corr_d, cell, side, wx)
                    break

        sx = i * col_w
        if full_hit:
            corr_d, cell, side, wx = full_hit
            wall_top_h = 1.75 if cell == 7 else 1.0
            y_bot = int(horizon + (eye_z / corr_d) * proj_scale)
            y_top = int(horizon - ((wall_top_h - eye_z) / corr_d) * proj_scale)
            tex = WALL_TEXTURES.get((cell, side, 1 if corr_d > 8.5 else 0))
            tx_i = int(wx * TEX_SIZE) % TEX_SIZE
            blit_wall_column(surf, tex, tx_i, sx, col_w, y_top, y_bot, w_h, 1.0)
            for k in range(col_w):
                if sx + k < w_w: z_buffer[sx + k] = corr_d

        for corr_d, corr_exit_d, cell, side, wx in reversed(low_hits):
            if cell == 8:
                pit_bot = int(horizon + ((eye_z + 0.32) / corr_d) * proj_scale)
                pit_top = int(horizon + (eye_z / corr_d) * proj_scale)
                pit_far = int(horizon + ((eye_z + 0.32) / corr_exit_d) * proj_scale)
                if pit_bot > pit_far:
                    pygame.draw.rect(surf, (58, 52, 46), (sx, max(0, pit_far), col_w, min(w_h, pit_bot) - max(0, pit_far)))
                tex = WALL_TEXTURES.get((8, side, 1 if corr_d > 8.5 else 0))
                tx_i = int(wx * TEX_SIZE) % TEX_SIZE
                blit_wall_column(surf, tex, tx_i, sx, col_w, pit_top, pit_bot, w_h, 0.5)
            else:
                h_box = 0.48 if cell == 5 else 0.32
                y_bot = int(horizon + (eye_z / corr_d) * proj_scale)
                y_top = int(horizon + ((eye_z - h_box) / corr_d) * proj_scale)
                y_top_far = int(horizon + ((eye_z - h_box) / corr_exit_d) * proj_scale)
                if eye_z > h_box and y_top > y_top_far:
                    cap_col = (142, 102, 58) if cell == 5 else (175, 150, 108)
                    cy1, cy2 = max(0, y_top_far), min(w_h, y_top)
                    if cy2 > cy1:
                        pygame.draw.rect(surf, cap_col, (sx, cy1, col_w, cy2 - cy1))
                tex = WALL_TEXTURES.get((cell, side, 1 if corr_d > 8.5 else 0))
                tx_i = int(wx * TEX_SIZE) % TEX_SIZE
                blit_wall_column(surf, tex, tx_i, sx, col_w, y_top, y_bot, w_h, 0.5)
                if y_top <= horizon:
                    for k in range(col_w):
                        if sx + k < w_w: z_buffer[sx + k] = min(z_buffer[sx + k], corr_d)

    for dw in dropped_weapons:
        dx, dy = dw["x"] - p_x, dw["y"] - p_y
        dist = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) - p_angle + math.pi) % (math.pi * 2) - math.pi
        if 0.2 < dist < 12.0 and abs(ang) < half_fov:
            sx = int((0.5 + ang / (half_fov * 2.0)) * w_w)
            sy = int(horizon + (eye_z / dist) * proj_scale)
            if 0 <= sx < w_w and dist < z_buffer[sx] + 0.3:
                pygame.draw.rect(surf, (45, 52, 62), (sx - 10, sy - 4, 20, 6), border_radius=2)
                pygame.draw.rect(surf, (255, 215, 0), (sx - 4, sy - 6, 8, 3))

    for dc in decals:
        dx, dy = dc["x"] - p_x, dc["y"] - p_y
        dist = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) - p_angle + math.pi) % (math.pi * 2) - math.pi
        if 0.2 < dist < 14.0 and abs(ang) < half_fov:
            sx = int((0.5 + ang / (half_fov * 2.0)) * w_w)
            if 0 <= sx < w_w and dist <= z_buffer[sx] + 0.25:
                sy = int(horizon + ((eye_z - dc["z"]) / dist) * proj_scale)
                pygame.draw.circle(surf, dc["col"], (sx, sy), max(2, int(dc["r"] / dist)))

    if c4_obj["planted"]:
        dx, dy = c4_obj["x"] - p_x, c4_obj["y"] - p_y
        dist = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) - p_angle + math.pi) % (math.pi * 2) - math.pi
        if 0.2 < dist < 16.0 and abs(ang) < half_fov:
            sx = int((0.5 + ang / (half_fov * 2.0)) * w_w)
            sy = int(horizon + (eye_z / dist) * proj_scale)
            if 0 <= sx < w_w and dist < z_buffer[sx] + 0.3:
                pygame.draw.rect(surf, (45, 55, 45), (sx - 6, sy - 6, 12, 8))
                if int(time.time() * 5) % 2 == 0:
                    pygame.draw.circle(surf, (255, 30, 30), (sx, sy - 3), 4)

    for fr in fires:
        dx, dy = fr["x"] - p_x, fr["y"] - p_y
        dist = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) - p_angle + math.pi) % (math.pi * 2) - math.pi
        if 0.25 < dist < 14.0 and abs(ang) < half_fov:
            sx = int((0.5 + ang / (half_fov * 2.0)) * w_w)
            sy = int(horizon + (eye_z / dist) * proj_scale)
            if 0 <= sx < w_w and dist < z_buffer[sx] + 0.4:
                rad = max(6, int(75 / dist))
                pygame.draw.circle(surf, (255, 110, 20), (sx, sy), rad)
                pygame.draw.circle(surf, (255, 220, 60), (sx, sy - rad // 3), rad // 2)

    for sm in smokes:
        dx, dy = sm["x"] - p_x, sm["y"] - p_y
        dist = math.hypot(dx, dy)
        ang = (math.atan2(dy, dx) - p_angle + math.pi) % (math.pi * 2) - math.pi
        if 0.2 < dist < 15.0 and abs(ang) < half_fov * 1.3:
            sx = int((0.5 + ang / (half_fov * 2.0)) * w_w)
            sy = int(horizon + ((eye_z - 0.35) / max(0.3, dist)) * proj_scale)
            rad = min(220, max(18, int(190 / max(0.4, dist))))
            sm_s = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
            pygame.draw.circle(sm_s, (185, 192, 200, 205), (rad, rad), rad)
            surf.blit(sm_s, (sx - rad, sy - rad))
    return z_buffer, horizon, eye_z, half_fov

def draw_minimap(surf, p_x, p_y, p_angle, bots, c4_obj):
    mw, mh = 106, 106
    mp_surf = pygame.Surface((mw, mh), pygame.SRCALPHA)
    pygame.draw.circle(mp_surf, (15, 20, 28, 190), (mw // 2, mh // 2), mw // 2)
    pygame.draw.circle(mp_surf, (80, 100, 130, 230), (mw // 2, mh // 2), mw // 2, 2)
    cx, cy = mw // 2, mh // 2
    pygame.draw.line(mp_surf, (90, 230, 130, 150), (cx, cy), (cx + int(math.cos(p_angle - 0.4) * 24), cy + int(math.sin(p_angle - 0.4) * 24)), 1)
    pygame.draw.line(mp_surf, (90, 230, 130, 150), (cx, cy), (cx + int(math.cos(p_angle + 0.4) * 24), cy + int(math.sin(p_angle + 0.4) * 24)), 1)
    pygame.draw.circle(mp_surf, (45, 235, 95), (cx, cy), 4)
    for b in bots:
        if b.hp <= 0: continue
        bx_rel = int((b.x - p_x) * 10)
        by_rel = int((b.y - p_y) * 10)
        if math.hypot(bx_rel, by_rel) < mw // 2 - 6:
            col = (235, 45, 45) if b.team != team_side else (45, 130, 235)
            pygame.draw.circle(mp_surf, col, (cx + bx_rel, cy + by_rel), 3)
    if c4_obj["planted"]:
        cx_rel = int((c4_obj["x"] - p_x) * 10)
        cy_rel = int((c4_obj["y"] - p_y) * 10)
        if math.hypot(cx_rel, cy_rel) < mw // 2 - 6:
            pygame.draw.circle(mp_surf, (255, 215, 0), (cx + cx_rel, cy + cy_rel), 4)
    surf.blit(mp_surf, (surf.get_width() - mw - 12, 10))

class MPManager:
    def __init__(self):
        self.mode = "OFFLINE"
        self.room_code = "1042"
        self.players_net = {}
        self.mm_searching = False
        self.mm_timer = 0.0
        self.running = True
        self.client_id = f"pycs_{random.randint(1000, 9999)}"
        threading.Thread(target=self._global_net_loop, daemon=True).start()

    def _global_net_loop(self):
        brokers = [("broker.emqx.io", 1883), ("broker.hivemq.com", 1883), ("test.mosquitto.org", 1883)]
        b_idx = 0
        while self.running:
            if self.mode != "OFFLINE" or self.mm_searching:
                s = None
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2.5)
                    b_ip, b_port = brokers[b_idx % len(brokers)]
                    b_idx += 1
                    s.connect((b_ip, b_port))
                    cid_b = self.client_id.encode("utf-8")
                    var_hdr = b"\x00\x04MQTT\x04\x02\x00\x3c" + struct.pack(">H", len(cid_b)) + cid_b
                    s.sendall(b"\x10" + bytes([len(var_hdr)]) + var_hdr)
                    s.recv(32)
                    topic = f"pycs05_room_{self.room_code}" if self.mode == "ROOM" else "pycs05_mm_lobby"
                    top_b = topic.encode("utf-8")
                    sub_pl = b"\x00\x01" + struct.pack(">H", len(top_b)) + top_b + b"\x00"
                    s.sendall(b"\x82" + bytes([len(sub_pl)]) + sub_pl)
                    s.setblocking(False)
                    while self.running and (self.mode != "OFFLINE" or self.mm_searching):
                        payload = json.dumps({
                            "id": self.client_id, "x": round(player_x, 2), "y": round(player_y, 2),
                            "z": round(player_z, 2), "a": round(player_angle, 2),
                            "hp": int(player_hp), "t": team_side, "w": current_weapon
                        }).encode("utf-8")
                        pub_pl = struct.pack(">H", len(top_b)) + top_b + payload
                        if len(pub_pl) < 127:
                            s.sendall(b"\x30" + bytes([len(pub_pl)]) + pub_pl)
                        try:
                            raw = s.recv(512)
                            if raw and b"{" in raw:
                                js_str = raw[raw.find(b"{"):raw.rfind(b"}") + 1].decode("utf-8", errors="ignore")
                                pkt = json.loads(js_str)
                                pid = pkt.get("id")
                                if pid and pid != self.client_id:
                                    self.players_net[pid] = pkt
                        except Exception:
                            pass
                        time.sleep(0.08)
                except Exception:
                    time.sleep(1.5)
                finally:
                    if s:
                        try: s.close()
                        except Exception: pass
            else:
                time.sleep(0.25)

mp_mgr = MPManager()

def check_los_and_smoke(x1, y1, x2, y2, grid, smokes):
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist < 0.25: return True
    steps = int(dist * 5) + 1
    for s in range(1, steps):
        tx = x1 + (x2 - x1) * (s / steps)
        ty = y1 + (y2 - y1) * (s / steps)
        ix, iy = int(tx), int(ty)
        if 0 <= ix < 16 and 0 <= iy < 16 and grid[iy][ix] in (1, 2, 3, 7): return False
        for sm in smokes:
            if math.hypot(tx - sm["x"], ty - sm["y"]) < 1.65: return False
    return True

class Bot:
    def __init__(self, name, x, y, team, is_zombie=False):
        self.name = name
        self.x, self.y, self.z = float(x), float(y), 0.0
        self.team = "ZOMBIE" if is_zombie else team
        self.max_hp = 250 if is_zombie else 100
        self.hp = self.max_hp
        self.armor = 0 if is_zombie else 50
        self.helmet = not is_zombie
        self.angle = random.uniform(0, math.pi * 2)
        self.timer = random.uniform(0.8, 2.2)
        self.target_x, self.target_y = self.x, self.y
        self.weapon = "Knife" if is_zombie else ("AK-47" if team == "T" else "M4A1-S")
        self.flash_timer = 0.0
        self.shoot_cd = random.uniform(0.4, 1.1)
        self.is_crouch = False

    def update(self, dt, p_x, p_y, p_hp, grid, smokes, fires, ai_mode):
        if self.hp <= 0: return
        ix, iy = max(0, min(15, int(self.x))), max(0, min(15, int(self.y)))
        self.z = -0.32 if grid[iy][ix] == 8 else (0.48 if grid[iy][ix] == 5 else (0.28 if grid[iy][ix] == 6 else 0.0))
        for fr in fires:
            if math.hypot(self.x - fr["x"], self.y - fr["y"]) < 1.45:
                self.hp -= 25.0 * dt
                if self.hp <= 0: return
        if self.flash_timer > 0:
            self.flash_timer -= dt
            return
        if ai_mode == 0: return
        self.shoot_cd = max(0.0, self.shoot_cd - dt)
        dist_p = math.hypot(p_x - self.x, p_y - self.y)
        is_enemy = (self.team != team_side)
        can_see = is_enemy and (p_hp > 0) and (dist_p < 14.0) and check_los_and_smoke(self.x, self.y, p_x, p_y, grid, smokes)
        if self.team == "ZOMBIE" or ai_mode == 1:
            self.weapon = "Knife"
            self.target_x, self.target_y = p_x, p_y
            spd = 1.72 if self.team == "ZOMBIE" else 1.35
            if is_enemy and dist_p < 1.35 and self.shoot_cd <= 0 and p_hp > 0:
                self.shoot_cd = 0.75
                damage_player(32, self.name, "Knife", False, self.x, self.y)
        else:
            self.weapon = "AK-47" if self.team == "T" else "M4A1-S"
            spd = 1.22 if ai_mode == 3 else 1.05
            if can_see:
                self.angle = math.atan2(p_y - self.y, p_x - self.x)
                if self.shoot_cd <= 0:
                    self.shoot_cd = random.uniform(0.42, 0.85) if ai_mode == 3 else random.uniform(0.75, 1.35)
                    hit_prob = max(0.20, (0.78 if ai_mode == 3 else 0.55) - dist_p * 0.035)
                    if random.random() < hit_prob:
                        is_hs = (random.random() < (0.25 if ai_mode == 3 else 0.10))
                        damage_player(26 if is_hs else 13, self.name, self.weapon, is_hs, self.x, self.y)
            self.timer -= dt
            if self.timer <= 0:
                self.timer = random.uniform(1.8, 3.6)
                if c4_state["planted"] and self.team == "CT":
                    self.target_x, self.target_y = c4_state["x"], c4_state["y"]
                elif random.random() < 0.6 or not is_enemy:
                    self.target_x = max(1.5, min(14.5, self.x + random.uniform(-3.5, 3.5)))
                    self.target_y = max(1.5, min(14.5, self.y + random.uniform(-3.5, 3.5)))
                else:
                    self.target_x, self.target_y = p_x, p_y
        dx, dy = self.target_x - self.x, self.target_y - self.y
        if math.hypot(dx, dy) > 0.35:
            move_a = math.atan2(dy, dx)
            if not can_see: self.angle = move_a
            nx = self.x + math.cos(move_a) * spd * dt
            ny = self.y + math.sin(move_a) * spd * dt
            if can_move_to(nx, self.y, 0.45, grid, True): self.x = nx
            if can_move_to(self.x, ny, 0.45, grid, True): self.y = ny
            else: self.timer = 0.0

proj_scale = H * 0.92
game_state = "MENU"
menu_tab = "HOME"
game_mode = "DEFUSE"
GAME_MODES = ["DEFUSE", "ARMS_RACE", "ZOMBIE", "WINGMAN", "TRAINING"]
current_map_name = "Mirage Palace"
team_side = "CT"
bot_count = 4
match_rounds = 7
bot_ai_mode = 2

player_x, player_y, player_z = 2.5, 2.5, 0.0
player_vz = 0.0
player_angle, player_pitch = 0.0, 0.0
player_hp, player_armor = 100, 100
has_helmet, has_defuse_kit = True, False
player_money = 1600
loss_streak = 0
is_crouching = False

current_weapon = "USP-S"
owned_weapons = ["Knife", "USP-S"]
ammo_clips = {"USP-S": 12}
ammo_res = {"USP-S": 36}
grenade_inv = ["HE", "FLASH", "SMOKE", "MOLOTOV"]
selected_nade = "HE"

shoot_cd = 0.0
recoil_timer = 0.0
reload_timer = 0.0
inspect_timer = 0.0
walk_timer = 0.0
flash_timer = 0.0
hitmarker_timer = 0.0
headshot_banner_t = 0.0
is_firing = False
is_zoomed = False
arms_race_idx = 0

c4_state = {"planted": False, "x": 0.0, "y": 0.0, "timer": 40.0, "action_p": 0.0}
round_summary = {"active": False, "timer": 0.0, "win_team": "", "mvp": "", "reward": 0}
killcam = {"active": False, "timer": 0.0, "killer": "", "weapon": "", "hs": False, "kx": 0.0, "ky": 0.0}
case_roll = {"active": False, "timer": 0.0, "won_skin": ""}
daily_msg = ""

bots = []
decals = []
dropped_weapons = []
smokes = []
fires = []
floating_damages = []
killfeed = []
score_ct, score_t = 0, 0

def check_daily_bonus():
    global daily_msg
    today = time.strftime("%Y-%m-%d")
    if save_data.get("last_daily") != today:
        save_data["last_daily"] = today
        save_data["coins"] = save_data.get("coins", 0) + 750
        daily_msg = tr("DAILY")
        save_game()

check_daily_bonus()

def equip_weapon(w_name):
    global current_weapon, is_zoomed, reload_timer
    if w_name not in WEAPONS: return
    current_weapon = w_name
    is_zoomed = False
    reload_timer = 0.0
    if w_name not in ammo_clips:
        ammo_clips[w_name] = WEAPONS[w_name]["clip"]
        ammo_res[w_name] = WEAPONS[w_name]["res"]

def damage_player(dmg, killer_name, w_name, is_hs, kx, ky):
    global player_hp, player_armor, has_helmet
    if player_hp <= 0 or round_summary["active"]: return
    actual = dmg * (1.85 if (is_hs and not has_helmet) else 1.0)
    if player_armor > 0:
        absorbed = int(actual * 0.38)
        player_armor = max(0, player_armor - absorbed)
        actual = max(1, int(actual - absorbed))
    player_hp = max(0, int(player_hp - actual))
    play_sfx("hit", 0.6)
    if player_hp <= 0:
        save_data["deaths"] = save_data.get("deaths", 0) + 1
        save_game()
        killcam.update({"active": True, "timer": 3.0, "killer": killer_name, "weapon": w_name, "hs": is_hs, "kx": kx, "ky": ky})
        killfeed.insert(0, {"txt": f"{killer_name} [{w_name}] YOU", "timer": 4.0})

def end_round(win_team, reason):
    global score_ct, score_t, player_money, loss_streak
    if round_summary["active"]: return
    if win_team == "CT": score_ct += 1
    else: score_t += 1
    p_won = (win_team == team_side)
    if p_won:
        loss_streak = 0
        rew = 3250
        save_data["wins"] = save_data.get("wins", 0) + 1
        save_data["coins"] = save_data.get("coins", 0) + 120
    else:
        loss_streak = min(4, loss_streak + 1)
        rew = 1400 + loss_streak * 500
    player_money = min(16000, player_money + rew)
    mvp_txt = "YOU (MVP)" if p_won else (bots[0].name if bots else "Bot_Alpha")
    round_summary.update({"active": True, "timer": 3.8, "win_team": f"{win_team} {tr('WIN')} ({reason})", "mvp": mvp_txt, "reward": rew})
    save_game()

def start_round(reset_match=False):
    global player_x, player_y, player_z, player_vz, player_hp, player_armor, has_helmet
    global owned_weapons, grenade_inv, bots, decals, dropped_weapons, smokes, fires, floating_damages, score_ct, score_t, arms_race_idx, player_money
    if reset_match:
        score_ct, score_t = 0, 0
        player_money = 16000 if game_mode == "TRAINING" else 1600
        arms_race_idx = 0
        owned_weapons = ["Knife", "USP-S" if team_side == "CT" else "Deagle"]
    grid = MAPS[current_map_name]["grid"]
    sp_pts = [(1.5, 1.5), (2.5, 1.5), (1.5, 2.5), (3.5, 1.5)] if team_side == "CT" else [(14.2, 14.2), (13.2, 14.2), (14.2, 13.2), (12.2, 14.2)]
    player_x, player_y = sp_pts[0]
    for sx_p, sy_p in sp_pts:
        if can_move_to(sx_p, sy_p, 0.5, grid):
            player_x, player_y = sx_p, sy_p
            break
    player_z, player_vz = 0.0, 0.0
    player_hp, player_armor, has_helmet = 100, 100, True
    grenade_inv = ["HE", "FLASH", "SMOKE", "MOLOTOV"]
    c4_state.update({"planted": False, "x": 0.0, "y": 0.0, "timer": 40.0, "action_p": 0.0})
    round_summary["active"] = False
    killcam["active"] = False
    decals, dropped_weapons, smokes, fires, floating_damages = [], [], [], [], []
    if game_mode == "ARMS_RACE":
        w = ARMS_RACE_ORDER[min(arms_race_idx, len(ARMS_RACE_ORDER) - 1)]
        owned_weapons = ["Knife", w]
        equip_weapon(w)
    else:
        for w in owned_weapons:
            ammo_clips[w] = WEAPONS[w]["clip"]
            ammo_res[w] = WEAPONS[w]["res"]
        equip_weapon(owned_weapons[-1])
    bots = []
    cnt = 0 if game_mode == "TRAINING" else (1 if game_mode == "WINGMAN" else bot_count)
    for i in range(cnt):
        bx, by = 8.5, 8.5
        for _ in range(55):
            tx, ty = random.uniform(2.5, 13.5), random.uniform(2.5, 13.5)
            if can_move_to(tx, ty, 0.0, grid, True) and math.hypot(tx - player_x, ty - player_y) > 4.2:
                bx, by = tx, ty
                break
        is_zom = (game_mode == "ZOMBIE")
        b_team = "T" if team_side == "CT" else "CT"
        bots.append(Bot(f"Bot_{i+1}", bx, by, b_team, is_zom))

def fire_weapon():
    global shoot_cd, recoil_timer, hitmarker_timer, headshot_banner_t, arms_race_idx, player_money
    w_cfg = WEAPONS[current_weapon]
    if shoot_cd > 0 or reload_timer > 0 or player_hp <= 0: return
    if current_weapon != "Knife":
        if ammo_clips.get(current_weapon, 0) <= 0:
            play_sfx("click")
            return
        ammo_clips[current_weapon] -= 1
        if game_mode == "TRAINING":
            ammo_clips[current_weapon] = w_cfg["clip"]
    shoot_cd = w_cfg["rate"]
    recoil_timer = 1.0
    save_data["shots_fired"] = save_data.get("shots_fired", 0) + 1
    play_sfx("knife" if current_weapon == "Knife" else ("awp" if current_weapon == "AWP" else "shoot"))
    grid = MAPS[current_map_name]["grid"]
    pellets = w_cfg.get("pellets", 1)
    spread = w_cfg["spread"] * (0.4 if is_crouching else 1.0) * (0.12 if is_zoomed else 1.0)
    p_eye_z = 0.52 + player_z - (0.20 if is_crouching else 0.0)
    hit_any = False

    for _ in range(pellets):
        ray_a = player_angle + random.uniform(-spread, spread)
        cos_a, sin_a = math.cos(ray_a), math.sin(ray_a)
        dmg_mult = 1.0
        wall_bang = False
        d = 0.1
        last_cell = -1
        while d < w_cfg["range"]:
            d += 0.06
            rx, ry = player_x + cos_a * d, player_y + sin_a * d
            ix, iy = int(rx), int(ry)
            if ix < 0 or ix >= 16 or iy < 0 or iy >= 16: break
            cell = grid[iy][ix]
            bullet_z = p_eye_z + d * (player_pitch * 0.46)
            if cell in (1, 2, 3, 7):
                if len(decals) < 35:
                    decals.append({"x": rx - cos_a * 0.06, "y": ry - sin_a * 0.06, "z": max(0.1, min(0.95, bullet_z)), "col": (255, 215, 75) if cell == 3 else (26, 28, 34), "r": 14})
                break
            elif cell == 5 and bullet_z < 0.48:
                if (ix, iy) != last_cell:
                    last_cell = (ix, iy)
                    if w_cfg["pen"] > 0:
                        dmg_mult *= w_cfg["pen"]
                        wall_bang = True
                    else: break
                    if dmg_mult < 0.15: break
            bot_hit = None
            for b in bots:
                if b.hp > 0 and b.team != team_side and math.hypot(b.x - rx, b.y - ry) < 0.46:
                    bot_hit = b
                    break
            if bot_hit:
                rel_z = bullet_z - bot_hit.z
                bot_h = 0.62 if bot_hit.is_crouch else 0.78
                if -0.22 <= rel_z <= bot_h + 0.22:
                    hit_any = True
                    hit_part = "head" if rel_z >= bot_h * 0.64 else ("legs" if rel_z < bot_h * 0.25 else "chest")
                    if current_weapon == "Knife": hit_part = "chest"
                    base_d = w_cfg["dmg"] * dmg_mult
                    dmg = int(base_d * ((3.0 if not bot_hit.helmet else 2.2) if hit_part == "head" else (0.75 if hit_part == "legs" else 1.0)))
                    if bot_hit.armor > 0 and hit_part == "chest":
                        abs_v = int(dmg * 0.32)
                        bot_hit.armor = max(0, bot_hit.armor - abs_v)
                        dmg = max(1, int(dmg - abs_v))
                    bot_hit.hp -= dmg
                    hitmarker_timer = 0.28
                    floating_damages.append({
                        "text": f"HEADSHOT -{dmg}" if hit_part == "head" else f"-{dmg}",
                        "x": bot_hit.x, "y": bot_hit.y, "z": bot_hit.z + 0.65,
                        "timer": 1.1, "color": (255, 215, 0) if hit_part == "head" else (255, 65, 65)
                    })
                    if len(decals) < 35:
                        decals.append({"x": bot_hit.x, "y": bot_hit.y, "z": max(0.15, bullet_z), "col": (210, 20, 30), "r": 22})
                    if hit_part == "head":
                        headshot_banner_t = 1.2
                        play_sfx("headshot")
                    else: play_sfx("hit")
                    if bot_hit.hp <= 0:
                        save_data["kills"] = save_data.get("kills", 0) + 1
                        if hit_part == "head": save_data["headshots"] = save_data.get("headshots", 0) + 1
                        wk = save_data.setdefault("weapon_kills", {})
                        wk[current_weapon] = wk.get(current_weapon, 0) + 1
                        player_money = min(16000, player_money + 300)
                        save_data["coins"] = save_data.get("coins", 0) + 45
                        if bot_hit.weapon != "Knife" and len(dropped_weapons) < 12:
                            dropped_weapons.append({"x": bot_hit.x, "y": bot_hit.y, "weapon": bot_hit.weapon})
                        icons = ("⌖" if hit_part == "head" else "") + ("🧱" if wall_bang else "")
                        killfeed.insert(0, {"txt": f"YOU [{current_weapon} {icons}] {bot_hit.name}", "timer": 4.0})
                        if game_mode == "ARMS_RACE":
                            arms_race_idx = min(len(ARMS_RACE_ORDER) - 1, arms_race_idx + 1)
                            equip_weapon(ARMS_RACE_ORDER[arms_race_idx])
                    break
    if hit_any:
        save_data["shots_hit"] = save_data.get("shots_hit", 0) + 1

def throw_grenade():
    global selected_nade, flash_timer
    if not grenade_inv or player_hp <= 0: return
    ntype = grenade_inv.pop(0)
    selected_nade = grenade_inv[0] if grenade_inv else ""
    gx = max(1.2, min(14.8, player_x + math.cos(player_angle) * 3.8))
    gy = max(1.2, min(14.8, player_y + math.sin(player_angle) * 3.8))
    if ntype == "HE":
        play_sfx("boom")
        for b in bots:
            d = math.hypot(b.x - gx, b.y - gy)
            if b.hp > 0 and d < 3.6: b.hp -= int(98 * (1.0 - d / 3.6))
    elif ntype == "FLASH":
        play_sfx("beep")
        flash_timer = 1.6
        for b in bots:
            if math.hypot(b.x - gx, b.y - gy) < 6.5: b.flash_timer = 3.8
    elif ntype == "SMOKE":
        smokes.append({"x": gx, "y": gy, "t": 11.0})
    elif ntype == "MOLOTOV":
        play_sfx("boom", 0.5)
        fires.append({"x": gx, "y": gy, "t": 7.5})

XHAIR_COLS = [(40, 255, 75), (255, 50, 50), (45, 225, 255), (255, 230, 45), (255, 255, 255)]

def draw_crosshair(surf, moving):
    if is_zoomed and current_weapon == "AWP": return
    xh = save_data["xhair"]
    col = XHAIR_COLS[xh.get("col", 0) % len(XHAIR_COLS)]
    ln, th = xh.get("len", 9), xh.get("thick", 2)
    gap = 4 + (int(recoil_timer * 10) + (5 if moving else 0) if xh.get("dyn", True) else 0)
    if is_crouching: gap = max(2, gap - 2)
    cx, cy = W // 2, H // 2
    pygame.draw.rect(surf, col, (cx - gap - ln, cy - th // 2, ln, th))
    pygame.draw.rect(surf, col, (cx + gap, cy - th // 2, ln, th))
    pygame.draw.rect(surf, col, (cx - th // 2, cy - gap - ln, th, ln))
    pygame.draw.rect(surf, col, (cx - th // 2, cy + gap, th, ln))
    if xh.get("dot", True): pygame.draw.circle(surf, col, (cx, cy), max(1, th))
    if hitmarker_timer > 0:
        hc = (255, 215, 0) if headshot_banner_t > 0.9 else (255, 55, 55)
        pygame.draw.line(surf, hc, (cx - 9, cy - 9), (cx - 3, cy - 3), 2)
        pygame.draw.line(surf, hc, (cx + 9, cy - 9), (cx + 3, cy - 3), 2)
        pygame.draw.line(surf, hc, (cx - 9, cy + 9), (cx - 3, cy + 3), 2)
        pygame.draw.line(surf, hc, (cx + 9, cy + 9), (cx + 3, cy + 3), 2)

def draw_hud_btn(surf, name, data, is_active=False, joy_offset=(0, 0)):
    bx, by = int(data["x"]), int(data["y"])
    r = max(14, int(data["r"] * data.get("s", 1.0)))
    alpha = max(10, min(255, int(data.get("a", 115))))
    bs = pygame.Surface((r * 2 + 8, r * 2 + 8), pygame.SRCALPHA)
    bg_a = alpha // 2 if name == "joy" else alpha
    col = (55, 145, 245, bg_a) if is_active else ((215, 55, 45, bg_a) if name == "fire" else (28, 34, 46, bg_a))
    pygame.draw.circle(bs, col, (r + 4, r + 4), r)
    pygame.draw.circle(bs, (220, 235, 255, min(255, alpha + 40)), (r + 4, r + 4), r, 2)
    if name == "joy":
        kx = r + 4 + int(max(-1.0, min(1.0, joy_offset[0])) * (r * 0.55))
        ky = r + 4 + int(max(-1.0, min(1.0, joy_offset[1])) * (r * 0.55))
        pygame.draw.circle(bs, (235, 245, 255, min(255, alpha + 70)), (kx, ky), max(10, int(r * 0.38)))
    else:
        labels = {"fire": "FIRE", "reload": "RLD", "zoom": "ZOOM", "jump": "JUMP", "crouch": "CRCH", "shop": "SHOP", "inspect": "INSP", "drop": tr("DROP")[:4], "grenade": selected_nade or "NADE", "c4_btn": "C4"}
        txt = font_xs.render(labels.get(name, name[:4].upper()), True, (255, 255, 255))
        txt.set_alpha(min(255, alpha + 65))
        bs.blit(txt, txt.get_rect(center=(r + 4, r + 4)))
    surf.blit(bs, (bx - r - 4, by - r - 4))

def spawn_one_bot(b_team):
    grid = MAPS[current_map_name]["grid"]
    bx, by = 8.5, 8.5
    for _ in range(45):
        tx, ty = random.uniform(2.5, 13.5), random.uniform(2.5, 13.5)
        if can_move_to(tx, ty, 0.0, grid, True) and math.hypot(tx - player_x, ty - player_y) > 3.5:
            bx, by = tx, ty
            break
    bots.append(Bot(f"Bot_{len(bots)+1}", bx, by, b_team, game_mode == "ZOMBIE"))

def main_loop():
    global game_state, menu_tab, game_mode, current_map_name, team_side, bot_count, bot_ai_mode
    global player_x, player_y, player_z, player_vz, player_angle, player_pitch, player_hp, player_armor, has_helmet, has_defuse_kit, player_money
    global current_weapon, is_crouching, is_firing, is_zoomed, shoot_cd, recoil_timer, reload_timer, inspect_timer, walk_timer, flash_timer, hitmarker_timer, headshot_banner_t, arms_race_idx
    active_hud_key = "fire"
    dragging_hud_key = None
    joy_vec = [0.0, 0.0]
    joy_finger_id = None
    look_finger_id = None
    fire_finger_id = None
    last_ui_click = 0
    show_pause_menu = False
    show_scoreboard = False
    nearby_drop = None
    running = True

    while running:
        dt = min(0.05, clock.tick(60) / 1000.0)
        now_ms = pygame.time.get_ticks()
        save_data["play_time"] = save_data.get("play_time", 0.0) + dt
        m_pos = pygame.mouse.get_pos()
        m_down = pygame.mouse.get_pressed()[0]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_game()
                running = False

            elif e.type == pygame.FINGERDOWN and game_state == "PLAY" and not show_pause_menu:
                fx, fy = e.x * W, e.y * H
                lay = save_data["layout"]
                jv = lay["joy"]
                jr = int(jv["r"] * jv.get("s", 1.0))
                fb = lay["fire"]
                fr_r = int(fb["r"] * fb.get("s", 1.0))
                if math.hypot(fx - jv["x"], fy - jv["y"]) <= jr * 2.0:
                    joy_finger_id = e.finger_id
                    joy_vec = [max(-1.0, min(1.0, (fx - jv["x"]) / max(1, jr))), max(-1.0, min(1.0, (fy - jv["y"]) / max(1, jr)))]
                elif math.hypot(fx - fb["x"], fy - fb["y"]) <= fr_r + 12:
                    fire_finger_id = e.finger_id
                    is_firing = True
                    fire_weapon()
                elif fx > W * 0.32:
                    look_finger_id = e.finger_id

            elif e.type == pygame.FINGERMOTION and game_state == "PLAY" and not show_pause_menu:
                fx, fy = e.x * W, e.y * H
                if e.finger_id == joy_finger_id:
                    jv = save_data["layout"]["joy"]
                    jr = int(jv["r"] * jv.get("s", 1.0))
                    joy_vec = [max(-1.0, min(1.0, (fx - jv["x"]) / max(1, jr))), max(-1.0, min(1.0, (fy - jv["y"]) / max(1, jr)))]
                elif e.finger_id == look_finger_id:
                    sens = save_data.get("sens", 1.0) * (0.45 if is_zoomed else 1.0)
                    player_angle = (player_angle + e.dx * W * 0.0055 * sens) % (math.pi * 2)
                    player_pitch = max(-0.75, min(0.75, player_pitch - e.dy * H * 0.005 * sens))

            elif e.type == pygame.FINGERUP:
                if e.finger_id == joy_finger_id:
                    joy_finger_id = None
                    joy_vec = [0.0, 0.0]
                elif e.finger_id == fire_finger_id:
                    fire_finger_id = None
                    is_firing = False
                elif e.finger_id == look_finger_id:
                    look_finger_id = None

            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                if game_state != "PLAY" and now_ms - last_ui_click < 180: continue
                last_ui_click = now_ms
                play_sfx("click", 0.4)

                if game_state == "MENU":
                    if 18 <= my <= 65:
                        for t_n, t_x in [("HOME", 25), ("INV", 145), ("MP", 265), ("STAT", 385), ("SET", 505)]:
                            if t_x <= mx <= t_x + 112: menu_tab = t_n
                    elif menu_tab == "HOME":
                        if W - 245 <= mx <= W - 25 and H - 90 <= my <= H - 22:
                            game_state = "TEAM_SELECT"
                        elif 40 <= mx <= 265:
                            if 155 <= my <= 188: current_map_name = MAP_NAMES[(MAP_NAMES.index(current_map_name) + 1) % len(MAP_NAMES)]
                            elif 192 <= my <= 225:
                                game_mode = GAME_MODES[(GAME_MODES.index(game_mode) + 1) % len(GAME_MODES)]
                                if game_mode == "TRAINING": bot_count = 0
                            elif 228 <= my <= 260: bot_count = 0 if bot_count >= 8 else bot_count + 1
                            elif 264 <= my <= 296: bot_ai_mode = (bot_ai_mode + 1) % 4
                            elif 300 <= my <= 332:
                                save_data["lang"] = "EN" if save_data.get("lang", "RU") == "RU" else "RU"
                                save_game()
                    elif menu_tab == "INV":
                        if 40 <= mx <= 260 and 100 <= my <= 148:
                            if save_data.get("coins", 0) >= 600:
                                save_data["coins"] -= 600
                                won = random.choice(list(SKINS.keys())[1:])
                                if won not in save_data["inv"]: save_data["inv"].append(won)
                                case_roll.update({"active": True, "timer": 2.5, "won_skin": won})
                                save_game()
                        elif 280 <= mx <= 500 and 100 <= my <= 148:
                            current_weapon = WEAPON_ORDER[(WEAPON_ORDER.index(current_weapon) + 1) % len(WEAPON_ORDER)]
                        y_s = 170
                        for sk_n in SKINS:
                            if 40 <= mx <= 500 and y_s <= my <= y_s + 32:
                                if sk_n in save_data["inv"] or sk_n == "Default":
                                    save_data["equipped"][current_weapon] = sk_n
                                    save_game()
                                elif save_data["coins"] >= SKINS[sk_n]["price"]:
                                    save_data["coins"] -= SKINS[sk_n]["price"]
                                    save_data["inv"].append(sk_n)
                                    save_data["equipped"][current_weapon] = sk_n
                                    save_game()
                            y_s += 36
                    elif menu_tab == "MP":
                        if 40 <= mx <= 310 and 130 <= my <= 176: mp_mgr.mode = "ROOM" if mp_mgr.mode == "OFFLINE" else "OFFLINE"
                        elif 330 <= mx <= 540 and 130 <= my <= 176: mp_mgr.room_code = str(1000 + (int(mp_mgr.room_code) - 999) % 8999)
                        elif 40 <= mx <= 310 and 195 <= my <= 242:
                            mp_mgr.mm_searching = not mp_mgr.mm_searching
                            mp_mgr.mm_timer = 0.0
                    elif menu_tab == "SET":
                        xh = save_data["xhair"]
                        if 40 <= mx <= 280:
                            if 110 <= my <= 145: xh["col"] = (xh["col"] + 1) % len(XHAIR_COLS)
                            elif 152 <= my <= 187: xh["len"] = 5 if xh["len"] >= 15 else xh["len"] + 2
                            elif 194 <= my <= 229: xh["thick"] = 1 if xh["thick"] >= 4 else xh["thick"] + 1
                            elif 236 <= my <= 271: xh["dot"] = not xh["dot"]
                            elif 278 <= my <= 313: xh["dyn"] = not xh["dyn"]
                            elif 320 <= my <= 355:
                                save_data["gfx"] = (save_data.get("gfx", 2) + 1) % 3
                                generate_realistic_textures()
                            elif 362 <= my <= 397:
                                save_data["lang"] = "EN" if save_data.get("lang", "RU") == "RU" else "RU"
                        elif W - 250 <= mx <= W - 30 and H - 85 <= my <= H - 28:
                            game_state = "HUD_EDIT"
                        save_game()

                elif game_state == "TEAM_SELECT":
                    if 105 <= my <= 190:
                        team_side = "CT"; start_round(reset_match=True); game_state = "PLAY"
                    elif 210 <= my <= 295:
                        team_side = "T"; start_round(reset_match=True); game_state = "PLAY"
                    elif 320 <= my <= 375: game_state = "MENU"

                elif game_state == "HUD_EDIT":
                    if W - 165 <= mx <= W - 20 and H - 62 <= my <= H - 15:
                        save_game(); game_state = "MENU"
                    elif active_hud_key in save_data["layout"] and (W // 2 - 170 <= mx <= W // 2 + 170 and 12 <= my <= 115):
                        bd = save_data["layout"][active_hud_key]
                        if W // 2 - 155 <= mx <= W // 2 - 105 and 42 <= my <= 72: bd["s"] = round(max(0.5, bd.get("s", 1.0) - 0.1), 2)
                        elif W // 2 + 10 <= mx <= W // 2 + 60 and 42 <= my <= 72: bd["s"] = round(min(1.8, bd.get("s", 1.0) + 0.1), 2)
                        elif W // 2 - 155 <= mx <= W // 2 - 105 and 76 <= my <= 106: bd["a"] = max(10, bd.get("a", 115) - 20)
                        elif W // 2 + 10 <= mx <= W // 2 + 60 and 76 <= my <= 106: bd["a"] = min(255, bd.get("a", 115) + 20)
                        elif W // 2 + 72 <= mx <= W // 2 + 160 and 45 <= my <= 102:
                            for k in save_data["layout"]: save_data["layout"][k]["a"] = bd["a"]
                        save_game()
                    else:
                        for bk, bv in save_data["layout"].items():
                            if math.hypot(mx - bv["x"], my - bv["y"]) <= int(bv["r"] * bv.get("s", 1.0)) + 12:
                                active_hud_key = bk; dragging_hud_key = bk; break

                elif game_state == "BUY_MENU":
                    if W - 165 <= mx <= W - 25 and 22 <= my <= 68: game_state = "PLAY"
                    y_b = 92
                    for w_n in WEAPON_ORDER[1:]:
                        if 40 <= mx <= 385 and y_b <= my <= y_b + 38:
                            pr = WEAPONS[w_n]["price"]
                            if player_money >= pr:
                                player_money -= pr
                                w_slot = WEAPONS[w_n]["slot"]
                                for old_w in owned_weapons[:]:
                                    if old_w != "Knife" and WEAPONS[old_w]["slot"] == w_slot and old_w != w_n:
                                        owned_weapons.remove(old_w); dropped_weapons.append({"x": player_x, "y": player_y, "weapon": old_w})
                                if w_n not in owned_weapons: owned_weapons.append(w_n)
                                ammo_clips[w_n] = WEAPONS[w_n]["clip"]; ammo_res[w_n] = WEAPONS[w_n]["res"]
                                equip_weapon(w_n)
                        y_b += 42
                    if 425 <= mx <= 755:
                        if 95 <= my <= 142 and player_money >= 1000: player_money -= 1000; player_armor = 100; has_helmet = True
                        elif 155 <= my <= 202 and player_money >= 400 and not has_defuse_kit: player_money -= 400; has_defuse_kit = True
                        elif 215 <= my <= 262 and player_money >= 300 and len(grenade_inv) < 4: player_money -= 300; grenade_inv = ["HE", "FLASH", "SMOKE", "MOLOTOV"]; selected_nade = "HE"

                elif game_state == "PLAY":
                    if show_pause_menu:
                        px0, py0 = W // 2 - 190, H // 2 - 135
                        if px0 + 20 <= mx <= px0 + 360 and py0 + 48 <= my <= py0 + 84: show_pause_menu = False
                        elif px0 + 20 <= mx <= px0 + 185 and py0 + 92 <= my <= py0 + 128: spawn_one_bot("CT")
                        elif px0 + 195 <= mx <= px0 + 360 and py0 + 92 <= my <= py0 + 128:
                            for b in reversed(bots):
                                if b.team == "CT": bots.remove(b); break
                        elif px0 + 20 <= mx <= px0 + 185 and py0 + 136 <= my <= py0 + 172: spawn_one_bot("T")
                        elif px0 + 195 <= mx <= px0 + 360 and py0 + 136 <= my <= py0 + 172:
                            for b in reversed(bots):
                                if b.team in ("T", "ZOMBIE"): bots.remove(b); break
                        elif px0 + 20 <= mx <= px0 + 185 and py0 + 180 <= my <= py0 + 216: bot_ai_mode = (bot_ai_mode + 1) % 4
                        elif px0 + 195 <= mx <= px0 + 360 and py0 + 180 <= my <= py0 + 216: bots.clear()
                        elif px0 + 20 <= mx <= px0 + 360 and py0 + 224 <= my <= py0 + 260:
                            show_pause_menu = False; game_state = "MENU"
                        continue

                    if 10 <= mx <= 95 and 10 <= my <= 44: show_pause_menu = True; continue
                    if W // 2 - 110 <= mx <= W // 2 + 110 and 8 <= my <= 42: show_scoreboard = not show_scoreboard; continue

                    if nearby_drop and (W // 2 - 95 <= mx <= W // 2 + 95 and H - 92 <= my <= H - 52):
                        wn = nearby_drop["weapon"]; w_slot = WEAPONS[wn]["slot"]
                        for old_w in owned_weapons[:]:
                            if old_w != "Knife" and WEAPONS[old_w]["slot"] == w_slot:
                                owned_weapons.remove(old_w); dropped_weapons.append({"x": player_x, "y": player_y, "weapon": old_w})
                        if nearby_drop in dropped_weapons: dropped_weapons.remove(nearby_drop)
                        owned_weapons.append(wn); equip_weapon(wn); nearby_drop = None
                        continue

                    lay = save_data["layout"]
                    shop_b = lay["shop"]
                    if math.hypot(mx - shop_b["x"], my - shop_b["y"]) <= int(shop_b["r"] * shop_b.get("s", 1.0)) + 12:
                        game_state = "BUY_MENU"; continue

                    bar_x = W // 2 - (len(owned_weapons) * 48)
                    clicked_slot = False
                    for idx_w, ow in enumerate(owned_weapons):
                        if bar_x + idx_w * 96 <= mx <= bar_x + idx_w * 96 + 90 and H - 44 <= my <= H - 6:
                            equip_weapon(ow); clicked_slot = True
                    if clicked_slot: continue

                    jv = lay["joy"]
                    jr = int(jv["r"] * jv.get("s", 1.0))
                    if math.hypot(mx - jv["x"], my - jv["y"]) <= jr * 1.95:
                        joy_vec = [max(-1.0, min(1.0, (mx - jv["x"]) / max(1, jr))), max(-1.0, min(1.0, (my - jv["y"]) / max(1, jr)))]
                    else:
                        for bk, bv in lay.items():
                            if bk in ("joy", "shop"): continue
                            br = int(bv["r"] * bv.get("s", 1.0))
                            if math.hypot(mx - bv["x"], my - bv["y"]) <= br + 10:
                                if bk == "fire": is_firing = True; fire_weapon()
                                elif bk == "reload" and current_weapon != "Knife":
                                    need = WEAPONS[current_weapon]["clip"] - ammo_clips.get(current_weapon, 0)
                                    if need > 0 and ammo_res.get(current_weapon, 0) > 0: reload_timer = 1.1; play_sfx("reload")
                                elif bk == "zoom": is_zoomed = not is_zoomed
                                elif bk == "jump" and player_vz == 0.0: player_vz = 2.65
                                elif bk == "crouch": is_crouching = not is_crouching
                                elif bk == "inspect": inspect_timer = 1.0
                                elif bk == "drop" and current_weapon != "Knife":
                                    dropped_weapons.append({"x": player_x + math.cos(player_angle) * 0.65, "y": player_y + math.sin(player_angle) * 0.65, "weapon": current_weapon})
                                    owned_weapons.remove(current_weapon); equip_weapon(owned_weapons[-1])
                                elif bk == "grenade": throw_grenade()

            elif e.type == pygame.MOUSEBUTTONUP:
                dragging_hud_key = None
                if fire_finger_id is None: is_firing = False
                if joy_finger_id is None: joy_vec = [0.0, 0.0]

            elif e.type == pygame.MOUSEMOTION:
                if game_state == "HUD_EDIT" and dragging_hud_key:
                    save_data["layout"][dragging_hud_key]["x"] = max(25, min(W - 25, e.pos[0]))
                    save_data["layout"][dragging_hud_key]["y"] = max(25, min(H - 25, e.pos[1]))
                elif game_state == "PLAY" and not show_pause_menu and m_down and joy_finger_id is None and look_finger_id is None:
                    jv = save_data["layout"]["joy"]
                    jr = int(jv["r"] * jv.get("s", 1.0))
                    if math.hypot(e.pos[0] - jv["x"], e.pos[1] - jv["y"]) <= jr * 2.2:
                        joy_vec = [max(-1.0, min(1.0, (e.pos[0] - jv["x"]) / max(1, jr))), max(-1.0, min(1.0, (e.pos[1] - jv["y"]) / max(1, jr)))]
                    elif e.pos[0] > W * 0.34:
                        sens = save_data.get("sens", 1.0) * (0.45 if is_zoomed else 1.0)
                        player_angle = (player_angle + e.rel[0] * 0.0055 * sens) % (math.pi * 2)
                        player_pitch = max(-0.75, min(0.75, player_pitch - e.rel[1] * 0.005 * sens))

        if game_state == "PLAY" and not show_pause_menu:
            shoot_cd = max(0.0, shoot_cd - dt)
            recoil_timer = max(0.0, recoil_timer - dt * 4.5)
            inspect_timer = max(0.0, inspect_timer - dt)
            flash_timer = max(0.0, flash_timer - dt)
            hitmarker_timer = max(0.0, hitmarker_timer - dt)
            headshot_banner_t = max(0.0, headshot_banner_t - dt)
            if reload_timer > 0:
                reload_timer -= dt
                if reload_timer <= 0:
                    take = min(WEAPONS[current_weapon]["clip"] - ammo_clips[current_weapon], ammo_res[current_weapon])
                    ammo_clips[current_weapon] += take; ammo_res[current_weapon] -= take
            if is_firing and WEAPONS[current_weapon]["auto"] and shoot_cd <= 0: fire_weapon()

            for fd in floating_damages[:]:
                fd["timer"] -= dt; fd["z"] += dt * 0.28
                if fd["timer"] <= 0: floating_damages.remove(fd)
            for kf in killfeed[:]:
                kf["timer"] -= dt
                if kf["timer"] <= 0: killfeed.remove(kf)
            for sm in smokes[:]:
                sm["t"] -= dt
                if sm["t"] <= 0: smokes.remove(sm)
            for fr in fires[:]:
                fr["t"] -= dt
                if math.hypot(player_x - fr["x"], player_y - fr["y"]) < 1.45 and player_hp > 0:
                    damage_player(18 * dt, "Molotov", "MOLOTOV", False, fr["x"], fr["y"])
                if fr["t"] <= 0: fires.remove(fr)

            nearby_drop = None
            for dw in dropped_weapons[:]:
                if math.hypot(player_x - dw["x"], player_y - dw["y"]) < 0.95:
                    wn = dw["weapon"]; w_slot = WEAPONS[wn]["slot"]
                    has_slot = any(WEAPONS[w]["slot"] == w_slot for w in owned_weapons if w != "Knife")
                    if not has_slot:
                        owned_weapons.append(wn); equip_weapon(wn); dropped_weapons.remove(dw)
                    else: nearby_drop = dw
                    break

            grid = MAPS[current_map_name]["grid"]
            moving = False
            if player_hp > 0 and (abs(joy_vec[0]) > 0.06 or abs(joy_vec[1]) > 0.06):
                moving = True; walk_timer += dt
                spd = (1.45 if is_crouching else 2.55) * dt
                fwd, strafe = -joy_vec[1] * spd, joy_vec[0] * spd
                nx = player_x + math.cos(player_angle) * fwd - math.sin(player_angle) * strafe
                ny = player_y + math.sin(player_angle) * fwd + math.cos(player_angle) * strafe
                if can_move_to(nx, player_y, player_z, grid): player_x = nx
                if can_move_to(player_x, ny, player_z, grid): player_y = ny

            ix_p, iy_p = max(0, min(15, int(player_x))), max(0, min(15, int(player_y)))
            cc = grid[iy_p][ix_p]
            ground_z = -0.32 if cc == 8 else (0.48 if cc == 5 else (0.32 if cc == 6 else 0.0))
            if player_z > ground_z or player_vz != 0.0:
                player_z += player_vz * dt; player_vz -= 6.8 * dt
                if player_z <= ground_z: player_z, player_vz = ground_z, 0.0
            else:
                player_z = ground_z

            c4_btn = save_data["layout"]["c4_btn"]
            holding_c4 = m_down and math.hypot(m_pos[0] - c4_btn["x"], m_pos[1] - c4_btn["y"]) <= 50
            if game_mode == "DEFUSE" and player_hp > 0:
                on_site = (cc == 4)
                if not c4_state["planted"] and team_side == "T" and on_site and holding_c4:
                    c4_state["action_p"] += dt / 3.0
                    if c4_state["action_p"] >= 1.0:
                        c4_state.update({"planted": True, "x": player_x, "y": player_y, "timer": 40.0, "action_p": 0.0})
                        save_data["bombs"] = save_data.get("bombs", 0) + 1
                        player_money = min(16000, player_money + 300); play_sfx("beep")
                elif c4_state["planted"] and team_side == "CT" and math.hypot(player_x - c4_state["x"], player_y - c4_state["y"]) < 1.8 and holding_c4:
                    def_time = 2.5 if has_defuse_kit else 5.0
                    c4_state["action_p"] += dt / def_time
                    if c4_state["action_p"] >= 1.0: end_round("CT", "BOMB DEFUSED")
                else: c4_state["action_p"] = 0.0
                if c4_state["planted"]:
                    c4_state["timer"] -= dt
                    if c4_state["timer"] <= 0: play_sfx("boom"); end_round("T", "BOMB EXPLODED")

            alive_enemies = 0
            for b in bots:
                b.update(dt, player_x, player_y, player_hp, grid, smokes, fires, bot_ai_mode)
                if b.hp > 0 and b.team != team_side: alive_enemies += 1
            if not round_summary["active"] and game_mode != "TRAINING" and len(bots) > 0:
                if alive_enemies == 0: end_round(team_side, "ENEMIES ELIMINATED")
                elif player_hp <= 0 and not killcam["active"]: end_round("T" if team_side == "CT" else "CT", "OPERATOR DOWN")

            if killcam["active"]:
                killcam["timer"] -= dt
                player_angle = math.atan2(killcam["ky"] - player_y, killcam["kx"] - player_x)
                if killcam["timer"] <= 0: killcam["active"] = False
            if round_summary["active"]:
                round_summary["timer"] -= dt
                if round_summary["timer"] <= 0: start_round(reset_match=False)

        if game_state == "PLAY":
            zb, horizon, eye_z, hfov = render_game_3d(screen, player_x, player_y, player_z, player_angle, player_pitch, current_map_name, decals, dropped_weapons, smokes, fires, c4_state)
            for b in sorted(bots, key=lambda x: math.hypot(x.x - player_x, x.y - player_y), reverse=True):
                if b.hp <= 0: continue
                dx, dy = b.x - player_x, b.y - player_y
                dist = math.hypot(dx, dy)
                ang = (math.atan2(dy, dx) - player_angle + math.pi) % (math.pi * 2) - math.pi
                if 0.25 < dist < 16.5 and abs(ang) < hfov * 1.15:
                    sx = int((0.5 + ang / (hfov * 2.0)) * W)
                    if 0 <= sx < W and dist <= zb[sx] + 0.35:
                        bh = int((H * 0.78) / dist)
                        sy = int(horizon + ((eye_z - b.z - 0.38) / dist) * proj_scale)
                        draw_operator_sprite(screen, sx, sy, bh, b.team, b.is_crouch, b.flash_timer > 0, b.weapon, b.hp / b.max_hp)

            for np_id, np_d in list(mp_mgr.players_net.items()):
                dx, dy = np_d.get("x", 0) - player_x, np_d.get("y", 0) - player_y
                dist = math.hypot(dx, dy)
                ang = (math.atan2(dy, dx) - player_angle + math.pi) % (math.pi * 2) - math.pi
                if 0.25 < dist < 16.5 and abs(ang) < hfov * 1.15:
                    sx = int((0.5 + ang / (hfov * 2.0)) * W)
                    if 0 <= sx < W and dist <= zb[sx] + 0.35:
                        bh = int((H * 0.78) / dist)
                        sy = int(horizon + ((eye_z - 0.38) / dist) * proj_scale)
                        draw_operator_sprite(screen, sx, sy, bh, np_d.get("t", "T"), False, False, np_d.get("w", "AK-47"), np_d.get("hp", 100) / 100.0)

            for fd in floating_damages:
                dx, dy = fd["x"] - player_x, fd["y"] - player_y
                dist = math.hypot(dx, dy)
                ang = (math.atan2(dy, dx) - player_angle + math.pi) % (math.pi * 2) - math.pi
                if 0.2 < dist < 13.0 and abs(ang) < hfov:
                    sx = int((0.5 + ang / (hfov * 2.0)) * W)
                    sy = int(horizon + ((eye_z - fd["z"]) / dist) * proj_scale)
                    txt_fd = font_sm.render(fd["text"], True, fd["color"])
                    screen.blit(txt_fd, txt_fd.get_rect(center=(sx, sy)))

            sk_eq = save_data["equipped"].get(current_weapon, "Default")
            draw_fp_weapon(screen, current_weapon, sk_eq, team_side, recoil_timer, walk_timer, is_zoomed, inspect_timer, reload_timer)
            draw_crosshair(screen, abs(joy_vec[0]) > 0.06 or abs(joy_vec[1]) > 0.06)
            draw_minimap(screen, player_x, player_y, player_angle, bots, c4_state)
            if flash_timer > 0:
                fs = pygame.Surface((W, H), pygame.SRCALPHA)
                fs.fill((255, 255, 255, min(245, int(flash_timer * 165))))
                screen.blit(fs, (0, 0))

            pygame.draw.rect(screen, (20, 24, 32), (10, 10, 82, 32), border_radius=6)
            screen.blit(font_xs.render(tr("PAUSE"), True, (255, 255, 255)), (24, 20))
            pygame.draw.rect(screen, (20, 24, 32), (W // 2 - 110, 8, 220, 32), border_radius=6)
            screen.blit(font_sm.render(f"CT {score_ct}  |  {game_mode[:6]}  |  {score_t} T", True, (255, 235, 120)), (W // 2 - 92, 15))
            if c4_state["planted"]:
                screen.blit(font_md.render(f"C4: {c4_state['timer']:.1f}s", True, (255, 50, 50)), (W // 2 - 48, 44))
            if c4_state["action_p"] > 0:
                pygame.draw.rect(screen, (40, 235, 95), (W // 2 - 80, H // 2 + 45, int(160 * c4_state["action_p"]), 10))
            if headshot_banner_t > 0:
                screen.blit(font_md.render(tr("HEADSHOT"), True, (255, 215, 0)), (W // 2 - 75, 70))

            for i_kf, kf in enumerate(killfeed[:4]):
                kf_surf = font_xs.render(kf["txt"], True, (255, 235, 150))
                pygame.draw.rect(screen, (18, 22, 30), (W - kf_surf.get_width() - 142, 14 + i_kf * 22, kf_surf.get_width() + 14, 19), border_radius=4)
                screen.blit(kf_surf, (W - kf_surf.get_width() - 135, 16 + i_kf * 22))

            if nearby_drop:
                pygame.draw.rect(screen, (38, 125, 215), (W // 2 - 95, H - 88, 190, 34), border_radius=6)
                screen.blit(font_sm.render(f"{tr('TAKE')} {nearby_drop['weapon']}", True, (255, 255, 255)), (W // 2 - 68, H - 79))

            screen.blit(font_md.render(f"HP: {player_hp}  |  ARM: {player_armor}  |  ${player_money}", True, (110, 245, 130)), (14, H - 32))
            if current_weapon != "Knife":
                screen.blit(font_md.render(f"{current_weapon}: {ammo_clips.get(current_weapon,0)}/{ammo_res.get(current_weapon,0)}", True, (255, 235, 140)), (W - 190, H - 32))

            bar_x = W // 2 - (len(owned_weapons) * 48)
            for idx_w, ow in enumerate(owned_weapons):
                r_box = (bar_x + idx_w * 96, H - 42, 88, 32)
                pygame.draw.rect(screen, (45, 125, 225) if ow == current_weapon else (28, 34, 44), r_box, border_radius=5)
                screen.blit(font_xs.render(ow, True, (255, 255, 255)), (r_box[0] + 12, r_box[1] + 9))

            for bk, bv in save_data["layout"].items():
                draw_hud_btn(screen, bk, bv, False, joy_vec if bk == "joy" else (0, 0))

            if round_summary["active"]:
                pygame.draw.rect(screen, (22, 28, 38), (W // 2 - 200, H // 2 - 65, 400, 115), border_radius=10)
                pygame.draw.rect(screen, (255, 215, 0), (W // 2 - 200, H // 2 - 65, 400, 115), 2, border_radius=10)
                screen.blit(font_md.render(round_summary["win_team"], True, (255, 230, 90)), (W // 2 - 175, H // 2 - 48))
                screen.blit(font_sm.render(f"{round_summary['mvp']}  |  +${round_summary['reward']}", True, (210, 230, 255)), (W // 2 - 150, H // 2 - 8))

            if show_pause_menu:
                ov = pygame.Surface((W, H), pygame.SRCALPHA); ov.fill((0, 0, 0, 175)); screen.blit(ov, (0, 0))
                px0, py0 = W // 2 - 190, H // 2 - 135
                pygame.draw.rect(screen, (26, 32, 44), (px0, py0, 380, 275), border_radius=10)
                screen.blit(font_lg.render(tr("PAUSE"), True, (255, 235, 100)), (px0 + 135, py0 + 10))
                pygame.draw.rect(screen, (45, 165, 85), (px0 + 20, py0 + 48, 340, 36), border_radius=6)
                screen.blit(font_sm.render(tr("RESUME"), True, (255, 255, 255)), (px0 + 115, py0 + 57))
                for bx_o, by_o, bw_o, lbl_o in [
                    (20, 92, 165, "+ Bot CT"), (195, 92, 165, "- Bot CT"),
                    (20, 136, 165, "+ Bot T"), (195, 136, 165, "- Bot T"),
                    (20, 180, 165, f"AI: {tr(f'AI_{bot_ai_mode}')[:10]}"), (195, 180, 165, "Clear Bots (0)"),
                    (20, 224, 340, tr("TO_MENU"))
                ]:
                    pygame.draw.rect(screen, (48, 62, 86) if by_o < 220 else (185, 48, 48), (px0 + bx_o, py0 + by_o, bw_o, 36), border_radius=6)
                    screen.blit(font_xs.render(lbl_o, True, (255, 255, 255)), (px0 + bx_o + 18, py0 + by_o + 11))

            if show_scoreboard:
                ov = pygame.Surface((W, H), pygame.SRCALPHA); ov.fill((0, 0, 0, 155)); screen.blit(ov, (0, 0))
                pygame.draw.rect(screen, (24, 30, 40), (W // 2 - 220, 55, 440, 290), border_radius=8)
                screen.blit(font_md.render(f"SCOREBOARD — CT {score_ct} : {score_t} T", True, (255, 230, 90)), (W // 2 - 135, 68))
                screen.blit(font_sm.render(f"YOU ({team_side}) — Kills: {save_data.get('kills',0)} | Cash: ${player_money}", True, (100, 255, 130)), (W // 2 - 195, 108))
                for i_sb, sb_b in enumerate(bots[:7]):
                    screen.blit(font_xs.render(f"{sb_b.name} [{sb_b.team}] — HP: {max(0, int(sb_b.hp))} | Weapon: {sb_b.weapon}", True, (215, 225, 245)), (W // 2 - 195, 138 + i_sb * 24))

        elif game_state == "TEAM_SELECT":
            screen.fill((20, 24, 32))
            screen.blit(font_lg.render(tr("CHOOSE_TEAM"), True, (255, 255, 255)), (W // 2 - 240, 42))
            pygame.draw.rect(screen, (38, 78, 138), (W // 2 - 260, 105, 520, 82), border_radius=10)
            screen.blit(font_md.render(tr("TEAM_CT"), True, (255, 255, 255)), (W // 2 - 230, 136))
            pygame.draw.rect(screen, (138, 72, 38), (W // 2 - 260, 210, 520, 82), border_radius=10)
            screen.blit(font_md.render(tr("TEAM_T"), True, (255, 255, 255)), (W // 2 - 230, 241))
            pygame.draw.rect(screen, (55, 62, 76), (W // 2 - 100, 320, 200, 48), border_radius=8)
            screen.blit(font_md.render(tr("CLOSE"), True, (255, 255, 255)), (W // 2 - 45, 334))

        elif game_state == "BUY_MENU":
            screen.fill((20, 24, 32))
            screen.blit(font_lg.render(f"{tr('SHOP_TITLE')}  —  ${player_money}", True, (110, 245, 130)), (40, 26))
            pygame.draw.rect(screen, (195, 50, 50), (W - 165, 22, 140, 44), border_radius=6)
            screen.blit(font_md.render(tr("CLOSE"), True, (255, 255, 255)), (W - 132, 34))
            y_b = 92
            for w_n in WEAPON_ORDER[1:]:
                pygame.draw.rect(screen, (36, 44, 58), (40, y_b, 345, 36), border_radius=5)
                screen.blit(font_sm.render(f"{w_n}   —   ${WEAPONS[w_n]['price']}", True, (255, 255, 255)), (55, y_b + 9))
                y_b += 42
            for lbl, yp in [(tr("KEVLAR"), 95), (tr("DEFUSE"), 155), (tr("NADES"), 215)]:
                pygame.draw.rect(screen, (42, 68, 105), (425, yp, 330, 46), border_radius=6)
                screen.blit(font_sm.render(lbl, True, (255, 255, 255)), (440, yp + 14))

        elif game_state == "HUD_EDIT":
            screen.fill((18, 22, 30))
            for bk, bv in save_data["layout"].items():
                draw_hud_btn(screen, bk, bv, bk == active_hud_key)
            if active_hud_key in save_data["layout"]:
                bd = save_data["layout"][active_hud_key]
                pygame.draw.rect(screen, (28, 34, 48), (W // 2 - 170, 12, 340, 102), border_radius=8)
                pygame.draw.rect(screen, (55, 135, 235), (W // 2 - 170, 12, 340, 102), 2, border_radius=8)
                screen.blit(font_sm.render(f"BUTTON: {active_hud_key.upper()}", True, (255, 230, 95)), (W // 2 - 152, 20))
                screen.blit(font_sm.render(f"[ - ]  {tr('SIZE')}: {int(bd.get('s',1.0)*100)}%  [ + ]", True, (255, 255, 255)), (W // 2 - 152, 48))
                screen.blit(font_sm.render(f"[ - ]  {tr('ALPHA')}: {int(bd.get('a',115))}   [ + ]", True, (135, 225, 255)), (W // 2 - 152, 82))
                pygame.draw.rect(screen, (48, 95, 165), (W // 2 + 72, 45, 88, 56), border_radius=6)
                screen.blit(font_xs.render(tr("ALL_ALPHA"), True, (255, 255, 255)), (W // 2 + 78, 66))
            pygame.draw.rect(screen, (45, 185, 85), (W - 165, H - 62, 145, 45), border_radius=6)
            screen.blit(font_md.render(tr("SAVE_HUD"), True, (255, 255, 255)), (W - 148, H - 48))

        elif game_state == "MENU":
            render_game_3d(screen, 8.0 + math.sin(time.time()*0.3)*0.6, 7.5 + math.cos(time.time()*0.3)*0.6, 0.0, time.time()*0.22, 0.0, "Mirage Palace", [], [], [], [], c4_state)
            pygame.draw.rect(screen, (20, 26, 36), (0, 15, W, 54))
            for t_n, t_x in [("HOME", 25), ("INV", 145), ("MP", 265), ("STAT", 385), ("SET", 505)]:
                pygame.draw.rect(screen, (45, 125, 225) if menu_tab == t_n else (38, 44, 56), (t_x, 22, 112, 38), border_radius=5)
                screen.blit(font_sm.render(tr(t_n), True, (255, 255, 255)), (t_x + 14, 32))
            r_name, r_col, _ = get_player_rank()
            screen.blit(font_sm.render(f"{tr('RANK')}: {r_name}", True, r_col), (625, 23))
            screen.blit(font_xs.render(f"{tr('COINS')}: {save_data['coins']}", True, (255, 215, 0)), (625, 44))

            if menu_tab == "HOME":
                draw_operator_sprite(screen, W // 2 + 25, H // 2 + 38, 185, "CT", False, False, current_weapon)
                pygame.draw.rect(screen, (22, 28, 38), (32, 112, 240, 232), border_radius=8)
                screen.blit(font_sm.render(tr("SELECT_MAP"), True, (255, 230, 90)), (44, 124))
                rows_h = [
                    f"Map: {current_map_name}",
                    f"Mode: {tr(f'MODE_{game_mode}')}",
                    f"Bots: {bot_count}",
                    f"AI: {tr(f'AI_{bot_ai_mode}')}",
                    tr("LANG")
                ]
                for idx_b, txt_b in enumerate(rows_h):
                    pygame.draw.rect(screen, (36, 44, 58), (42, 155 + idx_b * 36, 220, 31), border_radius=5)
                    screen.blit(font_xs.render(txt_b, True, (225, 238, 255)), (52, 164 + idx_b * 36))
                if daily_msg:
                    screen.blit(font_xs.render(daily_msg, True, (100, 255, 130)), (35, 86))
                pygame.draw.rect(screen, (45, 190, 85), (W - 245, H - 90, 220, 64), border_radius=10)
                screen.blit(font_lg.render(tr("PLAY"), True, (255, 255, 255)), (W - 180, H - 72))

            elif menu_tab == "INV":
                pygame.draw.rect(screen, (215, 145, 25), (40, 100, 215, 44), border_radius=6)
                screen.blit(font_sm.render(tr("OPEN_CASE"), True, (255, 255, 255)), (52, 114))
                pygame.draw.rect(screen, (45, 95, 165), (280, 100, 220, 44), border_radius=6)
                screen.blit(font_sm.render(f"Weapon: {current_weapon}", True, (255, 255, 255)), (300, 114))
                if case_roll["active"]:
                    case_roll["timer"] -= dt
                    screen.blit(font_md.render(f"★ UNBOXED: {case_roll['won_skin']}! ★", True, (255, 230, 80)), (520, 112))
                    if case_roll["timer"] <= 0:
                        case_roll["active"] = False
                y_s = 170
                for sk_n, sk_d in SKINS.items():
                    owned = (sk_n in save_data["inv"] or sk_n == "Default")
                    eq = (save_data["equipped"].get(current_weapon, "Default") == sk_n)
                    pygame.draw.rect(screen, (48, 88, 145) if eq else (32, 38, 50), (40, y_s, 460, 32), border_radius=5)
                    st = tr("EQUIPPED") if eq else (tr("OWNED") if owned else f"BUY: {sk_d['price']} C")
                    screen.blit(font_sm.render(f"{sk_n} [{sk_d['rarity']}]  —  {st}", True, sk_d["c1"]), (55, y_s + 7))
                    y_s += 36

            elif menu_tab == "MP":
                pygame.draw.rect(screen, (22, 28, 38), (30, 82, 540, 230), border_radius=8)
                screen.blit(font_md.render("GLOBAL INTERNET MULTIPLAYER (NO VPN)", True, (255, 235, 110)), (45, 94))
                pygame.draw.rect(screen, (45, 115, 205), (45, 132, 260, 42), border_radius=6)
                screen.blit(font_sm.render(f"Cloud Mode: {mp_mgr.mode}", True, (255, 255, 255)), (60, 145))
                pygame.draw.rect(screen, (52, 64, 86), (325, 132, 215, 42), border_radius=6)
                screen.blit(font_sm.render(f"Room Code: {mp_mgr.room_code}", True, (255, 255, 255)), (342, 145))
                pygame.draw.rect(screen, (45, 175, 95) if mp_mgr.mm_searching else (55, 65, 85), (45, 195, 260, 44), border_radius=6)
                screen.blit(font_sm.render("GLOBAL MATCHMAKING", True, (255, 255, 255)), (65, 209))
                if mp_mgr.mm_searching or mp_mgr.mode != "OFFLINE":
                    mp_mgr.mm_timer += dt
                    screen.blit(font_sm.render(f"Online Players in Room: {len(mp_mgr.players_net)} | {int(mp_mgr.mm_timer)}s", True, (110, 255, 140)), (45, 258))

            elif menu_tab == "STAT":
                k, d = save_data.get("kills", 0), max(1, save_data.get("deaths", 0))
                sf, sh = max(1, save_data.get("shots_fired", 0)), save_data.get("shots_hit", 0)
                wk = save_data.get("weapon_kills", {})
                fav_w = max(wk, key=wk.get) if wk else current_weapon
                stats_list = [
                    f"Rank: {r_name}",
                    f"Kills: {k}   |   Deaths: {save_data.get('deaths',0)}   |   K/D: {k/d:.2f}",
                    f"Headshots: {save_data.get('headshots',0)}   |   Accuracy: {(sh/sf)*100:.1f}%",
                    f"Matches Won: {save_data.get('wins',0)}   |   C4 Planted: {save_data.get('bombs',0)}",
                    f"Favorite Weapon: {fav_w}   |   Play Time: {int(save_data.get('play_time',0)//60)} min"
                ]
                for i_s, s_line in enumerate(stats_list):
                    pygame.draw.rect(screen, (28, 34, 46), (40, 100 + i_s * 54, 680, 44), border_radius=6)
                    screen.blit(font_md.render(s_line, True, (235, 242, 255)), (58, 111 + i_s * 54))

            elif menu_tab == "SET":
                xh = save_data["xhair"]
                gfx_lv = save_data.get("gfx", 2)
                set_rows = [
                    f"Crosshair Color: #{xh['col']+1}",
                    f"Crosshair Length: {xh['len']}",
                    f"Crosshair Thickness: {xh['thick']}",
                    f"Center Dot: {xh['dot']}",
                    f"Dynamic Spread: {xh['dyn']}",
                    f"{tr('GFX')}: {tr(f'GFX_{gfx_lv}')}",
                    tr("LANG")
                ]
                for idx_c, c_lbl in enumerate(set_rows):
                    pygame.draw.rect(screen, (32, 38, 52), (40, 110 + idx_c * 42, 250, 35), border_radius=5)
                    screen.blit(font_xs.render(c_lbl, True, (255, 255, 255)), (52, 121 + idx_c * 42))
                draw_crosshair(screen, False)
                pygame.draw.rect(screen, (55, 130, 235), (W - 250, H - 85, 220, 52), border_radius=8)
                screen.blit(font_sm.render(tr("CUSTOM_HUD"), True, (255, 255, 255)), (W - 232, H - 67))

        pygame.display.flip()

if __name__ == "__main__":
    main_loop()
