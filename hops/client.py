"""
This module provides the `Hops` class, which serves as an interface for
interacting with a Meshtastic network via a TCP connection. The class utilizes
the `pubsub` library to subscribe to various Meshtastic events and provides
callback methods to handle these events, such as connection establishment, data
reception, node updates, position updates, text messages, and user updates.
"""
import logging
from typing import Union
from typing import Optional
from pubsub import pub
import meshtastic
from meshtastic.stream_interface import StreamInterface
from .util import get_or_else
# from .hops import Hops

class Client:
    """
    Meshtastic bot
    """
    def __init__(self, interface: StreamInterface, hops):
        self.interface = interface
        self.hops = hops
        self.me = {}
        self.nodes = {}

        pub.subscribe(self._event_connect,    'meshtastic.connection.established')
        pub.subscribe(self._event_disconnect, 'meshtastic.connection.lost')
        pub.subscribe(self._event_node,       'meshtastic.node')
        pub.subscribe(self._event_text,       'meshtastic.receive.text')
        # pub.subscribe(self._event_position,   'meshtastic.receive.position')
        # pub.subscribe(self._event_data,       'meshtastic.receive.data.portnum')
        # pub.subscribe(self._event_user,       'meshtastic.receive.user')
        # pub.subscribe(self._event_store_forward,       'meshtastic.receive.storeForward')

    def send_text(
        self,
        text: str,
        channel_index: Optional[int],
        destination_id: Optional[Union[int, str]] = meshtastic.BROADCAST_ADDR,
    ):
        """
        Send a message
        """
        
        destination_id = destination_id if destination_id is None else meshtastic.BROADCAST_ADDR
        destination_id = destination_id if channel_index is None else meshtastic.BROADCAST_ADDR

        self.interface.sendText(
            text,
            channelIndex=channel_index if channel_index is not None else 0,
            destinationId=destination_id,
            wantAck=False,
            wantResponse=False,
        )

    def _event_connect(self, interface):
        '''
        Callback function for connection established

        :param interface: Meshtastic interface
        :param topic:     PubSub topic
        '''
        # logging.info(
        #     'Connected to the %s radio on %s hardware',
        #     self.me["user"]["longName"],
        #     self.me["user"]["hwModel"]
        # )
        logging.info('Connected')

    def _event_disconnect(self, interface, topic=pub.AUTO_TOPIC):
        '''
        Callback function for connection lost

        :param interface: Meshtastic interface
        :param topic:     PubSub topic
        '''
        logging.warning('Lost connection to radio!')
        exit()


    def _event_node(self, node):
        '''
        Callback function for node updates

        :param node: Node information
        '''

    def _event_text(self, packet: dict, interface):
        '''
        Callback function for received packets

        :param packet: Packet received
        '''
        sender = get_or_else(packet, ['from'])
        msg = get_or_else(packet, ['decoded', 'payload'], '').decode('utf-8')
        # portnum = get_or_else(packet, ['decoded', 'portnum'])
        # TEXT_MESSAGE_APP
        rx_id = get_or_else(packet, ['id'])
        channel_index = get_or_else(packet, ['channel'], None)

        self.hops.on_message(sender, channel_index, rx_id, msg, self)
