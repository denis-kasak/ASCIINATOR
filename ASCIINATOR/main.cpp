#include "asciinator.h"

using namespace std;


int main(int argc, char* argv[]) {

	InitTemp();

	int fontbgr[] = { 255,255,255 };
	int bgbgr[] = { 0,0,0 };
	string str_charpath = ".\\res\\charfilter\\tastatur\\";

	vector<CHARLIST> charlist;

	charlist = CreateColor(fontbgr, bgbgr, str_charpath, charlist);

	int charsize[] = {charlist.at(0).charimg.rows, charlist.at(0).charimg.cols};

	std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
	
	ImageToAscii(cv::imread("C:\\Users\\d-kas\\Pictures\\Camera Roll\\WIN_20221016_16_56_17_Pro.jpg"), 0, charsize, charlist);
	std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

	cout << chrono::duration_cast<chrono::milliseconds>(end - begin).count();
	return 0;
}
