import threading
MEMORY = {
    "key"      : ("ABC",None),
    "list_key" : (["a","b","c","d"],None)
}             # schema key ,value , timestamp   if no timestamp set it to None = doesnt expire 

BLOCKED_CLIENTS = {
    #"listKey" : []
              # schema key,[[client connection,locktime],[client connection,locktime]]
}
lock = threading.Lock()  # shared lock