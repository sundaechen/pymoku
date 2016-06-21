import pytest
from pymoku import Moku
from pymoku.instruments import *
import conftest
import numpy

def in_bounds(v, center, err):
	return abs(v - center) < abs(err)

class Test_Siggen:
	'''
		Test the generated output waveforms are as expected
	'''
	@pytest.mark.parametrize("ch, amp, freq, offset", [
		(1, 1.0, 1000, 0),
		])
	def test_sinewave_amplitude(self, base_instr, ch, amp, freq, offset):
		# Generate an output sinewave and loop to input
		# Ensure the amplitude is right
		# Ensure the frequency seems correct as well
		base_instr.set_source(ch,OSC_SOURCE_DAC)
		base_instr.synth_sinewave(ch,amp,freq,offset)
		base_instr.commit()

		# Get a few frames and test that the max amplitudes of the generated signals are within bounds
		for n in range(10):
			frame = i.get_frame(timeout=5)
			maxval = max(frame)
			minval = min(frame)
			print "Min: %.2f, Max: %.2f" % (minval, maxval)
			assert in_bounds(maxval, amp+offset, 0.03)
			assert in_bounds(minval, (-1*amp + offset), 0.03)

	def test_sinewave_frequency(self, base_instr, freq):
		# Depending on the input frequency, check that regularly spaced values are approximately the same amplitude (5%)


	def test_squarewave_amplitude(self, base_instr)


class Test_Trigger:
	'''
		We want this class to test everything around triggering settings for the oscilloscope
	'''

	@pytest.mark.parametrize("ch, edge, amp", [
		(OSC_TRIG_CH1, OSC_EDGE_RISING, 0.0),
		(OSC_TRIG_CH1, OSC_EDGE_RISING, 0.5),
		(OSC_TRIG_CH1, OSC_EDGE_RISING, 1.0),
		])
	def test_triggered_amplitude(self, base_instr, ch, edge, amp):
		'''
			Ensure that the start of the frame is the expected amplitude (within some error)
		'''
		i = base_instr
		allowable_error = 0.1 # Volts

		# Enforce buffer/frame offset of zero
		i.set_timebase(0,2e-6)
		# Set the trigger
		i.set_trigger(OSC_TRIG_CH1, OSC_EDGE_RISING, amp, hysteresis=0, hf_reject=False, mode=OSC_TRIG_NORMAL)
		i.commit()

		for n in range(10):
			frame = i.get_frame(timeout=5)
			print "Start of frame value: %.2f" % (frame.ch1[0])
			assert in_bounds(frame.ch1[0], amp, allowable_error)

		assert 0

	def test_triggered_edge(self, base_instr):
		'''
			Ensure the edge type looks right
		'''
		assert 1 == 1


class Test_Timebase:
	'''
		Ensure the timebase is correct
	'''



class Test_Source:
	'''
		Ensure the source is set and rendered as expected
	'''
	@pytest.mark.parametrize("ch, amp",[
		(1, 0.2),
		(1, 0.5),
		(2, 0.1),
		(2, 1.0),
		])
	def test_dac(self, base_instr, ch, amp):
		i = base_instr
		i.synth_sinewave(ch,amp,1e6,0)
		i.set_source(ch, OSC_SOURCE_DAC)
		i.set_timebase(0,2e-6)
		i.commit()

		# Max and min should be around ~amp
		frame = i.get_frame()
		assert in_bounds(max(getattr(frame, "ch"+str(ch))), amp, 0.05)
		assert in_bounds(min(getattr(frame, "ch"+str(ch))), amp, 0.05)
