from transliteration import russian, emojis, special_chars, numbers
from string import ascii_lowercase


class transliterationClass:
    def __init__(self):
        self.master_dict = {
            **russian.russian_to_latin,
            **emojis.letter_emoji_to_text,
            **special_chars.all_special_characters,
            **numbers.numbers_to_text
        }

    def transliterate(self, text):
        text = text.lower()
        filtered_text =  ''.join([self.master_dict.get(char, char) for char in text]).lower()
        ascii_filtered_text = ''.join([char for char in filtered_text if char in ascii_lowercase]) 
        return ascii_filtered_text
    
class filterClass:
    def __init__(self):
        self.weights = {x[0]: float(x[1]) for x in [x.split(':') for x in open('weights.txt').read().splitlines()]}
    def calculateDistance(self, text1, text2):
        score = 0
        text1, text2 = min(text1, text2), max(text1, text2)
        for enum, letter in enumerate(text1):
            if letter == text2[enum]:
                score += 1
            elif letter in text2[enum-1:enum+1:2]:
                score += 0.5
        return score/len(text1)

    def determineResemblance(self, text):
        violating_pairs = []
        score = 0
        for item, weight in self.weights.items():
            for enum, letter in enumerate(text):
                if enum + len(item) > len(text):
                    break
                distance = self.calculateDistance(item, text[enum:enum+len(item)])
                if distance > 0.5:
                    violating_pairs.append((item, weight, distance))
                    break
        for violation in violating_pairs:
            score += violation[1] * violation[2]
        return score
transliteration = transliterationClass()
filter = filterClass()

for username in open('usernames.txt', 'r', encoding='utf-8').read().splitlines():
    text_view = transliteration.transliterate(username)
    print(username, text_view, filter.determineResemblance(text_view))
