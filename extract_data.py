import re

log = "Sample log message containing message type: 'data', message data structure: {key1: value1, key2: value2}, and constraints: (constraint1, constraint2)"

# Regular expression pattern to match the message type
message_type_pattern = r"message type:\s+'(\w+)'"

# Regular expression pattern to match the message data structure
message_structure_pattern = r"message data structure:\s+{([^}]+)}"

# Regular expression pattern to match the constraints
constraint_pattern = r"constraints:\s+\(([^)]+)\)"

# Extracting the message type
message_type = re.search(message_type_pattern, log).group(1)

# Extracting the message data structure
message_structure = re.search(message_structure_pattern, log).group(1)

# Extracting the constraints
constraints = re.search(constraint_pattern, log).group(1)

# Printing the extracted data
print("Message Type: ", message_type)
print("Message Structure: ", message_structure)
print("Constraints: ", constraints)
