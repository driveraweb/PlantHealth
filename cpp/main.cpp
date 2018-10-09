#include <opencv2/opencv.hpp>
//#include <ctime>
#include <chrono>

#include <string>
#include <fstream>
#include <iostream>
#include <unistd.h>
using namespace cv;
using namespace std;

Mat cmap(256, 1, CV_8UC3);
Mat img_ndvi;

/****  ****/
void img_from_file(void) {
    const string &r_fpath = "/home/derrick/PlantHealth/planthealth/tests/Images/RGB.png";
    const string &nir_fpath = "/home/derrick/PlantHealth/planthealth/tests/Images/NGB.png";
    Mat img_NIR = imread(nir_fpath);
    Mat img_R = imread(r_fpath);
}

/****  ****/
void img_from_buffer(void) {

}

/****  ****/
void init(void) {
    int R = 0;
    int G = 0;
    int B = 0;
    int idx = 0;
    string line;
    ifstream myfile;
    const char* f = "/home/derrick/PlantHealth/planthealth/cmap.csv";
    myfile.open(f);

    if (myfile)
        while (getline(myfile, line)) {
            string substr;
            string acc = "";
            int commas = 0;
            for (uint i = 0; i < line.size()+1; i++) {
                if (i == line.size()) {
                    B = stoi(substr);
                    commas=0;
                } else if (line[i] == ',' || line[i] == '\n') {
                    switch (commas) {
                        case 0:
                            R = stoi(substr);
                            commas++;
                            break;
                        case 1:
                            G = stoi(substr);
                            commas++;
                            break;
                        default:
                            break;
                    }
                    substr="";
                }else
                    substr += line[i];
            }

            //cout << B << '\t' << G << '\t' << R << endl;

            cmap.at<Vec3b>(idx).val[0] = B;
            cmap.at<Vec3b>(idx).val[1] = G;
            cmap.at<Vec3b>(idx).val[2] = R;

            idx++;
        }
    else
        cout << "Not myfile" << endl;
    myfile.close();
    //cout << ::cmap << "  I'm in init" <<endl;

}

void timer_test(void) {
    chrono::high_resolution_clock::time_point t1 = chrono::high_resolution_clock::now();
    sleep(3);
    chrono::high_resolution_clock::time_point t2 = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(t2-t1).count();

    cout << "Sleeping for 3s results with time:  " << duration << "ms" << endl;

}

/****  ****/
Mat& color_map(const Mat& img_NIR, const Mat& img_R) {
    //const string& out_fpath = "NDVI.png";
    //img_ndvi = img_R.clone();
    Mat ndvi(img_R.rows, img_R.cols, CV_32FC1);
    float red;
    float nir;
    int idx;

    for(int r=0; r < img_R.rows; r++) {
        for (int c=0; c < img_R.cols; c++) {
            red = (float) (img_R.at<Vec3b>(r,c).val[2]);
            nir = (float) (img_NIR.at<Vec3b>(r,c).val[2]);
            ndvi.at<Vec3b>(r,c) = (int) (((nir-red)/(nir+red)+1.0)*128.0);

            idx = (int) ndvi.at<Vec3b>(r,c)[0];
            img_ndvi.at<Vec3b>(r,c).val[0] = (int)::cmap.at<Vec3b>(255-idx).val[0];
            img_ndvi.at<Vec3b>(r,c).val[1] = (int)::cmap.at<Vec3b>(255-idx).val[1];
            img_ndvi.at<Vec3b>(r,c).val[2] = (int)::cmap.at<Vec3b>(255-idx).val[2];
        }
    }
    return img_ndvi;
}

void ndvi_map(const Mat& img_NIR, const Mat& img_R) {
    //const string& out_fpath = "NDVI.png";
    //img_ndvi = img_R.clone();
    uint idx;
    float red;
    float nir;

    for(int r=0; r < img_R.rows; r++) {
        for (int c=0; c < img_R.cols; c++) {
            red = (float) (img_R.at<Vec3b>(r,c).val[2]);
            nir = (float) (img_NIR.at<Vec3b>(r,c).val[2]);
            idx = 255 - (int) (((nir-red)/(nir+red)+1.0)*128);

            img_ndvi.at<Vec3b>(r,c).val[0] = (int)::cmap.at<Vec3b>(idx).val[0];
            img_ndvi.at<Vec3b>(r,c).val[1] = (int)::cmap.at<Vec3b>(idx).val[1];
            img_ndvi.at<Vec3b>(r,c).val[2] = (int)::cmap.at<Vec3b>(idx).val[2];
        }
    }

    //return img_ndvi;
}

/********************************* MAIN *********************************/

int main(void) {

    init();

    /* How long to open image files */ /*
    chrono::high_resolution_clock::time_point t1 = chrono::high_resolution_clock::now();
    img_from_file();
    chrono::high_resolution_clock::time_point t2 = chrono::high_resolution_clock::now();
    auto secs = chrono::duration_cast<chrono::milliseconds>(t2-t1).count();
    cout << "Time to open image files:  " << secs << "s" << endl;
    /**/


    const string &r_fpath = "/home/derrick/PlantHealth/planthealth/tests/Images/RGB.png";
    const string &nir_fpath = "/home/derrick/PlantHealth/planthealth/tests/Images/NGB.png";
    Mat img_NIR = imread(nir_fpath, CV_LOAD_IMAGE_COLOR);
    Mat img_R = imread(r_fpath, CV_LOAD_IMAGE_COLOR);
    img_ndvi = img_R.clone();
    Mat splitChannels[3];
    split(img_NIR, splitChannels);
    Mat NIR = splitChannels[2];
    split(img_R, splitChannels);
    Mat R = splitChannels[2];

    /* How long to NDVI map using LUT ----need to change to NIR and R paramters and operations in function */ /*
    chrono::high_resolution_clock::time_point t1 = chrono::high_resolution_clock::now();
    ndvi_map(NIR, R);
    chrono::high_resolution_clock::time_point t2 = chrono::high_resolution_clock::now();
    auto secs = chrono::duration_cast<chrono::milliseconds>(t2-t1).count();
    cout << "Time to NDVI map images:  " << secs << "ms" << endl;
    imshow("NDVI Image", img_ndvi);
    waitKey();
    /**/


    /* How long to NDVI map using loops */
    chrono::high_resolution_clock::time_point t1 = chrono::high_resolution_clock::now();
    ndvi_map(img_R, img_NIR);
    chrono::high_resolution_clock::time_point t2 = chrono::high_resolution_clock::now();
    auto secs = chrono::duration_cast<chrono::milliseconds>(t2-t1).count();
    cout << "Time to NDVI map images:  " << secs << "ms" << endl;
    imshow("NDVI Image", img_ndvi);
    waitKey();
    /**/



    //timer_test();
}
