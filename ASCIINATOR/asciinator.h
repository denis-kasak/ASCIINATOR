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

struct ASCIIJOB {
    cv::Mat img;
    int indeximg;
    int charsize[2];
    vector<CHARLIST> charlist;
};

struct EDGEJOB {
    cv::Mat img;
    int indexnum;
    int linebgr[3];
    int bgbgr[3];
    int lowThreshold;
    int ratio;
};


vector<CHARLIST> CreateColor(const int fontbgr[], const int bgbgr[], const string skinname, vector<CHARLIST> charlist);
void InitTemp();
void ImageToAscii(cv::Mat img, int imgindex, const int charsize[2], vector<CHARLIST> charlist);
void ImageEdgeFilter(cv::Mat img, const int indexnum, const int linebgr[], const int bgbgr[], const int lowThreshold, const int ratio);
void FramesToAscii(const string videopath, const string skinname, int fontbgr[], int bgbgr[]);
void FramesToEdge(const string videopath, int linebgr[], int bgbgr[], int lowThreshold, int ratio);
