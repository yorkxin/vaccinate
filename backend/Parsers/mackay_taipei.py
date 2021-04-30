from typing import Tuple
import requests
from bs4 import BeautifulSoup
from hospital_types import HospitalID, AppointmentAvailability


def parseMackayTaipei() -> Tuple[HospitalID, AppointmentAvailability]:
    r = requests.get(
        "https://www.mmh.org.tw/register_single_doctor.php?depid=75&drcode=O75D",
        verify="../data/mmh-org-tw.pem",
        timeout=2,
    )
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"class": 'logn-table'})
    links = table.find_all("a")
    # PEP8 Style: if list is not empty, then there are appointments
    return (
        2,
        AppointmentAvailability.AVAILABLE
        if bool(links)
        else AppointmentAvailability.UNAVAILABLE,
    )
