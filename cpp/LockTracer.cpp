#include "LockTracer.h"

namespace pearlrt {

    LockTracer::LockTracer() {

    }

    void LockTracer::Add(LockTraceEntry& entry) {
        if(isActivated == false) {
            return;
        }        

        queue.push(entry);
        LockTracer::flushIfNeeded();
    }

    void LockTracer::flushIfNeeded() {
        if(queue.size() >= numberOfMaxEntries) {
            LockTracer::flush();
        }
    }

    void LockTracer::flush() {

    }
}