import { PowerCurvePlot } from "./components/CurvePlot";
import { useState } from "react";

function App() {
    const [turbineId, setTurbineId] = useState(1);
    const [startTime, setStartTime] = useState("2016-01-01");
    const [endTime, setEndTime] = useState("2016-12-30");

    return <PowerCurvePlot turbineId={turbineId} startTime={startTime} endTime={endTime} />;
}

export default App;
