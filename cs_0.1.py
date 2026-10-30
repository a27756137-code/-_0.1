import pygame
import math
import random
import socket
import threading
import json
import time
import os

pygame.init()


# Принудительно включаем горизонтальный режим для движка SDL2 в Pydroid
os.environ["SDL_HINT_ORIENTATIONS"] = "LandscapeLeft LandscapeRight"

pygame.init()

info = pygame.display.Info()
WIDTH = max(info.current_w, info.current_h)
HEIGHT = min(info.current_w, info.current_h)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

clock = pygame.time.Clock()

# Встроенный шрифт (не вызывает вылетов из-за отсутствия Arial на Android)
font_lg = pygame.font.Font(None, int(HEIGHT * 0.08))
font_md = pygame.font.Font(None, int(HEIGHT * 0.05))
font_sm = pygame.font.Font(None, int(HEIGHT * 0.035))

# ================= 3 КАРТЫ =================
MAPS = {
    "Dust Arena": {
        "sky": (135, 195, 235), "floor": (194, 178, 128), "wall": (210, 180, 130),
        "grid": [
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,2,2,0,0,0,0,0,2,0,1],
            [1,0,2,0,0,0,0,0,0,2,0,1],
            [1,0,0,0,0,3,3,0,0,0,0,1],
            [1,0,0,0,0,3,3,0,0,0,0,1],
            [1,0,2,0,0,0,0,0,0,2,0,1],
            [1,0,2,2,0,0,0,0,2,2,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    },
    "Pool Day": {
        "sky": (50, 60, 90), "floor": (180, 210, 220), "wall": (200, 90, 80),
        "grid": [
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,0,0,0,0,0,2,0,1],
            [1,0,0,0,3,0,0,3,0,0,0,1],
            [1,0,0,0,3,0,0,3,0,0,0,1],
            [1,0,0,0,3,0,0,3,0,0,0,1],
            [1,0,2,0,0,0,0,0,0,2,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    },
    "Bunker Maze": {
        "sky": (30, 30, 35), "floor": (75, 75, 80), "wall": (110, 120, 110),
        "grid": [
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,1,0,0,0,0,1,0,0,1],
            [1,0,0,1,0,2,2,0,1,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,2,0,1,1,0,2,2,0,1],
            [1,0,0,0,0,1,1,0,0,0,0,1],
            [1,1,0,1,0,0,0,0,1,0,1,1],
            [1,0,0,1,0,0,0,0,1,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    }
}

# ================= 5 ОРУЖИЙ + ЦЕНЫ =================
WEAPONS = [
    {"name": "Knife", "cost": 0,    "owned": True,  "dmg": 55,  "delay": 450,  "ammo": -1, "max": -1, "rng": 1.7,  "spr": 0.0,   "pel": 1, "col": (190, 195, 200)},
    {"name": "USP-S", "cost": 200,  "owned": True,  "dmg": 28,  "delay": 250,  "ammo": 12, "max": 12, "rng": 15.0, "spr": 0.02,  "pel": 1, "col": (70, 75, 80)},
    {"name": "M3",    "cost": 1200, "owned": False, "dmg": 20,  "delay": 850,  "ammo": 8,  "max": 8,  "rng": 8.5,  "spr": 0.14,  "pel": 6, "col": (110, 75, 45)},
    {"name": "AK-47", "cost": 2700, "owned": False, "dmg": 36,  "delay": 125,  "ammo": 30, "max": 30, "rng": 18.0, "spr": 0.045, "pel": 1, "col": (160, 100, 40)},
    {"name": "AWP",   "cost": 4750, "owned": False, "dmg": 120, "delay": 1250, "ammo": 5,  "max": 5,  "rng": 25.0, "spr": 0.003, "pel": 1, "col": (45, 95, 55)}
]

settings = {"sens": 1.0, "rays": 80, "bots": 3, "ip": "192.168.1."}
state = "MENU"
cur_map = "Dust Arena"

px, py, p_ang = 2.0, 2.0, 0.0
p_hp, p_kills, p_money = 100, 0, 800
cur_w = 1
last_shot, reload_t, recoil = 0, 0, 0
reloading, zoom = False, False

bots = []
net_players = {}
is_mp, is_host, sock = False, False, None

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

local_ip = get_ip()
if "." in local_ip:
    settings["ip"] = ".".join(local_ip.split(".")[:3]) + "."

def start_net(host_mode):
    global sock, is_mp, is_host
    is_mp, is_host = True, host_mode
    try:
        if sock: sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        if is_host: sock.bind(("0.0.0.0", 5555))
    except Exception:
        pass

    def net_loop():
        global p_hp, p_kills, p_money
        while is_mp:
            try:
                data, addr = sock.recvfrom(1024)
                msg = json.loads(data.decode('utf-8'))
                if msg.get("t") == "p":
                    net_players[f"{addr[0]}:{addr[1]}"] = {"x": msg["x"], "y": msg["y"], "hp": msg["hp"], "ts": time.time()}
                    if is_host:
                        sock.sendto(json.dumps({"t": "p", "x": px, "y": py, "hp": p_hp}).encode('utf-8'), addr)
                elif msg.get("t") == "h":
                    p_hp -= msg.get("d", 20)
                    if p_hp <= 0: respawn()
            except Exception:
                pass
            time.sleep(0.02)
    threading.Thread(target=net_loop, daemon=True).start()

def send_pos():
    if is_mp and sock and not is_host:
        try:
            sock.sendto(json.dumps({"t": "p", "x": px, "y": py, "hp": p_hp}).encode('utf-8'), (settings["ip"], 5555))
        except Exception:
            pass

def is_wall(x, y):
    g = MAPS[cur_map]["grid"]
    gx, gy = int(x), int(y)
    if gy < 0 or gy >= len(g) or gx < 0 or gx >= len(g[0]): return 1
    return g[gy][gx]

def respawn():
    global px, py, p_hp
    p_hp = 100
    for _ in range(100):
        rx, ry = random.uniform(1.5, 10.5), random.uniform(1.5, 7.5)
        if is_wall(rx, ry) == 0:
            px, py = rx, ry
            break

def spawn_bots():
    global bots
    while len(bots) < settings["bots"]:
        bx, by = random.uniform(1.5, 10.5), random.uniform(1.5, 7.5)
        if is_wall(bx, by) == 0 and math.hypot(bx - px, by - py) > 2.5:
            bots.append({"x": bx, "y": by, "hp": 100, "dir": random.uniform(0, 6.28), "cd": 0})

def init_game():
    global p_kills, p_money, cur_w, bots
    p_kills, p_money, cur_w = 0, 800, 1
    for i, w in enumerate(WEAPONS):
        w["ammo"] = w["max"]
        w["owned"] = (i <= 1)
    bots = []
    respawn()
    spawn_bots()

def shoot():
    global last_shot, recoil, p_kills, p_money, reloading, reload_t
    now = pygame.time.get_ticks()
    w = WEAPONS[cur_w]
    if reloading: return
    if w["ammo"] == 0:
        reloading, reload_t = True, now
        return
    if now - last_shot < w["delay"]: return

    last_shot = now
    if w["ammo"] > 0: w["ammo"] -= 1
    recoil = int(HEIGHT * 0.05)

    for _ in range(w["pel"]):
        ang = p_ang + random.uniform(-w["spr"], w["spr"])
        sa, ca = math.sin(ang), math.cos(ang)
        d, hit = 0.0, False
        while d < w["rng"] and not hit:
            d += 0.15
            tx, ty = px + ca * d, py + sa * d
            if is_wall(tx, ty) > 0: break
            for b in bots[:]:
                if math.hypot(b["x"] - tx, b["y"] - ty) < 0.45:
                    b["hp"] -= w["dmg"]
                    hit = True
                    if b["hp"] <= 0:
                        p_kills += 1
                        p_money = min(16000, p_money + 300)
                        bots.remove(b)
                        spawn_bots()
                    break
            if is_mp and not hit:
                for k, np in list(net_players.items()):
                    if math.hypot(np["x"] - tx, np["y"] - ty) < 0.45:
                        hit = True
                        p_money = min(16000, p_money + 100)
                        ap = k.split(":")
                        if len(ap) == 2:
                            try: sock.sendto(json.dumps({"t": "h", "d": w["dmg"]}).encode('utf-8'), (ap[0], int(ap[1])))
                            except Exception: pass
                        break

def render_3d():
    m = MAPS[cur_map]
    pygame.draw.rect(screen, m["sky"], (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, m["floor"], (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    fov = (math.pi / 3.0) / (2.2 if (zoom and cur_w == 4) else 1.0)
    nr = int(settings["rays"])
    sw = WIDTH // nr + 1
    zbuf = [20.0] * nr
    sa = p_ang - fov / 2.0
    da = fov / nr
    bc = m["wall"]

    for r in range(nr):
        ang = sa + r * da
        sina, cosa = math.sin(ang), math.cos(ang)
        d, wt = 0.0, 1
        while d < 15.0:
            d += 0.1
            w_check = is_wall(px + cosa * d, py + sina * d)
            if w_check > 0:
                wt = w_check
                break
        cd = max(0.1, d * math.cos(p_ang - ang))
        zbuf[r] = cd
        ph = min(int(HEIGHT / cd), HEIGHT * 2)
        sh = max(0.25, 1.0 - cd / 15.0)
        if wt == 2: c = (int(bc[0]*0.7*sh), int(bc[1]*0.85*sh), int(bc[2]*sh))
        elif wt == 3: c = (int(110*sh), int(150*sh), int(200*sh))
        else: c = (int(bc[0]*sh), int(bc[1]*sh), int(bc[2]*sh))
        pygame.draw.rect(screen, c, (r * (WIDTH // nr), HEIGHT // 2 - ph // 2, sw, ph))

    ents = [(b["x"], b["y"], b["hp"], (210, 50, 50)) for b in bots]
    for k, np in list(net_players.items()):
        if time.time() - np.get("ts", 0) < 3.0:
            ents.append((np["x"], np["y"], np["hp"], (50, 150, 240)))
    ents.sort(key=lambda e: math.hypot(e[0] - px, e[1] - py), reverse=True)

    for ex, ey, ehp, ecol in ents:
        dx, dy = ex - px, ey - py
        dist = math.hypot(dx, dy)
        if dist < 0.3: continue
        at = (math.atan2(dy, dx) - p_ang + math.pi) % (2 * math.pi) - math.pi
        if abs(at) < fov / 1.4:
            sx = int((0.5 + at / fov) * WIDTH)
            ri = max(0, min(nr - 1, int(sx / WIDTH * nr)))
            if dist < zbuf[ri]:
                sh = min(int(HEIGHT / dist * 0.75), HEIGHT)
                spw = int(sh * 0.45)
                ty = HEIGHT // 2 - sh // 2 + int(sh * 0.15)
                pygame.draw.rect(screen, ecol, (sx - spw // 2, ty + sh // 4, spw, sh * 3 // 4))
                pygame.draw.circle(screen, (240, 200, 160), (sx, ty + sh // 6), max(4, spw // 3))
                pygame.draw.rect(screen, (0, 220, 0), (sx - spw // 2, ty - 8, int(spw * max(0, ehp) / 100.0), 5))

def draw_radar_and_hud():
    global recoil
    w = WEAPONS[cur_w]
    if recoil > 0: recoil = max(0, recoil - 4)

    # 1. РАДАР (МИНИКАРТА) В ЛЕВОМ ВЕРХНЕМ УГЛУ
    grid = MAPS[cur_map]["grid"]
    cell = max(6, int(HEIGHT * 0.022))
    rx0, ry0 = 15, 15
    rw, rh = len(grid[0]) * cell, len(grid) * cell
    pygame.draw.rect(screen, (25, 30, 35), (rx0, ry0, rw, rh))
    for gy, row in enumerate(grid):
        for gx, val in enumerate(row):
            if val > 0:
                pygame.draw.rect(screen, (100, 110, 120), (rx0 + gx * cell, ry0 + gy * cell, cell - 1, cell - 1))
    # Боты на радаре
    for b in bots:
        pygame.draw.circle(screen, (255, 60, 60), (int(rx0 + b["x"] * cell), int(ry0 + b["y"] * cell)), max(2, cell // 3))
    # Игрок и линия взгляда на радаре
    p_rx, p_ry = int(rx0 + px * cell), int(ry0 + py * cell)
    pygame.draw.circle(screen, (80, 255, 80), (p_rx, p_ry), max(3, cell // 3))
    pygame.draw.line(screen, (255, 255, 255), (p_rx, p_ry), (int(p_rx + math.cos(p_ang) * cell * 1.5), int(p_ry + math.sin(p_ang) * cell * 1.5)), 2)

    # 2. СТАТУС: HP, ДЕНЬГИ ($), ПАТРОНЫ
    sx0 = rx0 + rw + 15
    pygame.draw.rect(screen, (25, 25, 30), (sx0, 15, int(WIDTH * 0.38), int(HEIGHT * 0.13)), border_radius=8)
    screen.blit(font_md.render(f"HP: {p_hp}", True, (60, 230, 60) if p_hp > 35 else (240, 60, 60)), (sx0 + 12, 20))
    screen.blit(font_md.render(f"${p_money}", True, (100, 240, 100)), (sx0 + int(WIDTH * 0.13), 20))
    astr = "INF" if w["ammo"] == -1 else ("RELOAD" if reloading else f"{w['ammo']}/{w['max']}")
    screen.blit(font_md.render(f"{w['name']}: {astr}", True, (240, 210, 90)), (sx0 + int(WIDTH * 0.23), 20))
    screen.blit(font_sm.render(f"Kills: {p_kills} | Tap locked slot to BUY weapon", True, (190, 190, 190)), (sx0 + 12, 15 + int(HEIGHT * 0.08)))

    # 3. ПРИЦЕЛ И ОРУЖИЕ
    cx, cy = WIDTH // 2, HEIGHT // 2
    if zoom and cur_w == 4:
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), int(HEIGHT * 0.44), 6)
        pygame.draw.line(screen, (0, 0, 0), (0, cy), (WIDTH, cy), 2)
        pygame.draw.line(screen, (0, 0, 0), (cx, 0), (cx, HEIGHT), 2)
    else:
        pygame.draw.line(screen, (0, 255, 0), (cx - 10, cy), (cx + 10, cy), 2)
        pygame.draw.line(screen, (0, 255, 0), (cx, cy - 10), (cx, cy + 10), 2)
        wx, wy = int(WIDTH * 0.62) + recoil // 2, int(HEIGHT * 0.68) + recoil
        pygame.draw.polygon(screen, w["col"], [(wx, wy), (wx + int(WIDTH * 0.18), HEIGHT), (wx + int(WIDTH * 0.05), HEIGHT), (wx - int(WIDTH * 0.04), wy + 25)])

    # Кнопка MENU
    pygame.draw.rect(screen, (160, 50, 50), (WIDTH - int(WIDTH * 0.12), 15, int(WIDTH * 0.1), int(HEIGHT * 0.08)), border_radius=6)
    screen.blit(font_sm.render("MENU", True, (255, 255, 255)), (WIDTH - int(WIDTH * 0.1), 25))

    # 4. МАГАЗИН / СЛОТЫ ОРУЖИЯ ВНИЗУ
    sw_slot, sh_slot = int(WIDTH * 0.1), int(HEIGHT * 0.11)
    st_x = WIDTH // 2 - (sw_slot * 5 + 40) // 2
    for i, wp in enumerate(WEAPONS):
        bx = st_x + i * (sw_slot + 10)
        by = HEIGHT - sh_slot - 12
        if i == cur_w: col = (210, 160, 40)
        elif wp["owned"]: col = (55, 75, 95)
        else: col = (35, 35, 40)
        pygame.draw.rect(screen, col, (bx, by, sw_slot, sh_slot), border_radius=6)
        pygame.draw.rect(screen, (160, 160, 160), (bx, by, sw_slot, sh_slot), 2, border_radius=6)
        screen.blit(font_sm.render(wp["name"], True, (255, 255, 255)), (bx + 6, by + 6))
        sub = "OWNED" if wp["owned"] else f"${wp['cost']}"
        sub_col = (180, 230, 180) if wp["owned"] else ((100, 255, 100) if p_money >= wp["cost"] else (230, 80, 80))
        screen.blit(font_sm.render(sub, True, sub_col), (bx + 6, by + sh_slot // 2 + 2))

    # 5. СЕНСОРНЫЕ КНОПКИ
    jx, jy, jr = int(WIDTH * 0.14), int(HEIGHT * 0.72), int(HEIGHT * 0.14)
    pygame.draw.circle(screen, (220, 220, 220), (jx, jy), jr, 3)
    pygame.draw.circle(screen, (180, 180, 180), (jx + int(joy_vec[0] * jr * 0.6), jy + int(joy_vec[1] * jr * 0.6)), int(jr * 0.38))

    fx, fy, fr = int(WIDTH * 0.86), int(HEIGHT * 0.7), int(HEIGHT * 0.12)
    pygame.draw.circle(screen, (210, 50, 50), (fx, fy), fr)
    screen.blit(font_md.render("FIRE", True, (255, 255, 255)), (fx - int(fr * 0.45), fy - int(fr * 0.2)))

    rx, ry, rr = int(WIDTH * 0.73), int(HEIGHT * 0.8), int(HEIGHT * 0.07)
    pygame.draw.circle(screen, (60, 130, 200), (rx, ry), rr)
    screen.blit(font_sm.render("REL", True, (255, 255, 255)), (rx - int(rr * 0.45), ry - int(rr * 0.2)))

    if cur_w == 4:
        zx, zy, zr = int(WIDTH * 0.73), int(HEIGHT * 0.56), int(HEIGHT * 0.07)
        pygame.draw.circle(screen, (60, 170, 90), (zx, zy), zr)
        screen.blit(font_sm.render("ZOOM", True, (255, 255, 255)), (zx - int(zr * 0.55), zy - int(zr * 0.2)))

touches = {}
joy_id, look_id = None, None
joy_vec = [0.0, 0.0]
fire_held = False

def draw_btn(txt, x, y, w, h, col=(60, 70, 90)):
    r = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, col, r, border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), r, 2, border_radius=8)
    s = font_md.render(txt, True, (255, 255, 255))
    screen.blit(s, (x + w // 2 - s.get_width() // 2, y + h // 2 - s.get_height() // 2))
    return r

running = True
while running:
    dt = clock.tick(60) / 1000.0
    now = pygame.time.get_ticks()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            if ev.type == pygame.FINGERDOWN:
                tx, ty, tid = int(ev.x * WIDTH), int(ev.y * HEIGHT), ev.finger_id
            else:
                tx, ty, tid = ev.pos[0], ev.pos[1], "m"

            if state == "MENU":
                bw, bh = int(WIDTH * 0.44), int(HEIGHT * 0.12)
                bx = WIDTH // 2 - bw // 2
                if pygame.Rect(bx, int(HEIGHT * 0.26), bw, bh).collidepoint(tx, ty):
                    is_mp = False
                    init_game()
                    state = "GAME"
                elif pygame.Rect(bx, int(HEIGHT * 0.41), bw, bh).collidepoint(tx, ty):
                    ks = list(MAPS.keys())
                    cur_map = ks[(ks.index(cur_map) + 1) % len(ks)]
                elif pygame.Rect(bx, int(HEIGHT * 0.56), bw, bh).collidepoint(tx, ty):
                    state = "MP"
                elif pygame.Rect(bx, int(HEIGHT * 0.71), bw, bh).collidepoint(tx, ty):
                    state = "SET"

            elif state == "SET":
                bw, bh = int(WIDTH * 0.46), int(HEIGHT * 0.12)
                bx = WIDTH // 2 - bw // 2
                if pygame.Rect(bx, int(HEIGHT * 0.25), bw, bh).collidepoint(tx, ty):
                    settings["sens"] = round(0.5 if settings["sens"] >= 2.5 else settings["sens"] + 0.5, 1)
                elif pygame.Rect(bx, int(HEIGHT * 0.42), bw, bh).collidepoint(tx, ty):
                    settings["rays"] = 50 if settings["rays"] >= 140 else settings["rays"] + 30
                elif pygame.Rect(bx, int(HEIGHT * 0.59), bw, bh).collidepoint(tx, ty):
                    settings["bots"] = 0 if settings["bots"] >= 6 else settings["bots"] + 1
                elif pygame.Rect(bx, int(HEIGHT * 0.76), bw, bh).collidepoint(tx, ty):
                    state = "MENU"

            elif state == "MP":
                bw, bh = int(WIDTH * 0.42), int(HEIGHT * 0.11)
                if pygame.Rect(int(WIDTH * 0.05), int(HEIGHT * 0.25), bw, bh).collidepoint(tx, ty):
                    start_net(True); init_game(); state = "GAME"
                elif pygame.Rect(int(WIDTH * 0.05), int(HEIGHT * 0.42), bw, bh).collidepoint(tx, ty):
                    start_net(False); init_game(); state = "GAME"
                elif pygame.Rect(int(WIDTH * 0.05), int(HEIGHT * 0.76), bw, bh).collidepoint(tx, ty):
                    state = "MENU"
                keys = ["1","2","3","4","5","6","7","8","9",".","0","DEL"]
                kw, kh = int(WIDTH * 0.11), int(HEIGHT * 0.11)
                for idx, k in enumerate(keys):
                    kx = int(WIDTH * 0.54) + (idx % 3) * (kw + 8)
                    ky = int(HEIGHT * 0.26) + (idx // 3) * (kh + 8)
                    if pygame.Rect(kx, ky, kw, kh).collidepoint(tx, ty):
                        if k == "DEL": settings["ip"] = settings["ip"][:-1]
                        elif len(settings["ip"]) < 15: settings["ip"] += k

            elif state == "GAME":
                if pygame.Rect(WIDTH - int(WIDTH * 0.12), 15, int(WIDTH * 0.1), int(HEIGHT * 0.08)).collidepoint(tx, ty):
                    is_mp = False; state = "MENU"; continue

                # Покупка и выбор оружия
                sw_slot, sh_slot = int(WIDTH * 0.1), int(HEIGHT * 0.11)
                st_x = WIDTH // 2 - (sw_slot * 5 + 40) // 2
                sc = False
                for i, wp in enumerate(WEAPONS):
                    if pygame.Rect(st_x + i * (sw_slot + 10), HEIGHT - sh_slot - 12, sw_slot, sh_slot).collidepoint(tx, ty):
                        if wp["owned"]:
                            cur_w, reloading, zoom = i, False, False
                        elif p_money >= wp["cost"]:
                            p_money -= wp["cost"]
                            wp["owned"] = True
                            wp["ammo"] = wp["max"]
                            cur_w, reloading, zoom = i, False, False
                        sc = True; break
                if sc: continue

                fx, fy, fr = int(WIDTH * 0.86), int(HEIGHT * 0.7), int(HEIGHT * 0.12)
                if math.hypot(tx - fx, ty - fy) <= fr * 1.25:
                    fire_held = True; shoot(); continue

                rx, ry, rr = int(WIDTH * 0.73), int(HEIGHT * 0.8), int(HEIGHT * 0.07)
                if math.hypot(tx - rx, ty - ry) <= rr * 1.25:
                    if WEAPONS[cur_w]["ammo"] < WEAPONS[cur_w]["max"] and WEAPONS[cur_w]["max"] > 0:
                        reloading, reload_t = True, now
                    continue
                if cur_w == 4:
                    zx, zy, zr = int(WIDTH * 0.73), int(HEIGHT * 0.56), int(HEIGHT * 0.07)
                    if math.hypot(tx - zx, ty - zy) <= zr * 1.25:
                        zoom = not zoom
                        continue

                jx, jy, jr = int(WIDTH * 0.14), int(HEIGHT * 0.72), int(HEIGHT * 0.14)
                if tx < WIDTH * 0.42 and math.hypot(tx - jx, ty - jy) <= jr * 1.8:
                    joy_id = tid
                    joy_vec = [max(-1.0, min(1.0, (tx - jx) / jr)), max(-1.0, min(1.0, (ty - jy) / jr))]
                else:
                    look_id = tid
                    touches[tid] = (tx, ty)

        elif ev.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION) and state == "GAME":
            if ev.type == pygame.FINGERMOTION:
                tx, ty, tid = int(ev.x * WIDTH), int(ev.y * HEIGHT), ev.finger_id
            else:
                tx, ty, tid = ev.pos[0], ev.pos[1], "m"

            if tid == joy_id:
                jx, jy, jr = int(WIDTH * 0.14), int(HEIGHT * 0.72), int(HEIGHT * 0.14)
                joy_vec = [max(-1.0, min(1.0, (tx - jx) / jr)), max(-1.0, min(1.0, (ty - jy) / jr))]
            elif tid == look_id and tid in touches:
                p_ang += (tx - touches[tid][0]) * 0.0035 * settings["sens"] * (0.4 if zoom else 1.0)
                touches[tid] = (tx, ty)

        elif ev.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            tid = ev.finger_id if ev.type == pygame.FINGERUP else "m"
            if tid == joy_id:
                joy_id, joy_vec = None, [0.0, 0.0]
            if tid == look_id:
                look_id = None
                touches.pop(tid, None)
            fire_held = False
    if state == "MENU":
        screen.fill((25, 30, 40))
        t = font_lg.render("COUNTER-PYTHON 3D MOBILE", True, (240, 190, 50))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, int(HEIGHT * 0.08)))
        bw, bh = int(WIDTH * 0.44), int(HEIGHT * 0.12)
        bx = WIDTH // 2 - bw // 2
        draw_btn("PLAY (WITH BOTS)", bx, int(HEIGHT * 0.26), bw, bh, (50, 140, 70))
        draw_btn(f"MAP: {cur_map}", bx, int(HEIGHT * 0.41), bw, bh)
        draw_btn("WIFI MULTIPLAYER", bx, int(HEIGHT * 0.56), bw, bh, (60, 110, 170))
        draw_btn("SETTINGS", bx, int(HEIGHT * 0.71), bw, bh)

    elif state == "SET":
        screen.fill((25, 30, 40))
        bw, bh = int(WIDTH * 0.46), int(HEIGHT * 0.12)
        bx = WIDTH // 2 - bw // 2
        draw_btn(f"Sensitivity: {settings['sens']}x", bx, int(HEIGHT * 0.25), bw, bh)
        draw_btn(f"3D Quality (Rays): {settings['rays']}", bx, int(HEIGHT * 0.42), bw, bh)
        draw_btn(f"Bots Count: {settings['bots']}", bx, int(HEIGHT * 0.59), bw, bh)
        draw_btn("BACK TO MENU", bx, int(HEIGHT * 0.76), bw, bh, (150, 50, 50))

    elif state == "MP":
        screen.fill((25, 30, 40))
        screen.blit(font_md.render(f"Your IP: {local_ip}", True, (180, 240, 180)), (int(WIDTH * 0.05), int(HEIGHT * 0.12)))
        bw, bh = int(WIDTH * 0.42), int(HEIGHT * 0.11)
        draw_btn("CREATE SERVER (HOST)", int(WIDTH * 0.05), int(HEIGHT * 0.25), bw, bh, (50, 140, 70))
        draw_btn(f"JOIN IP: {settings['ip']}", int(WIDTH * 0.05), int(HEIGHT * 0.42), bw, bh, (60, 110, 170))
        draw_btn("BACK", int(WIDTH * 0.05), int(HEIGHT * 0.76), bw, bh, (150, 50, 50))
        keys = ["1","2","3","4","5","6","7","8","9",".","0","DEL"]
        kw, kh = int(WIDTH * 0.11), int(HEIGHT * 0.11)
        for idx, k in enumerate(keys):
            draw_btn(k, int(WIDTH * 0.54) + (idx % 3) * (kw + 8), int(HEIGHT * 0.26) + (idx // 3) * (kh + 8), kw, kh, (80, 85, 105))

    elif state == "GAME":
        if fire_held:
            shoot()
        if reloading and now - reload_t > 1300:
            WEAPONS[cur_w]["ammo"] = WEAPONS[cur_w]["max"]
            reloading = False

        spd = 3.2 * dt
        fw, st = -joy_vec[1] * spd, joy_vec[0] * spd
        nx = px + math.cos(p_ang) * fw - math.sin(p_ang) * st
        ny = py + math.sin(p_ang) * fw + math.cos(p_ang) * st
        if is_wall(nx, py) == 0: px = nx
        if is_wall(px, ny) == 0: py = ny

        for b in bots:
            dp = math.hypot(px - b["x"], py - b["y"])
            if dp < 7.5:
                b["dir"] = math.atan2(py - b["y"], px - b["x"])
                if dp < 5.0 and now - b["cd"] > 1100:
                    b["cd"] = now
                    p_hp -= random.randint(6, 14)
                    if p_hp <= 0: respawn()
            bxn, byn = b["x"] + math.cos(b["dir"]) * 1.6 * dt, b["y"] + math.sin(b["dir"]) * 1.6 * dt
            if is_wall(bxn, byn) == 0 and dp > 1.2:
                b["x"], b["y"] = bxn, byn
            else:
                b["dir"] = random.uniform(0, 6.28)

        send_pos()
        render_3d()
        draw_radar_and_hud()

    pygame.display.flip()

pygame.quit()
