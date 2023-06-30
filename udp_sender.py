import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtNetwork import QUdpSocket, QHostAddress


def generate_default_xml():
    # Create the root element
    root = ET.Element("CaptureStart")
    # Create child elements and set attribute values
    name = ET.SubElement(root, "Name")
    name.set("VALUE", "Testing2")
    packet_id = ET.SubElement(root, "PacketID")
    packet_id.set("VALUE", "0")
    # Create the XML tree
    tree =  ET.ElementTree(root)
    return ET.tostring(root, encoding="utf-8").decode("utf-8")
    
def pretty_print_xml(xml_string):
    xml_string = xml_string.replace("\x00", "")
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        return pretty_xml
    except xml.parsers.expat.ExpatError:
        # If the XML is invalid, return the original message as plain text
        return xml_string
        
class UDPSender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDP Broadcast Sender")
        self.resize(400, 400)

        # Create the main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Create the message input textbox
        self.message_input = QTextEdit()
        layout.addWidget(self.message_input)
        self.message_input.setPlainText(pretty_print_xml(generate_default_xml()))  # Default message
        # Create the port label
        port_label = QLabel("Port:")
        layout.addWidget(port_label)

        # Create the port input textbox
        self.port_input = QTextEdit()
        self.port_input.setMaximumHeight(30)
        self.port_input.setPlainText("8989")  # Default port number
        layout.addWidget(self.port_input)

        # Create the send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_udp_message)
        layout.addWidget(send_button)

        # Create the UDP socket
        self.udp_socket = QUdpSocket()

    def send_udp_message(self):
        # Get the message from the input textbox
        message = self.message_input.toPlainText()

        # Get the port number from the input textbox
        port = int(self.port_input.toPlainText())

        # Send the UDP message as a broadcast on the specified port
        self.udp_socket.writeDatagram(message.encode(), QHostAddress.Broadcast, port)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set global font for the application
    app.setFont(QFont("Arial", 10))

    udp_sender = UDPSender()
    udp_sender.show()

    sys.exit(app.exec())
