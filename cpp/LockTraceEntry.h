#pragma once

#include <chrono>
#include <string>
#include "LockTraceEntryType.h"

namespace pearlrt {
    class LockTraceEntry
    {
        private:
            std::chrono::time_point<std::chrono::high_resolution_clock> dateTime;
            LockTraceEntryType entryType;
            std::string threadName;
            std::string objectName;
        public:
            std::chrono::time_point<std::chrono::high_resolution_clock> get_DateTime();
            LockTraceEntryType get_EntryType();
            std::string get_ThreadName();
            std::string get_ObjectName();
            LockTraceEntry();
            LockTraceEntry(std::chrono::time_point<std::chrono::high_resolution_clock> dt, LockTraceEntryType et, std::string tn, std::string on);
            LockTraceEntry(const LockTraceEntry&) = delete;
            LockTraceEntry(LockTraceEntry&&) = delete;
            LockTraceEntry& operator=(const LockTraceEntry&) = delete;
            LockTraceEntry& operator=(LockTraceEntry&&) = delete;
    };
}