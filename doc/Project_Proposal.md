# SafeHome Tracker

### **Project Summary**

Our project aims to create a website containing several reminders and maps that show the trends and distributions of crimes in Los Angeles. Based on the database recording crime in 2020 and other auxiliary databases, we will build a data model that analyzes the safety conditions for each location and rate these safety conditions to give the users a reminder for their visits. 

Apart from the general reminders of location for all users, we will also use the database to analyze the safety conditions for specific groups of people. For example, we will count the victims for each location, so that we can give suggestions for specific groups like kids, elders, women, etc. Besides, the time that crimes occurred and the type of the crimes will also be considered to build reminder maps vary from 24 hours and the crime’s types. Eventually, our algorithm will generate a safer path in the map inputting the user’s age, gender, departure time, and destination.

### Data Stored

We'll use [“Crime in Los Angeles Data from 2020 to Present”](https://www.kaggle.com/datasets/susant4learning/crime-in-los-angeles-data-from-2020-to-present) dataset which is a TA-proposed dataset. The dataset stores information about detailed crime data including specific date and time, latitude and longitude of the location, information about the victim(age, sex, etc), and type of crime.

We'll also use the crime data from earlier times: [“Crime in Los Angeles 2010-September 2017”](https://www.kaggle.com/datasets/cityofLA/crime-in-los-angeles) This database contains similar information as the TA-proposed dataset.

We'll also use datasets for crime code and modus operandi. 

### Basic Functions

Our project includes several simple functions:

1. **Location-Specific Safety Information:** We want to give users a detailed analysis of the safety rate in a given area. We'll use the information from the dataset to give a safety ratings in several aspects for a given area. When an user enters an address or a zip code, the safety rating information will be shown to the user.
2. **Crime Map**: Users can view a crime map of Los Angeles with simple colored visuals, helping people to determine which area is safer at a glance.

### Creative Component

Firstly, with the help of a wider time range of the crime data, we want to introduce a function called **Trend.** By analyzing the change in crime rate and type in the past year, we want to tell the users how safety rating in a regions has changed. (If a region only has an average safety rate, but its safety rate keeps increasing in the past years, this region can be a great choice for living)

Secondly, we want to design a function called **SaferRoute**. We want to use routing algorithms to help late-night travelers walk on a route that's safer. We'll take both time and safety rates into account and create a more suitable route. We also provide the route based on the age, time, and sex of the user as we think the safety in an area will differ for different groups of people at different times. If the overall safety rate is too low, we may advise the user to consider traveling at a later time.
To make the user experience more convinient, we'll allow users to save their 'favourate locations', which will make finding regular routes faster.

We'll also allow users to report new crimes or inacuurate data in a given location, thus we can use user input to make our service more accurate.

### **Description** of an Application

The primary application of our project is generating a map with safety conditions according to the input of ages and genders of the users, and the time of their departure. We will finally generate a safety map with notations on the location it often occurs crimes due to our database by selecting ages, genders, and times. We can solve the safety problems for specific groups of people so that they can reach their destinations safely in high-crime areas. 

### Usefulness

In today's ever-growing urban environments, safety is paramount. With urbanization and population growth, crime trends and patterns evolve. Our application's primary purpose is to equip users with accurate, real-time safety information based on empirical data, allowing them to make informed decisions about their travel routes and destinations. We hope our website can form a more multi-dimensional analysis of crime, and therefore, help provide a more personal travel and daily routine guide that takes safety seriously into account and reduces the crime rate.

There are indeed some platforms that share similar functionality, like SpotCrime which provides a crime map and alerts, visualizing data about recent criminal activity, and CrimeMapping, a tool used by many local law enforcement agencies to provide the public with valuable crime information. However, our project has the following advantages. Firstly, our website can be more personalized by considering the users’ needs by taking their inputs into account and may be able to form a safety route that are not accomplished by these or other maps applications. For example, we may provide specific recommendations for specific groups. Based on crime victim data, our application can offer specialized advice for different demographic groups such as children, elderly, and women. This adds another layer of personalization that many other platforms lack. What’s more, our application not only provides current data but also analyzes historical crime trends. It informs users about how safety in specific areas has changed over time, enabling more informed long-term decisions.

### Realness

Our dataset reflects incidents of crime in the City of Los Angeles dating back to 2020 and from 2010 to 2017. This data is transcribed from original crime reports that are typed on paper and therefore there may be some inaccuracies within the data. It contains the official file numbers, crime codes, time, and geographic information about these crimes, offering us 20+ columns of entries for data analysis. Besides, there are datasets about economic and population information about Los Angeles on Kaggle, which are closely related to our datasets and may enable us to go beyond the initially given factors in our future project analysis. 

The data we refer to comes from two authoritative sources: the Los Angeles Police Department (LAPD) and The Official Website of the City of Los Angeles. Both of these sources are publicly available organizations dedicated to providing the public with important information about the Los Angeles metropolitan area. Although these data come from news reports and may contain some inaccuracies, they are still generally authentic and reliable, considering that they come from official websites and that the amount of data is huge enough.

### Website Functionality

![Search Function](SafeHome_Tracker_img/search.gif)

Search Function

![Map Function](SafeHome_Tracker_img/map.gif)

Map Function

![SafeRoute Function](SafeHome_Tracker_img/route.gif)

SafeRoute Function

![Trends Function](SafeHome_Tracker_img/trends.gif)

Trends Function

### Work Distribution

Yuxi Chen will be responsible for the Backend development.

- Develop the algorithm for the "SaferRoute" function, incorporating various factors such as safety ratings, time, and demographic data.
- Develop APIs to facilitate data retrieval and integration with the frontend.
- Carry out database design.

Yihong Yang will be responsible for Backend development and testing.

- Work together with Yuxi Chen for the "SaferRoute" function.
- Conduct testing to identify bugs and ensure the system works seamlessly.
- Create documentation for the project, including user manuals and technical documentation.
- Complete database implementation.

Qiyang Wu will be responsible for Frontend development.

- Design the user interface and experience for the website, ensuring it is user-friendly and intuitive.
- Integrate a map service (like Google Maps) to visualize the crime data and safety ratings.
- Complete database implementation.

Shurui Liu will be responsible for Database Development.

- Set up a database to store and manage the crime data efficiently.
- Analyze the data to identify trends and patterns in crime rates over the years.
- Extract relevant data to be used in the safety rating system.
- Do database indexing.