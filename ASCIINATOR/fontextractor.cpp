#include <filesystem>

#include "asciinator.h"


using namespace std;



bool compareAvg(const CHARLIST& a, const CHARLIST& b) {
	return a.avgimg < b.avgimg;
}

vector<CHARLIST> CreateColor(const int fontbgr[], const int bgbgr[], const string skinname, vector<CHARLIST> charlist) {

	string skindir = SkinDir + skinname + "\\";

	filesystem::path charpath{ skindir };

	auto d = filesystem::directory_iterator(charpath);

	int count = distance(filesystem::begin(d),filesystem::end(d));

	charlist.resize(count);

	int index = 0;

	for (const auto& entry : filesystem::directory_iterator(charpath)) {
		const auto filenameStr = entry.path().filename().string();
		if (entry.is_regular_file()) {

			string path = skindir + filenameStr;

			cv::Mat charimg = cv::imread(path);
			int h = charimg.rows;
			int w = charimg.cols;

			float avgimg = 0;

			for (int y = 0; y < h; y++) {
				for (int x = 0; x < w; x++) {

					avgimg += charimg.ptr(y, x)[0]; //add only value of one channel because img is greyscale

					int ifontopac = charimg.ptr(y, x)[0];
					int ibgopac = 255 - ifontopac;

					float fontopac = (float)ifontopac / 256;
					float bgopac = (float)ibgopac / 256;

					cv::Vec3b& pixel = charimg.at<cv::Vec3b>(y, x);
					pixel.val[0] = (int)(fontbgr[0] * fontopac + bgbgr[0] * bgopac);
					pixel.val[1] = (int)(fontbgr[1] * fontopac + bgbgr[1] * bgopac);
					pixel.val[2] = (int)(fontbgr[2] * fontopac + bgbgr[2] * bgopac);
				}
			}

			avgimg = avgimg / (h * w);

			charlist.at(index).avgimg = avgimg;
			charlist.at(index).charimg = charimg;



			path = TempCharDir + to_string(index) + ".jpg";
			cv::imwrite(path, charimg);
			index++;
		}
	}

	sort(charlist.begin(), charlist.end(), compareAvg);

	for (int i = 1; i < charlist.size() - 1; i++) {
		if (abs(charlist.at(i).avgimg - charlist.at(i - 1).avgimg) < 0.0001) {
			charlist.erase(charlist.begin() + i - 1);
			i--;
			count--;
		}
	}

	float min = charlist.at(0).avgimg;

	float max = charlist.at(count - 1).avgimg;



	for (int i = 0; i < count; i++) {
		charlist.at(i).avgimg = ((charlist.at(i).avgimg - min) / max) * 256;
	}
	return charlist;
}
