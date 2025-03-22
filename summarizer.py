from transformers import pipeline  # Importing the pipeline module from Hugging Face Transformers

# Load the pre-trained Hugging Face summarization model (BART model for summarization)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize the provided text
def summarize_text(text):
    # Check if the provided text is empty or None
    if not text:
        return "No content available."  # Return a default message if the text is empty

    try:
        # Use the summarizer pipeline to generate a summary of the text
        # max_length: Maximum number of words in the summary
        # min_length: Minimum number of words in the summary
        # do_sample=False: Ensures deterministic output (no random sampling)    
        result = summarizer(text, max_length=100, min_length=30, do_sample=False)
        
        # Return the summarized text
        return result[0]['summary_text']
    
    except Exception as e:
        # If an error occurs during summarization, return an error message
        return f"Summarization Error: {str(e)}"
