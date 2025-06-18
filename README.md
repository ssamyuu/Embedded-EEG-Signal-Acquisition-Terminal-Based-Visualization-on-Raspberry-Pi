# Embedded-EEG-Signal-Acquisition-Terminal-Based-Visualization-on-Raspberry-Pi
This project showcases a real-time EEG signal acquisition system built using a Raspberry Pi 4 and the ADS1299 (Texas Instruments' 8-channel, 24-bit biopotential analog front end). The entire solution runs completely offline, without using any third-party Python libraries or internet connection.
The ADS1299 was interfaced with the Raspberry Pi via SPI, while GPIO interrupts were used to capture the EEG data in real time. All register configurations and command sequences for the ADS1299 were implemented manually in Python using spidev and RPi.GPIO.
Once captured, EEG signals from 8 channels were processed and scaled to microvolts. Instead of relying on GUI-based tools like matplotlib, the system prints live ASCII-based waveform data directly to the terminal, enabling visualization over SSH or headless setups.

🔧 Features:
-Real-time 8-channel EEG acquisition via SPI,
-Offline Python execution with only built-in libraries,
-GPIO interrupt-driven data polling (pin 37),
-ASCII waveform display directly in the terminal,
-100% compatible with air-gapped systems (no pip needed).
