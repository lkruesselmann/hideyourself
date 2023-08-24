# HideYourself - A Privacy Enhancement Tool

HideYourself is a Python script and graphical user interface (GUI) application designed to enhance your online privacy by providing tools to toggle Tor proxy, spoof MAC addresses, and change your computer name. This script is especially useful when you want to protect your identity and maintain a level of anonymity while using the internet.

## Features

- **Tor Proxy**: Easily toggle Tor proxy on and off to route your internet traffic through the Tor network for enhanced privacy.

- **MAC Address Spoofing**: Randomize your MAC address to make it harder for others to track your device on the network.

- **Computer Name Spoofing**: Change your computer's name to further enhance your anonymity.

## Requirements

Before using HideYourself, make sure you have the following requirements installed:

- [Tor](https://www.torproject.org/): You need to install Tor to use its proxy functionality.

- [spoof-mac](https://github.com/feross/spoof): This tool is required for MAC address spoofing.

Additionally, you should configure your Tor `torrc` file with the following settings:

```
SocksPort 127.0.0.1:9050
HTTPTunnelPort 127.0.0.1:9150
ControlPort 9051
```

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/HideYourself.git
   ```

2. Navigate to the project directory:

   ```bash
   cd HideYourself
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the `spoof-mac` tool:

   ```bash
   brew install spoof-mac
   ```

## Usage

To run HideYourself, execute the following command:

```bash
python hideyourself.py
```

This will launch the HideYourself application.

## How It Works

### Tor Proxy

- Click the "Toggle Tor Proxy" button to turn the Tor proxy on or off. When the proxy is active, your internet traffic will be routed through the Tor network, providing anonymity.

- Click the "Get New Relay" button to request a new Tor server, which will give you a fresh Tor circuit for added privacy.

### MAC Address Spoofing

- Click the "Spoof MAC" button to randomize your MAC address using the `spoof-mac` tool. This makes it more difficult for others to identify your device on the network.

- Click the "Reset MAC" button to revert your MAC address to its original state.

### Computer Name Spoofing

- Click the "Spoof Name" button to change your computer's name to a random string, enhancing your online anonymity.

- Click the "Reset Name" button to revert your computer's name to the one specified in the script. You can change the default name by modifying the script (line 124).

### Restarting Wi-Fi

- Whenever you change your MAC address, the Wi-Fi connection will be restarted automatically to apply the changes.

## Disclaimer

Please use HideYourself responsibly and in compliance with all applicable laws and regulations. Anonymity tools like Tor are designed to protect your privacy, but they should not be used for illegal activities.

---

**Note:** This script is provided as-is, without any warranty or support. Use it at your own risk.

If you encounter any issues or have suggestions for improvements, please feel free to [open an issue](https://github.com/lkruesselmann/hideyourself/issues) on the GitHub repository.
