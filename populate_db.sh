# # compile c++ tool
c++ -std=c++1y -O2 -o insertify db_import.cpp

# create db and build schema
# createdb $1
# psql --dbname=$1 --file=schema.sql 

for filename in sample_data/*.csv; do
	./insertify $(basename "$filename" .csv) "$filename" > "$filename".sql
done

cd sample_data
# populate db with sample_data
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=../schema.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=person.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=area.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=restaurant.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=proposal.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=meal.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=matched.csv.sql
psql --dbname=proj1part2 -U pvl2109 -h w4111db1.cloudapp.net --file=reservation.csv.sql