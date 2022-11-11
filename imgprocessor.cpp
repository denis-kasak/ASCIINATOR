#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <chrono>
#include "asciinator.h"
#include "ThreadPool.h"
#include "framebufferer.h"

using namespace std;

void FramesToAscii(const string videopath, const string skinname, int fontbgr[], int bgbgr[]) {
	InitTemp();

	vector<CHARLIST> charlist = CreateColor(fontbgr, bgbgr, skinname, charlist);
	const int charsize[2] = { charlist.at(0).charimg.rows, charlist.at(0).charimg.cols }; // charsize = {height,width}

	cv::VideoCapture cap(videopath);

	cv::Mat frame;
	int indeximg = 0;

	AsciiThreadPool* tp = new AsciiThreadPool();
	tp->Start();

	FrameBufferer* fb = new FrameBufferer();
	std::thread tfb(&FrameBufferer::ManageVideo,fb, cap.get(cv::CAP_PROP_FRAME_COUNT));

	

	while (true) {
		cv::Mat frame;
		// Capture frame-by-frame
		cap >> frame;



		// If the frame is empty, break immediately
		if (frame.empty()) {
			break;
		}
		else {
			ASCIIJOB job;
			job.img = frame;
			job.indeximg = indeximg;
			job.charsize[0] = charsize[0];
			job.charsize[1] = charsize[1];
			job.charlist = charlist;
			job.fb = fb;
			tp->QueueJob(job);
			indeximg++;
		}
	}
	cap.release();
	while (!tp->busy()) {

	}
	tp->Stop();
	delete tp;

	while (!fb->videofinished) {

	}
	tfb.join();
	delete fb;
}

FRAME ImageToAscii(cv::Mat img, int imgindex, const int charsize[2], vector<CHARLIST> charlist) {

	int charh = charsize[0]/4;
	int charw = charsize[1]/4;

	int h = img.size[0];
	int w = img.size[1];

	cv::blur(img, img, cv::Size(3, 3));

	cv::cvtColor(img, img, cv::COLOR_BGR2GRAY);
	cv::cvtColor(img, img, cv::COLOR_GRAY2BGR);

	for (int y = 0; y < h; y += charh) {
		for (int x = 0; x < w; x += charw) {

			int roiheight = charh;
			int roiwidth = charw;

			if (h - y < charh) {
				roiheight = h - y;
			}
			if (w - x < charw) {
				roiwidth = w - x;
			}
			cv::Rect roi(x, y, roiwidth, roiheight);
			cv::Scalar sum = cv::sum(img(roi));

			float roiavg = (float)sum[0] / (float)(charw * charh);

			int closestindex = 0;
			for (int i = 1; i < charlist.size(); i++) {
				float charavg = charlist.at(i).avgimg;

				if (abs(roiavg - charavg) < abs(roiavg - charlist.at(closestindex).avgimg)) {
					closestindex = i;
				}
				else {
					break;
				}
			}
			cv::Mat charimg = charlist.at(closestindex).charimg;
			cv::resize(charimg, charimg, cv::Size(roiwidth, roiheight));
			charimg.copyTo(img(roi));

		}
	}
	FRAME frame;
	frame.img = img;
	frame.indeximg = imgindex;
	return frame;
}

void FramesToEdge(const string videopath, int linebgr[], int bgbgr[], int lowThreshold=100, int ratio=3) {
	InitTemp();

	cv::VideoCapture cap(videopath);

	cv::Mat frame;
	int indexnum = 0;

	EdgeThreadPool* tp = new EdgeThreadPool();
	tp->Start();

	FrameBufferer* fb = new FrameBufferer();
	std::thread tfb(&FrameBufferer::ManageVideo, fb, cap.get(cv::CAP_PROP_FRAME_COUNT));

	while (true) {
		cv::Mat frame;
		// Capture frame-by-frame
		cap >> frame;



		// If the frame is empty, break immediately
		if (frame.empty()) {
			break;
		}
		else {
			EDGEJOB job;
			job.img = frame;
			job.indeximg = indexnum;
			job.linebgr[0] = linebgr[0];
			job.linebgr[1] = linebgr[1];
			job.linebgr[2] = linebgr[2];
			job.bgbgr[0] = bgbgr[0];
			job.bgbgr[1] = bgbgr[1];
			job.bgbgr[2] = bgbgr[2];
			job.lowThreshold = lowThreshold;
			job.ratio = ratio;
			job.fb = fb;
			tp->QueueJob(job);
			indexnum++;
		}
	}
	cap.release();
	while (!tp->busy()) {

	}
	tp->Stop();
	delete tp;

	while (!fb->videofinished) {

	}
	tfb.join();
	delete fb;
}


FRAME ImageEdgeFilter(cv::Mat img, const int imgindex, const int linebgr[], const int bgbgr[], const int lowThreshold, const int ratio) {

	cv::cvtColor(img, img, cv::COLOR_BGR2GRAY);

	cv::blur(img, img, cv::Size(3, 3));
	cv::Canny(img, img, lowThreshold, lowThreshold * ratio, 3);

	const int h = img.size[0];
	const int w = img.size[1];

	cv::cvtColor(img, img, cv::COLOR_GRAY2BGR);
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {


			if (img.at<cv::Vec3b>(y, x)[0] == 255) {
				img.at<cv::Vec3b>(y, x)[0] = linebgr[0];
				img.at<cv::Vec3b>(y, x)[1] = linebgr[1];
				img.at<cv::Vec3b>(y, x)[2] = linebgr[2];
			}
			else {
				img.at<cv::Vec3b>(y, x)[0] = bgbgr[0];
				img.at<cv::Vec3b>(y, x)[1] = bgbgr[1];
				img.at<cv::Vec3b>(y, x)[2] = bgbgr[2];
			}

		}
	}


	FRAME frame;
	frame.img = img;
	frame.indeximg = imgindex;
	return frame;

}
