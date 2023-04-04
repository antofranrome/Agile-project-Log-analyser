import re

# Define the log string
log = "YOUR_LOG_STRING_HERE"

# Define regular expression patterns to match the message type, message data structure, and constraints
message_type_pattern = r"message type:\s+'(\w+)'"
message_structure_pattern = r"message data structure:\s+{([^}]+)}"
constraint_pattern = r"constraints:\s+\(([^)]+)\)"

# Compile the patterns for improved performance
message_type_regex = re.compile(message_type_pattern)
message_structure_regex = re.compile(message_structure_pattern)
constraint_regex = re.compile(constraint_pattern)

# Use the regex to search for the patterns in the log string
message_type_match = message_type_regex.search(log)
message_structure_match = message_structure_regex.search(log)
constraint_match = constraint_regex.search(log)

# If a match is found, extract the desired data using group()
if message_type_match:
    message_type = message_type_match.group(1)
else:
    message_type = None

if message_structure_match:
    message_structure = message_structure_match.group(1)
else:
    message_structure = None

if constraint_match:
    constraints = constraint_match.group(1)
else:
    constraints = None

# Print the extracted data
print("Message Type: ", message_type)
print("Message Structure: ", message_structure)
print("Constraints: ", constraints)
