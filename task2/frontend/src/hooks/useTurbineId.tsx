import { createContext, useContext, useState } from "react";

interface TurbineIdContextType {
    turbineId: string;
    setTurbineId: (turbineId: string) => void;
}

const TurbineIdContext = createContext<TurbineIdContextType | undefined>(undefined);

export const useTurbineId = () => {
    const context = useContext(TurbineIdContext);
    if (context === undefined) {
        throw new Error("useTurbineId must be used within a TurbineIdProvider");
    }
    return context;
};

export const TurbineIdProvider = ({ children }: { children: React.ReactNode }) => {
    const [turbineId, setTurbineId] = useState("");

    return (
        <TurbineIdContext.Provider value={{ turbineId, setTurbineId }}>
            {children}
        </TurbineIdContext.Provider>
    );
};
