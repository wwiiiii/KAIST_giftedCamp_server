#include "grader.h"

int gradeAlgo()
{
	int result[MAP_NUM + 5];
	int sum = 0;
	setModeNoShow();
	for (int i = 1; i <= MAP_NUM; i++)
	{
		loadMapData(i);
		myFunction();
		sum += getCount();
		result[i] = getCount();
	}
	system("clear");
	for (int i = 1; i <= MAP_NUM; i++)
	{
		if(i==1)printf("%dst Move Count : %d\n", i, result[i]);
		else if(i==2)printf("%dnd Move Count : %d\n", i, result[i]);
		else if(i==3)printf("%drd Move Count : %d\n", i, result[i]);
		else printf("%dth Move Count : %d\n", i, result[i]);
	}
	return sum;
}

