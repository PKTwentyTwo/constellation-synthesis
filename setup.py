'''Setup script for the project.'''
import subprocess
import os
import lifelib
bash = lifelib.autocompile.get_local_bash()
compiler = lifelib.autocompile.get_compiler()
print('Bash: '+str(bash))
print('Compiler: '+str(compiler))
#The code for shipcolls, which is used to generate collisions.
SHIPCOLLS_CODE = '''
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <new>
#include <string.h>
#include <string>
#include <vector>
#include <time.h>
#include <random>

using namespace std;

string intlookup[51][11] = { {"0","f","f", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000"},{"1c","f","f", "10000000", "00000100", "00000001", "00100000", "00000001", "10000000", "00100000", "00000100"},{"1e","f","f", "00010000", "00000010", "00001000", "01000000", "00000010", "01000000", "00001000", "00010000"},{"2c","f","f", "10000100", "00000101", "00100001", "10100000", "00000101", "10100000", "00100001", "10000100"},{"2e","f","f", "01010000", "00010010", "00001010", "01001000", "00001010", "01010000", "01001000", "00010010"},{"2k","f","f", "10000010", "00001100", "01000001", "00110000", "00010001", "10001000", "00100010", "01000100"},{"2a","f","f", "10010000", "00000110", "00001001", "01100000", "00000011", "11000000", "00101000", "00010100"},{"2i","f","f","01000010","00011000","01000010","00011000","01000010","00011000","01000010","00011000"},{"2n","f","f", "10000001", "00100100", "10000001", "00100100", "10000001", "10000001", "00100100", "00100100"},{"3c","f","f", "10100100", "10000101", "00100101", "10100001", "00100101", "10100100", "10100001", "10000101"},{"3e","f","f", "01010010", "00011010", "01001010", "01011000", "00011010", "01011000", "01001010", "01010010"},{"3k","f","f", "10001010", "01001100", "01010001", "00110010", "01010001", "10001010", "00110010", "01001100"},{"3a","f","f", "11010000", "00010110", "00001011", "01101000", "00001011", "11010000", "01101000", "00010110"},{"3i","f","f", "11100000", "10010100", "00000111", "00101001", "00101001", "10010100", "11100000", "00000111"},{"3n","f","f", "11000100", "00010101", "00100011", "10101000", "00001101", "10110000", "01100001", "10000110"},{"3y","f","f", "10001100", "01000101", "00110001", "10100010", "01000101", "10100010", "00110001", "10001100"},{"3q","f","f", "10010001", "00100110", "10001001", "01100100", "10000011", "11000001", "00101100", "00110100"},{"3j","f","f", "11001000", "01010100", "00010011", "00101010", "01001001", "10010010", "01110000", "00001110"},{"3r","f","f", "11000010", "00011100", "01000011", "00111000", "00011001", "10011000", "01100010", "01000110"},{"4c","f","f", "10100101", "10100101", "10100101", "10100101", "10100101", "10100101", "10100101", "10100101"},{"4e","f","f", "01011010", "01011010", "01011010", "01011010", "01011010", "01011010", "01011010", "01011010"},{"4k","f","f", "10110010", "10001110", "01001101", "01110001", "00110011", "11001100", "10101010", "01010101"},{"4a","f","f", "11110000", "10010110", "00001111", "01101001", "00101011", "11010100", "11101000", "00010111"},{"4i","f","f", "11000110", "00011101", "01100011", "10111000", "00011101", "10111000", "01100011", "11000110"},{"4n","f","f", "11100100", "10010101", "00100111", "10101001", "00101101", "10110100", "11100001", "10000111"},{"4y","f","f", "10101100", "11000101", "00110101", "10100011", "01100101", "10100110", "10110001", "10001101"},{"4q","f","f", "11010001", "00110110", "10001011", "01101100", "10001011", "11010001", "01101100", "00110110"},{"4j","f","f", "11001010", "01011100", "01010011", "00111010", "01011001", "10011010", "01110010", "01001110"},{"4r","f","f", "11010010", "00011110", "01001011", "01111000", "00011011", "11011000", "01101010", "01010110"},{"4t","f","f", "11100010", "10011100", "01000111", "00111001", "00111001", "10011100", "11100010", "01000111"},{"4w","f","f", "11001001", "01110100", "10010011", "00101110", "11001001", "10010011", "01110100", "00101110"},{"4z","f","f", "10011001", "01100110", "10011001", "01100110", "11000011", "11000011", "00111100", "00111100"},{"5c","f","f", "01111010", "11011010", "01011110", "01011011", "01111010", "01011110", "11011010", "01011011"},{"5e","f","f", "10101101", "11100101", "10110101", "10100111", "11100101", "10100111", "10110101", "10101101"},{"5k","f","f", "01110101", "10110011", "10101110", "11001101", "10101110", "01110101", "11001101", "10110011"},{"5a","f","f", "00101111", "11101001", "11110100", "10010111", "11110100", "00101111", "10010111", "11101001"},{"5i","f","f", "00011111", "01101011", "11111000", "11010110", "11010110", "01101011", "00011111", "11111000"},{"5n","f","f", "00111011", "11101010", "11011100", "01010111", "11110010", "01001111", "10011110", "01111001"},{"5y","f","f", "01110011", "10111010", "11001110", "01011101", "10111010", "01011101", "11001110", "01110011"},{"5q","f","f", "01101110", "11011001", "01110110", "10011011", "01111100", "00111110", "11010011", "11001011"},{"5j","f","f", "00110111", "10101011", "11101100", "11010101", "10110110", "01101101", "10001111", "11110001"},{"5r","f","f", "00111101", "11100011", "10111100", "11000111", "11100110", "01100111", "10011101", "10111001"},{"6c","f","f", "01111011", "11111010", "11011110", "01011111", "11111010", "01011111", "11011110", "01111011"},{"6e","f","f", "10101111", "11101101", "11110101", "10110111", "11110101", "10101111", "10110111", "11101101"},{"6k","f","f", "01111101", "11110011", "10111110", "11001111", "11101110", "01110111", "11011101", "10111011"},{"6a","f","f", "01101111", "11111001", "11110110", "10011111", "11111100", "00111111", "11010111", "11101011"},{"6i","f","f", "11100111", "10111101", "11100111", "10111101", "10111101", "10111101", "11100111", "11100111"},{"6n","f","f", "01111110", "11011011", "01111110", "11011011", "01111110", "01111110", "11011011", "11011011"},{"7c","f","f", "01111111", "11111011", "11111110", "11011111", "11111110", "01111111", "11011111", "11111011"},{"7e","f","f", "11101111", "11111101", "11110111", "10111111", "11111101", "10111111", "11110111", "11101111"},{"8","f","f", "11111111", "11111111", "11111111", "11111111", "11111111", "11111111", "11111111", "11111111"} };
mt19937 rng;

//sets the rule by parsing the provided rulestring and updating intlookup
void set_rule(string rulestring)
{
	int bors = 1;	//birth is 1, survival is 2
	string currentNum = "";
	string currentChar = "";
	bool setToFalse = false;

	string nums = "012345678";
	string chars = "cekainyqjrtwz";

	for (int i = 0; i < rulestring.length(); i++)
	{
		if (rulestring[i] == '8')
		{
			intlookup[50][bors] = "t";
		}
		else if (nums.find(rulestring[i]) >= 0 && nums.find(rulestring[i]) < 9)
		{
			currentNum = rulestring.substr(i, 1);
			setToFalse = false;
			if (rulestring[i + 1] == '-')
			{
				setToFalse = true;
				for (int j = 0; j < 51; j++)
				{
					if (intlookup[j][0][0] == currentNum[0])
					{
						intlookup[j][bors] = "t";
					}
				}
			}
			else if ((nums.find(rulestring[i + 1]) > 0 && nums.find(rulestring[i + 1]) < 9) || rulestring[i+1] == '/' || rulestring[i+1] == 's' || rulestring[i + 1] == 'S' || rulestring[i + 1] == '\0')
			{
				for (int j = 0; j < 51; j++)
				{
					if (intlookup[j][0][0] == currentNum[0])
					{
						intlookup[j][bors] = "t";
					}
				}
			}
		}
		else if (chars.find(rulestring[i]) >= 0 && chars.find(rulestring[i]) < 13)
		{
			currentChar = rulestring.substr(i, 1);
			for (int j = 0; j < 51; j++)
			{
				if (strcmp(intlookup[j][0].c_str(), (currentNum + currentChar).c_str()) == 0)
				{
					if (setToFalse)
					{
						intlookup[j][bors] = "f";
					}
					else
					{
						intlookup[j][bors] = "t";
					}
				}
			}
		}
		else if (rulestring[i] == 'S' || rulestring[i] == 's')
		{
			bors = 2;
		}
	}
}

//converts a provided rle to a cell list (note: cell list format is {x0,y0,x1,y1...})
void rle_to_clist(vector<int>& target, string rle)
{
	int xpos = 0;
	int ypos = 0;
	int begin = 0;
	int end = 0;
	string currentstr = "";
	int len = 0;
	while (end != -1)
	{
		end = rle.find_first_of("bo$", begin) + 1;
		if (end == 0)
		{
			end = -1;
		}
		if (end != -1)
		{
			currentstr = rle.substr(begin, end - begin);
			len = currentstr.length();
			begin = end;
		}
		if (len > 1 && end != -1)
		{
			if (strcmp(currentstr.substr(len - 1, len).c_str(), "o") == 0)
			{
				for (int i = 0; i < atoi(currentstr.substr(0, len - 1).c_str()); i++)
				{
					target.push_back(xpos + i);
					target.push_back(ypos);
				}
			}
			if (strcmp(currentstr.substr(len - 1, len).c_str(), "$") == 0)
			{
				ypos = ypos + atoi(currentstr.substr(0, len - 1).c_str());
				xpos = 0;
			}
			else
			{
				xpos = xpos + atoi(currentstr.substr(0, len - 1).c_str());
			}
		}
		else if (end != -1)
		{
			if (strcmp(currentstr.c_str(), "o") == 0)
			{
				target.push_back(xpos);
				target.push_back(ypos);
			}
			if (strcmp(currentstr.c_str(), "$") == 0)
			{
				ypos++;
				xpos = 0;
			}
			else
			{
				xpos++;
			}
		}
	}
}

//checks if the cell at the provided coordinates is in a cell list
string get_state(int xpos, int ypos, vector<int>& clist)
{
	for (int i = 0; i < clist.size(); i = i + 2)
	{
		if (clist[i] == xpos && clist[i + 1] == ypos)
		{
			return "1";
		}
	}
	return "0";
}

//takes a cell list as an argument and returns another cell list advanced by one generation in the rule
vector<int> evolve_clist(vector<int> current)
{
	vector<int> newclist;
	int minx = current[0];
	int miny = current[1];
	int maxx = current[0];
	int maxy = current[1];
	string currentNeighborhood = "";

	for (int i = 0; i < current.size(); i = i + 2)
	{
		if (current[i] < minx)
		{
			minx = current[i];
		}
		else if (current[i] > maxx)
		{
			maxx = current[i];
		}
		if (current[i + 1] < miny)
		{
			miny = current[i + 1];
		}
		else if (current[i + 1] > maxy)
		{
			maxy = current[i + 1];
		}
	}

	for (int y = miny - 1; y <= maxy + 1; y++)
	{
		for (int x = minx - 1; x <= maxx + 1; x++)
		{
			currentNeighborhood = get_state(x - 1, y - 1, current) + get_state(x, y - 1, current) + get_state(x + 1, y - 1, current) + get_state(x - 1, y, current) + get_state(x + 1, y, current) + get_state(x - 1, y + 1, current) + get_state(x, y + 1, current) + get_state(x + 1, y + 1, current);
			for (int i = 0; i < 51; i++)
			{
				if (strcmp(get_state(x, y, current).c_str(), "0") == 0 && strcmp(intlookup[i][1].c_str(), "t") == 0)
				{
					for (int j = 3; j < 11; j++)
					{
						if (strcmp(currentNeighborhood.c_str(), intlookup[i][j].c_str()) == 0)
						{
							newclist.push_back(x);
							newclist.push_back(y);
							break;
						}
					}
				}
				else if (strcmp(get_state(x, y, current).c_str(), "1") == 0 && strcmp(intlookup[i][2].c_str(), "t") == 0)
				{
					for (int j = 3; j < 11; j++)
					{
						if (strcmp(currentNeighborhood.c_str(), intlookup[i][j].c_str()) == 0)
						{
							newclist.push_back(x);
							newclist.push_back(y);
							break;
						}
					}
				}
			}
		}
	}
	return newclist;
}

//checks if two cell lists are equivalent
bool equivalent(vector<int> current, vector<int> base, int &dx, int &dy)
{
	if (current.size() != base.size())
	{
		return false;
	}

	vector<int> translated;
	int diffx = current[0] - base[0];
	int diffy = current[1] - base[1];

	for (int i = 0; i < current.size(); i = i + 2)
	{
		translated.push_back(current[i] - diffx);
		translated.push_back(current[i + 1] - diffy);
	}

	for (int i = 0; i < translated.size(); i++)
	{
		if (translated[i] != base[i])
		{
			return false;
		}
	}
	dx = diffx;
	dy = diffy;
	return true;
}

//alters the provided cell list so that it's center is at (0,0)
void normalize(vector<int> &target)
{
	int minx = target[0];
	int miny = target[1];
	int maxx = target[0];
	int maxy = target[1];

	for (int i = 0; i < target.size(); i = i + 2)
	{
		if (target[i] < minx)
		{
			minx = target[i];
		}
		else if (target[i] > maxx)
		{
			maxx = target[i];
		}
		if (target[i + 1] < miny)
		{
			miny = target[i + 1];
		}
		else if (target[i + 1] > maxy)
		{
			maxy = target[i + 1];
		}
	}

	int centerx = (minx + maxx) / 2;
	int centery = (miny + maxy) / 2;

	for (int i = 0; i < target.size(); i = i + 2)
	{
		target[i] = target[i] - centerx;
		target[i + 1] = target[i + 1] - centery;
	}
}

//rotates a target cell list 90 degrees clockwise around (0,0)
void crot(vector<vector<int>> &target, int numRots)
{
	int currentx = 0;
	int currenty = 0;
	for (int r = 0; r < numRots % 4; r++)
	{
		for (int j = 0; j < target.size(); j++)
		{
			for (int i = 0; i < target[j].size(); i = i + 2)
			{
				currentx = target[j][i];
				currenty = target[j][i + 1];
				target[j][i] = 0 - currenty;
				target[j][i + 1] = currentx;
			}
		}
	}
}

//reflects a target cell list either over the y-axis or over the x-axis
void refl(vector<vector<int>> &target, bool horizontal, bool vertical)
{
	int h = 1;
	int v = 1;
	if (horizontal)
	{
		h = -1;
	}
	if (vertical)
	{
		v = -1;
	}
	for (int j = 0; j < target.size(); j++)
	{
		for (int i = 0; i < target[j].size(); i = i + 2)
		{
			target[j][i] = target[j][i] * h;
			target[j][i + 1] = target[j][i + 1] * v;
		}
	}
}

//gets a range between 2 numbers (inclusive)
int rand_range(int minNum, int maxNum)
{
	if (minNum == maxNum)
	{
		return minNum;
	}
	return rng() % (maxNum - minNum) + minNum;
}

//generates the parameters needed to place a glider
void generate_glider(int* target, int minDistance, int maxDistance, int displacementScale, int maxOffset, int gens, int dx, int dy)
{
	//format: {x,y,xoffset,yoffset,gen}
	int displacement;
	int temp;

	target[0] = rand_range(minDistance, maxDistance);
	if (dx == 0 || dy == 0)
	{
		target[1] = rand_range(0 - (target[0] / displacementScale), target[0] / displacementScale);
	}
	else if (dx == dy)
	{
		target[1] = target[0];
		displacement = rand_range(0 - (target[0] / displacementScale), target[0] / displacementScale);
		target[0] = target[0] + displacement;
		target[1] = target[1] - displacement;
	}
	else
	{
		target[1] = target[0] * 2;
		displacement = rand_range(0 - (target[0] / displacementScale), target[0] / displacementScale);
		target[0] = target[0] + displacement;
		target[1] = target[1] - displacement * 2;
		if (target[1] > maxDistance || target[1] < 0 - maxDistance)
		{
			target[0] = target[0] / 2;
			target[1] = target[1] / 2;
		}
	}
	if (target[0] > maxDistance || target[0] < 0 - maxDistance)
	{
		target[0] = maxDistance;
	}
	if (target[1] > maxDistance || target[1] < 0 - maxDistance)
	{
		target[1] = maxDistance;
	}
	if (rng() % 2 == 0)
	{
		target[0] = 0 - target[0];
	}
	if (rng() % 2 == 0)
	{
		target[1] = 0 - target[1];
	}
	for (int i = 0; i < rng() % 4; i++)
	{
		temp = target[0];
		target[0] = 0 - target[1];
		target[1] = temp;
	}
	target[2] = rand_range(0 - maxOffset, maxOffset);
	target[3] = rand_range(0 - maxOffset, maxOffset);
	target[4] = rng() % gens;
}

void glider_coords(int* glider, int* coords)
{
	//format: {x0,y0,x1,y1...}
	int currentpos = 0;
	coords[0] = glider[0];
	coords[1] = glider[1];
	coords[2] = 0; coords[3] = 0; coords[4] = 0; coords[5] = 0; coords[6] = 0; coords[7] = 0;
	currentpos = 2;

	if (glider[2] > 0)
	{
		coords[currentpos] = glider[0] + 1;
		coords[currentpos + 1] = glider[1];
		currentpos = currentpos + 2;
	}
	else if (glider[2] < 0)
	{
		coords[currentpos] = glider[0] - 1;
		coords[currentpos + 1] = glider[1];
		currentpos = currentpos + 2;
	}
	if (glider[3] > 0)
	{
		coords[currentpos] = glider[0];
		coords[currentpos + 1] = glider[1] + 1;
		currentpos = currentpos + 2;
	}
	else if (glider[3] < 0)
	{
		coords[currentpos] = glider[0];
		coords[currentpos + 1] = glider[1] - 1;
		currentpos = currentpos + 2;
	}
	if (glider[2] > 0 && glider[3] > 0)
	{
		coords[currentpos] = glider[0] + 1;
		coords[currentpos + 1] = glider[1] + 1;
	}
	else if (glider[2] > 0 && glider[3] < 0)
	{
		coords[currentpos] = glider[0] + 1;
		coords[currentpos + 1] = glider[1] - 1;
	}
	else if (glider[2] < 0 && glider[3] < 0)
	{
		coords[currentpos] = glider[0] - 1;
		coords[currentpos + 1] = glider[1] - 1;
	}
	else if (glider[2] < 0 && glider[3] > 0)
	{
		coords[currentpos] = glider[0] - 1;
		coords[currentpos + 1] = glider[1] + 1;
	}
}


int main(int argc, char* argv[])
{
	rng.seed(time(NULL));

	string gliderRLE = "null";
	string rulestring = "null";
	int numSoups = -1;
	int minDistanceFromCenter = 1;
	int maxDistanceFromCenter = 5;
	int displacementScale = 2;
	int numGliders = -1;
	int maxGen = 1000;
	bool displayHelp = false;

	//parsing provided arguments
	for (int i = 1; i < argc - 1; i++)
	{
		if (strcmp(argv[i], "-g") == 0)
		{
			gliderRLE = argv[i + 1];
		}
		else if (strcmp(argv[i], "-r") == 0)
		{
			rulestring = argv[i + 1];
		}
		else if (strcmp(argv[i], "-n") == 0)
		{
			numGliders = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-t") == 0)
		{
			numSoups = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-dmin") == 0)
		{
			minDistanceFromCenter = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-dmax") == 0)
		{
			maxDistanceFromCenter = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-dscale") == 0)
		{
			displacementScale = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-gmax") == 0)
		{
			maxGen = atoi(argv[i + 1]);
		}
		else if (strcmp(argv[i], "-h") == 0)
		{
			cout << "This program generates soups composed of a provided spaceship and outputs an RLE of said soup." << endl;
			cout << "Required arguments:" << endl;
			cout << "\t-g: The RLE of the spaceship on every generation. The RLE must be headerless." << endl;
			cout << "\t-r: The rule the spaceship is from. Make sure the input RLE is actually a glider in the input rule!" << endl;
			cout << "\t-n: The number of spaceships to be in each soup." << endl;
			cout << "\t-t: How many soups to output. If you're piping the output into apgsearch, you'll want to set this to 0, which will generate soups indefinitely." << endl;
			cout << "Other arguments:" << endl;
			cout << "\t-dmin: The minimum distance (measured in spaceships) from the center a ship can be. The default is 2, and it is recommended that it be left unchanged." << endl;
			cout << "\t-dmax: The minimum distance (measured in spaceships) from the center a ship can be. The default is 5. Set this higher if you are testing a lot of spaceships." << endl;
			cout << "\t-dscale: Used to calculate a spaceships displacement from the line all ships going in the same direction are placed on. Set this higher if you want ships to be less displaced. The default is 2." << endl;
			cout << "\t-gmax: The number of generations the given pattern will be run to check periodicity before this program gives up and terminates. Only change this if your ship has a very high period! The default is 1000." << endl;
			cout << "\t-h: Prints this message, then exits." << endl;
			return 0;
		}
	}

	//checking that all required arguments are passed
	if (strcmp(gliderRLE.c_str(), "null") == 0)
	{
		cout << "You must enter an RLE! Bring up the help message using the argument '-h 1' for more information." << endl;
		return 0;
		return 0;
	}
	if (strcmp(rulestring.c_str(), "null") == 0)
	{
		cout << "You must enter a rule! Bring up the help message using the argument '-h 1' for more information." << endl;
		return 0;
	}
	if (numGliders == -1)
	{
		cout << "You must enter the number of gliders to include in a soup! Bring up the help message using the argument '-h 1' for more information." << endl;
		return 0;
	}
	if (numSoups == -1)
	{
		cout << "You must enter a number of soups to generate! Bring up the help message using the argument '-h 1' for more information." << endl;
		return 0;
	}

	//some more input filtering
	if (numGliders < -1)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}
	if (numSoups < -1)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}
	if (minDistanceFromCenter < 0)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}
	if (maxDistanceFromCenter < 0)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}
	if (displacementScale < 0)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}
	if (maxGen < 0)
	{
		cout << "You entered a negative value!" << endl;
		return 0;
	}

	set_rule(rulestring);

	
	//stuff to fully characterize the glider
	vector<int> initClist;
	vector<vector<int>> initGlider;

	rle_to_clist(initClist, gliderRLE);
	initGlider.push_back(initClist);

	int dx;
	int dy;

	int tempcount = 0;
	while (!equivalent(evolve_clist(initGlider.back()), initClist, dx, dy))
	{
		initGlider.push_back(evolve_clist(initGlider.back()));
		tempcount++;
		if (tempcount > maxGen)
		{
			cout << "Failed to detect periodicity in " << maxGen << " generations. This is (probably) not a spaceship." << endl;
			return 0;
		}
	}
	for (int i = 0; i < initGlider.size(); i++)
	{
		normalize(initGlider[i]);
	}

	if (dx == 0 && dy == 0)
	{
		cout << "This is not a spaceship!" << endl;
		return 0;
	}

	//gets all rotations + reflections of glider
	vector<vector<int>> nNW;	//-1,-2	x>y,x<0,y<0,ax<ay
	vector<vector<int>> nne;	//1,-2	x>y,x>0,y<0,ax<ay
	vector<vector<int>> NEe;	//2,-1	x>y,x>0,y<0,ax>ay
	vector<vector<int>> see;	//2,1	x>y,x>0,y>0,ax>ay
	vector<vector<int>> sSE;	//1,2	x<y,x>0,y>0,ax<ay
	vector<vector<int>> ssw;	//-1,2	x<y,x<0,y>0,ax<ay
	vector<vector<int>> SWw;	//-2,1	x<y,x<0,y>0,ax>ay
	vector<vector<int>> nww;	//-2,-1	x<y,x<0,y<0,ax>ay

	if (dx >= 0 && dy >= 0)
	{
		if (dx >= dy)
		{
			see = initGlider;
			nNW = see;
			crot(nNW, 1);
			refl(nNW, false, true);
		}
		else if (dx < dy)
		{
			sSE = initGlider;
			nNW = sSE;
			crot(nNW, 2);
		}
	}
	else if (dx >= 0 && dy < 0)
	{
		if (dx >= 0 - dy)
		{
			NEe = initGlider;
			nNW = NEe;
			crot(nNW, 3);
		}
		else if (dx < 0 - dy)
		{
			nne = initGlider;
			nNW = nne;
			refl(nNW, true, false);
		}
	}
	else if (dx < 0 && dy < 0)
	{
		if (0 - dx >= 0 - dy)
		{
			nww = initGlider;
			nNW = nww;
			crot(nNW, 1);
			refl(nNW, true, false);
		}
		else if (0 - dx < 0 - dy)
		{
			nNW = initGlider;
		}
	}
	else if (dx < 0 && dy >= 0)
	{
		if (0 - dx >= dy)
		{
			SWw = initGlider;
			nNW = SWw;
			crot(nNW, 1);
		}
		else if (0 - dx < dy)
		{
			ssw = initGlider;
			nNW = ssw;
			refl(nNW, false, true);
		}
	}

	NEe = nNW;
	crot(NEe, 1);
	sSE = nNW;
	crot(sSE, 2);
	SWw = nNW;
	crot(SWw, 3);
	nne = nNW;
	refl(nne, true, false);
	see = nne;
	crot(see, 1);
	ssw = nne;
	crot(ssw, 2);
	nww = nne;
	crot(nww, 3);

	//getting the glider's max span
	int minx;
	int miny;
	int maxx;
	int maxy;
	int bigx = 0;
	int bigy = 0;
	for (int j = 0; j < initGlider.size(); j++)
	{
		minx = initGlider[j][0];
		miny = initGlider[j][1];
		maxx = initGlider[j][0];
		maxy = initGlider[j][1];
		for (int i = 0; i < initGlider[j].size(); i = i + 2)
		{
			if (initGlider[j][i] < minx)
			{
				minx = initGlider[j][i];
			}
			else if (initGlider[j][i] > maxx)
			{
				maxx = initGlider[j][i];
			}
			if (initGlider[j][i + 1] < miny)
			{
				miny = initGlider[j][i + 1];
			}
			else if (initGlider[j][i + 1] > maxy)
			{
				maxy = initGlider[j][i + 1];
			}
		}
		if (maxx - minx > bigx)
		{
			bigx = maxx - minx;
		}
		if (maxy - miny > bigy)
		{
			bigy = maxy - miny;
		}
	}
	int gliderSize = 0;
	if (bigx > bigy)
	{
		gliderSize = bigx + 1;
	}
	else
	{
		gliderSize = bigy + 1;
	}

	//getting absolute values of dx and dy
	if (dx < 0)
	{
		dx = 0 - dx;
	}
	if (dy < 0)
	{
		dy = 0 - dy;
	}

	//some final initialization before the main loop
	bool** mainSoup = new bool* [(gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2)];
	for (int i = 0; i < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); i++)
	{
		mainSoup[i] = new bool[(gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2)];
	}
	int* takenCoords = new int[numGliders * 4 * 2];
	int* gliderList = new int[numGliders * 5];
	int tempGlider[5];
	int tempCoords[8];
	int offset = gliderSize / 2;
	int gliderGens = initGlider.size();
	int gliderCount;
	bool isTaken;
	vector<vector<int>>* gptr = &nNW;

	string rle;
	string temprle;
	int currentNum;
	char currentChar;
	int minxsoup;
	bool hasHit;

	int zeroPoint = ((gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2)) / 2;

	int soupCount = 0;
	while (soupCount < numSoups || numSoups == 0)
	{
		//resetting some values...
		for (int y = 0; y < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); y++)
		{
			for (int x = 0; x < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); x++)
			{
				mainSoup[y][x] = false;
			}
		}
		for (int i = 0; i < numGliders * 4 * 2; i++)
		{
			takenCoords[i] = 0;
		}
		for (int i = 0; i < numGliders * 5; i++)
		{
			gliderList[i] = 0;
		}

		//generates glider positions, does basic validation
		gliderCount = 0;
		while (gliderCount < numGliders)
		{
			isTaken = false;
			generate_glider(tempGlider, minDistanceFromCenter, maxDistanceFromCenter, displacementScale, offset, gliderGens, dx, dy);
			glider_coords(tempGlider, tempCoords);
			for (int i = 0; i < numGliders * 4 * 2; i = i + 2)
			{
				if (tempCoords[0] == takenCoords[i] && tempCoords[1] == takenCoords[i + 1])
				{
					isTaken = true;
					break;
				}
			}
			if (isTaken)
			{
				continue;
			}

			for (int i = 0; i < 8; i++)
			{
				takenCoords[gliderCount * 2 * 4 + i] = tempCoords[i];
			}
			for (int i = 0; i < 5; i++)
			{
				gliderList[gliderCount * 5 + i] = tempGlider[i];
			}
			gliderCount++;
		}

		//places gliders on a grid
		for (int i = 0; i < numGliders * 5; i = i + 5)
		{
			if (gliderList[i] >= 0 && gliderList[i + 1] >= 0)
			{
				if (gliderList[i] >= gliderList[i + 1])
				{
					gptr = &nww;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
				else if (gliderList[i] < gliderList[i + 1])
				{
					gptr = &nNW;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
			}
			else if (gliderList[i] >= 0 && gliderList[i + 1] < 0)
			{
				if (gliderList[i] >= 0 - gliderList[i + 1])
				{
					gptr = &SWw;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
				else if (gliderList[i] < 0 - gliderList[i + 1])
				{
					gptr = &ssw;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
			}
			else if (gliderList[i] < 0 && gliderList[i + 1] < 0)
			{
				if (0 - gliderList[i] >= 0 - gliderList[i + 1])
				{
					gptr = &see;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
				else if (0 - gliderList[i] < 0 - gliderList[i + 1])
				{
					gptr = &sSE;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
			}
			else if (gliderList[i] < 0 && gliderList[i + 1] >= 0)
			{
				if (0 - gliderList[i] >= gliderList[i + 1])
				{
					gptr = &NEe;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
				else if (0 - gliderList[i] < gliderList[i + 1])
				{
					gptr = &nne;
					//cout << gliderList[i] << " " << gliderList[i + 1] << endl;
				}
			}

			for (int j = 0; j < gptr[0][gliderList[i + 4]].size(); j = j + 2)
			{
				//ypos = cell y on gen gliderList[i+4] in position [j+1] + gliderbox * glider y pos  + y offset
				mainSoup[(gptr[0][gliderList[i + 4]][j + 1] + (gliderSize + 2) * gliderList[i + 1] + gliderList[i + 3]) + zeroPoint][(gptr[0][gliderList[i + 4]][j] + (gliderSize + 2) * gliderList[i] + gliderList[i + 2]) + zeroPoint] = true;
			}
		}

		temprle = "";
		rle = "";
		minxsoup = (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2);
		for (int y = 0; y < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); y++)
		{
			for (int x = 0; x < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); x++)
			{
				if (mainSoup[y][x] && x < minxsoup)
				{
					minxsoup = x;
				}
			}
		}
		for (int y = (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2) - 1; y >= 0; y--)
		{
			hasHit = false;
			temprle = "$" + temprle;
			for (int x = (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2) - 1; x >= minxsoup; x--)
			{
				if (mainSoup[y][x])
				{
					hasHit = true;
					temprle = "o" + temprle;
				}
				else if (hasHit)
				{
					temprle = "b" + temprle;
				}
			}
		}
		currentChar = 'h';
		currentNum = 1;
		for (int i = 0; i <= temprle.length(); i++)
		{
			if (temprle[i] == currentChar)
			{
				currentNum++;
			}
			else
			{
				if (currentNum != 1)
				{
					rle = rle + to_string(currentNum);
				}
				if (currentChar != 'h')
				{
					rle = rle + currentChar;
				}
				currentChar = temprle[i];
				currentNum = 1;
			}
		}

		cout << "x = 0, y = 0, rule = B3/S23\\n" << rle << "!" << endl;
		soupCount++;
	}

	//cleanup
	for (int i = 0; i < (gliderSize + 2) * 2 * maxDistanceFromCenter + 2 * (gliderSize + 2); i++)
	{
		delete[] mainSoup[i];
	}
	delete[] mainSoup;
	delete[] takenCoords;
	delete[] gliderList;
	
}

'''
def compile_shipcolls():
    '''Compiles shipcolls using whatever version of bash is found.'''
    #Delete the old executable:
    if os.path.isfile(os.getcwd() + '/shipcolls'):
        os.remove(os.getcwd() + '/shipcolls')
    #Check if shipcolls source code is saved:
    if not os.path.isfile(os.getcwd() + '/shipcolls.cpp'):
        with open(os.getcwd() + '/shipcolls.cpp', 'w', encoding='utf-8') as f:
            f.write(SHIPCOLLS_CODE)
    #Compile shipcolls.
    #The command used is: g++ -o shipcolls shipcolls.cpp -std=c++11 -O3 -Ofast -flto -march=native
    print('Compiling shipcolls...')
    args = ['shipcolls.cpp','-o','shipcolls','-std=c++11','-O3','-Ofast','-flto','-march=native']
    command = compiler + args
    print(command)
    proc = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    i = 0
    proc.communicate()
    status = proc.returncode
    print('Process completed with status code '+str(status))
    if status == 0:
        print('Compilation complete!')
    else:
        print('Compilation failure!')
compile_shipcolls()
#Setting up directories:
print('Setting up directories...')
dirs = ['/data']
for x in dirs:
    if not os.path.isdir(os.getcwd() + x):
        os.mkdir(os.getcwd() + x)
print('Setup complete!')
