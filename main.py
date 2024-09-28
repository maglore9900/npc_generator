from modules import adapter


ad = adapter.Adapter("openai")

# print(ad.chat("What is the capital of France?"))
# print("----")
# print(ad.chat("What is the capital of France?", "alice"))
# print("----")
# print(ad.chat("What is the capital of France?", "bob"))
# print("----")
# print(ad.chat("What is the capital of France?", "charlie"))

print(ad.chat("Excuse me I am lost, can you tell me how to get to the townsquare?", "test"))