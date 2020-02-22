#include <iostream>
#include <cstdlib>
#include "LockTracer.cc"
#include "LockTraceEntry.cc"
#include "LockTraceEntryFormatter.cc"
using namespace std;

int main() 
{
    cout << "Start" << endl;
    setenv("OpenPEARL_LockTracer_Enabled", "true", true);
    setenv("OpenPEARL_LockTracer_Path", "/Users/marcelsobottka/Downloads/temp/", true);
    setenv("OpenPEARL_LockTracer_MaxEntries", "100", true);    
    cout << "LockTracingEnabled: " << getenv("OpenPEARL_LockTracer_Enabled") << endl;
    cout << "LockTracingPath: " << getenv("OpenPEARL_LockTracer_Path") << endl;
    cout << "NumberOfMaxEntries: " << getenv("OpenPEARL_LockTracer_MaxEntries") << endl << endl;

    pearlrt::LockTracer& logger = pearlrt::LockTracer::GetInstance();

    pearlrt::LockTraceEntry entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::ThreadStart, "0", "1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::ThreadStart, "0", "2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::ThreadStart, "0", "3");
    logger.Add(entry);

    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l7");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l3");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "1", "l7");
    logger.Add(entry);

    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l2");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l8");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l9");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l9");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l8");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l1");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "2", "l6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "2", "l1");
    logger.Add(entry);
    
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l5");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l5");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l7");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l7");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l6");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l5");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Lock, "3", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l4");
    logger.Add(entry);
    entry = pearlrt::LockTraceEntry(std::chrono::high_resolution_clock::now(), pearlrt::LockTraceEntryType::Unlock, "3", "l5");
    logger.Add(entry);

    cout << endl << "End" << endl;

    return 0;
}