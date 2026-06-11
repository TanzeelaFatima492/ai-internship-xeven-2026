
def remove_empty_strings(data):
    """
    Remove empty strings from the list.
    
    Parameters:
    data (list): The list to clean
    
    Returns:
    list: List without empty strings
    """
    cleaned = []
    
    for item in data:
        if item != "":
            cleaned.append(item)
    
    return cleaned

def remove_duplicates(data):
    """
    Remove duplicate items from the list while preserving order.
    
    Parameters:
    data (list): The list to clean
    
    Returns:
    list: List without duplicates
    """
    unique_data = []
    
    for item in data:
        # Check if item is already in unique_data
        found = False
        for existing_item in unique_data:
            if existing_item == item:
                found = True
                break
        
        if not found:
            unique_data.append(item)
    
    return unique_data

def remove_invalid_items(data):
    """
    Remove items that don't match valid categories (names or grades).
    Valid items: strings (names) or single letters (grades A-F) or numbers.
    
    Parameters:
    data (list): The list to clean
    
    Returns:
    list: List with only valid items
    """
    valid_data = []
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    
    for item in data:
        # Keep if it's a string that's not empty
        if isinstance(item, str):
            if len(item) > 0:
                valid_data.append(item)
        # Keep if it's a number
        elif isinstance(item, int) or isinstance(item, float):
            valid_data.append(item)
    
    return valid_data

def convert_to_string(data):
    """
    Convert all items in the list to strings for consistent formatting.
    
    Parameters:
    data (list): The list to convert
    
    Returns:
    list: List with all items as strings
    """
    string_data = []
    
    for item in data:
        string_data.append(str(item))
    
    return string_data

def strip_whitespace(data):
    """
    Remove leading and trailing whitespace from string items.
    
    Parameters:
    data (list): The list to clean
    
    Returns:
    list: List with whitespace removed
    """
    cleaned = []
    
    for item in data:
        if isinstance(item, str):
            cleaned.append(item.strip())
        else:
            cleaned.append(item)
    
    return cleaned

def clean_data_pipeline(data):
    """
    Complete data cleaning pipeline using multiple cleaning functions.
    Applies all cleaning operations in sequence.
    
    Parameters:
    data (list): The messy data to clean
    
    Returns:
    list: Fully cleaned data
    """
    # Step 1: Remove empty strings
    step1 = remove_empty_strings(data)
    print("After removing empty strings:")
    print(step1)
    print()
    
    # Step 2: Strip whitespace
    step2 = strip_whitespace(step1)
    print("After stripping whitespace:")
    print(step2)
    print()
    
    # Step 3: Remove invalid items
    step3 = remove_invalid_items(step2)
    print("After removing invalid items:")
    print(step3)
    print()
    
    # Step 4: Remove duplicates
    step4 = remove_duplicates(step3)
    print("After removing duplicates:")
    print(step4)
    print()
    
    return step4

def separate_by_type(data):
    """
    Separate cleaned data into names and grades.
    
    Parameters:
    data (list): The cleaned data
    
    Returns:
    tuple: (names_list, grades_list)
    """
    names = []
    grades = []
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    
    for item in data:
        item_str = str(item)
        
        # Check if it's a grade
        if item_str in valid_grades:
            grades.append(item_str)
        else:
            # It's a name or number
            names.append(item_str)
    
    return names, grades

def display_cleaned_data(data):
    """
    Display the cleaned data with statistics.
    
    Parameters:
    data (list): The cleaned data
    """
    print("="*50)
    print("CLEANED DATA SUMMARY")
    print("="*50)
    print(f"Total items: {len(data)}")
    print(f"Items: {data}")
    print()
    
    names, grades = separate_by_type(data)
    
    print(f"Names: {names}")
    print(f"Grades: {grades}")
    print("="*50)

# Run the complete cleaning pipeline
cleaned = clean_data_pipeline(messy_data)

# Display final results
display_cleaned_data(cleaned)