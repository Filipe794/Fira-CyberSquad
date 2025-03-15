// provavelmente vamos precisar fazer alterações quando for rodar no raspberry, pois o socket.io não vai funcionar
// mas é só pegar o IP dele e colocar no lugar do localhost
// var socket = io.connect('http://192.168.1.100:5000'); -> exemplo de como ficaria

var socket = io();

socket.on('update_data', function (data) {
    // Atualiza os valores dos motores
    document.getElementById("motor1_speed").innerHTML = data.motor_speeds.motor1.toFixed(2);
    document.getElementById("motor2_speed").innerHTML = data.motor_speeds.motor2.toFixed(2);
    document.getElementById("motor3_speed").innerHTML = data.motor_speeds.motor3.toFixed(2);
    document.getElementById("motor4_speed").innerHTML = data.motor_speeds.motor4.toFixed(2);

    // Atualiza os valores dos sensores ToF
    document.getElementById("tof_front").innerHTML = data.tof_distances.tof_front.toFixed(2);
    document.getElementById("tof_left").innerHTML = data.tof_distances.tof_left.toFixed(2);
    document.getElementById("tof_right").innerHTML = data.tof_distances.tof_right.toFixed(2);

    // Atualiza os parâmetros PID dos motores
    document.getElementById('motor1_kp').innerText = data.motor_pid.motor1.Kp;
    document.getElementById('motor1_ki').innerText = data.motor_pid.motor1.Ki;
    document.getElementById('motor1_kd').innerText = data.motor_pid.motor1.Kd;

    document.getElementById('motor2_kp').innerText = data.motor_pid.motor2.Kp;
    document.getElementById('motor2_ki').innerText = data.motor_pid.motor2.Ki;
    document.getElementById('motor2_kd').innerText = data.motor_pid.motor2.Kd;

    document.getElementById('motor3_kp').innerText = data.motor_pid.motor3.Kp;
    document.getElementById('motor3_ki').innerText = data.motor_pid.motor3.Ki;
    document.getElementById('motor3_kd').innerText = data.motor_pid.motor3.Kd;

    document.getElementById('motor4_kp').innerText = data.motor_pid.motor4.Kp;
    document.getElementById('motor4_ki').innerText = data.motor_pid.motor4.Ki;
    document.getElementById('motor4_kd').innerText = data.motor_pid.motor4.Kd;
});
