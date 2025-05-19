from my_sardine_tools import ZD_mono

clock.tempo = 140


def melody(p=1, i=0, amp=0.01, orbit=0):
    ziff = "| e 2 r 2 7 r 3 r 5 |"
    common_args = dict(i=i, ziff=ziff, sustain=0.25, orbit=orbit)
    fx = dict(hpf=400, shape=0.5, tremolodepth=0.6, tremolorate=32)
    dur = ZD("supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000, **common_args, **fx)
    ZD("supersquare", amp=amp, **common_args, **fx)
    again(mr, p=dur, i=i + 1)


def bass(p=1, i=0, orbit=1):
    ziff = "| <-3> h.1 h1 h.3 | <-3> h.0 h0 q.0 q0 e3 |"
    dur = ZD_mono("super808", ziff, orbit=orbit, amp=0.3, shape=0.85, lpf=100, i=i)
    again(br, p=dur, i=i + 1)


def hh(p=1, i=0, orbit=2):
    pat = "[1!11 [. 1]!3 1!12 .!3] * hh"
    D(pat, orbit=orbit, gain=0.5, sustain=0.1, shape=0.75, hpf=4000, i=i)
    again(hr, p=0.25, i=i + 1)


def snare_1(p=1, i=0, orbit=3):
    D(". sn:1", orbit=orbit, shape=0.5, i=i)
    again(sr1, p=2, i=i + 1)


def snare_2(p=1, i=0, orbit=4):
    pat = "[.!18 1 .!27 1 .!3 1 .!5 1 .!3 1!2 .!2] * sn:0"
    D(pat, speed="1!60 1.2!2 1!2", orbit=orbit, shape=0.3, i=i)
    again(sr2, p=0.25, i=i + 1)


sr1 = swim(snare_1)
sr2 = swim(snare_2)
hr = swim(hh)
br = swim(bass)
mr = swim(melody)

silence()

print(19 + 27 + 5 + 5 + 1 + 3)
