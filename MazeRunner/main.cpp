#include <stdio.h>
#include "grader.cpp"
int main(int argc, char *argv[])
{
	freopen(argv[2], "w", stdout);
	int res = gradeAlgo(argv[1]); //system("cls");
	//printf("Total Move Count : %d\n", res);
}
