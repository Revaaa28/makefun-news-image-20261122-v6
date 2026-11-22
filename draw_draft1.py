#!/usr/bin/env python3
"""THE SUNDAY LEDGER - Signature Edition (v6, draft 1).
One page of Sunday 22 November 2026 world news, drawn in code.
Deterministic: pure PIL drawing, fixed fonts, no randomness, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 22                      # page margin
CW = W - 2 * M              # content width = 980

PAPER = (247, 242, 228)
PANEL = (252, 249, 240)
INK = (26, 34, 29)
GREEN_D = (18, 58, 38)
GREEN = (25, 84, 52)
GREEN_M = (52, 122, 80)
GREEN_PALE = (216, 232, 214)
BRICK = (166, 42, 36)
GOLD = (190, 138, 40)
NAVY = (15, 32, 52)
GREY = (96, 100, 94)

FD = "/usr/share/fonts/truetype/noto/"
FJ = "/usr/share/fonts/truetype/dejavu/"
DISPLAY = FD + "NotoSerifDisplay-Black.ttf"
SERIF_B = FD + "NotoSerif-Bold.ttf"
SERIF_SB = FD + "NotoSerif-SemiBold.ttf"
SERIF = FD + "NotoSerif-Regular.ttf"
SANS_B = FD + "NotoSans-Bold.ttf"
SANS_SB = FD + "NotoSans-SemiBold.ttf"
SANS = FD + "NotoSans-Regular.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, text, font):
    return d.textlength(text, font=font)


def spaced(d, x, y, text, font, fill, tracking=2, anchor_left=True):
    """Draw letterspaced text; returns end x."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += tw(d, ch, font) + tracking
    return cx - tracking


def spaced_w(d, text, font, tracking=2):
    return sum(tw(d, ch, font) for ch in text) + tracking * max(0, len(text) - 1)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, width, leading, fill, max_lines, align="left"):
    """Wrap and draw a text block inside a fixed box; assert it fits."""
    lines = wrap(d, text, font, width)
    assert len(lines) <= max_lines, f"OVERFLOW {len(lines)}>{max_lines}: {text[:60]}"
    for ln in lines:
        if align == "center":
            d.text((x + (width - tw(d, ln, font)) / 2, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, bg, fg=(255, 255, 255), font_size=10):
    f = F(SANS_B, font_size)
    w_ = tw(d, text, f) + 10
    d.rounded_rectangle([x, y, x + w_, y + font_size + 7], 3, fill=bg)
    d.text((x + 5, y + 2), text, font=f, fill=fg)
    return w_


# ---------------------------------------------------------------- scenes
def grad(d, box, top, bot):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0 - 1))
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def scene_cop31(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (250, 196, 120), (120, 178, 168))
    cx, cy = x0 + 86, y0 + 40
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(252, 220, 130))
    d.ellipse([cx - 31, cy - 31, cx + 31, cy + 31], outline=(252, 230, 160), width=2)
    # clock
    kx, ky, kr = x1 - 52, y0 + 38, 26
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(252, 249, 240), outline=INK, width=2)
    d.line([(kx, ky), (kx, ky - 16)], fill=INK, width=3)
    d.line([(kx, ky), (kx + 11, ky + 6)], fill=INK, width=3)
    for a in range(0, 360, 90):
        import math
        d.line([(kx + 19 * math.cos(math.radians(a)), ky + 19 * math.sin(math.radians(a))),
                (kx + 23 * math.cos(math.radians(a)), ky + 23 * math.sin(math.radians(a)))], fill=INK, width=2)
    # delegate table
    ty = y1 - 26
    d.rectangle([x0 + 18, ty, x1 - 18, ty + 10], fill=(74, 48, 32))
    for i in range(9):
        px = x0 + 42 + i * 30
        d.ellipse([px - 6, ty - 16, px + 6, ty - 4], fill=(38, 44, 52))
        d.rectangle([px - 7, ty - 5, px + 7, ty + 2], fill=(38, 44, 52))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(96, 74, 48))


def scene_bahrain(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (13, 26, 48), (30, 58, 84))
    # radar mast + arcs
    mx = x0 + 44
    d.line([(mx, y1 - 30), (mx, y0 + 16)], fill=(200, 210, 220), width=3)
    d.polygon([(mx, y0 + 10), (mx + 16, y0 + 20), (mx, y0 + 30)], fill=(220, 226, 232))
    for r in (26, 44, 62):
        d.arc([mx + 6, y0 + 18 - r // 2, mx + 6 + r, y0 + 18 + r // 2], -50, 50,
              fill=(120, 200, 160), width=2)
    # sea
    d.rectangle([x0, y1 - 30, x1, y1], fill=(18, 44, 66))
    for i in range(6):
        sx = x0 + 30 + i * 46
        d.arc([sx, y1 - 24, sx + 22, y1 - 12], 0, 180, fill=(90, 140, 180), width=2)
    # tanker silhouette
    tx, ty = x1 - 168, y1 - 44
    d.polygon([(tx, ty), (tx + 120, ty), (tx + 108, ty + 13), (tx + 12, ty + 13)], fill=(10, 16, 24))
    d.rectangle([tx + 22, ty - 9, tx + 44, ty], fill=(10, 16, 24))
    d.rectangle([tx + 84, ty - 12, tx + 94, ty], fill=(10, 16, 24))
    # plant flames right
    for fx, fh in ((x1 - 34, 30), (x1 - 22, 40), (x1 - 46, 22)):
        d.polygon([(fx - 8, y1 - 30), (fx, y1 - 30 - fh), (fx + 8, y1 - 30)], fill=(238, 128, 44))
        d.polygon([(fx - 4, y1 - 30), (fx, y1 - 30 - fh // 2), (fx + 4, y1 - 30)], fill=(250, 196, 84))
    d.rectangle([x1 - 56, y1 - 32, x1 - 12, y1 - 30], fill=(10, 16, 24))


def scene_ukraine(d, box):
    import math
    x0, y0, x1, y1 = box
    grad(d, box, (10, 16, 34), (34, 48, 74))
    for sx, sy in ((30, 14), (90, 26), (150, 10), (210, 22), (262, 12), (120, 34), (240, 36)):
        d.point((x0 + sx, y0 + sy), fill=(230, 236, 245))
    # drone trails: dotted arcs
    for (ax, ay, r, a0, a1) in ((40, 66, 120, 200, 320), (90, 74, 150, 210, 330), (150, 60, 110, 190, 300)):
        for a in range(a0, a1, 9):
            px = x0 + ax + r * math.cos(math.radians(a)) * 0.62
            py = y0 + ay + r * math.sin(math.radians(a)) * 0.34
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(240, 178, 84))
    for dx, dy in ((120, 30), (196, 22), (250, 38)):
        d.ellipse([x0 + dx - 3, y0 + dy - 2, x0 + dx + 3, y0 + dy + 2], fill=(250, 200, 110))
    # skyline
    base = y1
    for bx, bw, bh in ((6, 34, 26), (44, 26, 38), (74, 40, 20), (118, 28, 44), (150, 36, 24),
                       (190, 26, 34), (220, 42, 18), (266, 30, 30)):
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(8, 12, 20))
        for wy in range(base - bh + 5, base - 4, 8):
            for wx in range(x0 + bx + 4, x0 + bx + bw - 4, 9):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.point((wx, wy), fill=(250, 214, 120))
    # searchlight
    d.polygon([(x0 + 236, y1), (x0 + 268, y0 + 8), (x0 + 282, y0 + 12), (x0 + 252, y1)],
              fill=(120, 150, 190))


def scene_ship(d, box, flame=True):
    x0, y0, x1, y1 = box
    grad(d, box, (24, 52, 78), (52, 96, 128))
    d.rectangle([x0, y1 - 9, x1, y1], fill=(16, 44, 70))
    tx, ty = x0 + 58, y1 - 24
    d.polygon([(tx, ty), (tx + 108, ty), (tx + 96, ty + 11), (tx + 10, ty + 11)], fill=(12, 18, 26))
    d.rectangle([tx + 16, ty - 10, tx + 30, ty], fill=(12, 18, 26))
    d.rectangle([tx + 62, ty - 7, tx + 88, ty], fill=(96, 40, 34))
    if flame:
        for fx, fh in ((tx + 68, 17), (tx + 78, 22), (tx + 88, 14)):
            d.polygon([(fx - 5, ty - 6), (fx, ty - 6 - fh), (fx + 5, ty - 6)], fill=(238, 128, 44))


def scene_memorial(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (30, 34, 44), (52, 56, 66))
    cx = (x0 + x1) // 2
    for off, fh in ((-26, 15), (0, 21), (26, 15)):
        d.polygon([(cx + off - 4, y1 - 8), (cx + off, y1 - 8 - fh), (cx + off + 4, y1 - 8)],
                  fill=(250, 196, 84))
        d.rectangle([cx + off - 3, y1 - 9, cx + off + 3, y1 - 5], fill=(238, 232, 214))


def scene_race(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (20, 22, 40), (44, 40, 66))
    # chequer strip
    s = 9
    for r in range(2):
        for c in range(12):
            if (r + c) % 2 == 0:
                d.rectangle([x0 + 10 + c * s, y0 + 6 + r * s, x0 + 19 + c * s, y0 + 15 + r * s],
                            fill=(240, 240, 240))
    # car
    cy = y1 - 16
    d.polygon([(x0 + 128, cy), (x0 + 150, cy - 10), (x0 + 196, cy - 10), (x0 + 214, cy)],
              fill=(178, 34, 30))
    d.rectangle([x0 + 124, cy, x0 + 218, cy + 6], fill=(140, 26, 24))
    for wx in (142, 200):
        d.ellipse([x0 + wx - 7, cy + 1, x0 + wx + 7, cy + 13], fill=(12, 12, 14))
    d.line([(x0 + 150, y0 + 26), (x0 + 236, y0 + 26)], fill=(250, 200, 90), width=2)


def scene_tanker(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (26, 54, 84), (58, 102, 138))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(18, 46, 72))
    tx, ty = x0 + 52, y1 - 22
    d.polygon([(tx, ty), (tx + 128, ty), (tx + 114, ty + 12), (tx + 12, ty + 12)], fill=(14, 20, 28))
    d.rectangle([tx + 20, ty - 8, tx + 96, ty], fill=(120, 52, 40))
    d.rectangle([tx + 104, ty - 13, tx + 114, ty], fill=(14, 20, 28))
    d.ellipse([tx + 88, ty - 4, tx + 98, ty + 4], outline=(250, 180, 90), width=2)


def scene_aid(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (196, 178, 140), (168, 148, 116))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(120, 104, 80))
    tx, ty = x0 + 56, y1 - 30
    d.rectangle([tx, ty, tx + 74, ty + 20], fill=(240, 238, 230))
    d.polygon([(tx + 74, ty + 4), (tx + 94, ty + 10), (tx + 94, ty + 20), (tx + 74, ty + 20)],
              fill=(214, 210, 200))
    d.rectangle([tx + 30, ty + 4, tx + 44, ty + 16], fill=(178, 40, 36))
    d.rectangle([tx + 35, ty + 2, tx + 39, ty + 18], fill=(178, 40, 36))
    for wx in (tx + 16, tx + 80):
        d.ellipse([wx - 7, ty + 16, wx + 7, ty + 28], fill=(16, 16, 18))


def scene_missile(d, box):
    import math
    x0, y0, x1, y1 = box
    grad(d, box, (16, 30, 54), (40, 66, 98))
    for a in range(200, 342, 8):
        px = x0 + 40 + 130 * math.cos(math.radians(a))
        py = y1 - 6 + 74 * math.sin(math.radians(a))
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(240, 178, 84))
    d.polygon([(x0 + 168, y0 + 8), (x0 + 176, y0 + 22), (x0 + 162, y0 + 24)], fill=(220, 224, 230))
    d.arc([x0 + 168, y1 - 34, x0 + 224, y1 + 8], 180, 300, fill=(120, 200, 160), width=3)
    d.rectangle([x0 + 188, y1 - 8, x0 + 200, y1], fill=(200, 206, 214))


def scene_badge(d, box):
    import math
    x0, y0, x1, y1 = box
    grad(d, box, (52, 66, 44), (76, 92, 60))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 13
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.48
        a = math.radians(-90 + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=(240, 200, 84))
    d.rectangle([x0 + 26, y1 - 7, x1 - 26, y1 - 4], fill=(30, 38, 26))


def scene_trade(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (38, 74, 96), (70, 116, 138))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(22, 52, 74))
    for i, col in enumerate(((178, 60, 44), (52, 110, 150), (190, 138, 44))):
        d.rectangle([x0 + 62 + i * 34, y1 - 26, x0 + 92 + i * 34, y1 - 12], fill=col)
        d.rectangle([x0 + 62 + i * 34, y1 - 40, x0 + 92 + i * 34, y1 - 27],
                    fill=tuple(max(0, c - 30) for c in col))
    d.line([(x0 + 40, y0 + 8), (x0 + 40, y1 - 40)], fill=(220, 224, 228), width=3)
    d.line([(x0 + 40, y0 + 8), (x0 + 96, y0 + 8)], fill=(220, 224, 228), width=3)


def scene_factory(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (70, 62, 58), (104, 92, 84))
    d.rectangle([x0 + 52, y1 - 22, x0 + 150, y1 - 6], fill=(40, 36, 34))
    for cx_ in (66, 88):
        d.rectangle([x0 + cx_, y1 - 38, x0 + cx_ + 9, y1 - 20], fill=(40, 36, 34))
    for fx, fh in ((150, 20), (162, 26), (174, 16)):
        d.polygon([(x0 + fx - 6, y1 - 20), (x0 + fx, y1 - 20 - fh), (x0 + fx + 6, y1 - 20)],
                  fill=(238, 128, 44))
    d.rectangle([x0, y1 - 6, x1, y1], fill=(30, 27, 25))


def scene_boat(d, box):
    x0, y0, x1, y1 = box
    grad(d, box, (30, 58, 88), (58, 100, 134))
    for i in range(5):
        sx = x0 + 24 + i * 44
        d.arc([sx, y1 - 16, sx + 26, y1 - 4], 0, 180, fill=(140, 190, 220), width=2)
    bx, by = x0 + 84, y1 - 26
    d.polygon([(bx, by), (bx + 72, by), (bx + 60, by + 10), (bx + 12, by + 10)], fill=(16, 22, 30))
    d.line([(bx + 36, by), (bx + 36, by - 13)], fill=(220, 224, 228), width=2)
    d.polygon([(bx + 36, by - 13), (bx + 50, by - 4), (bx + 36, by - 4)], fill=(238, 232, 214))


# ---------------------------------------------------------------- content
HEROES = [
    dict(n=1, scene=scene_cop31, tag="COP31: FINAL TEXT",
         kicker="ANTALYA, TÜRKİYE · CLIMATE", chip="REPORTED",
         head="COP31's deal never says “fossil fuels”",
         summ="After two days of overtime the final ten pages went to a Sunday "
              "plenary: the words are nowhere in it. The 35-by-35 power goal "
              "survives — and 1.5 °C is admitted overshot.",
         src="PRESIDENCY TEXT · AP"),
    dict(n=2, scene=scene_bahrain, tag="BAHRAIN: STRUCK",
         kicker="MANAMA, BAHRAIN · THE GULF", chip="REPORTED",
         head="Iran strikes Bahrain; Manama turns to the UN",
         summ="The Guards say they hit US radar sites. Bahrain says a civilian "
              "plant burned — smoke over Sitra — and on Sunday it demanded "
              "Security Council action and compensation.",
         src="AFP · BAHRAIN FOREIGN MINISTRY"),
    dict(n=3, scene=scene_ukraine, tag="UKRAINE: 186 DRONES",
         kicker="KYIV, UKRAINE · WAR", chip="REPORTED",
         head="186 drones in a single night over Ukraine",
         summ="The Air Force counts 186 drones: 161 downed or jammed, strikes "
              "at 18 places. In the Baltic, a Russian arms ship burned after "
              "a drone strike.",
         src="UKRAINIAN AIR FORCE"),
]

CARDS = [
    dict(n=4, scene=scene_ship, kicker="GULF OF FINLAND · WAR AT SEA",
         head="Arms ship Sparta II ablaze after drone strike",
         summ="Finland says Ukraine was likely behind it.", src="BBC"),
    dict(n=5, scene=scene_memorial, kicker="KRYVYI RIH · WAR",
         head="A double-tap's toll: a boy of seven, a paramedic",
         summ="Killed as rescuers reached the scene; 60 wounded.", src="CITY DEFENCE COUNCIL"),
    dict(n=6, scene=scene_race, kicker="LAS VEGAS · FORMULA 1",
         head="Verstappen wins a Vegas thriller by 0.639s",
         summ="35 lead changes; Piastri third from 17th.", src="FORMULA 1"),
    dict(n=7, scene=scene_tanker, kicker="STRAIT OF HORMUZ · SEA LANES",
         head="Two tankers struck in the strait",
         summ="Hit by unknown projectiles; no casualties.", src="UKMTO"),
    dict(n=8, scene=scene_aid, kicker="GAZA · WAR",
         head="Strikes kill four and wound 14 in Gaza",
         summ="Aid workers among the dead; the ceasefire frays.", src="REPORTS"),
    dict(n=9, scene=scene_missile, kicker="SAUDI ARABIA · AIR DEFENCE",
         head="Coalition downs three Houthi missiles",
         summ="Intercepted over the Mecca region before dawn.", src="COALITION"),
    dict(n=10, scene=scene_badge, kicker="SINALOA, MEXICO · CARTELS",
         head="“El Chapo Isidro” caught; 11 die in the raid",
         summ="An FBI Ten Most Wanted fugitive is held.", src="MEXICAN FORCES"),
    dict(n=11, scene=scene_boat, kicker="NIGERIA · DISASTER",
         head="At least 24 die as a funeral boat capsizes",
         summ="An overcrowded boat went down; search goes on.", src="REPORTS"),
]

ALSO = [
    (16, "Denmark expels a Russian attaché over an alleged plot (Guardian)"),
    (17, "Russian missiles stray into NATO airspace; council meets Monday (Reports)"),
    (18, "Europe wins a seat at the Russia talks in a five-nation group (Kyiv Independent)"),
    (19, "Britain and Ukraine to build Ukrainian drones on British soil (Kyiv)"),
    (20, "EU ban on waste-plastic exports to non-OECD states now in force (EUobserver)"),
    (21, "A drone hits a five-storey home in Vyshhorod; a child among two hurt (Officials)"),
    (22, "The Guards' claim: missiles hit US posts at Al-Riffa and Awali (IRNA)"),
    (23, "Tehran: reopening Hormuz is “pointless” until its demands are met (State TV)"),
    (24, "Fire at Basra's Hartha power station kills at least four (Iraqi state media)"),
    (25, "Gulf council backs Bahrain: its security is “inseparable” (GCC)"),
    (26, "Bolsonaro in intensive care with a bowel obstruction (Reports)"),
    (27, "Trump orders contractors to report Congress's information requests (Reports)"),
    (28, "Trump leans to an economic stranglehold over strikes on Iran (Reports)"),
    (29, "GTA VI launch sales top $3.8bn in a day, an industry record (Industry reports)"),
    (30, "EU–Indonesia trade pact signed after ten years; 98% of tariff lines freed (Reuters)"),
    (31, "Candy factory fire in Cikande: three dead, 39 missing (Reports)"),
    (32, "Manipur toxic liquor kills at least 11; over 180 in hospital (Chief minister)"),
    (33, "Leaders praise the Shenzhen peace declaration and its nuclear pledge (Xinhua)"),
    (34, "Seoul's education chief resigns over an AI cheating scandal (Reports)"),
    (35, "Tunis jails rights activist Sihem Bensedrine for five years (Reports)"),
    (36, "WHO warns drug resistance is outpacing the search for new antibiotics (WHO)"),
]

# dotted world map: rows of a coarse land mask, '#' = land
MAP = [
    "                                                                        ",
    "        ####  ##                                                        ",
    "     ########## ####          ###    #########  ##                      ",
    "   ###############  #       ######## #################                  ",
    "    #############          #############################  ###           ",
    "     ##########            ############################ #####           ",
    "      ########              ##########################                  ",
    "       ######                ######################    ##               ",
    "        ####   #              ##################                        ",
    "        ###  ###               ################     #                   ",
    "         ## #####                #############                          ",
    "         ########                 ###########        ##                 ",
    "          ######        #          #########      ########              ",
    "          #####        ###          #######       ##########            ",
    "           ####         #            #####         #########            ",
    "           ###                        ###           #######    #        ",
    "           ##                          #             #####    ###       ",
    "           #                                          ###    #####      ",
    "                                                      ##      ###       ",
    "                                                                       ",
]
PINS = {  # story number -> (lon, lat)
    1: (30.7, 36.9), 2: (50.6, 26.2), 3: (30.5, 50.4), 4: (27.0, 60.0),
    5: (33.4, 47.9), 6: (-115.1, 36.2), 7: (56.3, 26.5), 8: (34.3, 31.4),
    10: (-107.4, 24.8), 11: (8.5, 9.1), 30: (106.8, -6.2), 31: (108.5, -8.5),
}


# ---------------------------------------------------------------- layout
def hero(d, x, y, w, h, it):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    ih = 86
    it["scene"](d, (x + 2, y + 2, x + w - 2, y + ih))
    chip(d, x + 8, y + 8, it["tag"], BRICK, font_size=10)
    tx = x + 11
    ky = y + ih + 7
    nf = F(SANS_B, 13)
    d.ellipse([tx, ky + 1, tx + 15, ky + 16], fill=BRICK)
    d.text((tx + 3.5, ky + 1.5), str(it["n"]), font=F(SANS_B, 10), fill=(255, 255, 255))
    kx = tx + 21
    spaced(d, kx, ky + 1, it["kicker"], F(SANS_B, 11), GREEN_D, 1)
    cw = chip(d, x + w - 11 - 74, ky - 1, it["chip"], GREEN, font_size=9)
    hy = ky + 21
    hy = block(d, tx, hy, it["head"], F(SERIF_B, 23), w - 22, 27, INK, 2)
    sy = hy + 3
    block(d, tx, sy, it["summ"], F(SERIF, 14), w - 22, 18, (52, 56, 50), 4)
    d.text((tx, y + h - 17), it["src"], font=F(SANS_B, 9), fill=GREEN)


def card(d, x, y, w, h, it):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    ih = 38
    it["scene"](d, (x + 1, y + 1, x + w - 1, y + ih))
    tx = x + 8
    ky = y + ih + 4
    d.ellipse([tx, ky, tx + 13, ky + 13], fill=BRICK)
    d.text((tx + 3, ky + 1), str(it["n"]), font=F(SANS_B, 9), fill=(255, 255, 255))
    spaced(d, tx + 17, ky + 1, it["kicker"], F(SANS_B, 9), GREEN_D, 0)
    hy = ky + 16
    hy = block(d, tx, hy, it["head"], F(SERIF_B, 16), w - 16, 19, INK, 2)
    block(d, tx, hy + 1, it["summ"], F(SERIF, 12), w - 16, 15, (52, 56, 50), 2)
    d.text((x + w - 8 - tw(d, it["src"], F(SANS_B, 8)), y + h - 13),
           it["src"], font=F(SANS_B, 8), fill=GREEN)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # top strip
    spaced(d, M, 5, "ONE PAGE · THE WHOLE DAY · SET IN TYPE BEFORE THE GAVEL",
           F(SANS_B, 10), INK, 1)
    t = "SUNDAY EDITION"
    spaced(d, W - M - spaced_w(d, t, F(SANS_B, 10), 1), 5, t, F(SANS_B, 10), INK, 1)
    d.line([(M, 24), (W - M, 24)], fill=INK, width=2)

    # masthead
    title = "THE SUNDAY LEDGER"
    tf = F(DISPLAY, 62)
    d.text(((W - tw(d, title, tf)) / 2, 30), title, font=tf, fill=INK)
    d.line([(M, 104), (W - M, 104)], fill=INK, width=1)
    d.text((M, 109), "SUNDAY 22 NOVEMBER 2026", font=F(SANS_B, 14), fill=INK)
    mid = "Sunday, the twenty-second of November, two thousand and twenty-six"
    mf = F(SERIF, 13)
    d.text(((W - tw(d, mid, mf)) / 2, 110), mid, font=mf, fill=GREY)
    t = "SIGNATURE EDITION"
    d.text((W - M - tw(d, t, F(SANS_B, 14)), 109), t, font=F(SANS_B, 14), fill=GREEN)
    d.line([(M, 128), (W - M, 128)], fill=INK, width=3)
    d.line([(M, 133), (W - M, 133)], fill=INK, width=1)

    # stat strip
    stats = [("186", "DRONES IN ONE NIGHT OVER UKRAINE"),
             ("2", "TANKERS HIT IN THE STRAIT OF HORMUZ"),
             ("39", "HOURS OF OVERTIME AT COP31"),
             ("35", "LEAD CHANGES IN LAS VEGAS"),
             ("11", "KILLED IN THE SINALOA RAID"),
             ("98%", "OF EU–INDONESIA TARIFF LINES FREED")]
    sy = 140
    d.rectangle([M, sy, W - M, sy + 46], fill=GREEN_D)
    sw = CW / 6
    for i, (num, lab) in enumerate(stats):
        cx = M + i * sw
        nf = F(SANS_B, 24)
        d.text((cx + (sw - tw(d, num, nf)) / 2, sy + 2), num, font=nf, fill=(255, 255, 255))
        lf = F(SANS, 8)
        for j, ln in enumerate(wrap(d, lab, lf, sw - 8)):
            d.text((cx + (sw - tw(d, ln, lf)) / 2, sy + 30 + j * 9), ln, font=lf,
                   fill=GREEN_PALE)
        if i:
            d.line([(cx, sy + 6), (cx, sy + 40)], fill=GREEN_M, width=1)

    # region bar
    ry = 192
    regions = [("EUROPE 9", GREEN_D), ("MIDDLE EAST 8", GREEN), ("AMERICAS 6", GREEN_M),
               ("ASIA-PACIFIC 5", (84, 142, 102)), ("AFRICA 2", (116, 164, 128)),
               ("WORLD 6", (148, 182, 148))]
    widths = [150, 196, 168, 196, 120, 150]
    cx = M
    for (name, col), wdt in zip(regions, widths):
        d.rectangle([cx, ry, cx + wdt, ry + 24], fill=col)
        nf = F(SANS_B, 12)
        d.text((cx + (wdt - tw(d, name, nf)) / 2, ry + 5), name, font=nf,
               fill=(255, 255, 255))
        cx += wdt

    # heroes
    hy = 224
    hw = (CW - 24) // 3
    for i, it in enumerate(HEROES):
        hero(d, M + i * (hw + 12), hy, hw, 238, it)

    # cards: 4 x 2
    cy = 474
    cw_ = (CW - 24) // 4
    for i, it in enumerate(CARDS):
        r, c = divmod(i, 4)
        card(d, M + c * (cw_ + 8), cy + r * 138, cw_, 130, it)

    # map + also
    my = 756
    d.text((M, my), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    d.text((M + 168, my + 2), "pins match story numbers", font=F(SERIF, 11), fill=GREY)
    mapx, mapy, mapw, maph = M, my + 20, 400, 168
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(24, 44, 66))
    rows = len(MAP)
    cols = max(len(r) for r in MAP)
    for ri, row in enumerate(MAP):
        for ci, ch in enumerate(row):
            if ch == "#":
                px = mapx + 6 + ci * (mapw - 12) / cols
                py = mapy + 6 + ri * (maph - 12) / rows
                d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(196, 178, 132))
    for n, (lon, lat) in PINS.items():
        px = mapx + (lon + 180) / 360 * mapw
        py = mapy + (90 - lat) / 180 * maph
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=BRICK)
        s = str(n)
        d.text((px - tw(d, s, F(SANS_B, 9)) / 2, py - 5), s, font=F(SANS_B, 9),
               fill=(255, 255, 255))

    ax = M + 424
    d.text((ax, my), "ALSO ON SUNDAY 22 NOVEMBER", font=F(SANS_B, 13), fill=INK)
    d.text((ax + 252, my + 2), "— 21 more stories", font=F(SERIF, 11), fill=GREY)
    colw = (W - M - ax - 14) // 2
    af = F(SERIF, 12)
    for ci in range(2):
        items = ALSO[ci * 11:(ci + 1) * 11]
        yy = my + 22
        for n, text in items:
            lines = wrap(d, text, af, colw - 26)
            d.text((ax + ci * (colw + 14), yy), str(n), font=F(SANS_B, 11), fill=BRICK)
            for ln in lines:
                d.text((ax + ci * (colw + 14) + 24, yy), ln, font=af, fill=INK)
                yy += 15
            yy += 2

    # date check
    dy = 950
    d.rectangle([M, dy, W - M, dy + 44], outline=BRICK, width=2)
    d.text((M + 10, dy + 6), "DATE CHECK — LEFT OUT ON PURPOSE", font=F(SANS_B, 11),
           fill=BRICK)
    d.text((M + 10, dy + 23),
           "Not Sunday's news: the Shenzhen summit itself (Thu 19 Nov) · the ICJ's Myanmar judgment (Thu 19 Nov) · the 400-drone,",
           font=F(SERIF, 12), fill=INK)
    d.text((M + 10, dy + 37 - 6),
           "110-missile barrage (night of 19–20 Nov) · COP31's Article 6 decisions (Fri 20 Nov) · Wall Street's AI sell-off (Fri 20 Nov).",
           font=F(SERIF, 12), fill=INK)

    # ledger line
    ly = 1002
    d.line([(M, ly - 4), (W - M, ly - 4)], fill=INK, width=1)
    t = "THE LEDGER LINE — 36 STORIES IN · 5 LEFT OUT · EVERY STORY REPORTED OR STILL DEVELOPING ON SUNDAY 22 NOVEMBER 2026"
    tf2 = F(SANS_B, 11)
    d.text(((W - tw(d, t, tf2)) / 2, ly), t, font=tf2, fill=GREEN_D)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_draft1.png")
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
