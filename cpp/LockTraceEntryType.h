#pragma once

namespace pearlrt {
    enum class LockTraceEntryType {
        ThreadStart,
        Lock,
        Unlock
    };
}