// @flow
import * as React from 'react';
import { useTranslation } from 'react-i18next';
import Content from '../Components/Content';
import Map from '../Components/Map';
import VaccineDataGrid from '../Components/VaccineDataGrid';
import Spinner from '../Components/Spinner';

export default function Home(): React.Node {
  const [hospitals, setHospitals] = React.useState([]);
  const [availabilities, setAvailabilities] = React.useState({});
  const [vaccineType, setVaccineType] = React.useState('GovernmentPaid');
  const [gt] = useTranslation('app');
  const hospitalsPath = '/data/hospitals.csv.json';
  const availabilitiesPath = '/data/scraped/availabilities.json';

  React.useEffect(() => {
    fetch(hospitalsPath).then((data) => data.json()).then((res) => setHospitals(res));
    fetch(availabilitiesPath).then((data) => data.json()).then((res) => setAvailabilities(res));
  }, []); // Empty list makes this useEffect similar to componentDidMount();

  return (
    <>
      <div className="row" style={{ marginTop: 50 }}>
        <div className="col">
          <Content />
        </div>
        <div className="col d-none d-md-block">
          <Map />
        </div>
      </div>
      <h2 style={{ textAlign: 'center' }}>{ gt('txt-vaccineAvailability') }</h2>
      {hospitals.length === 0 ? <Spinner />
        : (
          <>
            <div style={{ textAlign: 'center' }}>
              <form
                className="btn-group"
                role="group"
                aria-label="Select type of vaccination."
              >
                {/* eslint-disable jsx-a11y/label-has-associated-control */}
                <input
                  type="radio"
                  className="btn-check"
                  name="btnradio"
                  id="btnradio1"
                  autoComplete="off"
                  onClick={() => setVaccineType('SelfPaid')}
                  checked={vaccineType === 'SelfPaid'}
                />
                <label
                  className="btn btn-outline-primary"
                  htmlFor="btnradio1"
                >
                  { gt('txt-selfPaidVaccine') }
                </label>
                <input
                  type="radio"
                  className="btn-check"
                  name="btnradio"
                  id="btnradio2"
                  autoComplete="off"
                  onClick={() => setVaccineType('GovernmentPaid')}
                  checked={vaccineType === 'GovernmentPaid'}
                />
                <label
                  className="btn btn-outline-primary"
                  htmlFor="btnradio2"
                >
                  { gt('txt-governmentPaidVaccine') }
                </label>
              </form>
            </div>
            <VaccineDataGrid
              vaccineType={vaccineType}
              hospitals={hospitals}
              availabilities={availabilities}
            />
          </>
        )}
    </>
  );
}
