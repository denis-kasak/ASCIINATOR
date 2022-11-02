#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <chrono>
#include "asciinator.h"

using namespace std;

void ImageToAscii(cv::Mat img, int imgindex, int charsize[2], vector<CHARLIST> charlist) {



	int charh = charsize[0]/2;
	int charw = charsize[1]/2;

	int h = img.size[0];
	int w = img.size[1];

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
	cv::imwrite(".\\temp\\frames_out\\1.jpg", img);
}
