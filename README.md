# (Almost) Transparent Persistent Boolean Values

## Requirements

* Python 3.8 or above

## Usage

A store is created from the `Store` class: `store = Store()`

A store can also be initialized with a different file for storing data: `store = Store(filename="my_store.json")`

To create a new boolean, simply assign a value to it: `store.my_bool = True`.

Accessing is just as simple: `print(store.my_bool)`

A value can be toggled by reassigning it to itself: `store.my_bool = store.my_bool.toggle()`

## Background

As I was perusing Reddit, my attention was caught by [u/takeonzach](https://reddit.com/u/takeonzach)'s [post](https://www.reddit.com/r/learnpython/comments/lu6phc/i_made_a_small_library_to_easily_create/) about their new library for storing boolean values persistently.
My first thought was about how niche the use case was as traditional databases are much better for data storage than pickling data to a file, but I checked out the linked [repository](https://github.com/zachvance/persistent_switch) anyway.

As I looked through the code I realized that I had a very different idea when I first saw the post to how persistent boolean values would work to how they were actually implemented by Zach.
He was accessing data using the traditional key-value pair, but I had imagined accessing and assigning the values just as you would any other Python variable.
So I took on the challenge to create it myself, forking Zach's repo to give implicit credit to his original idea.

The first problem to solve was the creation of arbitrary attributes to my class, which was easily solved by using Python's `__setattr__` magic method.
This allows persistent booleans to be created with a simple assignment `store.my_bool = True` instead of the more clunky \(in my opinion\) `store.set("my_bool", True)`.
I also had to figure out how to allow a `toggle()` method on the attribute such that `store.my_bool.toggle()` would invert the value in-place, but still allow the value to be accessed through `store.my_bool` and not `store.my_bool.value`.

The toggle functionality turned out to be the most challenging piece of the puzzle because the `__bool__` magic method is only useful when deciding "truthyness" of an object and not when directly comparing to an actual boolean like so `store.my_bool == True`.
I first considered subclassing the `bool` type, but a quick Google search ruled that out, so I went a step higher and subclassed `int` instead \([take that Guido](https://stackoverflow.com/a/2172204/13298346)\).
However, if I wanted my precious `toggle()` so as to stay inline with the original implementation, I would need to make it return a new `ToggleableBoolean` instead of directly modifying the value.

While I \(mostly\) achieved what I set out to do, I wouldn't recommend ever using this in an actual project.
Dedicated database software like MySQL or PostgreSQL are much more suited for persistent storage, even if they are more clunky to interact with.
