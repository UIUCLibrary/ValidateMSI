import yaml
TEST_FILE = "frozen.yml"

def main():
    print(__file__)
    with open(TEST_FILE, "r") as f:
        s = yaml.load(f)
        print(s['required'])



if __name__ == '__main__':
    main()