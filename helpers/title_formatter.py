def title_formatter(input_string):
    with open('data/title_case_exceptions.txt', 'r') as f:
        title_case_exceptions = [line.strip().lower() for line in f]

    word_list = input_string.split()
    title_case_list = []

    # Always capitalize the first word in the title
    title_case_list.append(word_list[0].capitalize())

    # Capitalize words that are not in the exception list
    for word in word_list[1:]:
        title_case_list.append(word if word.lower(
        ) in title_case_exceptions else word.capitalize())

    return ' '.join(title_case_list)
