"""EVE domains."""
from .resources import (publications,
                        notices_publications,
                        unpaywall_dump,
                        openapc_dump,
                        opencitations_dump,
                        tasks,
                        scanr)

EVE_DOMAINS = {
    "publications": publications,
    "notices_publications": notices_publications,
    "unpaywall_dump": unpaywall_dump,
    "openapc_dump": openapc_dump,
    "opencitations_dump": opencitations_dump,
    "tasks": tasks,
    "scanr": scanr
}
