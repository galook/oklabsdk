import base64
import os
from openai import OpenAI, AzureOpenAI
from .helpers import pdftomd
from .oklabsdk import config, initConfigFromEnv

use_azure = False
model_name = None
model = None

def init():
    global use_azure, model_name, model
    if config["openai"]["endpoint"]:
        use_azure = True
    else:
        use_azure = False
    model_name = None

    model = None
    if use_azure:
        model = AzureOpenAI(azure_endpoint=config["openai"]["endpoint"], api_key=config["openai"]["api_key"], api_version=config["openai"]["api_version"], azure_deployment=config["openai"]["model_name"]) 
        model_name = config["openai"]["model_name"]
    else:
        model = OpenAI(api_key=config["llama"]["api_key"], base_url=config["llama"]["endpoint"])
        model_name = config["llama"]["model_name"]


def get_response(prompt, max_tokens=4096, system_message=None, seed=None):
    """Returns the completion from the LLM model. High time consumption."""
    init()
    messages=[{"role": "user", "content": prompt}]
    
    if(system_message):
        messages.insert(0, {"role": "system", "content": system_message})

    completion = model.chat.completions.create(
                model="gpt-4o",
                max_tokens=max_tokens,
                messages=messages,
                seed=seed
            )
    # print(f"Usage statistics: {completion.usage}")
    return (
        completion
        .choices[0]
        .message.content
    )


def get_picture_description(image_path, context, descriptions=[]):
    """Returns the description of an image."""
    history = ""
    if(len(descriptions) > 0): 
        history = "Here are the descriptions you already used: " + "".join([f"\"{d}\"" for d in descriptions])
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        return get_response(
            prompt=[
                {
                    "type": "text",
                    "text": f"Describe the image. {history} I am providing you with the context of the image to help you describe it.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
                {
                    "type": "text",
                    "text": context,
                },
            ],
            system_message="""You're an expert image descriptor. 
            Provide a short, one sentences, 'alt' text for the image.
            Never use formulas such as "This is an image of..." or "On the screen there is...", get to the point!
            Use Czech language. 
            Try to use similar wording to the context and previous descriptions.
            Do not output anything else than those two sentences.""",
            seed=3
        )




def describe_all_images(markdown_file_path):
    descriptions = []
    file_contents = open(markdown_file_path, "r", encoding="utf8").read()
    lines = file_contents.split("\n")
    amountOfImages = len([line for line in lines if line.startswith("![](")])
    n = 0
    print("Describing images...")
    for i in range(0, len(lines)):
        if(lines[i].startswith("![](")):
            progress_bar(n, amountOfImages)
            image_path = lines[i].split("(")[1].split(")")[0]
            description = get_picture_description(image_path, file_contents, descriptions=descriptions)
            print(f"Image {n+1}/{amountOfImages}: {description}")
            descriptions.append(description)
            lines[i] = f"![{description}]({image_path})"
            n+=1
    output = "\n".join(lines)
    with open(markdown_file_path + "described.md", "w", encoding="utf8") as f:
        f.write(output)
    return output




def progress_bar(current, total):
    """Prints a progress bar."""
    print(f"[{'='*current}{' '*(total-current)}] {current}/{total}", end="\r")

if __name__ == "__main__":
    initConfigFromEnv()
    filename = "H_Pracovnepravni_vztahy.pdf"
    pdftomd(filename)
    describe_all_images(filename + ".md")