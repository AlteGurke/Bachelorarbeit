#pragma once

#include "LockTraceEntry.h"
#include "LockTraceEntryFormatter.h"
#include "concurrentqueue.h"

namespace pearlrt {
    class LockTracer {
        private:
            unsigned short numberOfMaxEntries = 20;
            const unsigned short DefaultNumberOfMaxEntries = 20;
            const char* NameOfEnvironmentVariableForActivation = "OpenPEARL_LockTracer_Enabled";
            const char* NameOfEnvironmentVariableFilePath = "OpenPEARL_LockTracer_Path";
            const char* NameOfEnvironmentVariableNumberOfMaxEntries = "OpenPEARL_LockTracer_MaxEntries";            
            bool isActivated;
            std::string filePath;
            moodycamel::ConcurrentQueue<LockTraceEntry> queue;
            std::mutex flushMutex;

            LockTraceEntryFormatter formatter;
            
            LockTracer();
            void SetNumberOfMaxEntries();
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