# Quizzes
Quizzes is a Django app that allows users to create and take Quizzes & Questions.

# Models
The app contains the following models:

- Tag: Represents a tag that can be associated with a question.
- Question: Represents a question in a quiz. A question has a stem, type, explanation, and can be associated with multiple tags.
- Options: Represents an option for a question. An option has an option number and content and is associated with a question.
- Answer: Represents an answer to a question. An answer has an option number and is associated with a question.
- Quiz: Represents a quiz. A quiz has a name, start time, end time, time limit, and can be associated with multiple questions.

# Views
The app contains the following views:

- Question
- Add Question
- Update Question
- Delete Question

# Tests
The app contains the following tests:

- `Tag` Test
This test checks the functionality of the `Tag` model by creating a new instance of Tag and adding it to a Question object. It verifies that the tag is added correctly to the Question object.

- `Options` Test
This test checks the functionality of the `Options` model by creating a new instance of Options and adding it to a Question object. It verifies that the content of the Options is added correctly to the Question object.

- `Answer` Test
This test checks the functionality of the `Answer` model by creating a new instance of Answer and adding it to a Question object. It verifies that the correct answer is added correctly to the Question object.

- `Question` Test
This test checks the functionality of the `Question` model by creating a new instance of Question and adding it to a Quiz object. It verifies that the Question object contains the correct number of Options, Answer and Tag objects.

- `Quiz` Test
This test checks the functionality of the `Quiz` model by creating a new instance of Quiz and adding multiple Question objects to it. It verifies that the Quiz object contains the correct number of Question objects.

Each test class contains a setUp method that initializes the required objects for the tests to be run. Finally, each test method is given a descriptive name that specifies what is being tested.