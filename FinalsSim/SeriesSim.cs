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
        
        /// <summary>
        /// Constructor
        /// </summary>
        /// <param name="awayProb"></param>
        /// <param name="homeProb"></param>
        public SeriesSim(double awayProb, double homeProb)
        {
            AwayProb = awayProb;
            HomeProb = homeProb;
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
            int homeWins = 0;
            int awayWins = 0;

            // Run the first four games
            gameSim('h', ref homeWins, ref awayWins);
            gameSim('h', ref homeWins, ref awayWins);
            gameSim('a', ref homeWins, ref awayWins);
            gameSim('a', ref homeWins, ref awayWins);

            // Run Next three games if necessary
            if (homeWins != 4 && awayWins != 4)
                gameSim('h', ref homeWins, ref awayWins);
            if (homeWins != 4 && awayWins != 4)
                gameSim('a', ref homeWins, ref awayWins);
            if (homeWins != 4 && awayWins != 4)
                gameSim('h', ref homeWins, ref awayWins);

            if (homeWins > awayWins)
                return homeWins + awayWins - 4;
            
            return homeWins + awayWins;
        }

        /// <summary>
        /// Predicts the result of a single game using the field probabilities. 
        /// User must specify type of game('h' or 'a' for home or away).
        /// </summary>
        /// <param name="type"></param>
        private void gameSim(char type, ref int homeWins, ref int awayWins)
        {
            Random rng = new();
            double predict = rng.NextDouble();

            if (type == 'h')
            { 
                if (predict <= HomeProb)
                    homeWins++;
                else awayWins++;
            }
            if(type == 'a')
            {
                if (predict <= AwayProb)
                    awayWins++;
                else homeWins++;
            }
        }
    }
}
