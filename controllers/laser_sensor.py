import board
import adafruit_vl53l0x

# sudo pip3 install adafruit-circuitpython-vl53l0x

# TODO: adicionar suporte aos sensores laterais

class DistanceSensor:
    def __init__(self):
        i2c = board.I2C()  # Usa o barramento I2C
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

    def get_distance(self):
        return self.sensor.range

'''
Exemplo de uso
distance_sensor = DistanceSensor()

while True:
    distance = distance_sensor.get_distance()
    time.sleep(0.1)

'''
