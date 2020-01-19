#include "LockTraceEntry.h"

namespace pearlrt {

    LockTraceEntry::LockTraceEntry() {
    }

    LockTraceEntry::LockTraceEntry(std::chrono::time_point<std::chrono::system_clock> dt, LockTraceEntryType et, unsigned short ti, std::string on){
        dateTime = dt;
        entryType = et;
        threadId = ti;
        objectName = on;
    }

    std::chrono::time_point<std::chrono::system_clock> LockTraceEntry::get_DateTime() {
        return dateTime;
    }

    LockTraceEntryType LockTraceEntry::get_EntryType() {
        return entryType;
    }

    unsigned short LockTraceEntry::get_ThreadId() {
        return threadId;
    }

    std::string LockTraceEntry::get_ObjectName() {
        return objectName;
    }
}