#include "grader.h"
#define INF 1987654321
int gradeAlgo()
{
	int result[MAP_NUM + 5];
	int sum = 0;
	setModeNoShow();
	for (int i = 1; i <= MAP_NUM; i++)
	{
		loadMapData(i);
		myFunction();
		if (getSuccess() == 0) result[i] = INF;
		else {
			sum += getCount();
			result[i] = getCount();
		}
	}
	system("clear");
	for (int i = 1; i <= MAP_NUM; i++)
	{
		if (result[i] == INF)
		{
			if (i == 1)printf("%dst Move Count : Failed\n", i);
			else if (i == 2)printf("%dnd Move Count : Failed\n", i);
			else if (i == 3)printf("%drd Move Count : Failed\n", i);
			else printf("%dth Move Count : Failed\n", i);
		}
		else {
			if (i == 1)printf("%dst Move Count : %d\n", i, result[i]);
			else if (i == 2)printf("%dnd Move Count : %d\n", i, result[i]);
			else if (i == 3)printf("%drd Move Count : %d\n", i, result[i]);
			else printf("%dth Move Count : %d\n", i, result[i]);
		}
	}
	return sum;
}

