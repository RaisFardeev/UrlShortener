class EmailMasker:
    def __init__(self, masking_char="x"):
        self.masking_char = masking_char

    def mask(self, email):
        masked = email.index('@')
        return self.masking_char * masked + email[masked::]


class PhoneMasker:
    def __init__(self, masking_char="x", mask_length=3):
        self.masking_char = masking_char
        self.mask_length = mask_length

    def mask(self, phone_number):
        splitted = [char for char in phone_number.split(' ') if char]
        i, n = 1, self.mask_length
        while n > 0:
            l = len(splitted[-i])
            splitted[-i] = self.masking_char * l if n >= l else splitted[-i][:-n:] + self.masking_char * n
            n -= l
            i += 1
        return ' '.join(splitted)


class SkypeMasker:
    def __init__(self, masking_char="x"):
        self.masking_char = masking_char

    def mask(self, link):
        start_index = link.find('skype:')
        q = link.find('?')
        link = link[:start_index + 6] + self.masking_char * 3 + (link[q::] if q != -1 else '')
        return ''.join(link)