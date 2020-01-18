#include <iostream>
#include <cstdlib>
#include "LockTracer.cpp"
#include "LockTraceEntry.cpp"
#include "LockTraceEntryFormatter.cpp"
using namespace std;
using namespace pearlrt;

int main() 
{
    cout << "Start" << endl;
    setenv("OpenPEARL_LockTracer_Enabled", "true", true);
    setenv("OpenPEARL_LockTracer_Path", "/Users/marcelsobottka/Downloads/temp/", true);
    cout << "LockTracingEnabled: " << getenv("OpenPEARL_LockTracer_Enabled") << endl;
    cout << "LockTracingPath: " << getenv("OpenPEARL_LockTracer_Path") << endl << endl;

    LockTracer logger = LockTracer::GetInstance();

    LockTraceEntry entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::ThreadStart, 0, "1");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::ThreadStart, 0, "2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::ThreadStart, 0, "3");
    logger.Add(entry);

    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 1, "L1");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 1, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 1, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 1, "L1");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 1, "L3");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 1, "L3");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 1, "L1");
    logger.Add(entry);

    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 2, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 2, "L3");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 2, "L1");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 2, "L1");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 2, "L3");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 2, "L2");
    logger.Add(entry);
    
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L5");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L6");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L6");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L5");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L2");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L7");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Lock, 3, "L8");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L8");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L7");
    logger.Add(entry);
    entry = LockTraceEntry(std::chrono::system_clock::from_time_t(0), LockTraceEntryType::Unlock, 3, "L2");
    logger.Add(entry);

    cout << endl << "End" << endl;

    return 0;
}