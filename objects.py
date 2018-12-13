

class EnumServerState:
    REGISTERING = 0
    BROADCAST_START = 1
    SELLING = 2
    CLOSED = 3


class EnumClientState:
    DISCONNECTED = 0
    CONNECTED = 1
    REGISTERED = 2
    AUCTION_STARTED = 3
    BIDDING = 4
    NOT_BIDDING = 5


class EnumThreadNames:
    REGISTERCLIENT = "RegisterClient"
    LISTENER = "Listener"
    CHECKSTART = "CheckStart"


class EnumCommands:
    # ------------ Client Commands ------------
    REGISTER = "&Register"
    REQUEST = "&Request"
    BID = "&BidPlaced"
    # ------------ Server Commands ------------
    BROADCAST_START = "&StartBidding"
    NEW_ITEM = "&NewItem"
    BID_RECEIVED = "&BidReceived"
    HIGHEST_BID = "&HighestBid"
    OUTBID = "&OutBid"
    BID_CLOSED = "&BidClosed"


