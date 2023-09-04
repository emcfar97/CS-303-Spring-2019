#include <iostream>
#include <string>
#include <stack>

std::stack<char> reverseWords(std::string str) {

	std::stack <char> reverse;
	std::stack <char> word;

	for (std::string::const_iterator iter = str.begin(); iter != str.end(); iter++) {
		if (*iter == ' ' or *iter == '.') {
			const int size = word.size();
			for (int i = 0; i < size; i++) {
				reverse.push(word.top());
				word.pop();
			}
			reverse.push(*iter);
		}
		else {
			word.push(*iter);
		}
	}
	return reverse;
}
int main() {
	std::stack <char> reverse = reverseWords("The quick brown fox jumps over the lazy dog.");
	
	const int size = reverse.size();
	for (int i = 0; i < size; i++) {
		std::cout << reverse.top();
		reverse.pop();
	}
	std::cout << std::endl;
	system("pause");
}