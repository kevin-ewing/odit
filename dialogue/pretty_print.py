import os

def pprint(string):
    columns, rows = os.get_terminal_size()
    final_string = ""
    split_string = string.split(" ")
    num_words = len(split_string)
    if num_words == 0:
        return string
    elif num_words == 1:
        return string
    else:
        curr_len = 0
        curr_break = columns - 5

        for x in range(num_words):
            curr_len = curr_len + len(split_string[x])
            if x == 0:
                pass
            else:
                if curr_len >= curr_break:
                    curr_len = curr_break
                    curr_break = curr_break + columns - 10
                    final_string = final_string + split_string[x-1] + "\n"
                else:
                    curr_len += 1
                    final_string = final_string + split_string[x-1] + " "

        final_string = final_string + split_string[-1] 
    return final_string


# if __name__ == "__main__":
#     print(pprint("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."))