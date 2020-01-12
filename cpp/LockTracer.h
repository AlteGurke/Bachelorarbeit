#include <queue>
#include "LockTraceEntry.h"

namespace pearlrt {
    class LockTracer {
        private:
            bool isActivated;
            std::queue<LockTraceEntry> queue;
            const unsigned short numberOfMaxEntries = 20;
            void flushIfNeeded();
            void flush();
        public:
            void Add(LockTraceEntry& entry);
            LockTracer();
    };
}