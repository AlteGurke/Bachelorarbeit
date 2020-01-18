#include <filesystem>
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>
#include "LockTracer.h"

namespace pearlrt {

    LockTracer::LockTracer() : formatter() {
        isActivated = false;

        char* envVar = std::getenv(nameOfEnvironmentVariableForActivation);
        if(envVar != NULL && strcmp(envVar, "true") == 0) {
            envVar = std::getenv(nameOfEnvironmentVariableFilePath);
            if(envVar != NULL && std::filesystem::exists(envVar)) {
                std::time_t t = std::time(nullptr);
                std::tm tm = *std::localtime(&t);

                std::ostringstream oss;
                oss << std::put_time(&tm, "%Y-%m-%d_%H-%M.log");
                std::string str = oss.str();

                filePath = std::string(envVar) + str;
                isActivated = true;
            }   
        }
    }

    void LockTracer::flushIfNeeded() {
        if(queue.size() >= numberOfMaxEntries) {
            LockTracer::flush();
        }
    }

    void LockTracer::flush() {
        std::ofstream fileStream;
        fileStream.open(filePath, std::ios_base::app);
        for (int i = 0; i < numberOfMaxEntries; i++)
        {
            LockTraceEntry entry = queue.front();
            fileStream << formatter.FormatLogTraceEntry(entry);
            queue.pop();
        }
        fileStream.close();
    }

    LockTracer& LockTracer::GetInstance()
    {
        static LockTracer instance;
        return instance;
    }

    void LockTracer::Add(LockTraceEntry& entry) {
        if(isActivated == false) {
            return;
        }        

        queue.push(entry);
        LockTracer::flushIfNeeded();
    }
}