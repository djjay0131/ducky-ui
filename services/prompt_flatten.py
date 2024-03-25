def convert_multiline_to_single_line(text):
    # Replace the newline character `\n` with the literal string "/n"
    single_line_text = text.replace('\n', '\\n')
    return single_line_text



# Assuming external_module.py is in the same directory or in your Python path
import prompts
import inspect

# Function to call all user-defined functions in an external module with parameters formatted as requested
def call_all_functions(module):
    for name in dir(module):  # Iterate through everything defined in the module
        obj = getattr(module, name)  # Get the object by name
        if inspect.isfunction(obj):  # Check if it's a function
            if not name.startswith('_'):  # Optionally, skip 'private' functions
                try:
                    # Get function signature
                    sig = inspect.signature(obj)
                    # Build arguments dictionary with parameter names as both keys and values, formatted as requested
                    args = {param: f"{{{param}}}" for param in sig.parameters}
                    # Print the function name before calling it
                    print(f"Calling function '{name}':")
                    # Attempt to call the function with the constructed arguments
                    # Assuming convert_multiline_to_single_line is defined elsewhere and handles function output
                    print(convert_multiline_to_single_line(obj(**args).strip()))
                    # Print a blank line after calling the function for visual separation
                    print()
                except TypeError as e:
                    print(f"Function '{name}' invocation failed or it requires special arguments, error: {e}")

# Example usage
if __name__ == "__main__":
    call_all_functions(prompts)
