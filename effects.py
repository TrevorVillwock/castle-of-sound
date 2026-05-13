from pyo import Metro, SfPlayer, Mixer, TrigFunc, Delay, Selector, Sine, Adsr, STRev, Disto, Fader, MoogLP


class Effects:
	def __init__(self, source):
		self.reverb_state = False
		print("source: ")
		print(source)
		# Effects signal chain: 
		self.distortion = Disto(source)
		
		self.filter = MoogLP(self.distortion, freq=1000)
		self.filter_selector = Selector([self.distortion, self.filter], voice=0)

		self.guitar_delay = Delay(self.filter_selector, 0.1, 0.7, 5)
		self.delay_selector = Selector(inputs=[self.filter_selector, self.guitar_delay], mul=[0.5, 0.5], voice=0).out()
		
		# We don't create a selector object for the reverb so we can directly control the amount 
		# of wet reverb signal while leaving the original signal audible
		self.reverb_fader = Fader()
		self.reverb = STRev(self.delay_selector, revtime=10, mul=self.reverb_fader).out()
	
	def connect(self, source):
		self.distortion.set_input(source)