#include "asciinator.h"

using namespace std;


int main(int argc, char* argv[]) {

	int fontbgr[] = { 0,255,0 };
	int bgbgr[] = { 0,0,0 };
	string videopath = "";
	string skinname = "";

	FramesToAscii(videopath, skinname, fontbgr, bgbgr);
	
	return 0;
}
