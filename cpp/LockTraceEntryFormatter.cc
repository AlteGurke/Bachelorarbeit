#include "LockTraceEntryFormatter.h"

namespace pearlrt {

    using namespace std::chrono;
    using namespace std;

    LockTraceEntryFormatter::LockTraceEntryFormatter() {
    }

    std::string LockTraceEntryFormatter::FormatLockTraceEntry(LockTraceEntry& logTraceEntry) {
        
        std::string prefix = "";
        switch (logTraceEntry.get_EntryType())
        {
            case LockTraceEntryType::Lock:
                prefix = "l";
                break;
            case LockTraceEntryType::Unlock:
                prefix = "u";
                break;
            default:
                return emptyReturnValue;
        }

        return LockTraceEntryFormatter::createDateTimeEntry(logTraceEntry.get_DateTime())
        + prefix + "(" + logTraceEntry.get_ThreadName() + "," + logTraceEntry.get_ObjectName() + ")"
        + endMarker;
    }

    std::string LockTraceEntryFormatter::createDateTimeEntry(std::chrono::time_point<std::chrono::high_resolution_clock> timePoint) {
        return std::to_string(std::chrono::time_point_cast<std::chrono::microseconds>(timePoint).time_since_epoch().count()) + ":";
    }

    LockTraceEntryFormatter& LockTraceEntryFormatter::GetInstance()
    {
        static LockTraceEntryFormatter instance;
        return instance;
    }
}