#!/usr/bin/env python3
from substrateinterface import SubstrateInterface
from pprint import pprint


def hash_by_task(cores):
    """
    Take a QueryMapResult corresponding to core (descriptors|schedules)
    returns a dict with {task_id: assignments, ...}
    """
    tasks = {}
    for core in cores:
        if (current_work := core[1]["current_work"].value) is not None:
            # Get all tasks assignments on this core
            for task_id, descriptor in (
                (a[0]["Task"], a[1])
                for a in current_work["assignments"]
                if "Task" in a[0]
            ):
                tasks.setdefault(task_id, []).append(descriptor)
    return tasks


def find_duplicates(cores):
    """
    Take a QueryMapResult corresponding to core (descriptors|schedules) and return the duplicates
    """
    tasks = hash_by_task(cores)
    return {
        task_id: descriptors
        for task_id, descriptors in tasks.items()
        if len(descriptors) > 1
    }


if __name__ == "__main__":
    RELAY_URL = "wss://rococo-rpc.polkadot.io"
    relay = SubstrateInterface(url=RELAY_URL)

    print("Tasks with multiple cores in the current workload:")
    core_descriptors = relay.query_map("CoretimeAssignmentProvider", "CoreDescriptors")
    current_dupes = find_duplicates(core_descriptors)
    pprint(current_dupes)

    print("Tasks with multiple cores in upcoming workloads:")
    core_schedules = relay.query_map("CoretimeAssignmentProvider", "CoreSchedules")
    future_dupes = find_duplicates(core_schedules)
    pprint(future_dupes)
