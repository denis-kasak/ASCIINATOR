#include "asciinator.h"
#include "ThreadPool.h"
#include <thread>
#include "framebufferer.h"

using namespace std;

//Generated code variant: do not change
void AsciiThreadPool::Start() {
    const uint32_t num_threads = thread::hardware_concurrency(); // Max # of threads the system supports
    threads.resize(num_threads);
    for (uint32_t i = 0; i < num_threads; i++) {
        threads.at(i) = thread(&AsciiThreadPool::ThreadLoop, this);
    }
}

void AsciiThreadPool::ThreadLoop() {
    while (true) {
        ASCIIJOB job;
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            mutex_condition.wait(lock, [this] {
                return !jobs.empty() || should_terminate;
                });
            if (should_terminate) {
                return;
            }
            job = jobs.front();
            jobs.pop();
        }
        FrameBufferer* fb = job.fb;
        fb->AppendFrame(ImageToAscii(job.img, job.indeximg, job.charsize, job.charlist));
        
    }
}

void AsciiThreadPool::QueueJob(ASCIIJOB job) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        jobs.push(job);
    }
    mutex_condition.notify_one();
}

bool AsciiThreadPool::busy() {
    bool poolbusy;
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        poolbusy = jobs.empty();
    }
    return poolbusy;
}

void AsciiThreadPool::Stop() {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        should_terminate = true;
    }
    mutex_condition.notify_all();
    for (std::thread& active_thread : threads) {
        active_thread.join();
    }
    threads.clear();
}

//Generated code variant: do not change
void EdgeThreadPool::Start() {
    const uint32_t num_threads = thread::hardware_concurrency(); // Max # of threads the system supports
    threads.resize(num_threads);
    for (uint32_t i = 0; i < num_threads; i++) {
        threads.at(i) = thread(&EdgeThreadPool::ThreadLoop, this);
    }
}

void EdgeThreadPool::ThreadLoop() {
    while (true) {
        EDGEJOB job;
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            mutex_condition.wait(lock, [this] {
                return !jobs.empty() || should_terminate;
                });
            if (should_terminate) {
                return;
            }
            job = jobs.front();
            jobs.pop();
        }
        
        FrameBufferer* fb = job.fb;
        fb->AppendFrame(ImageEdgeFilter(job.img, job.indeximg, job.linebgr, job.bgbgr, job.lowThreshold, job.ratio));
    }
}

void EdgeThreadPool::QueueJob(EDGEJOB job) {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        jobs.push(job);
    }
    mutex_condition.notify_one();
}

bool EdgeThreadPool::busy() {
    bool poolbusy;
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        poolbusy = jobs.empty();
    }
    return poolbusy;
}

void EdgeThreadPool::Stop() {
    {
        std::unique_lock<std::mutex> lock(queue_mutex);
        should_terminate = true;
    }
    mutex_condition.notify_all();
    for (std::thread& active_thread : threads) {
        active_thread.join();
    }
    threads.clear();
}