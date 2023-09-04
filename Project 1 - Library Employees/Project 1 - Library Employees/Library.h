#pragma once
class Library
{
private:
	std::list<Books> archive;
	std::list<Books> circulation;
	std::queue<Employees> employees;
public:
	Library();
	void add_book(std::string title);
	void add_employee(std::string name);
	void circulate_book(std::string title, Date date);
	void pass_on(std::string title, Date date);
};

