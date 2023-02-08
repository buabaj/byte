# byte

Proof of concept for Text data transmission over sound modulator-demodulator model. 

This project basically takes the input from the user, encodes it into binary and then modulates it into sound. The sound is then transmitted wirelessly through the speakers of the device. The transmitted sound is then received and recorded by the microphone of the demodulation device. The recorded sound is then demodulated and decoded to get the original message.

## Steps to run the project

- clone the repository on both the modulator and demodulator devices

```bash
git clone https://github.com/buabaj/byte.git
```

- set up the modulator device

```bash
cd byte
pip install -r requirements.txt
cd encode
python3 modulator.py
```

- set up the demodulator device

```bash
cd byte
pip install -r requirements.txt
cd decode
python3 demodulator.py
```

- After running the script on the modulator device, you will be prompted to enter the message to be transmitted. Enter the message in the terminal and press enter.

- Immediately after pressing enter, run the script on the demodulator device. This will start the demodulation process which records the sound produced by the modulator device and decodes it to get the original message.

- The decoded message will be displayed on the terminal of the demodulator device.

## Problems faced

- The modulator device should be kept close to the demodulator device, at high volume for the transmission to be successful.

- The devices should be kept in a quiet environment in order to prevent the recording of background noise which may interfere with the transmission.

- The demodulator script breaks if the input is too long. This is because the binary data is stored in a list which has a fixed size. This can be fixed by using a dynamic data structure like a linked list i think.

### Motivation

- I endeavored to learn about this approach of data transmission after seeing the mobile app proof of concept by Nigerian app developer, [Chiziaruhoma](https://twitter.com/chiziaruhoma/status/1329508952007208962?s=61&t=dPHMD-cyrsD_JnQRor2-Vw). I was guided by the many available open source projects on github.
