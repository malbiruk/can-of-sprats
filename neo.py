from my_sardine_tools.utils import D

clock.tempo = 140


@swim
def melody(
    p=1,
    i=0,
    amp=0.05,
):
    notes = "E3 . E3 C4 . F3 . A3"
    common_args = dict(n=notes, i=i, sustain=0.25, orbit=0)
    fx = dict(
        hpf=400,
        shape=0.5,
        tremolodepth=0.6,
        tremolorate=32,
    )
    D("supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000, **common_args, **fx)
    D("supersquare", amp=amp, **common_args, **fx)
    again(melody, p=0.5, i=i + 1)


silence()
