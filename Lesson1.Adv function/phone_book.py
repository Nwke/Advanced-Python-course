class Contact:
    def __init__(self, name, surname, phone, favorite_contact=False, **kwargs):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.add_info = kwargs
        self.favorite = favorite_contact

    def __str__(self):
        all_user_info = {'name': self.name, 'surname': self.surname, 'phone': self.phone}
        all_user_info.update(self.add_info)

        all_information = ''
        for field, value in all_user_info.items():
            all_information += f'{field}: {value} \n'

        return all_information


class PhoneBook:
    def __init__(self, book_title):
        self.title = book_title
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def del_contact(self, phone):
        for contact in self.contacts:
            if contact.phone == phone:
                self.contacts.remove(contact)

    def print_contacts(self):
        for contact in self.contacts:
            print(contact)

    def search_contact(self, name, surname):
        for contact in self.contacts:
            if contact.name == name and contact.surname == surname:
                print('found')
                print(contact)

    def search_favorite(self):
        for contact in self.contacts:
            if contact.favorite:
                print(contact)


jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com', favorite_contact=True)
denis = Contact('Denis', 'Smith', '+71234567808', telegram='@jhony', email='jhony@smith.com')

ph = PhoneBook(book_title='PH')
ph.add_contact(jhon)
ph.add_contact(denis)
ph.del_contact(phone='+71234567808')
ph.print_contacts()
ph.search_favorite()
ph.search_contact('Jhon', 'Smith')
