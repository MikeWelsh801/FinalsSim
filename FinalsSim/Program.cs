// Result list indices (sample space): H4, H5, H6, H7, A4, A5, A6, A7
// Hometeam wins are first four indices and how many games the series ran. Example: 
// index zero is how many series simulations resulted in a sweep for the team with
// home court advantage. 
using FinalsSim;

List<int> result = new() { 0, 0, 0, 0, 0, 0, 0, 0 };

string intro = "Calculating Series Odds...";
Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (intro.Length / 2)) + "}", intro));
Console.WriteLine();
Console.WriteLine();

// Get the probabilities and home/away teams from training file
if (args.Length != 1)
    throw new ArgumentException("Incrorect number of arguemnts");

string[] pars = File.ReadAllLines(args[0]);

// Predicted probability of team with homecourt advantage winning a home game. 
// (derived from neural net and rounded)
string HomeTeam = pars[0];
double HomePercentage = Double.Parse(pars[1]);

// Predicted probability of team without homecourt advantage winning a home game. 
// (derived from neural net and rounded)
string AwayTeam = pars[2];
double AwayPercentage = Double.Parse(pars[3]);

SeriesSim sim = new(AwayPercentage, HomePercentage);
int runs = 10_000_000;

// Run series simulation N times and count results
for (int i = 0; i < runs; i++)
{
    int index = sim.Run();
    result[index]++;
}

double homeTeamProb = 0;
double awayTeamProb = 0;
double check = 0;

// add up probabilities and print results
for (int i = 0; i < result.Count; i++)
{
    double prob = (result[i] / (double)runs);
    string winner = (i < 4) ? HomeTeam : AwayTeam;
    int games = (i < 4) ? i + 4 : i;
    check += prob;
    Console.WriteLine($"\tThere is a(n) {prob * 100:F1} percent chance of the {winner} winning the series in {games} games.");
    Console.WriteLine();

    if(i < 4)
        homeTeamProb += result[i];
    else awayTeamProb += result[i];
}

homeTeamProb /= runs;
awayTeamProb /= runs;

Console.WriteLine();

Console.ForegroundColor = ConsoleColor.Green;
string outro1 = "****************** Final Odds ******************";
string outro2 = "************************************************";

Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (outro1.Length / 2)) + "}", outro1));
Console.WriteLine(String.Format("{0," + ((Console.WindowWidth / 2) + (outro2.Length / 2)) + "}", outro2));
Console.ResetColor();

Console.WriteLine();
Console.WriteLine($"\tThe {HomeTeam} have a(n) {homeTeamProb * 100:F1} percent chance of winning the series.");
Console.WriteLine();
Console.WriteLine($"\tThe {AwayTeam} have a(n) {awayTeamProb * 100:F1} percent chance of winning the series.");
Console.WriteLine();
