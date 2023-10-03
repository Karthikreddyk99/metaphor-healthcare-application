import gradio as gr
import openai
from metaphor_python import Metaphor

# Initializing Metaphor and Openai API's
metaphor = Metaphor("f0b10fe6-8d8b-4af1-87d6-9721526ae403")
openai.api_key = "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"

# Title of the Application
title = "<h1>One Stop for Healthcare Resources</h1> " \
        "<h2>This application is leveraged with Neural search provided by Metaphor API attaching to LLM OPENAI API</h2>"

# Function to find Hospitals based on drug and locations
def hospital_search(disease, city, state, zipcode):
    query = f"I'm looking for the top hospitals for {disease} in {city}, {state}, {zipcode}"
    results = metaphor.search(query, num_results=10, use_autoprompt=True)
    print(results.results[:10])
    hyperlinks = [f"<p><a href='{result.url}'>{result.url}</a></p>" for result in results.results]
    return hyperlinks

# Example inputs for best hospital search
tab1_examples = [
    ["seizures", "San Francisco", "CA", "94107"],
    ["Dogs", "New York", "NY", "10001"],
    ["Fever", "Chicago", "IL", "60601"]
]

# Function to find drug stores based on drug and locations
def drug_search(drug_name, city, state, zipcode):
    query = f"I'm looking for drug stores that carry {drug_name} in {city}, {state} {zipcode}"
    results = metaphor.search(query, num_results=10, use_autoprompt=True)
    print(results.results[:10])
    hyperlinks = [f"<p><a href='{result.url}'>{result.url}</a></p>" for result in results.results]
    return hyperlinks

# Example inputs for how to search for a drug store
tab2_examples = [
    ["Tylenol", "San Francisco", "CA", "94107"],
    ["Aspirin", "New Paltz", "NY", "12561"],
    ["Advil", "Kennett Square", "PA", "19348"]
]

# Function to retrieve the latest healthcare information and summarises with citations.
def latest_info(topic):
    query = f"I'm looking for the latest information on {topic}, such as papers, articles, and other resources"
    results = metaphor.search(query, num_results=10, use_autoprompt=True)
    ids = [result.id for result in results.results]

    # Get contents for all the IDs
    contents_result = metaphor.get_contents(ids)

    # Extract URLs and titles from the results
    urls = [result.url for result in results.results]
    titles = [result.title for result in results.results]

    # Create hyperlinks
    hyperlinks = [f"<p><a href='{url}'>{title}</a></p>" for url, title in zip(urls, titles)]

    # Summarize the content
    first_result = contents_result.contents[0]
    SYSTEM_MESSAGE = "You are a helpful assistant who summarises the content of a webpage and provides a summary with citations of the website so that the user can visit that website. Summarise the feedback from the users."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": first_result.extract},
        ],
    )
    summary = completion.choices[0].message.content

    return hyperlinks, summary


# Example inputs for latest information search
tab3_examples = [
    ["Neuro Science"],
    ["Diabetes"],
    ["immunotherapy"]
]

# Creating the Gradio Blocks interface for Tabs
with gr.Blocks() as demo:
    gr.Markdown(title)

    with gr.Tabs():
        with gr.Tab("Best Hospital Finder"):
            gr.row = gr.Interface(hospital_search,
                                  inputs=["text", "text", "text", "text"],
                                  outputs=gr.outputs.HTML(),
                                  title="Best Hospital Search",
                                  description="Enter a disease and location to find top hospitals. How it searches? I'm looking for the top hospitals for {disease} in {city}, {state}, {zipcode}.",
                                  examples=tab1_examples)

        with gr.Tab("Where to Buy Drugs"):
            gr.row = gr.Interface(drug_search,
                                  inputs=["text", "text", "text", "text"],
                                  outputs=gr.outputs.HTML(),
                                  title="Drug store Finder",
                                  description="Enter a drug you are looking for and location to find drug stores. How it searches? I'm looking for drug stores that carry {drug_name} in {city}, {state} {zipcode}.",
                                  examples=tab2_examples)

        with gr.Tab("Latest Medical Information"):
            gr.row = gr.Interface(latest_info,
                                  inputs=["text"],
                                  outputs=gr.outputs.HTML(),
                                  title="Trending Information in Healthcare. How it searches? I'm looking for the latest information on {topic}, such as papers, articles, and other resources.",
                                  description="Enter a Topic you are looking for to find relevant latest information",
                                  examples=tab3_examples)

if __name__ == "__main__":
    demo.launch()
