#pragma once

#include <queue>
#include "LockTraceEntry.h"
#include "LockTraceEntryFormatter.h"

namespace pearlrt {
    class LockTracer {
        private:
            const unsigned short numberOfMaxEntries = 20;
            const char* nameOfEnvironmentVariableForActivation = "OpenPEARL_LockTracer_Enabled";
            const char* nameOfEnvironmentVariableFilePath = "OpenPEARL_LockTracer_Path";
            
            bool isActivated;
            std::string filePath;
            std::queue<LockTraceEntry> queue;
            std::mutex flushMutex;

            LockTraceEntryFormatter formatter;
            
            LockTracer();
            void flushIfNeeded();
            void flush();
        public:
            static LockTracer& GetInstance();
            void Add(LockTraceEntry& entry);
            LockTracer(const LockTracer&) = delete;
            LockTracer(LockTracer&&) = delete;
            LockTracer& operator=(const LockTracer&) = delete;
            LockTracer& operator=(LockTracer&&) = delete;
    };
}