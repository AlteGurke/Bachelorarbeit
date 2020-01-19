#pragma once

#include <string>
#include "LockTraceEntry.h"

namespace pearlrt {
    class LockTraceEntryFormatter {
        private:
            const std::string endMarker = "\r\n";
            const std::string emptyReturnValue = "";
            std::string createDateTimeEntry(std::chrono::time_point<std::chrono::system_clock> timePoint);
            LockTraceEntryFormatter();
        public:
            static LockTraceEntryFormatter& GetInstance();
            std::string FormatLogTraceEntry(LockTraceEntry& logTraceEntry);
            LockTraceEntryFormatter(const LockTraceEntryFormatter&) = delete;
            LockTraceEntryFormatter(LockTraceEntryFormatter&&) = delete;
            LockTraceEntryFormatter& operator=(const LockTraceEntryFormatter&) = delete;
            LockTraceEntryFormatter& operator=(LockTraceEntryFormatter&&) = delete;
    };
}