from app import lambda_handler

# Mock the AWS event and context
event = {}
context = {}

print("--- Starting Local Test (No Docker) ---")
result = lambda_handler(event, context)
print(result)