from selenium import webdriver


class TestBrowser:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def test(self):
        self.browser.get('http://ec2-54-208-152-154.compute-1.amazonaws.com/')
        assert 'React App' in self.browser.title

        # Initialize the left and right input scales. Only four positions on each are necessary
        pos_left_0 = self.browser.find_element_by_id("left_0")
        pos_left_1 = self.browser.find_element_by_id("left_1")
        pos_left_2 = self.browser.find_element_by_id("left_2")
        pos_left_3 = self.browser.find_element_by_id("left_3")

        pos_right_0 = self.browser.find_element_by_id("right_0")
        pos_right_1 = self.browser.find_element_by_id("right_1")
        pos_right_2 = self.browser.find_element_by_id("right_2")
        pos_right_3 = self.browser.find_element_by_id("right_3")

        # Initial page elements
        self.weigh = self.browser.find_element_by_id("weigh")
        self.reset = self.browser.find_elements_by_id("reset")
        self.weighings = self.browser.find_element_by_class_name("game-info")

        # Storing the left and right positions into list of inputs to be passed to weigh_bars
        self.left_inputs = [pos_left_0, pos_left_1, pos_left_2, pos_left_3]
        self.right_inputs = [pos_right_0, pos_right_1, pos_right_2, pos_right_3]

        input_values = [0, 1, 2, 3, 5, 6, 7, 8]

        result = self.weigh_bars(input_values, 4)

        # Output results
        print(str(result))
        result_click = self.browser.find_element_by_id("coin_" + str(result))
        result_click.click()
        self.alert = self.browser.switch_to.alert
        print(self.alert.text)
        self.alert.accept()
        print(self.weighings.text)

    # Used to find fake bar. Returning number of fake bar. Receives list of inputs and size. Using divide and conquer to
    # find correct value
    def weigh_bars(self, input_values, size):

        # Calculate length of input_values then splits them in half, using mid_index to aid this
        length = len(input_values)
        mid_index = length // 2

        half_one = input_values[:mid_index]
        half_two = input_values[mid_index:]

        # Inputting the two halves into the left and right bowls
        for x in range(len(half_one)):
            self.left_inputs[x].send_keys(half_one[x])
            self.right_inputs[x].send_keys(half_two[x])

        # Weighing bowls then clicking reset
        self.weigh.click()
        status = self.reset[0].text
        self.reset[1].click()

        # Recurring method until correct value is found. Default case is when both sides are equal, meaning midpoint
        # would be correct value
        if status == "=":
            return 4
        elif status == ">":
            if size > 2:
                return self.weigh_bars(half_two, len(half_two))
            else:
                return half_two[0]
        elif status == "<":
            if size > 2:
                return self.weigh_bars(half_one, len(half_one))
            else:
                return half_one[0]

    def close(self):
        self.browser.close()


test = TestBrowser()
test.test()

