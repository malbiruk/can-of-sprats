Pa * d("(set pk [1 . . .]) * bd")
Pb * d("(set ps [.!4 1 .!2 1]) * sd")
Pc * d("(get pk) ^| (get ps) * bleep")  # outputs [1 ... 1 .. 1]

Pa.stop()

silence()


@swim
def demo(p=1 / 4, i=0):
    D("moog:5", lpf="(sin (time)*2500)", res="(cos (time))/2", i=i, legato=0.1)
    D("cp", speed="0+(abs -rand*5)", d=8, i=i)
    again(demo, p=1 / 8, i=i + 1)


d1 * s("0 60")

hush()
silence()


@swim
def gui_loop(p=1, i=0):
    blip = d1.stream.get("0", 0)
    bloop = d1.stream.get("60", 1)
    print(blip)
    print(bloop)
    again(gui_loop, p=1, i=i + 1)
