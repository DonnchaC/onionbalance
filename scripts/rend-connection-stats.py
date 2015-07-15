# -*- coding: utf-8 -*-
"""
Log information about the number and rate of rendezvous connections to a HS.
"""

import sys
import time
import argparse
import logging
import logging.handlers
import threading

import stem
from stem.control import Controller
import schedule

handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]: %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("onionbalance")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

lock = threading.RLock()

# Track circuits established in current time period.
new_rend_circuits_established = 0
rend_circuits_closed = 0


def circ_event_handler(event):
    """
    Handle the event received when Tor emits an event related the a rendezvous
    circuit
    """
    global new_rend_circuits_established, rend_circuits_closed

    if event.purpose == "HS_SERVICE_REND" and event.hs_state == "HSSR_JOINED":
        if event.type == "CIRC_MINOR":
            # Log when a new rendezvous circuit is successfully established.
            # A CIRC_MINOR event is emitted when the rendezvous circuit moves
            # from HS_STATE=HSSR_CONNECTING to HS_STATE=HSSR_JOINED
            logger.debug("New rendezvous circuit established (CircID: %s)",
                         event.id)
            new_rend_circuits_established += 1

        elif event.type == "CIRC" and event.status == "CLOSED":
            logger.debug("Rendezvous circuit closed (CircID: %s)", event.id)
            rend_circuits_closed += 1
    return


def output_status(controller):
    """
    Output the current counts every tick period.
    """
    global new_rend_circuits_established, rend_circuits_closed

    # Count number of currently established rendezvous circuits for this HS.
    rend_circ_count = len([circ for circ in controller.get_circuits()
                           if circ.purpose == "HS_SERVICE_REND"
                           and circ.hs_state == "HSSR_JOINED"])

    with lock:
        logger.info("New rend circuits: %d - Closed rend circuits: %d - "
                    "Established rend circuits: %d",
                    new_rend_circuits_established,
                    rend_circuits_closed,
                    rend_circ_count)
        new_rend_circuits_established = 0
        rend_circuits_closed = 0

    return None


def parse_cmd_args():
    """
    Parses and returns command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="%s logs stats about Tor rendezvous circuits" %
        sys.argv[0])

    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="Tor controller IP address")

    parser.add_argument("-p", "--port", type=int, default=9051,
                        help="Tor controller port")

    parser.add_argument("-t", "--tick", type=int, default=60,
                        help="Output total every tick seconds "
                        "(default: %(default)s)")

    parser.add_argument("--log-file", type=str, default="rendezvous.log",
                        help="Location to log the rendezvous connection"
                        "data.")

    parser.add_argument("-v", "--verbosity", type=str, default="info",
                        help="Minimum verbosity level for logging.  Available "
                             "in ascending order: debug, info, warning, "
                             "error, critical).  The default is info.")

    return parser.parse_args()


def main():

    args = parse_cmd_args()
    logger.setLevel(logging.__dict__[args.verbosity.upper()])

    if args.log_file:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            args.log_file, when='D')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info("Beginning rendezvous circuit monitoring."
                "Status output every %d seconds", args.tick)

    with Controller.from_port(port=args.port) as controller:
        # Create a connection to the Tor control port
        controller.authenticate()

        # Add event listeners for HS_DESC and HS_DESC_CONTENT
        controller.add_event_listener(circ_event_handler,
                                      stem.control.EventType.CIRC)
        controller.add_event_listener(circ_event_handler,
                                      stem.control.EventType.CIRC_MINOR)

        # Schedule rendezvous status output.
        schedule.every(args.tick).seconds.do(output_status, controller)
        schedule.run_all()

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping rendezvous circuit monitoring.")

    sys.exit(0)

if __name__ == '__main__':
    main()
