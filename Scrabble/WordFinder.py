word_list = [ "hi", "bye", "eye"]
player_letters_global = "be?i"

# During the loop, can we stomp on the letters in word_list?
# Reference vs. value semantics

# for word_list_word in word_list:
#     word_list_letter_match = 0
#     for word_list_letter in word_list_word:
#         if word_list_letter in player_letters:
#             # TODO: Remove this letter from the player's list
#             word_list_letter_match = word_list_letter_match + 1
#             if word_list_letter_match == len(word_list_word):
#                 print(word_list_word)
#         else:
#             break


def match_word(player_letters):
    for word_list_word in word_list:
        word_list_letter_match = 0
        word_list_word_length = len(word_list_word)
        player_letters_temp = player_letters
        player_letters_length = len(player_letters_temp)

        for i in range(player_letters_length):
            for j in range(word_list_word_length):
                if player_letters_temp[i] == word_list_word[j] or player_letters_temp[i] == "?":
                    word_list_letter_match = word_list_letter_match + 1
                    player_letters_temp = player_letters_temp[0:i] + "." + player_letters_temp[i + 1:player_letters_length]
                    if word_list_letter_match == len(word_list_word):
                        print(word_list_word)
                        print(player_letters_temp)
 
match_word(player_letters_global)
            
    
