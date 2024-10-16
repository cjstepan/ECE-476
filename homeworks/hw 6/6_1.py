from metronome import Metronome
# Build a metronome with your Pi-Pico. Output a 10ms beep every N ms
# On startup, N = 1000ms (60 beats per minute)
# Increase N by 1% each time you press GP15
# Decrese N by 1% each time you press GP14
# Display beats per minute on the graphics display

# 1) Write a Python program which outputs a 10ms pulse every 1000ms using Timer interrupts
# -Test your program
# -(100ms pulse should read 0.33V, 200ms pulse should read 0.66V, ticks_us() should read 1000000 micro-seconds between beeps)

Metronome()

while True:
    pass
