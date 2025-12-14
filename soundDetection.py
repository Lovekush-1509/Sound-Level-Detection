
import streamlit as st
import numpy as np
import sounddevice as sd
import time

# Parameters
DURATION = 1  # seconds
SAMPLE_RATE = 44100
LOW_THRESHOLD = 0.01
MEDIUM_THRESHOLD = 0.03

# Functions
def calculate_rms(audio):
    return np.sqrt(np.mean(audio**2))

def classify_sound_level(rms):
    if rms < LOW_THRESHOLD:
        return "Low"
    elif rms < MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "High"

# Streamlit placeholders
st.title("Real-Time Sound Level Detector")
chart = st.line_chart([])
status = st.empty()

rms_values = []

st.write("Press Stop to end detection.")

try:
    while True:
        # Record audio
        audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        audio = audio.flatten()

        # RMS and level
        rms = calculate_rms(audio)
        level = classify_sound_level(rms)

        # Update chart
        rms_values.append(rms)
        chart.line_chart(rms_values)

        # Show current level
        status.text(f"Sound Level: {level}  |  RMS: {rms:.5f}")

        time.sleep(0.1)

except KeyboardInterrupt:
    st.write("Detection stopped.")
except Exception as e:
    st.error(f"Error: {e}")
