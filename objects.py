

class EnumServerState:
    REGISTERING = 0
    BROADCAST_START = 1
    SELLING = 2
    CLOSED = 3


class EnumClientState:
    DISCONNECTED = 0
    CONNECTED = 1
    REGISTERED = 2
    BIDDING = 3
    NOT_BIDDING = 4


class EnumThreadNames:
    REGISTERCLIENT = "RegisterClient"
    LISTENER = "Listener"
    CHECKSTART = "CheckStart"


class EnumCommands:
    # ------------ Client Commands ------------
    REGISTER = "&Register"
    REQUEST = "&Request"
    BID = "&Bid"
    # ------------ Server Commands ------------
    BROADCAST_START = "&StartBidding"
    NEW_ITEM = "&NewItem"
    HIGHEST_BID = "&HighestBid"
    OUTBID = "&OutBid"


