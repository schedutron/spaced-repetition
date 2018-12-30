# spaced-repetition

[![Build Status](https://travis-ci.org/schedutron/spaced-repetition.svg?branch=master)](https://travis-ci.org/schedutron/spaced-repetition)
[![Coverage Status](https://coveralls.io/repos/github/schedutron/spaced-repetition/badge.svg?branch=master)](https://coveralls.io/github/schedutron/spaced-repetition?branch=master)
![Lines of code](https://tokei.rs/b1/github/schedutron/spaced-repetition)

![Wikipedia Illustration](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Leitner_system_alternative.svg/460px-Leitner_system_alternative.svg.png)

This is tool to enhance your learning by the spaced repetition technique. Spaced Repetition is a technique which uses increasing intervals of time between previously learned material for more effective and long-term learning. Read more about it on [Wikipedia](https://en.wikipedia.org/wiki/Spaced_repetition).


Create `env.py` with the following contents:

```
DATABASE_URL = 'your postgres database url'
TEST_DATABASE_URL = 'url of test database'
```

## Commands
`insert entry` - To add a newly learned item in the database

`insert source` - To add a source of knowledge, e.g., a book or a website

`display all` - To display all the entries in the database

`today` - To display the items you need to revise today

`update` - To update the "confidence level" of an item after you revised it

`exit` - To exit the REPR
