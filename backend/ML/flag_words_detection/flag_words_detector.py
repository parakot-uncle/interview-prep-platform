def detect_flag_words(user_answer, flag_words):
    # replacing end splitting the text
    # when newline ('\n') is seen.
    filtered_list = user_answer.split(" ")

    keyword_list = flag_words

    # using set intersection to get number of identical elements
    res = len(set(filtered_list) & set(keyword_list))

    # printing result
    print("Summation of Identical elements : " + str(res))

    num_words = len(keyword_list)

    print("Number of words:")
    print(num_words)
    print("Percentage of similarity:", (res / num_words) * 100)
    percentage_similarity = (res / num_words) * 100

    return percentage_similarity
