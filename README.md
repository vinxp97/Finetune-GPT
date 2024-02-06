# Finetune-GPT

Fine-tuning scripts that create jsonls from Excel datasets for OpenAIs text-models (babbage/davinci) and chat-models (GPT-3.5-turbo/GPT-4). 

# Purpose

The script ingests a file using pandas, and can be edited to support csv. Natively supports xlsx. For each row in the dataset, it will iterate through each of the templates (either text or chat-based templates) and create a json-object that identifies  a prompt/completion pair (for LLMs), or, a system/user/assistant object (for Chat Models). These pairings help influence the output of the model(s) when similar inputs are submitted to the fine-tuned models.
