from my_sardine_tools import D, loop

clock.tempo = 140


def melody(p=1, i=0, amp=0.05, orbit=0):
    n = "E3 . E3 C4 . F3 . A3"
    common_args = dict(midinote=n, sustain=0.25, orbit=orbit)
    fx = dict(hpf=400, shape=0.5, tremolodepth=0.6, tremolorate=32)

    dur = loop(
        (
            D,
            dict(sound="supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000) | common_args | fx,
        ),
        (D, dict(sound="supersquare", amp=amp) | common_args | fx),
        n_steps=16,
        p=0.5,
    )
    again(mr, p=dur, i=i + 1)


def bass(p=1, i=0, orbit=1):
    n = "D0!2 F0 C0!4 F0"
    p = "[3 2 3!2 2 1.5 1 0.5]"

    params = dict(sustain=1.5, cut=1, amp=0.3, shape=0.85, lpf=100)

    dur = loop(
        (D, dict(sound="super808", n=n, orbit=orbit) | params),
        n_steps=8,
        p=p,
    )
    again(br, p=dur, i=i + 1)


def hh(p=1, i=0, orbit=2):
    pat = "[1!11 [. 1]!3 1!12 .!3] * hh"
    params = dict(gain=0.5, sustain=0.1, shape=0.75, hpf=4000)
    dur = loop(
        (D, dict(sound=pat, orbit=orbit) | params),
        n_steps=32,
        p=0.25,
    )
    again(hr, p=dur, i=i + 1)


def snare_1(p=1, i=0, orbit=3):
    D(". sn:1", orbit=orbit, shape=0.5, i=i)
    again(sr1, p=2, i=i + 1)


def snare_2(p=1, i=0, orbit=4):
    pat = "[.!18 1 .!27 1 .!3 1 .!9 1!2 .!2] * sn:0"
    dur = loop(
        (D, dict(sound=pat, speed="1!60 1.2!2 1!2", orbit=orbit, shape=0.3)),
        n_steps=64,
        p=0.25,
    )
    again(sr2, p=dur, i=i + 1)


def crash(p=1, i=0, orbit=5):
    pat = "crash:0 .!15"
    params = dict(amp=1, pan=0.1)
    dur = loop(
        (D, dict(sound=pat, orbit=orbit) | params),
        n_steps=16,
        p=1,
    )
    again(cr, p=dur, i=i + 1)


cr = swim(crash)


mr = swim(melody)
br = swim(bass)
sr1 = swim(snare_1)
sr2 = swim(snare_2)
hr = swim(hh)

silence()

# make crashes
# crashes should be at ~1.7x speed
# to maintain original pitch freq = 261.63 / speed
# first panned left and pitched 2 semitones low (note=-2)
# second and third -- original pitch and panned right
