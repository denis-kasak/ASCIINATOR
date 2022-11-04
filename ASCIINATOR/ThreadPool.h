#pragma once

#include <mutex>
#include <vector>
#include <queue>
#include "asciinator.h"

using namespace std;

//Generated code variant: do not change
class AsciiThreadPool {
public:
    void Start();
    void QueueJob(ASCIIJOB job);
    void Stop();
    bool busy();

private:
    void ThreadLoop();

    bool should_terminate = false;           // Tells threads to stop looking for jobs
    std::mutex queue_mutex;                  // Prevents data races to the job queue
    std::condition_variable mutex_condition; // Allows threads to wait on new jobs or termination 
    std::vector<std::thread> threads;
    std::queue<ASCIIJOB> jobs;
};

//Generated code variant: do not change
class EdgeThreadPool {
public:
    void Start();
    void QueueJob(EDGEJOB job);
    void Stop();
    bool busy();

private:
    void ThreadLoop();

    bool should_terminate = false;           // Tells threads to stop looking for jobs
    std::mutex queue_mutex;                  // Prevents data races to the job queue
    std::condition_variable mutex_condition; // Allows threads to wait on new jobs or termination 
    std::vector<std::thread> threads;
    std::queue<EDGEJOB> jobs;
};

