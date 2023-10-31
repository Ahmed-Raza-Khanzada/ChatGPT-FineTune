# import openai
import json
from bs4 import BeautifulSoup
# Set your OpenAI API token
# api_key = "YOUR_API_KEY"
# openai.api_key = api_key

# Sample data


data = json.load(open("Final_Ticket_messages.json"))

def clean_html(message):
    soup = BeautifulSoup(message, 'html.parser')
    text = soup.get_text()
    return text

unique_ticket_ids = set()

# Iterate through the list and add unique Thread IDs to the set
for ticket_id in data:
    unique_ticket_ids.add(ticket_id["Thread ID"])

# Convert the set back to a list if needed
unique_ticket_ids_list = list(unique_ticket_ids)
train_part = int(0.9 * len(unique_ticket_ids_list))

train_data = unique_ticket_ids_list[:train_part]
val_data = unique_ticket_ids_list[train_part:]
def check_message(current_conversation):
    assistant = False
    user = False
    local_words = 0
    for h in current_conversation:
        if h["role"] == "assistant":
            assistant =True
        if h["role"] == "user":
            user = True
        local_words += len(h["content"].split(" "))
        if assistant and user:
            break
    if assistant and user:
        return True,local_words
    return False, local_words
def get_data(data, data1,chat_limit = 100000):
    training_data = []
    current_conversation = []
    no_of_tokens = 0
    current_ticket_id = None
    def check_var(var):
        if var==None:
            return "NA"
        return var.strip()
    for message in data:
        ticket_id = message["Thread ID"]
        if ticket_id not in data1:
             continue
        if len(training_data) >= chat_limit:
            break
        if ticket_id != current_ticket_id:
            if current_conversation:
                flag,local_tokens = check_message(current_conversation)
                if flag:
                    no_of_tokens += local_tokens
                    training_data.append({"messages": current_conversation})
                else:
                    
                    current_conversation = []
                    continue
            current_conversation = []
            model,manufacturer,year_of_manufactured,ecu_number = message["Model"],message["Manufacturer"],message["Year of Manufacture"],message["ECU Number"]
            model,manufacturer,year_of_manufactured,ecu_number = check_var(model),check_var(manufacturer),check_var(year_of_manufactured),check_var(ecu_number)
            current_conversation.append({"role": "system", "content": f"You are an assistant from staff that responds to Clients queries\nhere are their vehicle details:\nModel:{model}\nManufacturer:{manufacturer}\nYear of Manufature:{year_of_manufactured}\nECU Number:{ecu_number}\n"})
            current_ticket_id = ticket_id

        role = "user" if message["Message Type"] == "User Message" else "assistant"
        message = " ".join(clean_html(message["Message Content"]).split("\u00a0"))
        current_conversation.append({"role": role, "content": message})

    if current_conversation:
        flag ,local_tokens= check_message(current_conversation)
        if flag:
            no_of_tokens += local_tokens
            training_data.append({"messages": current_conversation})
        else:
          
            current_conversation = []
    print("No_Of_Tokens: ", no_of_tokens)
    return training_data
train_smaple_size = 1000
val_sample_size = 100
if train_smaple_size > len(train_data):
    train_smaple_size = len(train_data)
if val_sample_size > len(val_data):
    val_sample_size = len(val_data)
print("*"*20,"Training Data ","*"*20)
training_data = get_data(data, train_data,chat_limit=train_smaple_size)
print("Training Data goted",)
print("Creating file for Training Data")
# Write training data to a JSONL file
with open(f'training_data_{train_smaple_size}.jsonl', 'w') as jsonl_file:
    for entry in training_data:
        jsonl_file.write(json.dumps(entry) + '\n')


print("Training Data File Created")
print("*"*20,"Validation Data","*"*20)
print("Creating file for Validation Data")
validation_data = get_data(data, val_data,chat_limit=val_sample_size)
print("Validation Data goted",)
print("Creating file for Validation Data")
# Write validation data to a JSONL file
with open(f'validation_data_{val_sample_size}.jsonl', 'w') as jsonl_file:
    for entry in validation_data:
        jsonl_file.write(json.dumps(entry) + '\n')
print("Validation Data File Created")
print(len(training_data), len(validation_data))
print("Done Creating JSONL Files")



# # Train the model
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=training_data,
# )

# # Print the model's reply
# print(response['choices'][0]['message']['content'])
