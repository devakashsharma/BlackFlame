from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    if not text.strip():
        return "Nothing to summarize."

    # Break into chunks if needed
    chunks = []
    max_chunk_size = 1500  # characters
    while len(text) > max_chunk_size:
        chunks.append(text[:max_chunk_size])
        text = text[max_chunk_size:]
    chunks.append(text)

    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            summaries.append(f"⚠️ Error: {str(e)}")

    return "\n".join(summaries)