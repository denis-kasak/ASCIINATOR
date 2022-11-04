//This project is using the C++20 Standard

#include "asciinator.h"
#include <iostream>

using namespace std;




int main(int argc, char** argv)
{
	cv::Mat img = cv::imread("C:\\Users\\d-kas\\Pictures\\Camera Roll\\WIN_20220111_17_14_53_Pro.jpg", cv::IMREAD_COLOR); // Load an image	
	
	int line[] = { 0,255,0 };
	int bg[] = { 0,0,0 };

	FramesToEdge("C:\\Users\\d-kas\\Pictures\\Camera Roll\\WIN_20221020_19_28_55_Pro.mp4", line, bg, 20, 3);

	return 0;
}
