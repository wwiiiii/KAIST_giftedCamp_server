#ifndef __MAZE_API_H__
#define __MAZE_API_H__

#include <stdio.h>
#include <stdlib.h>

#define LEFT 0
#define RIGHT 1
#define UP 2
#define DOWN 3
#define BLACK 8*16+8
#define WHITE 7*16+7
#define GREEN 2*16+7
void loadMapData(int);
void deleteMap();
void winGame();

static int** map;
extern int nearMap[3][3];
static int row, col, mode = 1;//mode 0 : show only result, mode 1 : show GUI
static int posx, posy, cnt, lastDir, clear;
static int marginx = 10, marginy = 5;
static int dx[] = {-1,1,0,0};
static int dy[] = {0,0,-1,1};
static int delay = 100;
//static char character[4][2] = { "っ","た","で","ぬ" };
/*
 * move Funciton list. 
 * if cannot move, increase count and return -1
 * if move succeeds, increase count and return 1, modify x/y position
 */

int move(int);//call matching function

//update near array, return pointer of near array
void findNear(int [3][3]);
void setModeShow(int newDelay);
void setModeNoShow();
int getCount();
int getSuccess();

#endif
