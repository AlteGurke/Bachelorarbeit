#include "LockTraceEntry.h"

namespace pearlrt {

    LockTraceEntry::LockTraceEntry() {
    }

    LockTraceEntry::LockTraceEntry(std::chrono::time_point<std::chrono::high_resolution_clock> dt, LockTraceEntryType et, std::string tn, std::string on){
        dateTime = dt;
        entryType = et;
        threadName = tn;
        objectName = on;
    }

    std::chrono::time_point<std::chrono::high_resolution_clock> LockTraceEntry::get_DateTime() {
        return dateTime;
    }

    LockTraceEntryType LockTraceEntry::get_EntryType() {
        return entryType;
    }

    std::string LockTraceEntry::get_ThreadName() {
        return threadName;
    }

    std::string LockTraceEntry::get_ObjectName() {
        return objectName;
    }
}