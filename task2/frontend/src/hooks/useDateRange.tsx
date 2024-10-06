import { createContext, useContext, useState } from "react";

import { DateRange } from "react-day-picker";
import { addDays } from "date-fns";

interface DateRangeContextType {
    dateRange: DateRange | undefined;
    setDateRange: (dateRange: DateRange) => void;
}

const DateRangeContext = createContext<DateRangeContextType | undefined>(undefined);

export const useDateRange = () => {
    const context = useContext(DateRangeContext);
    if (context === undefined) {
        throw new Error("useDateRange must be used within a DateRangeProvider");
    }
    return context;
};

export const DateRangeProvider = ({ children }: { children: React.ReactNode }) => {
    const [dateRange, setDateRange] = useState<DateRange>({
        from: new Date(2016, 0, 1),
        to: addDays(new Date(2016, 0, 1), 30),
    });

    return (
        <DateRangeContext.Provider value={{ dateRange, setDateRange }}>
            {children}
        </DateRangeContext.Provider>
    );
};
