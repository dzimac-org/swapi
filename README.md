## Intro to TT SWAPI / Next steps to improve
Firstly, I assumed - the problem we are trying to solve - is more broad and we might need to create more ETL connectors ;) hence `base_etl` implementation - somewhat basic start to full template method design pattern.
I've tried to keep the memory footprint low and separate ETL steps implementations into different modules (`extract`, `transform`, `load`). 


In terms of performance, I'm not using any task queues but that's probably one of the "cheapest" optimisations that can be done besides caching.


As for next steps - for better testability, separation of concerns and long term maintenance in more complex project, I would consider abstracting away ORM using repository pattern. 


I actually had some good fun coding this, and it was a nice refresher - I might have missed some more optimal solutions on how to implement specific django details, but I'm more than happy to receive any feedback.


## Running the app
`make up` to run the project. Visit http://localhost:8080 in browser.

`make test` to run tests.

`make down` to remove all docker artifacts.


