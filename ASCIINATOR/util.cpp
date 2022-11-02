#include <filesystem>
#include <windows.h>

#include "asciinator.h"

using namespace std;

bool DirExists(const string& dirName_in)
{
	DWORD ftyp = GetFileAttributesA(dirName_in.c_str());
	if (ftyp == INVALID_FILE_ATTRIBUTES)
		return false;  //something is wrong with your path!

	if (ftyp & FILE_ATTRIBUTE_DIRECTORY)
		return true;   // this is a directory!

	return false;    // this is not a directory!
}

void InitDir(string dirpath) {

	if (DirExists(dirpath)) {
		filesystem::remove_all(dirpath);
	}

	filesystem::create_directories(dirpath);

}

void InitTemp() {
	InitDir(".\\temp\\");
	InitDir(".\\temp\\frames_out\\");
	InitDir(".\\temp\\chars\\");
}

