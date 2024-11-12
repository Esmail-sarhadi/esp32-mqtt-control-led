import numpy as np
from scipy import signal
import matplotlib.pyplot as plt




# Time settings
t = np.linspace(0, 0.1, 1000)  # 100ms duration
t_detail = np.linspace(0, 0.01, 1000)  # 10ms for detailed view

def save_plot(filename, dpi=300):
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close()

# 1. Input AC
plt.figure(figsize=(12, 6), dpi=300)
input_ac = 220 * np.sqrt(2) * np.sin(2 * np.pi * 50 * t)
plt.plot(t * 1000, input_ac, 'b-', linewidth=2)
plt.grid(True)
plt.title('1. Input AC Waveform (220V, 50Hz)', fontsize=12)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
save_plot('1_input_ac.png')

# 2. After Bridge Rectifier (before filtering)
plt.figure(figsize=(12, 6), dpi=300)
rectified = np.abs(input_ac)
plt.plot(t * 1000, rectified, 'r-', linewidth=2)
plt.grid(True)
plt.title('2. Full-Wave Rectified Output (After Bridge Rectifier)', fontsize=12)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
save_plot('20_rectified.png')

# 3. DC Link (after filtering)
plt.figure(figsize=(12, 6), dpi=300)
plt.plot(t * 1000, rectified, 'r--', label='Before Filtering', linewidth=1)
dc_filtered = 310 * np.ones_like(t)
plt.plot(t * 1000, dc_filtered, 'g-', label='After Filtering', linewidth=2)
plt.grid(True)
plt.title('3. DC Link Stage (310V DC)', fontsize=12)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
plt.legend(fontsize=10)
save_plot('3_dc_link.png')

# 4. PWM Carrier and Reference
plt.figure(figsize=(12, 6), dpi=300)
# Creating PWM signals
carrier_freq = 15000  # 15 kHz
carrier = 1.1 * signal.sawtooth(2 * np.pi * carrier_freq * t_detail, 0.5)  # Triangle wave
reference = np.sin(2 * np.pi * 50 * t_detail)  # 50 Hz reference
plt.plot(t_detail * 1000, carrier, 'r-', label='Carrier (15 kHz)', linewidth=1)
plt.plot(t_detail * 1000, reference, 'b-', label='Reference (50 Hz)', linewidth=2)
plt.grid(True)
plt.title('4. PWM Generation Signals', fontsize=12)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Normalized Amplitude', fontsize=10)
plt.legend(fontsize=10)
save_plot('4_pwm_signals.png')

# 5. Final High-Frequency Output
plt.figure(figsize=(12, 6), dpi=300)
output_freq = 15000  # 15 kHz
output_ac = 600 * np.sqrt(2) * np.sin(2 * np.pi * output_freq * t_detail)
plt.plot(t_detail * 1000, output_ac, 'b-', linewidth=2)
plt.grid(True)
plt.title('5. Final Output AC Waveform (600V, 15kHz)', fontsize=12)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Voltage (V)', fontsize=10)
save_plot('5_output_ac.png')

# 6. Complete Process Overview
plt.figure(figsize=(12, 10), dpi=300)

# Input AC
plt.subplot(4, 1, 1)
plt.plot(t * 1000, input_ac, 'b-', linewidth=2)
plt.grid(True)
plt.title('Complete AC-DC-AC Conversion Process', fontsize=14)
plt.ylabel('Input AC (V)', fontsize=10)

# Rectified
plt.subplot(4, 1, 2)
plt.plot(t * 1000, rectified, 'r-', linewidth=2)
plt.grid(True)
plt.ylabel('Rectified (V)', fontsize=10)

# DC Link
plt.subplot(40, 1, 3)
plt.plot(t * 1000, dc_filtered, 'g-', linewidth=2)
plt.grid(True)
plt.ylabel('DC Link (V)', fontsize=10)

# Output AC
plt.subplot(4, 1, 4)
t_window = t_detail[0:100]
output_window = output_ac[0:100]
plt.plot(t_window * 1000, output_window, 'b-', linewidth=2)
plt.grid(True)
plt.xlabel('Time (ms)', fontsize=10)
plt.ylabel('Output AC (V)', fontsize=10)

plt.tight_layout()
save_plot('6_complete_process.png')
