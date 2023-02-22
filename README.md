# FinalsSim
This is a simulation of an NBA finals series.
This application takes in single game win probabities for a home team and an away team, and calculates the probabilities of each team winning a 7-game finals series, along with
the probability of each posible outcome (e.g. home team wins in 5 games). 

I built the NN by going through the MadeWithML Neural Net lesson plan, then adapting to fit a project that analyzes nba team data from basketball-reference.com from the 2021-2022 
season. The url for the Neural Net lesson plan is cited below. I highly recommend their website for anyone looking to learn more about machine learning. 

The training data I used is per 100 possession team data from basketball reference. I placed visitor/home team data in line with the game result, denoted as H (home team won) or
V (away team won). The home/away team stats were my X in my training data and Y was the result. 

The trained network can predict the probability of a single game home team win, given the stats for two teams. I then passed these probabilities into the 7-game series sim to predict
the 2021-2022 NBA finals between Boston and Golden State. The model assigned the highest probability to Golden State winning in 7 games (just under 17 percent). The actual result was 
Golden State winning in 6 games.

Model shortcommings: I was only able to find data for the end of season stats. This means that if two teams played at the beginning of the year, the model was using their stats from the 
end of the season to predict who won. This is a problem if a team underwent changes that a significant impact on their team statistics (e.g. a key player injury). If I had been able to use 
data from the date that games were played, this likely would have resulted in a better model. Also, I'm not convinced that a Neural Network is the best way to predict highly volitile outcomes
like NBA games due to its tendency toward overfitting. I might try to rework this as a logistic regression model in the future.

I made this project as a learning experience. I had a lot of fun discovering how neural networks work and how to train and build a statistical prediction model. As I was mainly using this project
as for my own education, if anyone finds this code useful, feel free to use part or all of this project for whatever you'd like. If you feel inclined, you can help me out by citing this repository
in your project. Thank you to Made With ML for making their tutorials and material available learners like myself. You can find a link to their website below.

@article{madewithml,
    author       = {Goku Mohandas},
    title        = { Neural networks - Made With ML },
    howpublished = {\url{https://madewithml.com/}},
    year         = {2022}
}