from datasets import load_dataset
import openai
import requests

# Codex result
codex_prompt = "{code}\n# What is this code used for?.\n\"\"\""
def get_codex_completion(data_entry):
    snippet = data_entry["code"].replace(data_entry["docstring"], "")
    prompt = codex_prompt.format(code=snippet)

    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=1.0,
        max_tokens=128,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\"", "\n\n", "#"],
        n=1,
    )

    return response["choices"][0]["text"]

# Trelent result
def get_trelent_result(data_entry):
    snippet = data_entry["code"].replace(data_entry["docstring"], "")
    func_name = data_entry["func_name"]

    body = {
        "user_id": "TEST",
        "sender": "DEV",
        "language": "python",
        "format": "rest",
        "function": {
            "function_code": snippet,
            "function_name": func_name,
            "function_params": []
        },
        "context": None
    }

    response = requests.post(
        "https://prod-api.trelent.net/docs/docstring",
        json=body
    )

    docstr = response.json()["data"]["docstring"]
    # Remove docstring pre/suffix and the :return: line and below
    docstr = docstr.replace("r\"\"\"", "").replace("\"\"\"", "")
    idx = docstr.find(":return:")
    if idx != -1:
        docstr = docstr[:idx]

    return docstr.strip()

dataset = load_dataset("code_x_glue_ct_code_to_text", "python")

validation_set = dataset["validation"]
trelent_results = ""
codex_results = ""
references = ""
i = 1
while(i < 10):
    data_entry = validation_set[i]
    trelent_results += get_trelent_result(data_entry) + "\n====SPLIT====\n"
    codex_results += get_codex_completion(data_entry) + "\n====SPLIT====\n"
    references += data_entry["docstring"] + "\n====SPLIT====\n"
    print("iter", i)
    i+=1

with open("data/codex.txt", "a") as f:
    f.write(codex_results)

with open("data/trelent.txt", "a") as f:
    f.write(trelent_results)

with open("data/references.txt", "a") as f:
    f.write(references)