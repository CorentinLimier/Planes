from logger.logger import Logger


class ProtocolDataUnit():

    def __init__(self, pdu_or_object):
        self.pdu = {}

        Logger.debug("PDU init (%s:%s)", (type(pdu_or_object), pdu_or_object), 'network_protocol')
        if isinstance(pdu_or_object, dict):
            Logger.trace("PDU init from dict", category='network_protocol')
            self.from_dictionary(pdu_or_object)
        else:
            Logger.trace("PDU init from object", category='network_protocol')
            self.from_object(pdu_or_object)

    def from_dictionary(self, dictionary):
        self.pdu = dictionary

    def from_object(self, obj):
        raise NotImplementedError("PDU: from_object")

    def get_object(self):
        raise NotImplementedError("PDU: get_object")

    def get_pdu(self):
        raise NotImplementedError("PDU: get_pdu")

