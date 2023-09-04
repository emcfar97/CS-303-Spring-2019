#pragma once
class Books
{
private:
	std::string title;
	Date circStart;
	Date cirEnd;
	bool archived;
	std::queue<Employees> waitList;
public:
	Books(std::string inputTitle);

};

