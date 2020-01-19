#pragma once

#include <chrono>
#include <string>
#include "LockTraceEntryType.h"

namespace pearlrt {
    class LockTraceEntry
    {
        private:
            std::chrono::time_point<std::chrono::system_clock> dateTime;
            LockTraceEntryType entryType;
            unsigned short threadId;
            std::string objectName;
        public:
            std::chrono::time_point<std::chrono::system_clock> get_DateTime();
            LockTraceEntryType get_EntryType();
            unsigned short get_ThreadId();
            std::string get_ObjectName();
            LockTraceEntry();
            LockTraceEntry(std::chrono::time_point<std::chrono::system_clock> dt, LockTraceEntryType et, unsigned short ti, std::string on);
    };
}