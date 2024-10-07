import { DatePickerWithRange } from "./components/DatePicker";
import { DateRangeProvider } from "./hooks/useDateRange";
import { PowerCurvePlot } from "./components/PowerCurvePlot";
import { TurbineIdProvider } from "./hooks/useTurbineId";
import { TurbineInput } from "./components/TurbineInput";

function App() {
    return (
        <div className="flex flex-col gap-10">
            <DateRangeProvider>
                <TurbineIdProvider>
                    <PowerCurvePlot />
                    <div className="flex flex-row gap-10 justify-center">
                        <TurbineInput />
                        <DatePickerWithRange />
                    </div>
                </TurbineIdProvider>
            </DateRangeProvider>
        </div>
    );
}

export default App;
