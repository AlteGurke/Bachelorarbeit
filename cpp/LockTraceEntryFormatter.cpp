#include "LockTraceEntryFormatter.h"
#include "date.h"

namespace pearlrt {

    using namespace date;
    using namespace std::chrono;
    using namespace std;

    LockTraceEntryFormatter::LockTraceEntryFormatter() {
    }

    std::string LockTraceEntryFormatter::FormatLogTraceEntry(LockTraceEntry& logTraceEntry) {
        
        std::string prefix = "";
        switch (logTraceEntry.get_EntryType())
        {
            case LockTraceEntryType::ThreadStart:
                prefix = "s";
                break;
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
        + prefix + "(" + std::to_string(logTraceEntry.get_ThreadId()) + "," + logTraceEntry.get_ObjectName() + ")"
        + endMarker;
    }

    std::string LockTraceEntryFormatter::createDateTimeEntry(std::chrono::time_point<std::chrono::system_clock> timePoint) {
        return date::format("%F %T", date::floor<milliseconds>(timePoint)) + ":";
    }

    LockTraceEntryFormatter& LockTraceEntryFormatter::GetInstance()
    {
        static LockTraceEntryFormatter instance;
        return instance;
    }
}