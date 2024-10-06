import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import { useEffect, useState } from "react";

import axios from "axios";
import { useDateRange } from "@/hooks/UseDateRange";
import { useTurbineId } from "@/hooks/useTurbineId";

interface TurbineDataResponse {
    turbine_id: number;
    timestamp: string;
    wind_speed_ms: number;
    power_output_kw: number;
}

interface TurbineDataAverage {
    windSpeedMs: number;
    avgPowerOutputKw: number;
}

const BASE_URL = "http://127.0.0.1:8000"; // Should probably be moved somewhere else

export const PowerCurvePlot = () => {
    const [turbineDataAverage, setTurbineDataAverage] = useState<TurbineDataAverage[]>([]);
    const { dateRange } = useDateRange();
    const { turbineId } = useTurbineId();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get<TurbineDataResponse[]>(
                    `${BASE_URL}/turbine/${turbineId}`,
                    {
                        params: { start_time: dateRange?.from, end_time: dateRange?.to },
                    }
                );
                const averages = getPowerOutputAverages(response.data);
                setTurbineDataAverage(averages);
            } catch (error) {
                console.error("Error during fetch:", error);
            }
        };

        fetchData();
    }, [turbineId, dateRange]);

    const maxWindSpeed = Math.ceil(Math.max(...turbineDataAverage.map((data) => data.windSpeedMs)));
    const maxPowerOutput = Math.ceil(
        Math.max(...turbineDataAverage.map((data) => data.avgPowerOutputKw))
    );

    return (
        <ResponsiveContainer width="100%" height={800}>
            <LineChart
                data={turbineDataAverage}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                    dataKey="windSpeedMs"
                    domain={[0, maxWindSpeed]}
                    ticks={Array.from({ length: maxWindSpeed + 1 }, (_, i) => i)}
                />
                <YAxis
                    label={{ value: "Power Output (kW)", angle: -90, position: "insideLeft" }}
                    allowDataOverflow={true}
                    domain={[0, maxPowerOutput + 100]}
                />
                <Tooltip />
                <Line type="monotone" dataKey="avgPowerOutputKw" stroke="#8884d8" />
            </LineChart>
        </ResponsiveContainer>
    );
};

type GroupedData = Record<number, number[]>;

/**
 * Reduce the data to the average poweroutput per windmill in a format that can be passed to a LineChart.
 * Also sort on windmill speed to get a growing graph
 */
const getPowerOutputAverages = (data: TurbineDataResponse[]) => {
    // Group all poweroutputs to their respective windmill speed
    const windspeedToPoweroutputs = data.reduce<GroupedData>((acc, turbineData) => {
        const wind_speed = turbineData.wind_speed_ms;

        acc[wind_speed] = acc[wind_speed] ?? [];
        acc[wind_speed].push(turbineData.power_output_kw);

        return acc;
    }, {});

    // Create a list with the windmill speed and the respective average power output
    const averagePowerOutputs = Object.keys(windspeedToPoweroutputs).map((windSpeedKey) => {
        const windSpeed = parseFloat(windSpeedKey);
        const powerOutputs = windspeedToPoweroutputs[windSpeed];
        const avgPowerOutput =
            powerOutputs.reduce((sum, value) => sum + value, 0) / powerOutputs.length;

        return {
            windSpeedMs: windSpeed,
            avgPowerOutputKw: Math.round(avgPowerOutput * 100) / 100,
        };
    });

    return averagePowerOutputs.sort((a, b) => a.windSpeedMs - b.windSpeedMs);
};
