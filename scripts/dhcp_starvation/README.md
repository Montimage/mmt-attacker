# DHCP Starvation Attack

## Overview
Exhausts DHCP server IP address pool by sending numerous DHCP DISCOVER requests with spoofed MAC addresses.

## Usage
```bash
sudo python3 dhcp_starvation.py -i eth0 -c 100 -r 10
```

## Options
- `-i, --interface`: Network interface
- `-c, --count`: Number of DHCP requests
- `-r, --rate`: Requests per second
- `-v, --verbose`: Verbose output

## License
Proprietary - Montimage
