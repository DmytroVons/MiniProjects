from voltage_measuring import VoltageMeasurement


def test_init_voltage_measurement():
    """
    Tests that the `VoltageMeasurement` class can be initialized with the specified COM port, baud rate,
    and NPLC (Number of Power Line Cycles) for voltage measurement.
    """
    voltage_measurement = VoltageMeasurement("COM3", 9600, 1.0)

    assert voltage_measurement.port == "COM3"
    assert voltage_measurement.baud_rate == 9600
    assert voltage_measurement.nplc == 1.0


def test_connect():
    """
    Tests that the `VoltageMeasurement` class can connect to the serial port.
    """
    voltage_measurement = VoltageMeasurement("COM3", 9600, 1.0)
    voltage_measurement.connect()

    assert voltage_measurement.serial_conn.is_open


def test_read_voltage():
    """
    Tests that the `VoltageMeasurement` class can read the voltage measurement from the device.
    """
    voltage_measurement = VoltageMeasurement("COM3", 9600, 1.0)
    voltage_measurement.connect()

    voltage = voltage_measurement.read_voltage()

    assert isinstance(voltage, float)
    assert voltage > 0.0


def test_calculate_statistics():
    """
    Tests that the `VoltageMeasurement` class can calculate statistics for the collected voltage data.
    """
    voltage_measurement = VoltageMeasurement("COM3", 9600, 1.0)
    voltage_measurement.connect()

    voltage_measurement.read_voltage()
    voltage_measurement.read_voltage()

    voltage_measurement.calculate_statistics()

    assert isinstance(voltage_measurement.mean, float)
    assert isinstance(voltage_measurement.median, float)
    assert isinstance(voltage_measurement.mode, float)
    assert isinstance(voltage_measurement.std_dev, float)


def test_close_connection():
    """
    Tests that the `VoltageMeasurement` class can close the serial connection.
    """
    voltage_measurement = VoltageMeasurement("COM3", 9600, 1.0)
    voltage_measurement.connect()
    voltage_measurement.close_connection()

    assert not voltage_measurement.serial_conn.is_open
