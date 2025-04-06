# app.py
from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for signal processing and plot generation
@app.route('/generate_signal', methods=['POST'])
def generate_signal():
    # Get user inputs for signal parameters
    frequency = float(request.form['frequency'])
    amplitude = float(request.form['amplitude'])
    phase = float(request.form['phase'])
    signal_type = request.form['signal_type']

    # Generate time vector
    t = np.linspace(0, 1, 1000)

    # Generate the signal based on the selected type
    if signal_type == 'sine':
        signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    elif signal_type == 'square':
        signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t + phase))
    else:
        signal = np.zeros_like(t)

    # Fourier Transform
    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(t), t[1] - t[0])

    # Plot signal and Fourier transform
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # Plot time-domain signal
    ax1.plot(t, signal, label='Signal')
    ax1.set_title(f'{signal_type.capitalize()} Wave')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Amplitude')
    ax1.legend()

    # Plot frequency-domain (Fourier transform)
    ax2.plot(freq[:len(freq)//2], np.abs(fft_signal)[:len(fft_signal)//2])
    ax2.set_title('Fourier Transform')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Amplitude')

    # Save plot to a BytesIO object and encode it to base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render_template('index.html', img_data=img)

if __name__ == '__main__':
    app.run(debug=True)
