# Web Development Course

  This is a course taken on [udacity][https://classroom.udacity.com/courses/cs253] about web development.

# Requirements

  To use it, you need to install google app engine from [here][https://cloud.google.com/appengine/].

# The web application

## Main Page

   You can reach the Main Page either by running the web application locally or on following this [link][https://4-dot-hello-udacity-155021.appspot.com/] (if still available).

   To run it locally, on a terminal, type:

      dev_appserver.py app.yaml

   From the main page you can run differents applications by choosing them and clicking the "GO" button.

## Birthdate

   Here you can type your birthdate in the 3 input boxes.

   The month has to be either in letters format ("January", "May", ..), with only the first three letters required, and in english, or it can be in number format (from 1 to 12).
   The day has to be a number from 1 to 31. The actual number of days in each month is still not taken into account.
   The year has to be between 1900 and 2020.

## Rot13

   This script allow you to enter some text in the text area and then applies the rot13 function on your text. It actually offsets the letters by 13 ranks among the alphabet.

## Shopping list

   There you can create a list of elements, in this case a shopping list of food elements, and it dynamically displays the list below the input box.

## Fizzbuzz

   This script displays a list of length equal to the number entered.

   Each element is equal to its rank number, except for elements with rank number multiple of 3 who are replaced by "Fizz", multiple of 5 replace by "Buzz" and multiple of 3 and 5 replaced by "FizzBuzz".

## ASCII blog

   This is an ascii chan where you can post ascii art.

   Your ip address, if available, is registered and the corresponding location displayed on the map at the top of the page.


## Blog

   This is a blog where you can post articles (title + text).

   The last 10 entries are displayed on the "/blog" page.

   To create a new post, you have to go to "/blog/newpost" page.

   You will then be redirected to a permalink page "/blog/post_id" where post_id is the id of the post newly created in the database.

   You can signup on "/signup".

   You can login on "/login" page and logout on "/logout" page.

   Either way, if you don't logout, a cookie will keep you connected and redirect you to the "/welcome" page.

   Finally, this blog can also display its content in json by adding ".json" at the end of either "/blog" or "/blog/post_id".


## Visits

   This page just increments a cookie to count how many times you connected to this specific page. A surprise attends those who reach a certain number...



Adam FACI.