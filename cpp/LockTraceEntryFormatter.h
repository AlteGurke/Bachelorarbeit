#include <string>
#include "LockTraceEntry.h"

namespace pearlrt {
    class LockTraceEntryFormatter {
        private:
            const std::string endMarker = "\\r\\n";
            const std::string emptyReturnValue = "";
            std::string createDateTimeEntry(std::chrono::time_point<std::chrono::system_clock> timePoint);
        public:
            std::string FormatLogTraceEntry(LockTraceEntry& logTraceEntry);
    };
}