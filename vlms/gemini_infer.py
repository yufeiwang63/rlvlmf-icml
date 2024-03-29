import pathlib
import textwrap
import os
from PIL import Image
import google.generativeai as genai
import time
from io import BytesIO
from matplotlib import pyplot as plt
import numpy as np

genai.configure(api_key=os.environ["Gemini_API_Key"])


model = genai.GenerativeModel('gemini-pro-vision')
text_model = genai.GenerativeModel('gemini-pro')

# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("What is the meaning of life?")
# print(response.text)

def add_title_to_image(image, text):
    
    # Create a figure and axis to plot on
    fig, ax = plt.subplots()

    # Plot your data (example: simple line)
    ax.imshow(image)

    # Add title or any other plot decorations here

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Load this image into PIL and convert to NumPy array
    image = Image.open(buf)
    image_array = np.array(image)

    # Close the figure to free memory

    # remove axis and white space
    plt.close(fig)

    # Now `image_array` is a NumPy array representation of the plot
    return image_array

def gemini_query(query_list, temperature=0, key="left:right", return_text=False):
    key_1 = key.split(":")[0]
    key_2 = key.split(":")[1]
    
    beg = time.time()
    success = False
    try_cnt = 0
    while not success:
        try:
            response = model.generate_content(query_list,
                                            generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    # candidate_count=1,
                    # stop_sequences=['x'],
                    # max_output_tokens=20,
                    temperature=temperature)
            )

            response.resolve()
            success = True
        except:
            print("gemini retrying...")
            try_cnt += 1
            time.sleep(3)
            if try_cnt >= 3:
                break


    end = time.time()
    print("time elapsed: ", end - beg)
    if success:      
        # print(response.text)
        if return_text:
            return response.text
          
        for line in response.text.split("\n"):
            if "output:" in line.lower()    :
                if key_1 in line.lower():
                    return 0
                elif key_2 in line.lower():
                    return 1
                elif "unsure" in line.lower():
                    return -1
        return -1
    else:
        if return_text:
            return ""
        return -1 
        
def gemini_query_1(query_list, temperature=0):
    beg = time.time()

    success = False
    try_cnt = 0
    while not success:
        # try:
            response = model.generate_content(query_list,
            # response = model.generate_content([prompt, image1, image2],
                                            generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    # candidate_count=1,
                    # stop_sequences=['x'],
                    # max_output_tokens=20,
                    temperature=temperature),
                safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS",
                            "threshold": "BLOCK_NONE",
                        },
                    ]
            )

            response.resolve()
            success = True    
        # except:
        #     print("gemini retrying...")
        #     time.sleep(3)
        #     try_cnt += 1
        #     if try_cnt >= 5:
        #         break

    

    end = time.time()
    print("time elapsed: ", end - beg)
    if success:
        try:
            # print("response: ")
            # print(response.text)
            return response.text.split("\n")[-1].strip().lstrip()
        except:
            return -1
    else:
        return -1

def gemini_query_2(query_list, summary_prompt, temperature=0):
    beg = time.time()

    success = False
    try_cnt = 0
    while not success:
        try:
            response = model.generate_content(query_list,
            # response = model.generate_content([prompt, image1, image2],
                                            generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    # candidate_count=1,
                    # stop_sequences=['x'],
                    # max_output_tokens=20,
                    temperature=temperature),
                safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS",
                            "threshold": "BLOCK_NONE",
                        },
                    ]
            )

            response.resolve()
    
            # import pdb; pdb.set_trace()
            summary_response = text_model.generate_content(
                    summary_prompt.format(response.text),
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                    ),
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE",
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS",
                            "threshold": "BLOCK_NONE",
                        },
                    ]
            )
            summary_response.resolve()
            success = True    
        except:
            print("gemini retrying...")
            time.sleep(2)
            try_cnt += 1
            if try_cnt >= 3:
                break

    

    end = time.time()
    print("time elapsed: ", end - beg)
    if success:
        try:
            # print("response: ")
            # print(response.text)
            # print("summary response: ")
            # print(summary_response.text)
            return summary_response.text.split("\n")[0].strip().lstrip()
        except:
            return -1
    else:
        return -1

if __name__ == "__main__":
    from prompt import (
        gemini_free_query_env_prompts, gemini_summary_env_prompts,
        gemini_free_query_prompt1, gemini_free_query_prompt2,

    ) 
    import numpy as np
    from matplotlib import pyplot as plt

    def process_image(image):
        # image = np.array(image)
        mask1 = (image[:, :, 0] == 255) & (image[:, :, 1] == 255) & (image[:, :, 2] == 255)
        mask2 = (image[:, :, 0] == 0) & (image[:, :, 1] >= 170) & (image[:, :, 2] == 0)
        mask = mask1 | mask2
        # import pdb; pdb.set_trace()
        # image = image[mask]
        image[~mask] = (0, 0, 0)
        return image

    image_path = "data/images/metaworld_sweep-into-v2/image_30_combined.png"
    # image_path = "data/images/metaworld_sweep-into-v2/image_5_combined.png"
    image = Image.open(image_path)
    image = np.array(image)[100:, :, :]
    # image = process_image(image)
    # plt.imshow(image)
    # plt.show()
    image = Image.fromarray(image)

    image_1_path = "data/images/metaworld_sweep-into-v2/image_5_1.png"
    image_2_path = "data/images/metaworld_sweep-into-v2/image_5_2.png"
    # image_1_path = "data/images/metaworld_sweep-into-v2/image_30_1.png"
    # image_2_path = "data/images/metaworld_sweep-into-v2/image_30_2.png"
    image_1_path = "data/images/metaworld_sweep-into-v2/image_6_1.png"
    image_2_path = "data/images/metaworld_sweep-into-v2/image_6_2.png"
    image_1 = Image.open(image_1_path)
    image_2 = Image.open(image_2_path)

    env_name = "metaworld_sweep-into-v2"
    gemini_query_2(
    [
        gemini_free_query_prompt1,
        image_1, 
        gemini_free_query_prompt2,
        image_2, 
        gemini_free_query_env_prompts[env_name]
    ],
        gemini_summary_env_prompts[env_name]
    )
    # gemini_query_2(image_2, image_1, prompt, temperature=0)
