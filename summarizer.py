from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    if not text.strip():
        return "Nothing to summarize."

    # Reduce text to fit model capacity
    text = text[-1500:]  # Last 1500 characters (approx 300-400 words)

    try:
        summary = summarizer(text, max_length=120, min_length=40, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"⚠️ Error during summarization: {str(e)}"
