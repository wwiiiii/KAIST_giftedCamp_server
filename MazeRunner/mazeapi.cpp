#include "mazeapi.h"

//now location : arr[nowy][nowx]

int nearMap[3][3];

void loadMapData(char* mapname, char*resname)
{
	FILE * f = fopen(mapname, "r"); resf = resname;
	int a, b; fscanf(f, "%d %d", &a, &b); 
	row = a, col = b; posx = posy = 1; cnt = 0; clear = 0;
	mode = 0;
	map = (int**)malloc(sizeof(int*) * a);
	for (int i = 0; i < a; i++)
	{
		map[i] = (int*)malloc(sizeof(int)*b);
		for (int j = 0; j < b; j++)
		{
			fscanf(f, "%d", &map[i][j]);
		}
	}
}

void deleteMap()
{
	for (int i = 0; i < row; i++) free(map[i]);
	free(map);
}


int move(int dir)
{
	cnt++; lastDir = dir;
	if (map[posy + dy[dir]][posx + dx[dir]] == 0) {
		return -1;
	}
	posx += dx[dir]; posy += dy[dir];
	if (posx == col-2&& posy == row-2) winGame();
	return 1;
}


void findNear(int arr[3][3])
{
	for (int i = 0; i < 3; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			arr[i][j] = map[posy+i-1][posx+j-1];
		}
	}
}

void setModeShow(int d) { mode = 1; delay = d; }
void setModeNoShow() { mode = 0; }

void winGame()
{
	clear = 1;
	FILE * fp = fopen(resf, "w");
	fprintf(fp,"Clear : %d\n", cnt);
	fp.close();
	exit(0);
}



int getCount() {
	return cnt;
}

int getSuccess() { return clear; }