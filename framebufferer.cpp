#include "framebufferer.h"

using namespace std;

void FrameBufferer::AppendFrame(FRAME frame) {
	bool iswritten = false;
	while (!iswritten) {
		if (frame.indeximg == wantedindex) {
			{
				std::unique_lock<std::mutex> lock(queue_mutex);
				//cv::imwrite(TempFramesOutDir + to_string(frame.indeximg) + ".jpg", frame.img);
				frames.push(frame.img);
				wantedindex++;
				iswritten = true;
			}
		}

	}
}

void FrameBufferer::ManageVideo(int numframes) {
	int processedframes = 0;

	cv::Size framsize(static_cast<int>(1920), static_cast<int>(1080));

	cv::VideoWriter videowriter(".\\output.mp4", cv::VideoWriter::fourcc('M', 'P', '4', 'A'), 30, framsize, true);

	while (processedframes < numframes) {
		if (frames.size() != 0) {
			std::unique_lock<std::mutex> lock(queue_mutex);
			cv::Mat frame = frames.front();
			frames.pop();
			videowriter.write(frame);
			processedframes++;
			std::cout << to_string(100 * processedframes / numframes) + "% fertig\n";
		}		
	}
	videowriter.release();
	videofinished = true;
}