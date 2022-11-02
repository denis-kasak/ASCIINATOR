#pragma once

#include <opencv2/opencv.hpp>

using namespace std;

const string SkinDir = ".\\res\\charfilter\\";
const string TempDir = ".\\temp\\";
const string TempFramesOutDir = ".\\temp\\Frames_out\\";
const string TempCharDir = ".\\temp\\chars\\";

struct CHARLIST {
	float avgimg;
	cv::Mat charimg;
};

struct IMG2ASCIIJOB {
    cv::Mat img;
    int indeximg;
    int charsize[2];
    vector<CHARLIST> charlist;
};

vector<CHARLIST> CreateColor(int [], int [], string, vector<CHARLIST>);
void InitTemp();
void ImageToAscii(cv::Mat, int, int[2], vector<CHARLIST>);
void FramesToAscii(string videopath, string skinname, int fontbgr[], int bgbgr[]);

class ThreadPool {
public:
    void Start();
    void QueueJob(IMG2ASCIIJOB job);
    void Stop();
    bool busy();

private:
    void ThreadLoop();

    bool should_terminate = false;           // Tells threads to stop looking for jobs
    std::mutex queue_mutex;                  // Prevents data races to the job queue
    std::condition_variable mutex_condition; // Allows threads to wait on new jobs or termination 
    std::vector<std::thread> threads;
    std::queue<IMG2ASCIIJOB> jobs;
};