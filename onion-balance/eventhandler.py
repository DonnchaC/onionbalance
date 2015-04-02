# -*- coding: utf-8 -*-
import stem

import log
import config

logger = log.get_logger()


class EventHandler(object):

    """
    Handles asynchronous Tor events.
    """

    def __init__(self, controller):

        self.controller = controller

    def new_desc(self, desc_event):
        """
        Parse HS_DESC response events
        """
        logger.debug("Received new HS_DESC event: %s" %
                     str(desc_event))

    def new_desc_content(self, desc_content_event):
        """
        Parse HS_DESC_CONTENT response events for descriptor content

        Update the HS instance object with the data from the new descriptor.
        """
        logger.debug("Received new HS_DESC_CONTENT event for %s" %
                     desc_content_event.address)

        # Make sure the descriptor is not empty
        descriptor_text = str(desc_content_event.descriptor).encode('utf-8')
        if len(descriptor_text) < 5:
            logger.debug("Empty descriptor received for %s" %
                         desc_content_event.address)
            return

        # Find the HS instance for this descriptor
        for service in config.cfg.hidden_services:
            for instance in service.instances:
                if instance.onion_address == desc_content_event.address:
                    instance.update_descriptor(descriptor_text)
                    return

    def new_event(self, event):
        """
        Dispatches new Tor controller events to the appropriate handlers.
        """
        if isinstance(event, stem.response.events.HSDescEvent):
            self.new_desc(event)

        elif isinstance(event, stem.response.events.HSDescContentEvent):
            self.new_desc_content(event)

        else:
            logger.warning("Received unexpected event %s." % str(event))
