import pandas as pd;import random;import string;import os;from typing import List, Tuple;from datetime import datetime

def load_and_preprocess(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def swap_word_letters(word: str) -> str:
    if len(word) <= 3: return word
    middle = list(word[1:-1]);random.shuffle(middle)
    return word[0] + ''.join(middle) + word[-1]

def random_case_change(text: str) -> str:
    chars = list(text);num_changes = max(1, int(len(chars) * 0.2))
    positions = random.sample(range(len(chars)), num_changes)
    for pos in positions:
        if chars[pos].isalpha(): chars[pos] = chars[pos].swapcase()
    return ''.join(chars)

def character_perturbations(text: str, perturbation_rate: float = 0.1) -> str:
    if not text or not isinstance(text, str): return text
    words = text.split()
    for i in range(len(words)):
        if random.random() < 0.2: words[i] = swap_word_letters(words[i])
    text = ' '.join(words);chars = list(text);num_perturbations = max(1, int(len(chars) * perturbation_rate))
    perturbation_types = ['swap','insert','delete','substitute','case_change']
    char_map = {'a':['@','4'],'e':['3'],'i':['1','!'],'o':['0'],'s':['5','$'],'t':['7'],'b':['6'],'g':['9'],'l':['1'],'z':['2']}
    for _ in range(num_perturbations):
        if len(chars) < 2: continue
        pos = random.randint(0, len(chars) - 1);perturbation = random.choice(perturbation_types)
        if perturbation == 'swap' and pos < len(chars) - 1: chars[pos],chars[pos + 1] = chars[pos + 1],chars[pos]
        elif perturbation == 'insert':chars.insert(pos,random.choice(string.ascii_letters + string.digits + string.punctuation))
        elif perturbation == 'delete':chars.pop(pos)
        elif perturbation == 'substitute':
            char = chars[pos].lower()
            if char in char_map:chars[pos] = random.choice(char_map[char])
        elif perturbation == 'case_change' and chars[pos].isalpha():chars[pos] = chars[pos].swapcase()
    if random.random() < 0.3: return random_case_change(''.join(chars))
    return ''.join(chars)

def perturb_dataset(input_file: str, output_file: str, text_column: str, perturbation_rate: float = 0.1) -> None:
    try:
        df = load_and_preprocess(input_file)
        df[text_column] = df[text_column].apply(lambda x: character_perturbations(x, perturbation_rate))
        df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

if __name__ == "__main__":
    INPUT_FILE = "test_examples_labels.csv"
    OUTPUT_FILE = f"perturbed_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    TEXT_COLUMN = "test_examples"
    PERTURBATION_RATE = 0.1
    perturb_dataset(INPUT_FILE, OUTPUT_FILE, TEXT_COLUMN, PERTURBATION_RATE)
