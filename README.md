# DNS Amplification Demo

A university project created for a cybersecurity course. It demonstrates DNS amplification in a Mininet lab.

> **Disclaimer:** This project is for educational purposes only. Run it only in an isolated lab or on networks where you have explicit authorization. Do not use it against public or third-party systems.

## Run

On a 64-bit Linux system with Mininet and Open vSwitch installed, install the Python dependencies (Ubuntu/Debian example):

```bash
sudo apt update
sudo apt install mininet openvswitch-switch python3 python3-venv python3-dnslib
```

From the project directory, create the Python environment and start the topology:

```bash
python3 -m venv --system-site-packages pcyb
sudo systemctl start openvswitch-switch
sudo ./pcyb/bin/python topologia.py
```

When the Mininet CLI appears, enter `exit` to stop the simulation.
