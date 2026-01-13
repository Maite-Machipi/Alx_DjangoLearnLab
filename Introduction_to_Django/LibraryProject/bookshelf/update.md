b = Book.objects.get(id=book.id)
b.title = "Nineteen Eighty-Four"
b.save()
b
