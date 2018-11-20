import os, serial, time, datetime, threading, requests

rate = 9600
iface = os.getenv('RX_IFACE', '/dev/ttyUSB0')
debug = os.getenv('RX_DEBUG') == '1'
timeout = float(os.getenv('RX_TIMEOUT', 2))

def receive(input):
  output = []
  status = input.pop()
  if status == 'OK\r\n':
    id = input[0]
    url = os.getenv('RX_URL_' + id)
    token = os.getenv('RX_TOKEN_' + id)
    if url:
      output = forward(url, input, token)

  return output

def forward(url, input, token):
  headers = {'X-Thermo-Token' : token}
  output = []
  try:
    r = requests.post(url = url, json = {'data': input}, headers = headers, timeout = timeout)
    if (r.status_code == requests.codes.ok):
      data = r.json()
      if data:
        output = data['data']
  except Exception as e:
    print(e)

  return output

class dataDigest (threading.Thread):
    def __init__(self, data):
      threading.Thread.__init__(self)
      self.data = data
    def run(self):
      output = receive(data)
      if output:
        output_str = ';'.join(output) + '\r\n'
        if debug:
          print(datetime.datetime.now(), end='')
          print(' - ' + output_str, end='')
        rx.write(output_str.encode())

while True:
  try:
    with serial.Serial(iface, rate) as rx:
      while True:
        data = []
        line = rx.readline()
        if debug:
            print(datetime.datetime.now(), end='')
            print(' - ' + line.decode(), end='')
        data = line.decode().split(';')
        if data:
          digest = dataDigest(data)
          digest.start()
  except serial.serialutil.SerialException as e:
    print(e)
    time.sleep(30)
