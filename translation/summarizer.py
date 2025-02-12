from transformers import T5Tokenizer, T5ForConditionalGeneration

def summarize_text(input_text, model_name='t5-small', max_length=150, min_length=40, length_penalty=2.0, num_beams=4):
    """
    Summarize the input text using a transformer-based model.

    Parameters:
        input_text (str): The text to be summarized.
        model_name (str): The pre-trained model to use (default: 't5-small').
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.
        length_penalty (float): Penalty for longer summaries.
        num_beams (int): Number of beams for beam search.

    Returns:
        str: The generated summary.
    """
    # Load the tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Preprocess the input text
    input_text = "summarize: " + input_text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(
        input_ids,
        max_length=max_length,
        min_length=min_length,
        length_penalty=length_penalty,
        num_beams=num_beams,
        early_stopping=True
    )

    # Decode and return the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    # Example text to summarize
    input_text = (
        "The Transformer model, introduced in the paper 'Attention Is All You Need', is widely used in NLP tasks. "
        "It employs a self-attention mechanism to process sequential data efficiently. Variants like BERT, GPT, and T5 "
        "have been developed for tasks such as text generation, translation, and summarization."
    )

    # Generate summary
    summary = summarize_text(input_text)
    print("Original Text:")
    print(input_text)
    print("\nGenerated Summary:")
    print(summary)
