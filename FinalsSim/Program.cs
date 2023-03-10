
// Result list indices (sample space): H4, H5, H6, H7, A4, A5, A6, A7
// Hometeam wins are first four indices and how many games the series ran. Example: 
// index zero is how many series simulations resulted in a sweep for the team with
// home court advantage. 
using FinalsSim;

List<int> result = new() { 0, 0, 0, 0, 0, 0, 0, 0 };

string HomeTeam = "Golden State";
string AwayTeam = "Boston";

string intro = "Calculating Series Odds...";
Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (intro.Length / 2)) + "}", intro));
//Console.WriteLine("\tCalculating Series Odds... ");
Console.WriteLine();
Console.WriteLine();

// Predicted probability of team with homecourt advantage winning a home game. 
// (derived from neural net and rounded)
// 
// 2022 finals probabilities: Home - 54%, Away - 52%
if (args.Length != 2)
    throw new ArgumentException("Incorrect number of arguments.");

double HomePercentage = Double.Parse(args[0]);
// double HomePercentage = 0.54;

// Predicted probability of team without homecourt advantage winning a home game. 
double AwayPercentage = Double.Parse(args[1]);
// double AwayPercentage = 0.52;

SeriesSim sim = new(AwayPercentage, HomePercentage);
int runs = 10_000_000;

// Run series simulation N times and count results
for (int i = 0; i < runs; i++)
{
    int index = sim.Run();
    result[index]++;
}

//int mostLikely = result.IndexOf(result.Max());
//double percent = (double)(result.Max() / 10000.0) * 100.0;

//if(mostLikely < 4)
//    Console.WriteLine($"There is a {percent} percent chance of {HomeTeam} winning the series in {mostLikely+4} games.");
//else
//    Console.WriteLine($"There is a {percent} percent chance of {AwayTeam} winning the series in {mostLikely} games.");

double homeTeamProb = 0;
double awayTeamProb = 0;
double check = 0;

for (int i = 0; i < result.Count; i++)
{
    double prob = (result[i] / (double)runs);
    string winner = (i < 4) ? HomeTeam : AwayTeam;
    int games = (i < 4) ? i + 4 : i;
    check += prob;
    Console.WriteLine($"\tThere is a {prob * 100:F1} percent chance of {winner} winning the series in {games} games.");
    Console.WriteLine();

    if(i < 4)
        homeTeamProb += result[i];
    else awayTeamProb += result[i];
}

homeTeamProb /= runs;
awayTeamProb /= runs;
Console.WriteLine();
string outro1 = "****************** Final Odds ******************";
string outro2 = "************************************************";
Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (outro1.Length / 2)) + "}", outro1));
Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (outro2.Length / 2)) + "}", outro2));

Console.WriteLine();
Console.WriteLine($"\t{HomeTeam} has a {homeTeamProb * 100:F1} percent chance of winning the series.");
Console.WriteLine($"\t{AwayTeam} has a {awayTeamProb * 100:F1} percent chance of winning the series.");
Console.WriteLine();
