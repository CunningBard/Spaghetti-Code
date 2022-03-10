import threading
import time
import zlib
import pyzipper
import string

found_pass = ""
time_lasted = 0
end_time = 0


class Base:
    # counting system
    def __init__(self, base: int):
        self.base = base
        self._nums = [0]

    def inc(self, num: int = 1):
        ind = 0
        run = True
        self._nums[0] += num
        nums = self._nums
        while run:
            if ind + 1 <= len(nums):
                if nums[ind] >= self.base:
                    try:
                        nums[ind] = 0
                        nums[ind + 1] += 1
                    except IndexError:
                        nums.append(1)
                else:
                    break
                ind += 1
            else:
                run = False

    def __repr__(self):
        return f"Base: {self._nums}"

    def value(self):
        return self._nums.copy()

    def value_reversed(self):
        vs = self.value()
        return list(reversed(vs))


def brute_force(name: int = 1, start: int = 0, inc: int = 1):
    global found_pass
    global end_time
    print(f"({name}): Starting...")
    letters = string.ascii_lowercase.replace("", " ").split()
    brute = ""
    a = Base(base=27)
    a.inc(start)
    last = 0
    run = True
    print(f"({name}): Started")

    while run:
        if found_pass:
            return
        brute = ""
        a.inc(inc)

        for ds in a.value_reversed():
            brute += letters[ds - 1]

        with pyzipper.AESZipFile("empty folder - 4 letters.zip", 'r', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as \
                extracted_zip:
            try:
                extracted_zip.extractall(path="output", pwd=str.encode(brute))
                run = False
            except RuntimeError:
                pass
            except zlib.error as e:
                print(e)

        if len(a.value()) > last:
            last = len(a.value())
            print(f"({name}): number of letters: {last}")

    print(f"({name}): END")
    found_pass = brute
    end_time = time.time()


if __name__ == '__main__':
    threads = []
    number_of_threads = 1
    for i in range(number_of_threads):
        s = threading.Thread(target=brute_force, args=(i + 1, i, 2))
        threads.append(s)
        s.start()

    time_start = time.time()
    brute_force(2, 2, 2)

    while found_pass == "":
        time.sleep(2)

    time_lasted = end_time - time_start
    print(f"Finished\n\n"
          f"Password: '{found_pass}'\n"
          f"duration: {time_lasted} seconds")
