#include <iostream>
#include <cstdlib>
#include "LockTracer.cpp"
#include "LockTraceEntry.cpp"
#include "LockTraceEntryFormatter.cpp"
using namespace std;

int main() 
{
    cout << "Start" << endl;
    setenv("OpenPEARL_LockTracer_Enabled", "true", true);
    setenv("OpenPEARL_LockTracer_Path", "/Users/marcelsobottka/Downloads/temp/", true);
    setenv("OpenPEARL_LockTracer_MaxEntries", "1", true);    
    cout << "LockTracingEnabled: " << getenv("OpenPEARL_LockTracer_Enabled") << endl;
    cout << "LockTracingPath: " << getenv("OpenPEARL_LockTracer_Path") << endl;
    cout << "NumberOfMaxEntries: " << getenv("OpenPEARL_LockTracer_MaxEntries") << endl << endl;

    pearlrt::LockTracer& logger = pearlrt::LockTracer::GetInstance();

    pearlrt::LockTraceEntry entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::ThreadStart, "0", "1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::ThreadStart, "0", "2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::ThreadStart, "0", "3");
    logger.Add(entry);

    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "1", "L1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "1", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "1", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "1", "L1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "1", "L3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "1", "L3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "1", "L1");
    logger.Add(entry);

    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "2", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "2", "L3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "2", "L1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "2", "L1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "2", "L3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "2", "L2");
    logger.Add(entry);
    
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L5");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L5");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L7");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Lock, "3", "L8");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L8");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L7");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::system_clock::from_time_t(0), pearlrt::LockTraceEntryType::Unlock, "3", "L2");
    logger.Add(entry);

    cout << endl << "End" << endl;

    return 0;
}