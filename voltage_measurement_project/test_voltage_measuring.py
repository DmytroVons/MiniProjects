import statistics
from unittest.mock import patch
import pytest
from io import StringIO
import sys

from voltage_measurement import VoltageMeasurement


@patch('serial.Serial')
def test_voltage_measurement(mock_serial):
    # Arrange
    mock_serial.return_value.is_open = True
    mock_serial.return_value.readline.return_value.decode.return_value = "3.14"
    measurement = VoltageMeasurement("COM3", 9600, 1.0)
    measurement.serial_conn = mock_serial.return_value

    # Act
    voltage = measurement.read_voltage()

    # Assert
    assert voltage == 3.14


def test_calculate_statistics():
    # Arrange
    voltages = [1.23, 2.34, 3.45, 4.56, 5.67]
    measurement = VoltageMeasurement("COM3", 9600, 1.0)
    measurement.data = voltages

    # Redirect standard output for testing print statements
    captured_output = StringIO()
    sys.stdout = captured_output

    # Act
    measurement.calculate_statistics()

    # Get the printed output
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    # Assert
    expected_output = "Mean: 3.45V\nMedian: 3.45V\nMode: 1.23V\nStandard Deviation: 1.76V\n"
    assert output == expected_output

    # Check standard deviation with a tolerance of 0.05
    calculated_std_dev = statistics.stdev(voltages)
    expected_std_dev = 1.76
    assert abs(calculated_std_dev - expected_std_dev) < 0.05


if __name__ == "__main__":
    pytest.main()
