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
		printf("%dth result : %d\n", i, result[i]);
	}
	return sum;
}

