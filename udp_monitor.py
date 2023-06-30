import sys
from PySide6.QtCore import QObject, Signal, QDateTime
from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtNetwork import QUdpSocket, QHostAddress
from PySide6.QtGui import QIcon
import xml.dom.minidom

class UDPMonitor(QObject):
    message_received = Signal(str, str)

    def __init__(self, port=8989, parent=None):
        super().__init__(parent)
        self.port = port
        self.udp_socket = QUdpSocket()
        self.setup_udp_socket()

    def setup_udp_socket(self):
        self.udp_socket.bind(QHostAddress.Any, self.port)
        self.udp_socket.readyRead.connect(self.process_pending_datagrams)

    def process_pending_datagrams(self):
        while self.udp_socket.hasPendingDatagrams():
            datagram, host, port = self.udp_socket.readDatagram(self.udp_socket.pendingDatagramSize())
            message = datagram.data().decode('utf-8')
            ip_address = host.toString().split(':')[-1]
            self.message_received.emit(message, ip_address)

    def change_port(self, new_port):
        if new_port != self.port:
            self.udp_socket.close()
            self.port = new_port
            self.setup_udp_socket()

  
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("UDP Monitor")
        self.resize(400, 300)
        self.port = 8989
        self.port_label = QLabel("Port:")
        self.port_edit = QLineEdit(str(self.port))
        self.port_edit.editingFinished.connect(self.handle_port_change)
        self.text_edit = QTextEdit()
        self.layout = QVBoxLayout()
        self.port_layout = QHBoxLayout()
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addWidget(self.port_edit)
        
        self.layout.addLayout(self.port_layout)
        self.layout.addWidget(self.text_edit)
        
        
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.udp_monitor = UDPMonitor(port=self.port)
        self.udp_monitor.message_received.connect(self.display_message)
        
    def handle_port_change(self):
        new_port = int(self.port_edit.text())
        if new_port != self.port:
            self.port = new_port
            self.text_edit.append(f"Changing port to {self.port}")
            self.udp_monitor.change_port(self.port)
              
    def display_message(self, message, port):        
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss.zzz")
        self.text_edit.append("Recived at " + timestamp + " from: " + port)
        self.text_edit.append(self.pretty_print_xml(message))
        self.text_edit.append("----------------------------------------\n")
    def pretty_print_xml(self, xml_string):
        xml_string = xml_string.replace("\x00", "")
        try:
            dom = xml.dom.minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml(indent="  ")
            return pretty_xml
        except xml.parsers.expat.ExpatError:
            # If the XML is invalid, return the original message as plain text
            return xml_string

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("upd_app_icon.png"))
    window = MainWindow()
    window.setWindowIcon(QIcon("upd_app_icon.png"))
    window.show()
    sys.exit(app.exec())
