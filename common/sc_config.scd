(
s.reboot {
    // Critical timing settings
    s.options.hardwareBufferSize = 2048;
    s.options.blockSize = 256;

    // Resource allocation
	s.options.numBuffers = 1024 * 256;
	s.options.memSize = 8192 * 32;
	s.options.numWireBufs = 256;
	s.options.maxNodes = 1024 * 32;

    // Audio settings
	s.options.numOutputBusChannels = 2;
	s.options.numInputBusChannels = 2;

	s.options.threads = 8;


	s.waitForBoot {
		~dirt = SuperDirt(2, s);
		~dirt.loadSoundFiles;
		~dirt.loadSynthDefs("/home/klim/Documents/REAPER Media/can_of_sprats/common/synthdefs/");
		~dirt.loadSoundFiles("/home/klim/Documents/REAPER Media/can_of_sprats/common/samples/*");
		s.sync;
		// ~dirt.start(57120, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]);
		~dirt.start(57120, 0 ! 12);
		(
			~d1 = ~dirt.orbits[0]; ~d2 = ~dirt.orbits[1]; ~d3 = ~dirt.orbits[2];
			~d4 = ~dirt.orbits[3]; ~d5 = ~dirt.orbits[4]; ~d6 = ~dirt.orbits[5];
			~d7 = ~dirt.orbits[6]; ~d8 = ~dirt.orbits[7]; ~d9 = ~dirt.orbits[8];
			~d10 = ~dirt.orbits[9]; ~d11 = ~dirt.orbits[10]; ~d12 = ~dirt.orbits[11];
		);
	};
	s.latency = 0.3;
};
)
