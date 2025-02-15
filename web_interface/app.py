from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random

# descomentar quando executar no rasp
# from utils.pid_manager import load_pid_params
# from controllers.laser_sensor import get_distance as get_tof_distance
# from controllers.encoder_reader import get_speed as get_encoder_speed

app = Flask(__name__)
socketio = SocketIO(app)

MOTOR_NAMES = ["motor1", "motor2", "motor3", "motor4"]
TOF_SENSORS = ["tof_front", "tof_left", "tof_right"]


@app.route("/")
def index():
    return render_template("index.html")

# # função original
# def send_sensor_data():
#     while True:
#         motor_speeds = {motor: get_encoder_speed(motor) for motor in MOTOR_NAMES}
#         tof_distances = {sensor: get_tof_distance(sensor) for sensor in TOF_SENSORS}
        
#         motor_pid_values = {}
#         for motor in MOTOR_NAMES:
#             kp, ki, kd = load_pid_params(motor)
#             motor_pid_values[motor] = {"Kp": kp, "Ki": ki, "Kd": kd}

#         data = {
#             "motor_speeds": motor_speeds,
#             "tof_distances": tof_distances,
#             "motor_pid": motor_pid_values,            
#         }
        
#         socketio.emit('update_data', data)
#         time.sleep(0.5)


# Função para simular os dados dos sensores
def simulate_sensor_data():
    motor_speeds = {
        "motor1": round(random.uniform(10, 15), 2),
        "motor2": round(random.uniform(10, 15), 2),
        "motor3": round(random.uniform(10, 15), 2),
        "motor4": round(random.uniform(10, 15), 2),
    }

    tof_distances = {
        "tof_front": round(random.uniform(10, 50), 2),
        "tof_left": round(random.uniform(10, 50), 2),
        "tof_right": round(random.uniform(10, 50), 2),
    }

    motor_pid = {
        "motor1": {"Kp": round(random.uniform(0.5, 2.0), 2), "Ki": round(random.uniform(0.01, 0.2), 2), "Kd": round(random.uniform(0.01, 0.1), 2)},
        "motor2": {"Kp": round(random.uniform(0.5, 2.0), 2), "Ki": round(random.uniform(0.01, 0.2), 2), "Kd": round(random.uniform(0.01, 0.1), 2)},
        "motor3": {"Kp": round(random.uniform(0.5, 2.0), 2), "Ki": round(random.uniform(0.01, 0.2), 2), "Kd": round(random.uniform(0.01, 0.1), 2)},
        "motor4": {"Kp": round(random.uniform(0.5, 2.0), 2), "Ki": round(random.uniform(0.01, 0.2), 2), "Kd": round(random.uniform(0.01, 0.1), 2)},
    }

    return motor_speeds, tof_distances, motor_pid

def send_sensor_data():
    while True:
        motor_speeds, tof_distances, motor_pid = simulate_sensor_data()

        data = {
            "motor_speeds": motor_speeds,
            "tof_distances": tof_distances,
            "motor_pid": motor_pid,
        }

        socketio.emit('update_data', data)
        time.sleep(0.5)
        
        
threading.Thread(target=send_sensor_data, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)