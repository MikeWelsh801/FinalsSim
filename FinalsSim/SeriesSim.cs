using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace FinalsSim
{
    /// <summary>
    /// This class runs a 7-gane nba series simulation.
    /// </summary>
    internal class SeriesSim
    {
     
        public double AwayProb { get; private set; }
        public double HomeProb { get; private set; }

        public int HomeWins { get; private set; }
        public int AwayWins { get; private set; }


        

        /// <summary>
        /// Constructor
        /// </summary>
        /// <param name="awayProb"></param>
        /// <param name="homeProb"></param>
        public SeriesSim(double awayProb, double homeProb)
        {
            AwayProb = awayProb;
            HomeProb = homeProb;
            HomeWins = 0;
            AwayWins = 0;
        }

        /// <summary>
        /// Runs a 7 game series  
        /// 
        /// Returns the index of the result in an 8 element array containing all possible
        /// outcomes.
        /// </summary>
        /// <returns></returns>
        public int Run()
        {
            // Reset series wins
            this.HomeWins = 0;
            this.AwayWins = 0;

            // Run the first four games
            gameSim('h');
            gameSim('h');
            gameSim('a');
            gameSim('a');

            // Run Next three games if necessary
            if (HomeWins != 4 && AwayWins != 4)
                gameSim('h');
            if (HomeWins != 4 && AwayWins != 4)
                gameSim('a');
            if (HomeWins != 4 && AwayWins != 4)
                gameSim('h');

            if (HomeWins > AwayWins)
                return HomeWins + AwayWins - 4;
            
            return HomeWins + AwayWins;
        }

        /// <summary>
        /// Predicts the result of a single game using the field probabilities. 
        /// User must specify type of game('h' or 'a' for home or away).
        /// </summary>
        /// <param name="type"></param>
        private void gameSim(char type)
        {
            
            if(type == 'h')
            {
                Random rng = new Random();
                double predict = rng.NextDouble();
                if (predict <= HomeProb)
                    this.HomeWins++;
                else this.AwayWins++;
            }
            if(type == 'a')
            {
                Random rng = new Random();
                double predict = rng.NextDouble();
                if (predict <= AwayProb)
                    this.AwayWins++;
                else this.HomeWins++;
            }

        }
    }
}
