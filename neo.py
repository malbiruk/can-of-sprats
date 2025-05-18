from my_sardine_tools import create_player, zd_mono

bass = create_player("bass")
clock.tempo = 140


@swim
def melody(p=1, i=0, amp=0.05):
    ziff = "| e 2 r 2 7 r 3 r 5 |"
    common_args = dict(i=i, ziff=ziff, sustain=0.25, orbit=0)
    fx = dict(
        hpf=400,
        shape=0.5,
        tremolodepth=0.6,
        tremolorate=32,
    )

    dur = ZD("supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000, **common_args, **fx)
    ZD("supersquare", amp=amp, **common_args, **fx)
    again(melody, p=dur, i=i + 1)


ziff = "| <-3> h.1 h1 h.3 h.0 h0 q.0 q0 e3 |"
bass_pattern = zd_mono("super808", decay=0, orbit=1, amp=0.5, ziff=ziff, shape=0.85, lpf=100)
bass >> bass_pattern
