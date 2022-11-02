#pragma once

#include <opencv2/opencv.hpp>

using namespace std;


struct CHARLIST {
	float avgimg;
	cv::Mat charimg;
};

vector<CHARLIST> CreateColor(int [], int [], string, vector<CHARLIST>);
void InitTemp();
void ImageToAscii(cv::Mat, int, int[2], vector<CHARLIST>);