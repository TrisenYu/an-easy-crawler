#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

unsigned char arr[] = {
    -25, 79, -85, -101, -69, -66, -24, -91, 68, 3, 64, -99, 82, -38, -7, -34,
	50, -51, 111, -80, 15, 20, 126, 120, 28, 42, -114, 115, -75, 122, -30, 95,
	99, 34, 69, 70, 80, 100, 19, 124, -67, -22, 63, 107, 90, 11, -72, -105, -57,
	-28, -19, 39, 62, 55, -83, 88, 58, 8, 121, -11, -45, -118, 21, 53, -41, 104,
	106, -96, 54, 22, -52, -59, 51, 76, 17, -10, -125, -46, 118, 23, -32, -2, -116,
	-84, -23, -48, -70, -43, -54, 45, 105, -120, -37, 94, 24, 5, 49, 127, -5, -53,
	113, 125, -6, -92, 108, -9, -35, -26, 4, 66, -74, -76, 110, -86, 47, 98, 18, 2,
	109, -16, 12, -97, 60, -50, -44, -128, -68, 41, -36, -103, 30, 52, -106, 89, 29,
	101, -82, 112, 32, 114, -33, -88, 36, 27, -115, -119, 43, 77, -95, 26, 48, 116,
	-39, 46, 75, -3, -112, 61, -17, 25, -63, 7, -61, -49, -31, 93, 37, -108, -42,
	-56, -47, -94, 123, -79, -110, 73, 86, -104, 40, -78, -27, 44, -12, 84, 6, -113,
	 117, 57, -117, -90, -55, -13, -93, 31, -40, 92, 56, 102, -14, 35, 119, -126, 1,
	-98, -107, -58, -18, -122, -20, -109, 65, 0, -1, 91, 85, -89, 78, 72, 81, 16, 96,
	-124, -102, 14, -121, -64, 13, -62, -127, -21, -81, 74, -123, -60, 33, 97, -73,
	-8, -29, -100, 38, -4, -111, -71, -77, 9, 83, -15, -65, 67, 87, 103, 71, -87, 59, 10
};
/* 没见过这个 s 盒。
    0xe7,0x4f,0xab,0x9b,0xbb,0xbe,0xe8,0xa5,0x44,0x03,0x40,0x9d,0x52,0xda,0xf9,0xde,
    0x32,0xcd,0x6f,0xb0,0x0f,0x14,0x7e,0x78,0x1c,0x2a,0x8e,0x73,0xb5,0x7a,0xe2,0x5f,
    0x63,0x22,0x45,0x46,0x50,0x64,0x13,0x7c,0xbd,0xea,0x3f,0x6b,0x5a,0x0b,0xb8,0x97,
    0xc7,0xe4,0xed,0x27,0x3e,0x37,0xad,0x58,0x3a,0x08,0x79,0xf5,0xd3,0x8a,0x15,0x35,
    0xd7,0x68,0x6a,0xa0,0x36,0x16,0xcc,0xc5,0x33,0x4c,0x11,0xf6,0x83,0xd2,0x76,0x17,
    0xe0,0xfe,0x8c,0xac,0xe9,0xd0,0xba,0xd5,0xca,0x2d,0x69,0x88,0xdb,0x5e,0x18,0x05,
    0x31,0x7f,0xfb,0xcb,0x71,0x7d,0xfa,0xa4,0x6c,0xf7,0xdd,0xe6,0x04,0x42,0xb6,0xb4,
    0x6e,0xaa,0x2f,0x62,0x12,0x02,0x6d,0xf0,0x0c,0x9f,0x3c,0xce,0xd4,0x80,0xbc,0x29,
    0xdc,0x99,0x1e,0x34,0x96,0x59,0x1d,0x65,0xae,0x70,0x20,0x72,0xdf,0xa8,0x24,0x1b,
    0x8d,0x89,0x2b,0x4d,0xa1,0x1a,0x30,0x74,0xd9,0x2e,0x4b,0xfd,0x90,0x3d,0xef,0x19,
    0xc1,0x07,0xc3,0xcf,0xe1,0x5d,0x25,0x94,0xd6,0xc8,0xd1,0xa2,0x7b,0xb1,0x92,0x49,
    0x56,0x98,0x28,0xb2,0xe5,0x2c,0xf4,0x54,0x06,0x8f,0x75,0x39,0x8b,0xa6,0xc9,0xf3,
    0xa3,0x1f,0xd8,0x5c,0x38,0x66,0xf2,0x23,0x77,0x82,0x01,0x9e,0x95,0xc6,0xee,0x86,
    0xec,0x93,0x41,0x00,0xff,0x5b,0x55,0xa7,0x4e,0x48,0x51,0x10,0x60,0x84,0x9a,0x0e,
    0x87,0xc0,0x0d,0xc2,0x81,0xeb,0xaf,0x4a,0x85,0xc4,0x21,0x61,0xb7,0xf8,0xe3,0x9c,
    0x26,0xfc,0x91,0xb9,0xb3,0x09,0x53,0xf1,0xbf,0x43,0x57,0x67,0x47,0xa9,0x3b,0x0a
*/
int main(int argc, char *argv[]) {
    for (int i = 0; i < 256; i ++) {
        printf("0x%02x,", arr[i]);
    }
    return 0;
}