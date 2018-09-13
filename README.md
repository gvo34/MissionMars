# Mission to Mars

Is a web scraping project with BeatuifulSoup that retrieves the following information:

* Obtain latest [news](https://mars.nasa.gov/news/)
* Obtain [featured article and image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
* Obtain lastest weather information from [twitter](https://twitter.com/marswxreport?lang=e)
* Obtain [Mars Facts](http://space-facts.com/mars/)
* Get the latest images of [Mars hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

### Jupyter notebook

The jupyter notebook contains all the steps needed to perform the collected information. See details in [mission_to_mars.ipynb](https://github.com/gvo34/MissionMars/blob/master/mission_to_mars.ipynb)

### Application

Using a flask app the same steps are reproduced relying on a local mongodb collection to temporaarly hold the data.
The app renders information from the mongodb collection. The flask app endpoint /scrape executes the steps to obtain the latest information and refreshes the data stored in the collection.
