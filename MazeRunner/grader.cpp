#include "grader.h"
#define INF 1987654321
int gradeAlgo(char * mapname, char *resname)
{
	setModeNoShow();
	loadMapData(mapname, resname);
	myFunction();
	if (getSuccess() == 0) {
		FILE * fp = fopen(resf, "w");
		fprintf(fp, "Failed.\n");
		fclose(fp);
	}
	else {
		FILE * fp = fopen(resf, "w");
		fprintf(fp, "Error.\n");
		fclose(fp);
	}
	exit(0);
}

