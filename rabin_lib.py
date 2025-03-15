import random
import string
import itertools
import math
import hashlib
from datetime import datetime

# 检查是否为素数
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# 生成素数 p 和 q，满足 p != q 且 p ≡ q ≡ 3 mod 4
def miyao():
    while True:
        p = 4 * random.randint(100, 10000) + 3
        q = 4 * random.randint(100, 10000) + 3
        if p != q and is_prime(p) and is_prime(q):
            return p, q

# 转换字符串为Unicode码列表
def string_to_unicode(s):
    return [ord(c) for c in s]

# 加密过程

def JiaMi(unicode_ints, p, q):
    """
    使用给定的素数 p 和 q 对输入的Unicode整数列表进行加密。
    
    参数:
        unicode_ints (list of int): 输入的Unicode整数列表。
        p (int): 素数 p。
        q (int): 素数 q。
    
    返回:
        tuple: 包含密文列表和商列表的元组。shang[]可用于当明文
        Unicode码值远大于p*q时，保存倍数关系，使得便于还原，即：m=k*n+c,其中m为明文，k为商，n为p*q，c为密文
    """
    n = p * q
    miwen = []
    shang = []
    for m in unicode_ints:
        c_m = pow(m, 2, n)
        k_m = m // n
        miwen.append(c_m)
        shang.append(k_m)
    return miwen, shang


# 解密过程
def JieMi(miwen, p, q, shang):
    n = p * q
    characters = []     # 存储解密后的字符
    
    def Getst(a, b):   # 扩展欧几里得算法，用于计算逆元
        if b == 0:
            return 1, 0
        else:
            s1, t1 = Getst(b, a % b)
            s = t1
            t = s1 - (a // b) * t1
            return s, t
    
    s, t = Getst(p, q)   # 获取扩展欧几里得结果
    
    for i in range(len(miwen)):
        c = miwen[i]
        k = shang[i]
        m_mod_p = c % p
        m_mod_q = c % q
        
        try:
            m_sqrt_p = pow(m_mod_p, (p + 1) // 4, p)  # 计算模p的平方根
            m_sqrt_q = pow(m_mod_q, (q + 1) // 4, q)  # 计算模q的平方根
        except:
            characters.append([])  # 如果无法计算平方根，返回空列表
            continue
        
        M1 = (m_sqrt_p * t * q + m_sqrt_q * s * p) % n + n * k
        M2 = (m_sqrt_p * t * q - m_sqrt_q * s * p) % n + n * k
        M3 = (-m_sqrt_p * t * q + m_sqrt_q * s * p) % n + n * k
        M4 = (-m_sqrt_p * t * q - m_sqrt_q * s * p) % n + n * k
        
        characters.append([M1, M2, M3, M4])
    
    return characters


# 标签方式一：在每个字符后添加一个随机字母
def add_random_letter_to_string(input_string, letter_range):
    result = ''
    for char in input_string:
        random_letter = random.choice(letter_range)
        random_letter_code = f"{ord(random_letter):04d}"
        combined_code = f"{ord(char)}{random_letter_code}"
        combined_code_int = int(combined_code)
        result += str(combined_code_int) + " "
    return result.strip()

# 将字符串Unicode码以整数形式返回每个组合码,用于加密解密计算
def string_to_unicode_with_tuple(s):
    unicode_ints = []
    for code_str in s.split():
        try:
            code_int = int(code_str)
            unicode_ints.append(code_int)
        except ValueError:
            pass
    return unicode_ints

# 将解密后的整数分割为字符和字母的 Unicode 码
def split_code(m, letter_digits=4):
    m_str = str(m)
    if len(m_str) <= letter_digits:
        return None, None  # 不足以分割出字符和字母部分
    
    letter_code_str = m_str[-letter_digits:]
    char_code_str = m_str[:-letter_digits]
    try:
        char_code = int(char_code_str)
        letter_code = int(letter_code_str)
        return char_code, letter_code
    except ValueError:
        return None, None


# 标签方式一：筛选解密结果，返回符合条件的所有组合
def filter_decrypt_combinations(decrypted_chars, mark_range, letter_digits=4):
    valid_combinations = []
    valid_options_per_char = []
    
    for decryptions in decrypted_chars:
        valid_options = []
        for m in decryptions:
            char_code, letter_code = split_code(m, letter_digits)
            if char_code is None or letter_code is None:
                continue
            try:
                letter = chr(letter_code)
                char = chr(char_code)
            except ValueError:
                continue
            # 如果字母在指定的标记范围内，保存该解
            if letter in mark_range:
                valid_options.append(char + letter)
        if not valid_options:
            # 如果某个字符没有符合条件的解，整个组合无效
            return []
        valid_options_per_char.append(valid_options)
    
    all_combinations = list(itertools.product(*valid_options_per_char))
    for combination in all_combinations:
        combination_str = ''.join(combination)
        valid_combinations.append(combination_str)
    
    return valid_combinations

# 获取限制字母范围
def get_reduced_alphabet(start='a', end='f'):
    return string.ascii_lowercase[string.ascii_lowercase.index(start):string.ascii_lowercase.index(end) + 1]

# 移除字符串中的指定范围字母，因为每个字符后都加了一个随机字母，所以取偶数位为结果，索引index从0开始
def remove_letters_from_string(s):
    result = ''
    for index,char in enumerate(s):
        if index%2==1:
            continue       
        result += char
    return result


# 标签方式二：在每个字符前添加序列号和校验和
def add_sequence_and_checksum_to_string(input_string):
    result = []
    for i, char in enumerate(input_string):
        seq_num = int(f"{i:04d}")
        char_code = int(ord(char))
        checksum_full = hashlib.sha256(f"{seq_num}{char_code}".encode()).hexdigest()
        checksum_int = int(checksum_full[:4], 16)
        checksum = f"{checksum_int:04d}"[-4:]
        combined_code = f"{seq_num}:{checksum}:{char_code}"
        result.append(combined_code)
    return ' '.join(result)

# 将组合编码分割为前八位和char_code部分
def split_encoding(encoded_string):
    """
    将每个字符的组合编码分为前八位（seq_num:checksum）和后面的编码（char_code）。
    返回两个列表：prefixes 和 char_codes。
    """
    prefixes = []
    char_codes = []
    for part in encoded_string.split():
        try:
            seq_num, checksum, char_code = part.split(':')
            prefixes.append(f"{seq_num}:{checksum}")
            char_codes.append(int(char_code))
        except ValueError:
            # 如果格式不正确，跳过该部分
            continue
    return prefixes, char_codes

# 标签方式二：将前八位与解密后的编码拼接并进行校验
def combine_and_verify(prefixes, decrypted_char_codes):
    valid_combinations = []
    
    for i, (prefix, decryptions) in enumerate(zip(prefixes, decrypted_char_codes)):
        try:
            seq_num, checksum = prefix.split(':')
            seq_num = int(seq_num)
        except ValueError:
            return []
        
        valid_options = []
        for m in decryptions:
            char_code = int(m)
            checksum_full = hashlib.sha256(f"{seq_num}{char_code}".encode()).hexdigest()
            calculated_checksum_int = int(checksum_full[:4], 16)
            calculated_checksum = f"{calculated_checksum_int:04d}"[-4:]
            
            if checksum == calculated_checksum:
                try:
                    char = chr(char_code)
                    valid_options.append(char)
                except ValueError:
                    continue
        
        if not valid_options:
            return []
        
        valid_combinations.append(valid_options)
    
    all_combinations = [''.join(p) for p in itertools.product(*valid_combinations)]
    return all_combinations

# 标签方式三，时间戳

def generate_timestamp():
    """
    生成当前时间的12位时间戳，格式为YYYYMMDDHHMM。
    """
    return datetime.now().strftime('%Y%m%d%H%M')

def add_timestamp_to_unicode(input_text):
    """
    为每个Unicode编码后添加一个12位时间戳，返回带时间戳的Unicode编码列表和时间戳列表。
    
    参数:
        unicode_ints (list of int): 原始Unicode编码列表。
    
    返回:
        tuple: (带时间戳的Unicode编码列表, 时间戳列表)
    """
    unicode_with_timestamps = []
    timestamps = []
    # 将输入字符串转换为Unicode编码列表
    unicode_ints = [ord(c) for c in input_text]

    for m in unicode_ints:
        timestamp = generate_timestamp()
        combined_code = int(f"{m}{timestamp}")
        unicode_with_timestamps.append(combined_code)
        timestamps.append(timestamp)
    return unicode_with_timestamps, timestamps

def strip_timestamp_from_unicode(unicode_with_timestamps):
    """
    从带时间戳的Unicode编码中剥离出原始Unicode编码和时间戳。
    
    参数:
        unicode_with_timestamps (list of int): 带时间戳的Unicode编码列表。
    
    返回:
        tuple: (原始Unicode编码列表, 时间戳列表)
    """
    original_unicode = []
    extracted_timestamps = []
    for combined in unicode_with_timestamps:
        combined_str = str(combined)
        if len(combined_str) <= 12:
            # 无法剥离出时间戳
            original_unicode.append(None)
            extracted_timestamps.append(None)
            continue
        timestamp = combined_str[-12:]
        unicode_str = combined_str[:-12]
        try:
            unicode_val = int(unicode_str)
            original_unicode.append(unicode_val)
            extracted_timestamps.append(timestamp)
        except ValueError:
            original_unicode.append(None)
            extracted_timestamps.append(None)
    return original_unicode, extracted_timestamps

def verify_and_extract_characters(correct_timestamps, decrypted_chars):
    """
    比对剥离后的时间戳与存储的时间戳，返回正确的字符列表。
    
    参数:
        correct_timestamps (list of str): 原始时间戳列表。
        decrypted_unicode_with_timestamps (list of int): 解密后的带时间戳的Unicode编码列表。
    
    返回:
        list: 符合时间戳的正确字符（带时间戳）列表和剥离后的字符列表。
    """
    valid_chars_with_timestamps = []
    valid_chars = []
    
    for idx, decryptions in enumerate(decrypted_chars):
        current_valid_chars_with_ts = []
        current_valid_chars = []
        expected_ts = correct_timestamps[idx]

        for decrypted in decryptions:
            decrypted_str = str(decrypted)
            if len(decrypted_str) <= 12:
                continue  # 无法剥离出时间戳
            timestamp = decrypted_str[-12:]
            unicode_str = decrypted_str[:-12]

            if timestamp != expected_ts:
                continue  # 时间戳不匹配

            try:
                unicode_val = int(unicode_str)
                char = chr(unicode_val)
                current_valid_chars_with_ts.append(f"{char}{timestamp}")
                current_valid_chars.append(char)
            except (ValueError, OverflowError):
                continue  # 无效的Unicode编码

        if not current_valid_chars:
            # 如果某个字符位置没有符合条件的解，整个解密无效
            return [], [], []

        valid_chars_with_timestamps.append(current_valid_chars_with_ts)
        valid_chars.append(current_valid_chars)

    # 生成所有可能的解密组合
    all_combinations = list(itertools.product(*valid_chars))
    all_valid_combinations = [''.join(comb) for comb in all_combinations]

    return valid_chars_with_timestamps, valid_chars, all_valid_combinations