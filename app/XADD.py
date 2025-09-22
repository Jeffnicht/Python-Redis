from customDatatypes import stream
def XADD(clientConnection,command:list):
    stream = stream([
    {"sensor-id": "1", "temperature": "19.8"},
    {"sensor-id": "2", "temperature": "20.1"},
])
    testStream = stream()