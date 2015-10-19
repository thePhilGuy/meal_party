#include <pqxx/pqxx>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char const *argv[]) {
	
	if (argc != 3) {
		cerr << "usage: " << argv[0] << " table filename\n";
		return 1;
	}

	string table(argv[1]);
	ifstream input_file(argv[2]);
	string input_line;
	ostringstream sql_stream;

	getline(input_file, input_line);
	sql_stream << "INSERT INTO " << table 
			   << "(" << input_line << ") VALUES \n";

	while(getline(input_file, input_line)) {
		sql_stream << "( " << input_line
			       << "), \n";
	}

	string sql_string = sql_stream.str();
	sql_string = sql_string.substr(0, sql_string.size() - 3);

	cout << sql_string;

	return 0;
}