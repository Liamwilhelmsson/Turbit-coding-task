import { useTurbineId } from "@/hooks/useTurbineId";

export const TurbineInput = () => {
    const { turbineId, setTurbineId } = useTurbineId();

    return (
        <div className="flex flex-row items-center gap-3">
            <h1>Turbine ID</h1>
            <input
                type="number"
                value={turbineId}
                onChange={(e) => setTurbineId(e.target.value)}
                className="flex-1 border rounded py-2 px-3 text-gray-800 leading-tight"
            />
        </div>
    );
};
