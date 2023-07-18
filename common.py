import os

def f_write_arr(arr, path): 		   #create file and populate it with array
	try:	
		with open (path, "a+") as fd:
			for line in arr:
				fd.write(line + "\n")
		return True
	except IOError:
		return False

def f_write_src(src, path):
	try:	
		with open (path, "a+") as fd:
			fd.write(src)
		return True
	except IOError:
		return False

def f_read_arr(path):
    try:
        with open(path, "r") as fd:
            lines = fd.readlines()
            buffer = [line.rstrip("\n") for line in lines]
        return buffer
    except IOError:
        return None


def f_remove(path):					   #self explanatory
	if os.path.exists(path):
		os.remove(path)
		return True

	return False

def f_mkdir(path):
	try:
		os.mkdir(path)
	except OSError as error:
		print(error)

def main(): 						   #test cases						   
	word_dict = {
	    1: "Tiger",
	    2: "Pizza",
	    3: "Elephant",
	    4: "Guitar",
	    5: "Sunshine",
	    6: "Happiness",
	    7: "Dolphin",
	    8: "Chocolate",
	    9: "Mountain",
	    10: "Adventure"
	}
	path = r"/home/rot/Desktop/site/user_content/user/"
	result = "✅ Passed"
	for i in range(10):
		if f_write_arr(list(word_dict.values()), (path + str(i))) == False:
			result = "❌ Failed"
			break

	print(f"Test case(1): {result}")

	result = "✅ Passed"
	for i in range(10):
		if (list(word_dict.values()) != f_read_arr(path + str(i))):
			result = "❌ Failed"
			break
	
	print(f"Test case(2): {result}")

	result = "✅ Passed"
	for i in range(10):
		if f_remove(path + str(i)) == False:
			result = "❌ Failed"
			break

	print(f"Test case(3): {result}")

	f_mkdir(path + "testdir")

if __name__ == "__main__":
	main()