# UDP Monitor and Sender

UDP Monitor and Sender is a Python application that consists of two components: a monitor (`udp_monitor.py`) and a sender (`udp_sender.py`). The monitor component listens for UDP messages on a specific port and displays them in a graphical user interface (GUI). The sender component sends UDP messages to a specified IP address and port.

## Prerequisites

- Python 3.6 or above
- PySide6 library

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/ulvs/udp_trigger.git
   ```

2. Change to the project directory:

   ```shell
   cd udp_trigger
   ```

3. Install the required packages using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

### Monitor

Run the `udp_monitor.py` file to start the UDP Monitor application:

```shell
python udp_monitor.py
```

The UDP Monitor GUI window will appear. You can enter the desired port number in the "Port" field and click the "Enter" key or focus out of the field to change the monitoring port. The received UDP messages will be displayed in the text area below, along with the timestamp and the source IP address.

### Sender

The `udp_sender.py` file can be used to send UDP messages to a specified IP address and port. You can modify the code in `udp_sender.py` to customize the message content and target IP address/port.

Run the `udp_sender.py` file to send UDP messages:

```shell
python udp_sender.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```