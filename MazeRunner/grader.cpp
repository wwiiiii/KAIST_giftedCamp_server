#include "grader.h"
#define INF 1987654321
int gradeAlgo(char * mapname)
{
	setModeNoShow();
	loadMapData(mapname);
	myFunction();
	if (getSuccess() == 0) {
		printf("Failed\n");
	}
	else {
		printf("Error\n");
	}
	fflush(stdout);
	exit(0);
}

