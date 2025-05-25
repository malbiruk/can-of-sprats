from my_sardine_tools import D, State, loop

clock.tempo = 140

state = State()


def lead(p=1, i=0, orbit=0):
    n = "E3 . E3 C4 . F3 . A3"
    amp = 0.025
    state.lead.init(n_steps=16, p=0.5, orbit=orbit, n=n, sustain=0.25)
    state.lead.fx.init(hpf=400, shape=0.5, tremolodepth=0.6, tremolorate=32)
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
    state.reverb.init(n_steps=16, p=0.5, orbit=orbit, pan="0 1", room=0.75, size=0.9, dry=0.75)
    dur = loop(
        (D, dict(sound="bd", amp=0) | state.reverb.params()),
        n_steps=state.reverb.n_steps,
        p=state.reverb.p,
    )
    again(swim(reverb), p=dur, i=i + 1)


def bass(p=1, i=0, orbit=1):
    state.bass.init(n_steps=8, p="[3 2 3!2 2 1.5 1 0.5]")
    n = "D0!2 F0 C0!4 F0"
    state.bass.init(orbit=orbit, sound="super808", n=n, sustain=1.5, cut=1, amp=0.3)
    state.bass.fx.init(shape=0.85, lpf=100)
    dur = loop(
        (D, state.bass.fx | state.bass.params()),
        n_steps=state.bass.n_steps,
        p=state.bass.p,
    )
    again(swim(bass), p=dur, i=i + 1)


def hh(p=1, i=0, orbit=2):
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


def snare_1(p=1, i=0, orbit=3):
    state.drums.sn1.init(n_steps=2, p=2, orbit=orbit, sound=". sn:1")
    state.drums.sn1.fx.init(shape=0.5)
    dur = loop(
        (D, state.drums.sn1.fx | state.drums.sn1.params()),
        n_steps=state.drums.sn1.n_steps,
        p=state.drums.sn1.p,
    )
    again(swim(snare_1), p=dur, i=i + 1)


def snare_2(p=1, i=0, orbit=4):
    sound = "[.!18 1 .!27 1 .!3 1 .!9 1!2 .!2] * sn:0"
    state.drums.sn2.init(n_steps=64, p=0.25, orbit=orbit, sound=sound, speed="1!60 1.2!2 1!2")
    state.drums.sn2.fx.init(shape=0.35)
    dur = loop(
        (D, state.drums.sn2.fx | state.drums.sn2.params()),
        n_steps=state.drums.sn2.n_steps,
        p=state.drums.sn2.p,
    )
    again(swim(snare_2), p=dur, i=i + 1)


def crash(p=1, i=0, orbit=5):
    sound = "crash:0 .!2 crash:1 .!4 [.!3 crash:1]!2"
    pan = sound.replace("crash:0", "0.1").replace("crash:1", "0.8")
    amp = sound.replace("crash:0", "0.8").replace("crash:1", "0.6")
    state.drums.crash.init(n_steps=16, p=1, orbit=orbit, sound=sound, pan=pan, amp=amp)
    dur = loop(
        (D, state.drums.crash.params()),
        n_steps=state.drums.crash.n_steps,
        p=state.drums.crash.p,
    )
    again(swim(crash), p=dur, i=i + 1)


def tom(p=1, i=0, orbit=6):
    sound = ".!24 . house:7!3 [. house:7]!2"
    pan = ".!24 [0.2 0.8]!2 . 0.8"
    state.drums.tom.init(n_steps=32, p=0.5, orbit=orbit, sound=sound, pan=pan, amp=0.3)
    dur = loop(
        (D, state.drums.tom.params()),
        n_steps=state.drums.tom.n_steps,
        p=state.drums.tom.p,
    )
    again(swim(tom), p=dur, i=i + 1)


all = {lead, reverb, bass, hh, snare_1, snare_2, crash, tom}
melody = {lead, reverb}
hhh = {hh, snare_2, tom}

for func in all:
    swim(func)

# things to add:
# 1. police siren
# 2. choir
# 3. glass break
# 4. square impact
# 5. arp
# 6. air horn
# 7. mixing and mastering
