import streamlit as st
import time  # Import the time module
from scrape import (
    scrape_website,
    split_dom_content,
    clear_body_content,
    extract_body_content
)
from parse import (
    parse_with_ollama,
    get_model
)

st.title("AI Web Scrapper")
url = st.text_input("Enter a website URL:")

if st.button("Scraper Site:"):
    st.write("Scrapping the website")
    
    result = scrape_website(url)
    print(result)
    body_content = extract_body_content(result)
    cleaned_content = clear_body_content(body_content)
    
    st.session_state.dom_content = cleaned_content
    
    # Collapsible tab
    with st.expander("View Dom Content"):
        st.text_area("Dome Content", cleaned_content, height=300)
    
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")
            
            start_time = time.time()  # Start the timer
            
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            
            end_time = time.time()  # End the timer
            time_taken = end_time - start_time  # Calculate the time taken
            
            st.write(result)
            st.write(f"Time taken: {time_taken:.2f} seconds | Model used-> {get_model()}")