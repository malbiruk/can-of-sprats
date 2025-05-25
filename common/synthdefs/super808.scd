(
	SynthDef(\super808, {|out, rate=1, sustain=1, curve= -1.5, pan, voice=0, freq=440, speed=1, accelerate|
		var env, sound;
		freq = freq * DirtFreqScale.kr(speed, accelerate, sustain);
		env = EnvGen.ar(Env.linen(0.01, 0, 1, 1, curve), timeScale:sustain, doneAction:2);
		sound = LPF.ar(SinOscFB.ar(XLine.ar(freq.expexp(10, 2000, 1000, 8000), freq, 0.025/rate), voice), 9000);
		Out.ar(out, DirtPan.ar(sound, ~dirt.numChannels, pan, env))
	}).add
);
