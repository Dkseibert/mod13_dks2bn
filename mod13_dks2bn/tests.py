import unittest
from parameterized import parameterized
from typing import Callable
import graphGenerator
import dataFetcher
import timeSeriesFunctions
import userInput
import random
import string
import calendar
from itertools import chain

def generate_random_string(character_set, length):
    characters = list(character_set)
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def generate_random_mixed_string(character_set1, length1, character_set2, length2):
    random_string = generate_random_string(character_set1, length1) + generate_random_string(character_set2, length2)
    random_permutation = list(random_string)
    random.shuffle(random_permutation)
    random_string = ''.join(random_permutation)
    return random_string

def get_test_case_name(testcase_func, _, param):
    test_name = param.args[-1]
    return f"{testcase_func.__name__}_{test_name}"

class timeSeriesFunctions_input_tests(unittest.TestCase):
    random_repeats = 18
    numeric_characters = [str(i) for i in range(0, 10)]
            
    def test_symbol_input(self):
        print("\n==========================")
        print("testing symbol input check")
        print("==========================")
        
        print("\ntesting valid strings: 1-7 uppercase alpha characters\n")
        for i in range(1, 8):
            for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 2):
                s = generate_random_string(string.ascii_uppercase, i)
                self.assertTrue(timeSeriesFunctions.validate_symbol_input(s))
                print(f"string \"{s}\": Valid - OK")
        
        self.assertFalse(timeSeriesFunctions.validate_symbol_input(""))
        print("\ntesting invalid empty string: Invalid - OK")
        
        
        print("\ntesting invalid strings: 8-64 uppercase alpha characters\n")
        s = generate_random_string(string.ascii_uppercase, 8)
        self.assertFalse(timeSeriesFunctions.validate_symbol_input(s))
        print(f"string \"{s}\": Invalid - OK")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats - 1):
            s = generate_random_string(string.ascii_uppercase, random.randint(8, 64))
            self.assertFalse(timeSeriesFunctions.validate_symbol_input(s))
            print(f"string \"{s}\": Invalid - OK")
        
        
        print("\ntesting invalid strings: 1-7 mixed upper and lower case strings\n")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            length = random.randint(1, 7)
            special_length = random.randint(1, max(length - 1, 1))
            upper_length = length - special_length
            
            s = generate_random_mixed_string(string.ascii_lowercase, special_length, string.ascii_uppercase, upper_length)
            
            self.assertFalse(timeSeriesFunctions.validate_symbol_input(s))
            print(f"string \"{s}\": Invalid - OK")
        

        print("\ntesting invalid strings: 1-7 uppercase + numeric strings\n")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            length = random.randint(1, 7)
            numeric_length = random.randint(1, max(length - 1, 1))
            upper_length = length - numeric_length
            
            s = generate_random_mixed_string(timeSeriesFunctions_input_tests.numeric_characters, numeric_length, string.ascii_uppercase, upper_length)
            
            self.assertFalse(timeSeriesFunctions.validate_symbol_input(s))
            print(f"string \"{s}\": Invalid - OK")
        
            
        print("\ntesting invalid strings: 1-7 uppercase + special characters\n")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            length = random.randint(1, 7)
            special_length = random.randint(1, max(length - 1, 1))
            upper_length = length - special_length
            
            s = generate_random_mixed_string(string.punctuation + string.whitespace, special_length, string.ascii_uppercase, upper_length)
            
            self.assertFalse(timeSeriesFunctions.validate_symbol_input(s))
            print(f"string \"{s}\": Invalid - OK")
        print("")
        
    @parameterized.expand([
        (timeSeriesFunctions.validate_chart_input, 1, 2, "testing chart type input check"),
        (timeSeriesFunctions.validate_time_series_input, 1, 4, "testing time series input check")
    ], name_func=get_test_case_name)
    def test_single_numeric_input(self, function_pointer: Callable[[str], bool], minimum: int, maximum: int, test_title: str):
        
        if minimum > maximum or minimum > 9 or maximum > 9 or minimum < 0 or maximum < 0:
            raise ValueError("maximum must be bigger or equal to minimum, maximum and minimum should be a single digit from 0 to 9.")

        print(f"\n{'=' * len(test_title)}")
        print(test_title)
        print(f"{'=' * len(test_title)}")
        
        valid_digits = [f"\"{i}\"" for i in range(minimum, maximum + 1)]
        valid_digits = ", ".join(valid_digits)
        print(f"\ntesting valid strings: {valid_digits}:\n")
        for i in range(minimum, maximum + 1):
            s = str(i)
            self.assertTrue(function_pointer(s))
            print(f"string \"{s}\": Valid - OK")
        
        self.assertFalse(function_pointer(""))
        print("\ntesting invalid empty string: Invalid - OK")
        
        invalid_values = []
        if minimum - 1 >= 0:
            invalid_values = [i for i in range(0, minimum)]
        if maximum + 1 < 10:
            invalid_values = invalid_values + [i for i in range(maximum + 1, 10)]
        invalid_digits = [f"\"{i}\"" for i in invalid_values]
        invalid_digits = ", ".join(invalid_digits)
        print(f"\ntesting invalid strings: {invalid_digits}\n")
        for i in invalid_values:
            s = str(i)
            self.assertFalse(function_pointer(s))
            print(f"string \"{s}\": Invalid - OK")
            

        print("\ntesting invalid strings: 2-64 numeric characters\n")
        s = generate_random_string(timeSeriesFunctions_input_tests.numeric_characters, 2)
        self.assertFalse(function_pointer(s))
        print(f"string \"{s}\": Invalid - OK")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats - 1):
            s = generate_random_string(timeSeriesFunctions_input_tests.numeric_characters, random.randint(2, 64))
            self.assertFalse(function_pointer(s))
            print(f"string \"{s}\": Invalid - OK")
            

        print("\ntesting invalid strings: 1 alpha character\n")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            s = generate_random_string(string.ascii_letters, 1)
            self.assertFalse(function_pointer(s))
            print(f"string \"{s}\": Invalid - OK")
            

        print("\ntesting invalid strings: 1 special character\n")
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            s = generate_random_string(string.punctuation + string.whitespace, 1)
            self.assertFalse(function_pointer(s))
            print(f"string \"{s}\": Invalid - OK")


        print("")
        
    def test_date_string_input(self):
        
        print("\n===============================")
        print("testing date fields input check")
        print("===============================")

        print("\ntesting valid strings: properly formatted YYYY-MM-DD\n")
        
        cal = calendar.Calendar()
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats):
            year = random.randint(0, 3000)
            month = random.randint(1, 12)
            _, n_days = calendar.monthrange(year, month)
            day = random.randint(1, n_days)
            s = f"{year:04d}-{month:02d}-{day:02d}"
            self.assertTrue(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Valid - OK")


        print("\ntesting invalid strings: properly formatted YYYY-MM-DD but invalid dates\n")
        
        # invalid month
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 2):
            year = random.randint(0, 3000)
            month = random.choice(list(i for i in chain(range(-12, 1), range(13, 24))))
            day = random.randint(1, 28)
            s = f"{year:04d}-{month:02d}-{day:02d}"
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")
            
        # invalid day
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 2):
            year = random.randint(0, 3000)
            month = random.randint(1, 12)
            _, n_days = calendar.monthrange(year, month)
            day = random.choice(list(i for i in chain(range(-n_days, 1), range(n_days + 1, n_days * 2))))
            s = f"{year:04d}-{month:02d}-{day:02d}"
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")
            

        print("\ntesting invalid strings: improperly formatted YYYY-MM-DD but valid dates\n")
        
        # invalid year format
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 3):
            year = random.randint(0, 999)
            month = random.randint(1, 12)
            _, n_days = calendar.monthrange(year, month)
            day = random.randint(1, n_days)
            s = f"{year}-{month:02d}-{day:02d}"
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")
            
        # invalid month format
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 3):
            year = random.randint(0, 3000)
            month = random.randint(1, 9)
            _, n_days = calendar.monthrange(year, month)
            day = random.randint(1, n_days)
            s = f"{year:04d}-{month}-{day:02d}"
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")
            
        # invalid day format
        for _ in range(0, timeSeriesFunctions_input_tests.random_repeats // 3):
            year = random.randint(0, 3000)
            month = random.randint(1, 12)
            day = random.randint(1, 9)
            s = f"{year:04d}-{month:02d}-{day}"
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")
        
        print("\ntesting invalid strings: empty string and random strings of numbers, letters, and special characters\n")
        
        for i in range(0, timeSeriesFunctions_input_tests.random_repeats * 2):
            characterSet = []
            match i % 4:
                case 0:
                    characterSet = string.ascii_letters
                case 1:
                    characterSet = timeSeriesFunctions_input_tests.numeric_characters
                case 2:
                    characterSet = string.punctuation + string.whitespace
                case 3:
                    characterSet = string.ascii_letters + "".join(timeSeriesFunctions_input_tests.numeric_characters) + string.punctuation + string.whitespace
                    
            s = generate_random_string(characterSet, 0 if i == 0 else random.randint(1, 16))
            self.assertFalse(timeSeriesFunctions.validate_date_input(s))
            print(f"string \"{s}\": Invalid - OK")

        print("")
        
if __name__ == '__main__':
    unittest.main()
