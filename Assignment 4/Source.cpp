#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>

// Question #2
int to_number(std::string str) {

	if (str.length() == 1 && isdigit(str.at(0))) {
		return ((int)str.at(0) - (int)'0');
	}
	else {
		if (isdigit(str.at(0)))
			return ((int)str.at(0) - (int)'0') + to_number(str.substr(1, str.length()-1));
		else if (str.length() > 1)
			return to_number(str.substr(1, str.length()-1));
	}
	return 0;
}
// Question #3
/*template <class Item_Type>
int linear_search(std::vector<Item_Type>& items, Item_Type& target, size_t pos_first) {

	if (pos_first == 0) 
		return -1; 

	if (target == items[pos_first]) 
		return pos_first;
	
	else return linear_search(items, target, pos_first - 1); 
}*/
// Question #5
int selection_sort(std::vector<int>& vec) {

	for (int fill = 0; fill < vec.size(); ++fill) {

		int pos_min = fill; 
		for (int next = fill + 1; next < vec.size(); ++next) {
			if (vec[next] < vec[pos_min])      
				pos_min = next; 
		}
		if (vec[fill] != vec[pos_min]) {//make an exchange 
			int temp = vec[pos_min]; 
			vec[pos_min] = vec[fill]; 
			vec[fill] = temp;
		}
	}
}
void bubble_sort_improved(std::vector<int> &vec) {

	bool exchanges = false; 
	for (int i = 1; i <= vec.size(); i++) {

		exchanges = false;  
		for (int j = 0; j < vec.size() - i; j++) {

			if (vec[j + 1] < vec[j]) {

				std::swap(vec[j], vec[j + 1]);    
				exchanges = true; //an exchange happened   
			} 
		}
		// stop sorting if no exchanges happened
		if (!exchanges)break;
	}
}
void insertion_sort(std::vector<int> &num) {

	int i, j, key; 
	bool insertionNeeded = false; 
	
	for (j = 1; j < num.size(); j++) {
		key = num[j];
		insertionNeeded = false;

		for (i = j - 1; i >= 0; i--) {
		
			if (key < num[i]) {
				num[i + 1] = num[i]; // larger values move right  
				insertionNeeded = true; 
			}
			else break;
		}
		if (insertionNeeded) num[i + 1] = key;    //Put key into its proper location
	}
}
void shell_sort(std::vector<int> &num) {
	int i, temp, flag = 1, numLength = num.size();
	int gap = numLength;
	bool insertionNeeded = false;
	int swapPos = 0;
	int key;

	while (true) {    // boolean flag (true when not equal to 0) 
		gap = (gap - 1) / 2;
		if (gap == 0)
			break;

		for (int k = 0; k < gap; k++) {
			for (int j = gap + k; j < numLength; j += gap) {
				key = num[j];

				insertionNeeded = false;
				for (i = j - gap; i >= 0; i -= gap) {   // Smaller values move right

					if (key < num[i]) {
						swapPos = i;
						num[i + gap] = num[i];
						insertionNeeded = true;
					}
					else
						break;
				}
				if (insertionNeeded) {
					num[swapPos] = key;    //Put key into its proper location
				}
			}
		}
	}
	return;
}
void merge_sort(std::vector<int>& array) {
	
	std::vector<int> result = array; 
	mergesort(array, result, 0, array.size() - 1); 
}
void mergesort(std::vector<int>& array, std::vector<int>& result, int lowerBand, int upperBand) { 
	
	int midpoint; 
	if (lowerBand < upperBand) { 
		midpoint = (lowerBand + upperBand) / 2; 
		mergesort(array, result, lowerBand, midpoint); 
		mergesort(array, result, midpoint + 1, upperBand); 
	} 
}
void quick_sort(int first, int last, std::vector<int>& arr) {

	if (last - first > 1) {
		// There is data to be sorted.
	    // Partition the table. 
		int pivot = partitionB(first, last, arr);

		// Sort the left half. 
		quick_sort(first, pivot, arr);
		
		// Sort the right half. 
		quick_sort(pivot + 1, last,arr);
	}
}
void middle_quick_sort_wrapper(std::vector<int>& arr) {
	middle_quick_sort(0, arr.size(), arr);
}
void middle_quick_sort(int first, int last, std::vector<int>& arr) {
	if (last - first > 1) {
		// There is data to be sorted.
		// Partition the table.
		int pivot = partitionB(first, last, arr);

		// Sort the left half.
		middle_quick_sort(first, pivot, arr);

		// Sort the right half.
		middle_quick_sort(pivot + 1, last, arr);
	}
}
int partitionB(int first, int last, std::vector<int>& arr) {

	int up = first + 1; 
	int down = last - 1; 
	do {
		while ((up != last - 1) && !(arr[first] < arr[up])) { 
			++up; 
		}
		while (arr[first] < arr[down]) {
			--down; 
		}
		if (up < down) {
			// if up is to the left of down, 
			std::swap(arr[up],arr[down]);
		}
	}
	while (up < down); 
	// Repeat while up is left of down.
	std::swap(arr[first],arr[down]);
	return down;
}
int main() {/*
	// Question #2
	std::string str1 = "3ac4";
	std::string str2 = "jk2b58og2g9";
	std::string str3 = "23ur9b24i9f";

	int int1 = to_number(str1);
	int int2 = to_number(str2);
	int int3 = to_number(str3);

	// Question #3
	std::vector<int> list1{12,23,4,0,1};
	std::vector<char> list2{'t','6','g','d','1'};
	std::vector<double> list3{19.59,629.19,8.29,12.01};

	/*int search1 = linear_search(list1, 0, list1.size());
	int search2 = linear_search(list2, 'g', list2.size());
	int search3 = linear_search(list3, 8.29, list3.size());*/
	
	// Question #5
	std::vector<int> vec1;
	std::vector <int> vec2;
	std::vector<int> vec3;
	for (int i = 0; i < 10000; i++) { vec1.push_back(i); }
	for (int i = 10000; i > 0; i--) { vec2.push_back(i); }
	for (int i = 0; i < 10000; i++) { vec3.push_back(std::rand() % 10000); }

	int results[21];
	std::ofstream fout("output.csv");
	fout << "Number of Comparisons\n";
	fout << ", Random Array, Sorted Array, Reversed Array\n";

	selection_sort(vec1); 
	selection_sort(vec2); 
	selection_sort(vec3);
	fout << "Selection Sort," << "\n";

	bubble_sort_improved(vec1);
	bubble_sort_improved(vec2);
	bubble_sort_improved(vec3);
	fout << "Bubble Sort(improved)," << "\n";

	insertion_sort(vec1);
	insertion_sort(vec2);
	insertion_sort(vec3);
	fout << "Insertion Sort," << "\n";

	shell_sort(vec1);
	shell_sort(vec2);
	shell_sort(vec3);
	fout << "Shell Sort," << "\n";

	merge_sort(vec1);
	merge_sort(vec2);
	merge_sort(vec3);
	fout << "Merge Sort," << "\n";

	quick_sort(0, 10000, vec1);
	quick_sort(0, 10000, vec2);
	quick_sort(0, 10000, vec3);
	fout << "Quick Sort," << "\n";

	middle_quick_sort_wrapper(vec1);
	middle_quick_sort_wrapper(vec2);
	middle_quick_sort_wrapper(vec3);
	fout << "Quick Sort(Improved)," << "\n";

	fout << "\nNumber of Exchanges\n";
	fout << ", Random Array, Sorted Array, Reversed Array\n";
	
	fout << "Selection Sort (improved)," << "\n";
	
	fout << "Bubble Sort(improved)," << "\n";
	
	fout << "Insertion Sort(shifts)," << "\n";
	
	fout << "Shell Sort(shifts)," << "\n";
	
	fout << "Merge Sort (copies)," << "\n";
	
	fout << "Quick Sort," << "\n";
	
	fout << "Quick Sort(Improved),\n";
}