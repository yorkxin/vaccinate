# Usage:
# local_scraper.py > output.json

import argparse
import os
import json
from typing import TypedDict, Tuple, Dict, Callable, List, Any, Optional, NewType
from enum import Enum
from hospital_types import (
    AppointmentAvailability,
    ScrapedData,
    HospitalAvailabilitySchema,
)
from dotenv import load_dotenv
import asyncio
import aiohttp
import time
import sys


START_TIME: float = time.time()


# Parsers
from Parsers.ntu import *
from Parsers.tzuchi_taipei import *
from Parsers.changgung_chiayi import *
from Parsers.tzuchi_hualien import *
from Parsers.pch_nantou import *
from Parsers.mohw import *
from Parsers.tonyen_hsinchu import *
from Parsers.siaogang_kaohsiung import *
from Parsers.ncku_tainan import *
from Parsers.kmuh_kaohsiung import *
from Parsers.sanjunzong_penghu import *

def error_boundary(
    f: Callable[[], Coroutine[Any, Any, ScrapedData]]
) -> Callable[[], Coroutine[Any, Any, Optional[ScrapedData]]]:
    async def boundaried_function() -> Optional[ScrapedData]:
        try:
            f_start: float = time.time()
            value = await f()
            print("----%s: %s-----" % (f.__name__, str(time.time() - f_start)), file=sys.stderr)
            return value
        except:
            print("----%s: Unexpected error:" % f.__name__, sys.exc_info()[0], file=sys.stderr)
            return None

    return boundaried_function


PARSERS: List[Callable[[], Coroutine[Any, Any, Optional[ScrapedData]]]] = [
    error_boundary(parse_ntu_taipei),
    error_boundary(parse_ntu_hsinchu),
    error_boundary(parse_ntu_yunlin),
    error_boundary(parse_tzuchi_taipei),
    error_boundary(parse_tzuchi_hualien),
    error_boundary(scrape_changgung_chiayi),
    error_boundary(scrape_pch_nantou),
    error_boundary(parse_mohw_taoyuan),
    error_boundary(parse_mohw_keelung),
    error_boundary(parse_mohw_miaoli),
    error_boundary(parse_mohw_taichung),
    error_boundary(parse_mohw_taitung),
    error_boundary(parse_mohw_kinmen),
    error_boundary(parse_mohw_nantou),
    error_boundary(scrape_tonyen_hsinchu),
    error_boundary(scrape_siaogang_kaohsiung),
    error_boundary(parse_ncku_tainan),
    error_boundary(parse_kmuh_kaohsiung),
    error_boundary(scrape_sanjunzong_penghu),
]


# TODO: make it accepts an id of which site to scrape
async def scrape() -> List[ScrapedData]:
    availability: List[ScrapedData] = list(
        filter(None, list(await asyncio.gather(*[f() for f in PARSERS])))
    )
    as_dict: Dict[int, HospitalAvailabilitySchema] = dict(availability)

    # FIXME: use opaque ID so that we don't limit scrapers up to 32 items.
    for i in range(1, 32):
        if i in as_dict:
            continue
        else:
            as_dict[i] = {
                "self_paid": AppointmentAvailability.NO_DATA,
                "government_paid": AppointmentAvailability.NO_DATA,
            }

    return as_dict

if __name__ == "__main__":
    data = asyncio.run(scrape())
    print(json.dumps(data, indent=2)) # to stdout

    print("--- %s seconds ---" % (time.time() - START_TIME), file=sys.stderr)
