from art import tprint

Pa >> d("bd cp", p=0.5)  # sets period to 0.5, yields 2 notes per beat
Pa >> d("bd cp hh:2", p=0.5)  # adds the hh:2 sample, meter is now felt in 3
Pa >> d("bd cp hh:2", p=0.25)  # period is 0.25, 4 notes per beat, rhythm is twice as fast
Pa >> d("bd!2 cp hh:2 .", p=0.25)  # adds bd repeat and a rest "." - meter is felt in 5.

Pa >> d("reverbkick east:4 yeah:2 mt", speed="0.5 2", shape=0, p="0.25!2 1")
# Pa >> d('reverbkick east:4 yeah:2 mt', speed='1.2 2', shape=0.5, p='0.5 0.25')
# Pa >> d('reverbkick east:4 yeah:2 mt cr', speed='1.2 2.2', shape=0.7, p='0.5!2 0.25!5')

clock.tempo = 135
Pa >> d("bd cp", p=1)  # plays every beat, alternating bd and cp
Pb >> d(". hh27:2", p=0.5)  # plays every 1/2 beat
Pc >> d(". east:4 .", p=0.25)  # plays 2nd of the 1/3 beat
Pd >> d(". . . bleep:0", p=1)  # plays every 4th of the beat

Pa.stop()

clock.tempo

Pa >> n("C5 E5 G5", p=0.25)  # playing a chord, one note every 1/4 of a beat.
Pb >> cc(ctrl=20, chan=0, value="rand>>127")  # sending a random MIDI control on ctrl 20, channel 0
Pc >> d("tabla tabla:2")  # Playing audio samples of an indian tabla

Pa >> d("bd!2 cp hh27:2 . ", speed="1 2", room=0.6, dry=0.2, size=0.5, p=0.5)


@swim
def inFive(p=0.5, i=0):
    D("bd!2 cp hh27:2 . ", speed="1 2", room=0.6, dry=0.2, size=0.5, i=i)
    i += 1
    again(inFive, p=0.5, i=i)


silence(inFive)


Pa >> d("bd . cp!2 . bd cp .", p=0.5, gain="1!2 0.75!2")
Pb >> d(". hh27", p=0.5, room=0.2, size=0.5, phaserrate="0.1", phaserdepth="500")

silence(Pb)

tprint("Hi, all!", font="soft")
tprint("This is", font="soft")
tprint("flowers", font="soft")
tprint("in your", font="soft")
tprint("eyes", font="soft")
tprint("are you", font="soft")
tprint("ready?", font="soft")

Pa >> d("bd donk", p=0.5, speed=0.25, amp="0.75 0.5", sustain=0.5, orbit=11)


clock.tempo = 180

Pa.stop()
