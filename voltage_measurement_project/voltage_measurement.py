import statistics
from typing import List

import serial


class VoltageMeasurement:

    def __init__(self, port: str, baud_rate: int, nplc: float):
        """
        Initialize the VoltageMeasurement class with the specified COM port, baud rate,
        and NPLC (Number of Power Line Cycles) for voltage measurement.

        Args:
            port (str): The COM port to communicate with the device.
            baud_rate (int): The baud rate for serial communication.
            nplc (float): The Number of Power Line Cycles for voltage measurement.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.nplc = nplc
        self.data: List[float] = []

    def connect(self) -> None:
        """
        Establish a serial connection to the measuring device.
        """
        self.serial_conn = serial.Serial(self.port, self.baud_rate)
        if self.serial_conn.is_open:
            print(f"Connected to {self.port} at {self.baud_rate} baud")

    def read_voltage(self) -> float:
        """
        Read and return the voltage measurement from the device.

        Returns:
            float: The measured voltage.
        """
        if self.serial_conn.is_open:
            self.serial_conn.write(f"NPLC{self.nplc}".encode())
            raw_data = self.serial_conn.readline().decode().strip()
            voltage = float(raw_data)
            self.data.append(voltage)
            return voltage
        else:
            print("Connection not open.")
            return 0.0

    def calculate_statistics(self) -> None:
        """
        Calculate and print statistics for the collected voltage data.
        """
        if self.data:
            mean = statistics.mean(self.data)
            median = statistics.median(self.data)
            mode = statistics.mode(self.data)
            std_dev = statistics.stdev(self.data)
            print(f"Mean: {mean:.2f}V\nMedian: {median:.2f}V\nMode: {mode:.2f}V\nStandard Deviation: {std_dev:.2f}V")
        else:
            print("No data to calculate statistics.")

    def close_connection(self) -> None:
        """
        Close the serial connection.
        """
        if self.serial_conn.is_open:
            self.serial_conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    com_port = "COM3"  # Replace with your COM port
    baud_rate = 9600
    nplc = 1.0  # Set NPLC value here

    measurement = VoltageMeasurement(com_port, baud_rate, nplc)
    measurement.connect()

    try:
        while True:
            input("Press Enter to measure voltage or 'q' to quit: ")
            voltage = measurement.read_voltage()
            print(f"Voltage: {voltage:.2f}V")

    except KeyboardInterrupt:
        measurement.calculate_statistics()
        measurement.close_connection()
        print("Measurement ended.")
