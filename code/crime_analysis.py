import findspark
findspark.init()
from pyspark.sql import SparkSession
import os, time, glob
import matplotlib.pyplot as plt

spark = SparkSession \
    .builder \
    .getOrCreate()

df = spark.read.csv('../data/sf_data.csv',header=True,inferSchema=True)
# df.printSchema()
# num_of_row = df.count()
# print "number of crimes = ",num_of_row

# df.select('Category').groupBy('Category').count().orderBy("count",ascending=False).show(20,truncate=False)


# df.select('PdDistrict').groupBy('PdDistrict').count().orderBy("count").show()

def display_result(lon,lat):
	result = df.filter(df.X>lon-0.01)\
		.filter(df.X<lon+0.01)\
		.filter(df.Y>lat-0.01)\
		.filter(df.Y<lat+0.01)

	pdf = result[['X','Y']].toPandas()
	fig = plt.figure()
	plt.title('SF Crime Distribution')
	plt.xlabel('Longitude')
	plt.ylabel('Latitude')
	plt.scatter(pdf.X, pdf.Y, s = 2, c = 'r')

	if not os.path.isdir('static'):
		os.mkdir('static')
	else:
	# Remove old plot files
		for filename in glob.glob(os.path.join('static', '*.png')):
			os.remove(filename)
	# Use time since Jan 1, 1970 in filename in order make
	# a unique filename that the browser has not chached
	plotfile = os.path.join('static', str(time.time()) + '.png')
	plt.savefig(plotfile)
	return plotfile


