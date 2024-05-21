prompt = { 
"wide_to_long" : 
"""
One type of unclean table is called wide_to_long, which mainly refers to tables with repeated column groups.

For example, I'll provide the schema of a table and two rows of data that exhibit the wide_to_long type:

Index,Where are we?,Location-specific Question/Data query,Correct Answer (formula),Correct Answer,Direction given after correct answer,What is the referent?,PUZZLE A #,PUZZLE A #.1,PUZZLE A ANSWER,PUZZLE B #,PUZZLE B #.1,PUZZLE B ANSWER
1,3-208,Stand with your back to Vest's office.  How many N's do you see directly opposite?,6,6,Turn left.  Continue until next junction.,Room sign,1.7 NT,1.7,ARKANSAS,1.2 NT,1.2,LABORATORY
2,5-2 lobby,"What is the sum of all the room numbers, not counting building numbers, listed on your right?",268+245+320+400+400 = 1633,1633,Go straight ahead,Room sign,3.232,3.232,TOLKIEN,1.5 NT,1.5,SALMON
In this example, the section with PUZZLE A #, PUZZLE A #.1, PUZZLE A ANSWER, PUZZLE B #, PUZZLE B #.1, PUZZLE B ANSWER contains two similar column groups (PUZZLE A, PUZZLE B), indicating it is of the wide_to_long type. The start_idx is 7 and the end_idx is 12, because using 0 as the starting index, PUZZLE A # is at index 7 and PUZZLE B ANSWER is at index 12.

Now, I would like you to determine whether the following table is of the wide_to_long type. I will provide the schema and two rows of data.

Please output according to the following rules, and only respond with the content inside the braces () without any additional output, where start_idx and end_idx represent the column index range of the wide_to_long repeated columns, starting from index 0:

For tables with the wide_to_long type: (True, [start_idx, end_idx])
For tables without the wide_to_long type: (False, [])

Input table:

""", 

"stack":
"""
One type of unclean table is called stack, which mainly refers to tables with contiguous blocks of homogeneous columns.

For example, I'll provide the schema of a table and two rows of data that exhibit the stack type:

Role,"August 21, 2003","August 28, 2003","September 5, 2007","September 11, 2003","September 19, 2007"
Toastmaster,Ken Maclean,Irina Krylova,,,
Laughmaster,Irina Krylova,Cheryl Wiker,,,

In this example, the columns "August 21, 2003", "August 28, 2003", "September 5, 2007", "September 11, 2003", and "September 19, 2007" are all dates, creating too many contiguous similar columns, so this example is of the stack type. The start_idx is 1 and the end_idx is 5, because using 0 as the starting index, "August 21, 2003" is at index 1 and "September 19, 2007" is at index 5.

Alternatively, consider the following schema: attributes.Ambience.casual, attributes.BikeParking, attributes.BusinessAcceptsCreditCards, attributes.BusinessParking.street, attributes.HasTV, attributes.RestaurantsDelivery, attributes.GoodForMeal.breakfast, attributes.GoodForMeal.brunch, attributes.GoodForMeal.dessert, attributes.GoodForMeal.dinner, attributes.GoodForMeal.latenight, attributes.GoodForMeal.lunch, attributes.Alcohol, attributes.NoiseLevel
start_idx is 0 and end_idx is 13, because in this range, all columns are of the attribute type, so this example is of the stack type.

Or consider the following schema: profit, 0, 1, 2, 3, 4
start_idx is 1 and end_idx is 5, because in this range, all columns are numeric, so this example is of the stack type.

Now, I would like you to determine whether the following table is of the stack type. I will provide the schema and two rows of data.

Please output according to the following rules, and only respond with the content inside the braces () without any additional output, where start_idx and end_idx represent the column index range of the stack with homogeneous columns, starting from index 0:

For tables with the stack type: (True, [start_idx, end_idx])
For tables without the stack type: (False, [])

Input table:

""",

"transpose":
"""
One type of unclean table is called transpose, which mainly refers to tables with repeated row groups.

For example, consider the following table:

Product Name,Product 1
Product Description,Description 1
Product Price,Price 1
Product Discount,Discount 1
Product Name,Product 2
Product Description,Description 2
Product Price,Price 2
Product Discount,Discount 2

In this example, 第一個 row 與 第五個 row 同性質, 第二個 row 與 第六個 row 同性質, 第三個 row 與 第七個 row 同性質, 第四個 row 與 第八個 row 同性質, so it is of the pivot type.

Now, I would like you to determine whether the following table is of the pivot type. I will provide the table for you.

Please output according to the following rules, and only respond with the content inside the parentheses () without any additional output:

For tables with the pivot type: (True)
For tables without the pivot type: (False)

Input table:

""",

"pivot":
"""
One type of unclean table is called pivot, which mainly refers to tables with repeated row groups.

For example, consider the following table:

Product Name,Product 1
Product Description,Description 1
Product Price,Price 1
Product Discount,Discount 1
Product Name,Product 2
Product Description,Description 2
Product Price,Price 2
Product Discount,Discount 2

In this example, the first row is of the same nature as the fifth row, the second row is of the same nature as the sixth row, the third row is of the same nature as the seventh row, and the fourth row is of the same nature as the eighth row, so it is of the pivot type.

Now, I would like you to determine whether the following table is of the pivot type. I will provide the table for you.

Please output according to the following rules, and only respond with the content inside the parentheses () without any additional output:

For tables with the pivot type: (True)
For tables without the pivot type: (False)

Input table:

""",

"explode":
"""
One type of unclean table is called explode, which mainly refers to tables with columns containing composite values.

For example, consider the following table:

Player Name,Points,Year
Milt Bakken,"39, 34, 32",1955-56
0,"38,34,33,30",1994-95
1,"38, 35, 31, 31",1958-59
0,"38, 31, 30",1993-94
In this example, the Points column contains composite values like "39, 34, 32", so it is of the explode type.

Now, I would like you to determine whether the following table is of the explode type. I will provide the table for you.

Please output according to the following rules, and only respond with the content inside the parentheses () without any additional output:

For tables with the explode type: (True)
For tables without the explode type: (False)

Input table:

""",

"ffill":
"""
One type of unclean table is called ffill, which mainly refers to tables with missing values in the first column.

For example, consider the following table:

Quarter,Month,Output
1st,Jan,3.5
,Feb,1.2
,,0.8
,,0.6
,,0.5
,Mar,1.7
In this example, the first column has missing values, so it is of the ffill type.

Now, I would like you to determine whether the following table is of the ffill type. I will provide the table for you.

Please output according to the following rules, and only respond with the content inside the parentheses () without any additional output:

For tables with the ffill type: (True)
For tables without the ffill type: (False)

Input table:

""", 

"subtitle":
"""
One type of unclean table is called subtitle, which mainly refers to tables where the second row has values only in the first element, with the rest being missing values.

For example, consider the following table:

Common Name (click for description),Moisture Requirement,Deer Resistant?
FERNS,,
Christmas Fern,0.0,0.0
Cinnamon Fern,1.0,0.0
Hay-scented Fern,0.0,0.0
Lady Fern,2.0,0.0

In this example, the second row has values only in the first element, with the rest being missing values, so it is of the subtitle type.

Now, I would like you to determine whether the following table is of the subtitle type. I will provide the table for you.

Please output according to the following rules, and only respond with the content inside the parentheses () without any additional output:

For tables with the subtitle type: (True)
For tables without the subtitle type: (False)

Input table:

"""

}