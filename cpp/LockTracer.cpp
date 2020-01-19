#include <filesystem>
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>
#include "LockTracer.h"

namespace pearlrt {

    LockTracer::LockTracer() : formatter() {
        isActivated = false;

        char* envVar = std::getenv(NameOfEnvironmentVariableForActivation);
        if(envVar != NULL && strcmp(envVar, "true") == 0) {
            envVar = std::getenv(NameOfEnvironmentVariableFilePath);
            if(envVar != NULL && std::filesystem::exists(envVar)) {
                std::time_t t = std::time(nullptr);
                std::tm tm = *std::localtime(&t);

                std::ostringstream oss;
                oss << std::put_time(&tm, "%Y-%m-%d_%H-%M.log");
                std::string str = oss.str();

                filePath = std::string(envVar) + str;

                SetNumberOfMaxEntries();
                isActivated = true;
            }   
        }
    }

    void LockTracer::SetNumberOfMaxEntries() {
        char* envVar = std::getenv(NameOfEnvironmentVariableNumberOfMaxEntries);
        if(envVar != NULL) {
            try
            {
                numberOfMaxEntries = std::stoi(envVar);
            }
            catch(const std::exception& e)
            {
                numberOfMaxEntries = DefaultNumberOfMaxEntries;
            }
        }
        else {
            numberOfMaxEntries = DefaultNumberOfMaxEntries;
        }
    }

    void LockTracer::flushIfNeeded() {
        if(queue.size_approx() >= numberOfMaxEntries) {
            LockTracer::flush();
        }
    }

    void LockTracer::flush() {
        std::lock_guard lock(flushMutex);
        try
        {
            std::ofstream fileStream;
            fileStream.open(filePath, std::ios_base::app);
            for (int i = 0; i < numberOfMaxEntries; i++)
            {
                LockTraceEntry entry;
                if(queue.try_dequeue(entry)) {
                    fileStream << formatter.FormatLogTraceEntry(entry);
                }
            }
            fileStream.close();
        }
        catch(const std::exception& e)
        {
        }
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

        queue.enqueue(entry);
        LockTracer::flushIfNeeded();
    }
}