#!/usr/bin/env python3
from substrateinterface import SubstrateInterface
from pprint import pprint

# Get leases from Kusama to fix the state on the Coretime release.

if __name__ == "__main__":
    RELAY_URL = "wss://rpc-kusama.luckyfriday.io"
    CORETIME_URL = "wss://kusama-coretime-rpc.polkadot.io"

    TIMESLICE_PERIOD = 80
    LP_LENGTH = 604800
    # We're currently in LP37, so the lp_count is on top of this.
    LP_37_START = 22377600

    relay = SubstrateInterface(url=RELAY_URL)
    coretime = SubstrateInterface(url=CORETIME_URL)

    para_lease = []
    # Get leases from relay.
    leases = relay.query_map("Slots", "Leases")
    for [para_id, lps] in leases:
        para_id = para_id.value
        lp_count = len(lps)

        # Filter out system parachains and those with zero leases.
        if lp_count > 0 and para_id >= 2000:
            valid_until = lp_count * LP_LENGTH + LP_37_START
            round_up = 1 if valid_until % TIMESLICE_PERIOD > 0 else 0
            timeslice = valid_until // TIMESLICE_PERIOD + TIMESLICE_PERIOD * round_up
            para_lease.append((para_id, timeslice))

    para_lease.sort()
    print(f"vec!{para_lease}")

    # Sort by timeslice, work out region in which they end. CF Santi's script.
    para_lease.sort(key=lambda x: x[1])
    for (para_id, lease) in para_lease:
        SALE_START = (22793600 + 100800 - 1) // TIMESLICE_PERIOD
        PERIOD_LENGTH = 5040
        # End period rounds up.
        lease_left = lease - SALE_START
        round_up = 1 if lease_left % PERIOD_LENGTH > 0 else 0
        period = lease_left // PERIOD_LENGTH + 1
        # Special bootstrapping case.
        if period == 1: period += 1
        print(f"{para_id} ends in period {period}")
