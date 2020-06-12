import io

# Create a test file in the current directory and write to it.
file = open("test.txt", "w")
file.write("Hello world!")
file.close()

# Read and print the contents of the file we just created.
file2 = open("test.txt", "r")
contents = file2.read()
file2.close()
print(contents)