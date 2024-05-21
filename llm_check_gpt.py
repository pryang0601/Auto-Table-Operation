from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4",
  
  messages=[
    {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
    {"role": "user", "content": """
    
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

    Institution,Specific Graduate Program,Minimum Score Requirement,Restrictions,City,State
    "Adelphi University, Garden City",,,,,
    ,0,0.0,,Garden City,0
    Alfred University,,,,,
    ,Master of Fine Arts,1.0,,Alfred,0
    Alverno College,,,,,

    """}
  ]
)

print(completion.choices[0].message.content)