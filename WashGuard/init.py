import socket

broker_ip = str(socket.gethostbyname('broker.hivemq.com'))
broker_port = '1883'
username = ''  # if not needed - delete
password = ''  # if not needed - delete
conn_time = 0  # 0 stands for endless

Machine_ID = "Machine_31"  # will be different in every Machine
topic = "AA_WashGuard/Machine/" + Machine_ID
relay_topic = topic + "/relay"
WT_topic = topic + "/WT"
ED_topic = topic + "/ED"

db_init =  False   #False # True if need reinit
db_name = 'Machinedata_31-2025.db' # SQLite