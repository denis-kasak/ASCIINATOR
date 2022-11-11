#pragma once

#include <opencv2/opencv.hpp>
#include <vector>
#include <string>

const std::string SkinDir = ".\\res\\charfilter\\";
const std::string TempDir = ".\\temp\\";
const std::string TempFramesOutDir = ".\\temp\\Frames_out\\";
const std::string TempCharDir = ".\\temp\\chars\\";

struct FRAME {
    cv::Mat img;
    int indeximg;
};

class FrameBufferer {
public:
    void AppendFrame(FRAME frame);
    void ManageVideo(int numframes);
    bool videofinished = false;
private:
    
    int wantedindex = 0;
    std::queue<cv::Mat> frames;
    std::mutex queue_mutex;
    std::condition_variable mutex_condition;
    int bufferedframes = 0;
    cv::VideoWriter videowriter;
};

struct CHARLIST {
    float avgimg;
    cv::Mat charimg;
};

struct ASCIIJOB {
    cv::Mat img;
    int indeximg;
    int charsize[2];
    std::vector<CHARLIST> charlist;
    FrameBufferer *fb;
};

struct EDGEJOB {
    cv::Mat img;
    int indeximg;
    int linebgr[3];
    int bgbgr[3];
    int lowThreshold;
    int ratio;
    FrameBufferer* fb;
};



