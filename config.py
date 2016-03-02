# shows all requests, responses, etc.
DEBUG = True

# maximum number of input connections(from browser)
MAX_CONNECTIONS = 50

# maximum length of received data(in bytes)
MAX_DATA_RECV = 4096

# time, for which we stop listening for new messages from the channel
RECV_TIMEOUT = 0.4

# if true - waiting until receiving full response from the server(Store-and-Forward)
# if false - resending to the browser immediately(cut-through)
STORE_AND_FORWARD = True

# if true - uses list of forbidden words and block pages with such words
FILTERING_MODE = True
