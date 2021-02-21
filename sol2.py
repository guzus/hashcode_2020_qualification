import sys
from concurrent.futures import ThreadPoolExecutor


class Library:
    def __init__(self, i, N, T, M, books):
        self.id = i
        # number of books
        self.N = N
        # sign up time
        self.T = T
        # number of books per day
        self.M = M
        # books
        self.books = books

    def scan(self, days, books_queue, S):
        cnt = 0
        score = 0
        scanned_books = []
        # print(f"available: {days*self.M}")
        new_queue = []
        for book in books_queue:
            if cnt < days * self.M and book in self.books:
                scanned_books.append(book)
                cnt += 1
                score += S[book]
            else:
                new_queue.append(book)
        return (scanned_books, cnt, score, new_queue)

    def __repr__(self):
        return str(self.id)


def solve2(f, w):
    # Book, Library, Days
    B, L, D = map(int, f.readline().split())
    S = list(map(int, f.readline().split()))

    libraries = []
    books_queue = list(range(0, B))
    books_appearance_cnt = [0] * B

    for i in range(L):
        N, T, M = map(int, f.readline().split())
        library_books = list(map(int, f.readline().split()))
        for library_book in library_books:
            books_appearance_cnt[library_book] += 1

        library = Library(i, N, T, M, library_books)
        libraries.append(library)

    # sort library with T, M, N
    libraries = sorted(libraries, key=lambda x: (x.T, -x.M, -x.N))

    # sort books to scan by score of book, the number of available library
    books_queue = sorted(books_queue, key=lambda x: (-S[x], books_appearance_cnt[x]))

    total_scanned_books_cnt = 0
    # number of signed-up libraries
    A = 0
    # library ID
    Y = []
    # number of scanned books
    K = []
    total_scanned_books = []
    total_scanned_books_score = 0
    for library in libraries:
        D -= library.T
        if D <= 0:
            break
        A += 1
        Y.append(library.id)
        (
            scanned_books,
            scanned_books_cnt,
            scanned_books_score,
            new_queue,
        ) = library.scan(D, books_queue, S)
        books_queue = new_queue
        K.append(scanned_books_cnt)
        total_scanned_books.append(scanned_books)
        total_scanned_books_score += scanned_books_score

    print("---res---")
    w.write(str(A) + "\n")
    for i in range(A):
        w.write(str(Y[i]) + "\n")
        w.write(str(K[i]) + "\n")
        string = ""
        for scanned_book in total_scanned_books[i]:
            string += str(scanned_book) + " "
        w.write(string + "\n")
    print(f"total_scanned_books_score : {total_scanned_books_score}")


if __name__ == "__main__":
    IO_files = [
        ("tasks/a_example.txt", "results2/a_out.txt"),
        ("tasks/b_read_on.txt", "results2/b_out.txt"),
        ("tasks/c_incunabula.txt", "results2/c_out.txt"),
        ("tasks/d_tough_choices.txt", "results2/d_out.txt"),
        ("tasks/e_so_many_books.txt", "results2/e_out.txt"),
        ("tasks/f_libraries_of_the_world.txt", "results2/f_out.txt"),
    ]
    for IO_file in IO_files:
        with ThreadPoolExecutor(max_workers=6) as executor:
            executor.submit(solve2, open(IO_file[0], "r"), open(IO_file[1], "w"))