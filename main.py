import json
from datetime import datetime

class Library:
    def __init__(self, filename="library_records.json"):
        self.records = []
        self.filename = filename
        self.load_records()

    def load_records(self):
        try:
            with open(self.filename, "r") as f:
                content = f.read()
                self.records = json.loads(content) if content else []
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []

    def store_records(self):
        with open(self.filename, "w") as f:
            json.dump(self.records, f, indent=4)

    def add_book(self):
        data = {
            "name": input("Book Name: "),
            "writer": input("Author: "),
            "category": input("Genre: "),
            "year": int(input("Year Published: ")),
            "status": input("Have you read this? (yes/no): ").strip().lower() == "yes"
        }
        if data["status"]:
            data["finished_on"] = input("When did you read it? (YYYY-MM-DD): ")

        self.records.append(data)
        self.store_records()
        print("New book has been recorded.")

    def search_book(self):
        mode = input("Search by title or author? ").strip().lower()
        query = input("Search term: ").strip().lower()
        matched = [
            entry for entry in self.records
            if query in entry["name"].lower() or query in entry["writer"].lower()
        ]

        if matched:
            print("\nFound Books:")
            for idx, book in enumerate(matched, 1):
                status = "Read" if book["status"] else "Unread"
                print(f"{idx}. {book['name']} by {book['writer']} ({book['year']}) - {status}")
        else:
            print("No books matched your search.\n")

    def modify_book(self):
        title = input("Enter the title of the book to update: ")
        for entry in self.records:
            if entry["name"].lower() == title.lower():
                print("Leave input blank to retain existing value.")
                entry["name"] = input(f"New title ({entry['name']}): ") or entry["name"]
                entry["writer"] = input(f"New author ({entry['writer']}): ") or entry["writer"]
                entry["year"] = input(f"New year ({entry['year']}): ") or entry["year"]
                entry["category"] = input(f"New genre ({entry['category']}): ") or entry["category"]
                entry["status"] = input("Read it? (yes/no): ").strip().lower() == "yes"
                self.store_records()
                print("Book updated!\n")
                return
        print("Book not found.\n")

    def show_books(self):
        if not self.records:
            print("No books to display.")
            return

        for idx, book in enumerate(self.records, 1):
            status = "Read" if book["status"] else "Unread"
            print(f"{idx}. {book['name']} by {book['writer']} ({book['year']}) - {status}")

    def remove_book(self):
        title = input("Title of the book to remove: ")
        for entry in self.records:
            if entry["name"].lower() == title.lower():
                self.records.remove(entry)
                self.store_records()
                print("Book removed.")
                return
        print("Book not found.")

    def progress_summary(self):
        total = len(self.records)
        read = sum(1 for book in self.records if book["status"])
        progress = (read / total * 100) if total else 0
        print(f"Books in library: {total}")
        print(f"Reading Progress: {progress:.1f}%")

    def menu(self):
        while True:
            print("\n=== My Personal Library ===")
            print("1. Add Book")
            print("2. Update Book Info")
            print("3. Search Book")
            print("4. Remove Book")
            print("5. Show All Books")
            print("6. Show Reading Progress")
            print("7. Exit")
            option = input("Choose an option (1-7): ")

            match option:
                case '1': self.add_book()
                case '2': self.modify_book()
                case '3': self.search_book()
                case '4': self.remove_book()
                case '5': self.show_books()
                case '6': self.progress_summary()
                case '7':
                    self.store_records()
                    print("Exiting Library. Have a great day!")
                    break
                case _: print("Invalid input. Try again.")

if __name__ == "__main__":
    app = Library()
    app.menu()
