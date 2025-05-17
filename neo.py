from my_sardine_tools.utils import D

clock.tempo = 140


@swim
def melody(
    p=1,
    i=0,
    amp=0.05,
):
    notes = "E3 . E3 C4 . F3 . A3"
    kwargs = dict(
        n=notes,
        i=i,
        orbit=0,
        hpf=400,
        sustain=0.25,
        shape=0.5,
        tremolodepth=0.6,
        tremolorate=32,
    )
    D("supersaw", voice=0.01, amp=amp + 0.05, cutoff=5000, **kwargs)
    D("supersquare", amp=amp, **kwargs)
    again(melody, p=0.5, i=i + 1)


silence()
