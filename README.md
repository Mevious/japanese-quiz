# Ginga Quiz

Minimalist Japanese Hiragana/Katakana/Kanji Quiz. 

----

This python-based quiz was written to quickly memorize the Hiragana/Katakana/Kanji needed to pass the JLPT examination. To run this quiz you will need to have a python environment on your computer. You can get this by downloading Anaconda3. You need to make sure you have the packages listed in the requirements.txt. You should be then be able to open the program using the .bat file.

Basic Features: 

Add your own quizzes to the vocab folder to have them automatically added to the program (including a reversed quiz where you give the meaning not the kana). The standard formatting for the csv quiz files is (english,kana,meaning). Hiragana and Katana quizzes are placed in the alphabets folder. Words that are missed in non-alphabet quizzes will be stored in the respective file in the missed folder. You can clear the words in these files by clicking the "Clear Missed Words" button. Personally I like to add all work to a single file in all-words to quiz while I am watching TV so feel free to add any words to that in your own file. Percentage of words correct while quizzing will display on the bottom.

![](/readme-images/quizzes.png)

Correct Words
An answer is determined to be correct if the input matches a single definition or the entire definition.
![](/readme-images/correct.PNG)

Incorrect Words
![](/readme-images/incorrect.PNG)

Future Features:
- All JLPT quizzes
- Checkable box for reversed quizzes
- Fix bugs associated with missed words
- Auto downloading of required packages
