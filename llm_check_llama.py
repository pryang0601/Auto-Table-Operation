from openai import OpenAI
import pandas as pd
from prompt import prompt
import os
from langchain_community.llms import HuggingFaceEndpoint
from transformers import pipeline



os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

def is_pivot_gpt(table_file: str, head_num: int = 8, model: str = "failspy/Llama-3-70B-Instruct-abliterated-v3") -> bool:
    
    """Check if it need pivot operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    print(prompt["pivot"] + str(result_string))

    pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-70B")

    print(pipe)

    # llm_try = HuggingFaceEndpoint(repo_id = model)

    # print(llm_try.invoke(prompt["pivot"] + str(result_string)))


    # completion = client.chat.completions.create(
    #   model=model,
      
    #   messages=[
    #     {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
    #     {"role": "user", "content": prompt["pivot"] + str(result_string)}
    #   ]
    # )
    # # print(completion.choices[0].message.content)
    # return completion.choices[0].message.content #(True), (False)

def is_stack_gpt(table_file: str, head_num: int = 2, model: str = "01-ai/Yi-1.5-34B-Chat"):
    
    """Check if it need stack operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    print(prompt["stack"] + str(result_string))

    llm_try = HuggingFaceEndpoint(repo_id = model)

    print(llm_try.invoke(prompt["stack"] + str(result_string)))

    # global client

    # completion = client.chat.completions.create(
    #   model=model,
      
    #   messages=[
    #     {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
    #     {"role": "user", "content": prompt["stack"] + str(result_string)}
    #   ]
    # )

    # # print(completion.choices[0].message.content)
    # return completion.choices[0].message.content #(True, [start_idx, end_idx]), (False, [])

def is_wide_to_long_gpt(table_file: str, head_num: int = 2, model: str = "gpt-3.5-turbo-16k"):
    
    """Check if it need wide_to_long operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    # print(prompt["wide_to_long"] + str(result_string))

    global client

    completion = client.chat.completions.create(
      model=model,
      
      messages=[
        {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
        {"role": "user", "content": prompt["wide_to_long"] + str(result_string)}
      ]
    )

    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content #(True, [start_idx, end_idx]), (False, [])

def is_transpose_gpt(table_file: str, head_num: int = 12, model: str = "gpt-3.5-turbo-16k") -> bool:
    
    """Check if it need transpose operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    # print(prompt["transpose"] + str(result_string))

    global client

    completion = client.chat.completions.create(
      
      model=model,
      
      messages=[
        {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
        {"role": "user", "content": prompt["transpose"] + str(result_string)}
      ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content #(True), (False)


def is_explode_gpt(table_file: str, head_num: int = 12, model: str = "gpt-3.5-turbo-16k") -> bool:
    
    """Check if it need explode operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    # print(prompt["explode"] + str(result_string))

    global client

    completion = client.chat.completions.create(
      
      model=model,
      
      messages=[
        {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
        {"role": "user", "content": prompt["explode"] + str(result_string)}
      ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content #(True), (False)

def is_ffill_gpt(table_file: str, head_num: int = 12, model: str = "gpt-3.5-turbo-16k") -> bool:
    
    """Check if it need ffill operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    # print(prompt["ffill"] + str(result_string))

    global client

    completion = client.chat.completions.create(
      
      model=model,
      
      messages=[
        {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
        {"role": "user", "content": prompt["ffill"] + str(result_string)}
      ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content #(True), (False)

def is_subtitle_gpt(table_file: str, head_num: int = 3, model: str = "gpt-3.5-turbo-16k") -> bool:
    
    """Check if it need subtitle operation using GPT4"""

    data = pd.read_csv(table_file)

    result_string = data.head(head_num)

    result_string = result_string.to_csv(index=False, header=True).strip()

    # print(prompt["subtitle"] + str(result_string))

    global client

    completion = client.chat.completions.create(
      
      model=model,
      
      messages=[
        {"role": "system", "content": "You are an expert at detecting whether a table is clean."},
        {"role": "user", "content": prompt["subtitle"] + str(result_string)}
      ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content #(True), (False)

is_pivot_gpt("Tables/pivot1.csv")