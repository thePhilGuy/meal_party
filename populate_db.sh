# # compile c++ tool
c++ -std=c++1y -O2 -o insertify db_import.cpp

# create db and build schema
createdb $1
psql --dbname=$1 --file=schema.sql 

for filename in sample_data/*.csv; do
	./insertify $(basename "$filename" .csv) "$filename" > "$filename".sql
done

cd sample_data
# populate db with sample_data
psql --dbname=$1 --file=../schema.sql
psql --dbname=$1 --file=person.csv.sql
psql --dbname=$1 --file=area.csv.sql
psql --dbname=$1 --file=restaurant.csv.sql
psql --dbname=$1 --file=proposal.csv.sql
psql --dbname=$1 --file=meal.csv.sql
psql --dbname=$1 --file=matched.csv.sql
psql --dbname=$1 --file=reservation.csv.sql