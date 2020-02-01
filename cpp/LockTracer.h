#pragma once

#include <mutex>
#include "LockTraceEntry.h"
#include "LockTraceEntryFormatter.h"
#include "concurrentqueue.h"

namespace pearlrt {
    class LockTracer {
        private:
            const char* NameOfEnvironmentVariableEnabled = "OpenPEARL_LockTracer_Enabled";
            const char* NameOfEnvironmentVariablePath = "OpenPEARL_LockTracer_Path";
            const char* NameOfEnvironmentVariableNumberOfMaxEntries = "OpenPEARL_LockTracer_MaxEntries";  
            const unsigned short DefaultNumberOfMaxEntries = 20; 
            bool isEnabled;
            unsigned short numberOfMaxEntries = 20;
            std::string filePath;
            moodycamel::ConcurrentQueue<LockTraceEntry> queue;
            std::mutex flushMutex;
            
            LockTracer();
            bool directoryExists(const char *fileName);
            void setNumberOfMaxEntries();
            void flushIfNeeded();
            void flush();
        public:
            static LockTracer& GetInstance();
            void Add(LockTraceEntry& entry);
            LockTracer(const LockTracer&) = delete;
            LockTracer(LockTracer&&) = delete;
            LockTracer& operator=(const LockTracer&) = delete;
            LockTracer& operator=(LockTracer&&) = delete;
            ~LockTracer();
    };
}