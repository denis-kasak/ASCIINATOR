#pragma once

#include "config.h"
#include "framebufferer.h"

std::vector<CHARLIST> CreateColor(const int fontbgr[], const int bgbgr[], const std::string skinname, std::vector<CHARLIST> charlist);
void InitTemp();
FRAME ImageToAscii(cv::Mat img, int imgindex, const int charsize[2], std::vector<CHARLIST> charlist);
FRAME ImageEdgeFilter(cv::Mat img, const int indexnum, const int linebgr[], const int bgbgr[], const int lowThreshold, const int ratio);
void FramesToAscii(const std::string videopath, const std::string skinname, int fontbgr[], int bgbgr[]);
void FramesToEdge(const std::string videopath, int linebgr[], int bgbgr[], int lowThreshold, int ratio);
