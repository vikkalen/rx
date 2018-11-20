import serial

rate=9600
iface='/dev/ttyUSB0'
poulailler_id = '31'
output_data = ['0'] # ack
#output_data = ['2'] # send conf
#output_data = ['3', '1', '5', '14', '1', '58'] # configure
#output_data = ['4'] # ouvrir
#output_data = ['5'] # fermer

with serial.Serial(iface, rate) as rx:
  while True:
    line = rx.readline()
    print(line.decode())
    data = line.decode().split(';')
    if data:
      id = data[0]
      if id == poulailler_id:
        flag = data[1]
        status = data[7]
        if status == 'OK\r\n' and flag == '1':
          output = str(poulailler_id) + ';' + ';'.join(output_data) + '\r\n'
          print(output)
          rx.write(output.encode())
