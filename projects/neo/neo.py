import subprocess
from pathlib import Path

from my_sardine_tools import D, State, calculate_sample_lengths, cut, loop, start, stop

clock.tempo = 140
state = State()
calculate_sample_lengths("projects/neo/samples")


# MELODY
def lead(p=1, i=0, orbit=0):
    n = "E3 . E3 C4 . F3 . A3"
    amp = 0.025
    state.lead.init(n_steps=16, p=0.5, orbit=orbit, n=n, sustain=0.25)
    state.lead.fx.init(hpf=400, shape=0.5, tremolodepth=0.6, tremolorate=32)
    state.lead.fx.init(delaytime=0.5, delayfeedback=0.25, delay=0.25)
    state.lead.saw.init(sound="supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000)
    state.lead.square.init(sound="supersquare", amp=amp)
    dur = loop(
        (D, state.lead.params() | state.lead.fx | state.lead.saw),
        (D, state.lead.params() | state.lead.fx | state.lead.square),
        n_steps=state.lead.n_steps,
        p=state.lead.p,
    )
    again(swim(lead), p=dur, i=i + 1)


def reverb(p=1, i=0, orbit=0):
    state.reverb.init(n_steps=8, p=1, orbit=orbit, pan="0 1", room=0.75, size=0.9, dry=0.75)
    dur = loop(
        (D, dict(sound="bd", amp=0) | state.reverb.params()),
        n_steps=state.reverb.n_steps,
        p=state.reverb.p,
    )
    again(swim(reverb), p=dur, i=i + 1)


def choir(p=1, i=0, orbit=1):
    n = "C4 F3 E3 C3 F3 E3"
    p = "2 2 4 2 2 4"
    state.choir.init(n_steps=6, n=n, p=p, orbit=orbit)
    state.choir.init(sound="choir", amp=0.2, pan=0.4, sustain=2, legato=1.5)
    state.choir.fx.init(hpf=300, octersub=0.25, octersubsub=0.25, vowel="o", lpf=1000)
    state.fx.choir.init(size=0.5, room=0.5, dry=0.75)
    dur = loop(
        (D, state.choir.fx | state.choir.params()),
        n_steps=state.choir.n_steps,
        p=state.choir.p,
    )
    again(swim(choir), p=dur, i=i + 1)


def arp(p=1, i=0, orbit=2):
    n = "[C2 E2 F2 E2]!2 .!8 [C2 F2 G2 A2]!2 .!8 [C2 F2 G2 F2]!2 .!8 [C2 E2 E2 F2]!2 .!8"
    state.arp.init(n_steps=64, p=0.25, orbit=orbit, amp=0.03)
    state.arp.init(sound="superreese", n=n, sustain=0.1)
    state.arp.fx.init(hpf=500, delay=0.25, delaytime=0.5, lpf=1000, shape=0.9)
    dur = loop(
        (D, state.arp.fx | state.arp.params()),
        n_steps=state.arp.n_steps,
        p=state.arp.p,
    )
    again(swim(arp), p=dur, i=i + 1)


# RHYTHM
def bass(p=1, i=0, orbit=3):
    state.bass.init(n_steps=8, p="[3 2 3!2 2 1.5 1 0.5]")
    n = "D0!2 F0 C0!4 F0"
    state.bass.init(orbit=orbit, sound="super808", n=n, sustain=2, cut=1, amp=0.3)
    state.bass.fx.init(shape=0.9, lpf=120)
    dur = loop(
        (D, state.bass.fx | state.bass.params()),
        n_steps=state.bass.n_steps,
        p=state.bass.p,
    )
    again(swim(bass), p=dur, i=i + 1)


def hh(p=1, i=0, orbit=4):
    state.drums.hh.init(n_steps=32, p=0.25)
    sound = "[1!11 [. 1]!3 1!12 .!3] * hh"
    state.drums.hh.init(orbit=orbit, sound=sound, gain=0.55, sustain=0.1)
    state.drums.hh.fx.init(shape=0.75, hpf=4000)

    dur = loop(
        (D, state.drums.hh.fx | state.drums.hh.params()),
        n_steps=state.drums.hh.n_steps,
        p=state.drums.hh.p,
    )
    again(swim(hh), p=dur, i=i + 1)


def snare_1(p=1, i=0, orbit=5):
    state.drums.sn1.init(n_steps=8, p=2, orbit=orbit, sound=". sn:1")
    state.drums.sn1.fx.init(shape=0.5)
    dur = loop(
        (D, state.drums.sn1.fx | state.drums.sn1.params()),
        n_steps=state.drums.sn1.n_steps,
        p=state.drums.sn1.p,
    )
    again(swim(snare_1), p=dur, i=i + 1)


def snare_2(p=1, i=0, orbit=6):
    sound = "[.!18 1 .!27 1 .!3 1 .!9 1!2 .!2] * sn:0"
    state.drums.sn2.init(n_steps=64, p=0.25, orbit=orbit, sound=sound, speed="1!60 1.2!2 1!2")
    state.drums.sn2.fx.init(shape=0.35)
    dur = loop(
        (D, state.drums.sn2.fx | state.drums.sn2.params()),
        n_steps=state.drums.sn2.n_steps,
        p=state.drums.sn2.p,
    )
    again(swim(snare_2), p=dur, i=i + 1)


def crash(p=1, i=0, orbit=7):
    sound = "crash:0 .!2 crash:1 .!4 [.!3 crash:1]!2"
    pan = sound.replace("crash:0", "0.1").replace("crash:1", "0.8")
    amp = sound.replace("crash:0", "0.8").replace("crash:1", "0.6")
    state.drums.crash.init(n_steps=16, p=1, orbit=orbit, sound=sound, pan=pan, amp=amp)
    dur = loop(
        (D, state.drums.crash.fx | state.drums.crash.params()),
        n_steps=state.drums.crash.n_steps,
        p=state.drums.crash.p,
    )
    again(swim(crash), p=dur, i=i + 1)


def tom(p=1, i=0, orbit=8):
    sound = ".!24 . house:7!3 [. house:7]!2"
    pan = ".!24 [0.2 0.8]!2 . 0.8"
    state.drums.tom.init(n_steps=32, p=0.5, orbit=orbit, sound=sound, pan=pan, amp=0.3)
    dur = loop(
        (D, state.drums.tom.fx | state.drums.tom.params()),
        n_steps=state.drums.tom.n_steps,
        p=state.drums.tom.p,
    )
    again(swim(tom), p=dur, i=i + 1)


# SFX
def siren(p=1, i=0, orbit=9):
    cut("sfx:0", 16, pan="(pal [1:0;8])", amp=0.3, orbit=orbit)


def airhorn(p=1, i=0, orbit=9):
    params = dict(sound="[sfx:2 .]!3", pan="0.8!6 0.2!6", orbit=orbit, amp="[0.04 0.015]!!6")
    fx = dict(note=3, hpf=600, delay=0.5, delaytime=1.5, delayfeedback=0)
    loop(
        (D, params | fx),
        n_steps=12,
        p="[0.75 0.25 0.25 0.25 1.5 1]!4",
    )


def glass(p=1, i=0, orbit=10):
    D("sfx:1", pan=0.65, amp=0.15, room=0.75, size=0.9, dry=0.25, orbit=orbit)


def square_impact(p=1, i=0, orbit=11):
    p = "[0.5 0.25 0.25 0.5 0.5 0.75 0.25 0.75 0.25]"
    sound = "[. 1 . 1 . 1 . 1 .] * supersquare"
    params = dict(orbit=orbit, sound=sound, n="A#4", amp=0.05, cut=1, sustain=p + "* 0.5")
    fx = dict(pan=0.4, hpf=400, squiz=1.25, lpf=2500, tremolodepth=0.6, tremolorate=32, voice=0.5)
    loop(
        (D, params | fx),
        n_steps=8,
        p=p,
    )


# VOCALS (microphone live input)
def mic(p=1, i=0, orbit=12):
    state.mic.init(sound="in", amp=0.25, size=0.25, dry=0.75, orbit=orbit)
    D(i=i, **state.mic)
    again(swim(mic), p=1, i=i + 1)


# ARRANGEMENT
base = {bass, snare_1, crash}
melody = {lead, reverb}
hhh = {hh, snare_2, tom}


def arrangement(p=1, i=0):
    steps = [
        (lambda: start(base, melody, hhh, siren), 32),
        (lambda: start(glass, square_impact), 32),
        (lambda: start(airhorn, choir), 32),
        (lambda: (start(arp), stop(melody, tom)), 32),
        (lambda: (start(melody, glass, tom), stop(choir)), 32),
        (lambda: (start(choir), stop(hhh, arp)), 32),
        (lambda: (start(airhorn, glass, hhh), stop(choir)), 32),
        (lambda: start(choir), 16),
        (lambda: start(airhorn), 16),
        (lambda: stop(hhh, snare_1, choir, crash), 32),
        (lambda: silence(), 0),
    ]

    if i < len(steps):
        action, sleep_for = steps[i]
        action()
        if sleep_for > 0:
            again(swim(arrangement), p=sleep_for, i=i + 1)


# KARAOKE
karaoke_file = Path("karaoke.html")


def update_karaoke_display(text):
    with karaoke_file.open("w") as f:
        f.write(f"""
        <html>
        <head>
            <script>
                setTimeout(() => location.reload(), 300);
            </script>
            <style>
                body {{
                    background: black;
                    color: lime;
                    font-size: 48px;
                    text-align: center;
                    font-family: Courier;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    padding: 0 80px;
                    overflow: hidden;
                    box-sizing: border-box;
                }}
                html {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            {text}
        </body>
        </html>
        """)


def open_karaoke_window():
    update_karaoke_display("")
    subprocess.Popen(
        ["firefox", "--kiosk", "--new-window", f"file://{karaoke_file.resolve()}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def karaoke(p=1, i=0):
    lyrics = [
        ("", 40),
        ("НАСТОЯЩИЙ БЕЛЫЙ С УЛИЦ", 4),
        ("ИГРА ПОШЛА ПО ПОЛНОЙ", 4),
        ("СО МНОЮ ЗЛЫЕ СУКИ", 4),
        ("МЕШАЮ ДВЕ МИКСТУРЫ", 4),
        ("МЕШАЮ ВСЕ ТЕКСТУРЫ", 4),
        ("ОНИ НЕ В АДЕКВАТЕ", 4),
        ("ДУМАЮТ ЧТО Я НЕО", 4),
        ('ТОТ ЧЕЛ ИЗ ФИЛЬМА "MATRIX"', 4),
        ("НО МОИ СУКИ ПИЗЖЕ", 4),
        ("ОНИ СО МНОЙ БЕСПЛАТНО", 4),
        ("А НА НОГАХ MARGIELA", 4),
        ("И ЗОЛОТЫЕ GUCCI", 4),
        ("ОНА НА БЕЛОМ СВЭГЕ", 4),
        ("ЗАБРАЛ ИХ С УНИВЕРА", 4),
        ("Я САМ ХОДИЛ КОГДА-ТО", 4),
        ("МОЙ СВЭГ ОН С УЛИЦ БЭЙБИ, ДА", 6),
        ("Я НЕ ЗАМЕТИЛ КАК Я САМ УЖЕ ТЕПЕРЬ НА КРИМИНАЛЕ, ЭЙ", 10),
        ("НА МНЕ ДЕЛА РЕАЛЬНО, ДА", 6),
        ("Я НЕ ПРОСТО ТАК СКРЫВАЮ ЭТИ ТАЙНЫ ЭТИ ТАЙНЫ ЭТИ ТАЙНЫ, ДА", 14),
        ("ДА, ЭТИ СУКИ МОЙ СТИЛЬ ЛЮБЯТ МОЙ ФЛОУ", 10),
        ("ВСЕ ЭТИ РЭПЕРЫ МАКСИМУМ ФОН, А", 8),
        ("ОНА ЛЮБИТ МЕНЯ ТОЛЬКО ЗА МУЗОН, ДА", 6),
        ("ТОЛЬКО ЗА МОЙ МУВ И КАК Я ЕЁ ЕБУ", 10),
        ("ЛЮБЛЮ", 2),
        ("ЭТИ", 2),
        ("ЖОПЫ", 2),
        ("СИСЬКИ", 2),
        ("БЭЙБИ", 2),
        ("ДЕЛАЙ ВСЁ ЧТО ХОЧЕШЬ", 4),
        ("КРЭЙЗИ", 4),
        ("A", 6),
        ("ЖИЗНЬ СВОДИТ С УМА, ДА", 8),
        ("РОК-Н-РОЛЛЕР В ДЕЛЕ", 4),
        ("ЭТИ ШЛЮХИ В ДЕЛЕ, ДА", 4),
        ("ЭТИ ДЕНЬГИ В ДЕЛЕ, ДА", 4),
        ("МОИ ЛЮДИ В ТЕМЕ, ДА", 4),
        ("Я ДАВНО НА СХЕМЕ", 4),
        ("ВСЮ ЖИЗНЬ НА СХЕМЕ, ЭЙ", 4),
        ("Я МУЧУСЬ ТАК КРЭЙЗИ", 4),
        *[("А", 2)] * 5,
        ("ДА", 2),
        ("Я ВСЮ ЖИЗНЬ НА СХЕМЕ", 4),
        *[("А", 2)] * 5,
        ("ДА", 2),
        ("МУЧУСЬ ОЧЕНЬ КРЭЙЗИ", 4),
        ("", 0),
    ]

    if i < len(lyrics):
        line, sleep_for = lyrics[i]
        update_karaoke_display(line)

        if sleep_for > 0:
            again(swim(karaoke), p=sleep_for, i=i + 1)


# PERFORMANCE
# start(mic)
start(arrangement)
open_karaoke_window()
start(karaoke)

# # MANUAL ARRANGEMENT
# start(base, melody, hhh, siren)  # 32 beats

# start(glass, square_impact)  # 32 beats

# start(airhorn, choir)  # 32 beats

# start(arp)
# stop(melody, tom)  # 32 beats

# start(melody, glass, tom)
# stop(choir)  # 32 beats

# start(choir)
# stop(hhh, arp)  # 32 beats

# start(airhorn, glass, hhh)
# stop(choir)  # 32 beats

# start(choir)  # 16 beats

# start(airhorn)  # 16 beats

# stop(hhh, snare_1, choir, crash)  # 32 beats

# silence()
