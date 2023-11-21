import openai
from pyaxidraw import axidraw
import os

save_directory = '/Users/benramos/Desktop/gpt_drawings'
openai.api_key = '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'
ad = axidraw.AxiDraw()

while True:
    user_input = input("Please provide a prompt (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break

    custom_instructions = "Create an SVG representation with a 2-inch by 2-inch page size of the following:\n" + user_input + ". Never draw a border and never use text."
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates SVG representations."},
            {"role": "user", "content": custom_instructions}
        ]
    )

    response_content = completion.choices[0].message['content']
    start_index = response_content.find('<svg')
    end_index = response_content.find('</svg>', start_index) + len('</svg>')
    chatgpt_svg_content = response_content[start_index:end_index]

    chatgpt_svg_file = os.path.join(save_directory, user_input.replace(" ", "_") + ".svg")
    with open(chatgpt_svg_file, 'w') as svg_file:
        svg_file.write(chatgpt_svg_content)
    
    ad.plot_setup(chatgpt_svg_file)
    ad.plot_run()

print("Goodbye!")
