# # compile c++ tool
c++ -std=c++1y -O2 -o insertify db_import.cpp

# create db and build schema
createdb $1
psql --dbname=$1 --file=schema.sql 

for filename in sample_data/*.csv; do
	./insertify $(basename "$filename" .csv) "$filename" > "$filename".sql
	psql --dbname=$1 --file="$filename".sql
done
