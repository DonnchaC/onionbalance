# -*- coding: utf-8 -*-
import stem

from onionbalance import log
from onionbalance import descriptor

logger = log.get_logger()


class EventHandler(object):

    """
    Handles asynchronous Tor events.
    """

    @staticmethod
    def _new_desc(desc_event):
        """
        Parse HS_DESC response events
        """
        logger.debug("Received new HS_DESC event: %s", str(desc_event))

    @staticmethod
    def _new_desc_content(desc_content_event):
        """
        Parse HS_DESC_CONTENT response events for descriptor content

        Update the HS instance object with the data from the new descriptor.
        """
        logger.debug("Received new HS_DESC_CONTENT event for %s.onion",
                     desc_content_event.address)

        #  Check that the HSDir returned a descriptor that is not empty
        descriptor_text = str(desc_content_event.descriptor).encode('utf-8')
        if len(descriptor_text) < 5:
            logger.debug("Empty descriptor received for %s.onion",
                         desc_content_event.address)
            return None

        # Send content to callback function which will process the descriptor
        descriptor.descriptor_received(descriptor_text)

        return None

    def new_event(self, event):
        """
        Dispatches new Tor controller events to the appropriate handlers.
        """
        if isinstance(event, stem.response.events.HSDescEvent):
            self._new_desc(event)

        elif isinstance(event, stem.response.events.HSDescContentEvent):
            self._new_desc_content(event)

        else:
            logger.warning("Received unexpected event %s.", str(event))
