b = Book.objects.get(id=book.id)
b.delete()
Book.objects.all()
