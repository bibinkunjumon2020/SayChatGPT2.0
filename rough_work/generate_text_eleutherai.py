# from transformers import pipeline

# def generate_text_eleutheraai():
#     generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
#     response=generator("hi",do_sample=True,min_length=50)
#     print(response['generated_text'])

# generate_text_eleutheraai()

from transformers import GPT2Tokenizer, TFGPT2Model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
model = TFGPT2Model.from_pretrained('gpt2-medium')
text = "hi"
encoded_input = tokenizer(text, return_tensors='tf')
output = model(encoded_input)

response_text = tokenizer.decode(output[0][0].numpy()[0], skip_special_tokens=True)
print(response_text)