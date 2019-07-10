# Luigi example

A simple Luigi job demo at Python Stuttgart Meetup.

Use case: create daily sales report from sales transactions. Backup database dump to Google Cloud along the way.

**Slides available on SpeakerDeck: [Building Data Workflows with Luigi & Python](https://speakerdeck.com/chhantyal/building-data-workflows-with-luigi-and-python)**  


## Install

* Install all dependencies: `pipenv install`

* Start Luigi scheduler: `luigid --port 8000`

## Try

1. Run a task (report for one day)

`python -m luigi --module example SalesReport --date=2019-04-26`

2. Create reports for past days (back filling)

`python -m luigi --module example RangeDaily --of SalesReport --start=2019-04-21`
