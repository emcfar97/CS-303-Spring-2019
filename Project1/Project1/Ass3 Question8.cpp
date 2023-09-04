#include <iostream>
#include <string>
#include <stack>
#include <queue>

template <class myType>
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
template <class myType>
void moveToRear(std::queue<myType>& queue) {

	myType front = queue.front();
	queue.pop();
	queue.push(front);
}
int Postfix_Evaluator::eval(const std::string& expression) {
	// Be sure the stack is empty
	while (!operand_stack.empty())    
		operand_stack.pop();
	// Process each token
	istringstream tokens(expression);
	char next_char;
	while (tokens >> next_char) {
		if (isdigit(next_char)) {
			// if this character is a digit      
			tokens.putback(next_char);
			//put back to the expression string
			int value;      
			tokens >> value; 
			//now read the tokenas a number      
			operand_stack.push(value);    } 
		elseif (is_operator(next_char)) {
			int result = eval_op(next_char); 
			//evaluate: result= second op first      
			operand_stack.push(result); 
			//push the result back to the stack    
		} else { 
			//an invalid 
			characterthrowSyntax_Error("Invalid character encountered");    
		}  
	}
int main() {

	std::queue<int> que;	
	for (int i = 0; i <= 10; i += 2) {
		que.push(i);
	}
	moveToRear(que);
}