"""
Created on Sun Jan 15

@author: Mark Faust (JHED: mfaust4)
"""

# import numpy, pandas, and matplotlib modules to help create numpy arrays,
# reading csv files, and visualizing data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rand


def calculate_ratings(filename):
    """
    

    Parameters
    ----------
    filename : String
        The csv file that the user wants to read.

    Returns
    -------
    dictionary : dictionary
        A dictionary containing the players' names and ratings.

    """
    
    # Ensuring that the user inputs a string value as the filename
    assert (isinstance(filename, str)), "Enter valid filename"

    # Setting up try-catch block just in case error is thrown
    try:
        
        # Creating a numpy array to hold the 8 players in the tournament
        players = np.arange(8)
        # Creating a numpy array to hold the ratings of each player 
        # in the tournament
        ratings = 1500 * np.ones(8, dtype = np.float32)
        c = 100
    
        # Creating a data frame out of the data read form the inputted
        # csv file using pandas
        data_frame = pd.read_csv(filename, index_col = 0)
        
        # taking data from the inputted csv to populate the numpy arrays that
        # were created
        for index, row in data_frame.iterrows():
            
            # designating player A and player B from the csv data
            player_A = row["player_A"]
            player_B = row["player_B"]
            
            # calculating the difference in skill level between the two players
            # who are competing based on their ratings
            delta = (ratings[player_A] - ratings[player_B]) / c
            # calculating the probability that player A wins the game
            probability_A = np.exp(delta) / (1 + np.exp(delta))
            # calculating the probability that player A wins the game
            probability_B = 1 - probability_A
            
            # reading the csv file to see who won the matchup
            if row["winner"] == player_A:
                # adjusting the players' ratings based on the outcome of the match
                ratings[player_A] += 5 * (1.0 - probability_A)
                ratings[player_B] += 5 * (0.0 - probability_B)
            else:
                # adjusting the players' ratings based on the outcome of the match
                ratings[player_A] += 5 * (0.0 - probability_A)
                ratings[player_B] += 5 * (1.0 - probability_B)
    
    # Preparing to throw FileNotFoundError if inputted filename is not found
    except FileNotFoundError:
        print("File \"" + filename + "\" was not found.")
    # Throws message if unknown error arises while reading the data
    except:
        print("Unknown error while accessing data in \"" + filename + "\"")
    else:
        # Creating dicitonary to be returned
        dictionary = {}
        
        # Adding the contents of the numpy arrays to the dictionary to be returned
        for player, rating in zip(players, ratings):
            dictionary[str(player)] = rating
        
        # Returning array containing the player's names and ratings
        return dictionary
    

def display_ratings(dictionary):
    """
    

    Parameters
    ----------
    dictionary : Dictionary
        Dictionary containing the players' names and ratings..

    Returns
    -------
    None.

    """
    
    # Ensuring that the user inputs a dictionary value as the argument
    assert (isinstance(dictionary, dict)), "Enter valid dictionary"
    
    # edit the fonts of the graph
    plt.rc('font', family = 'serif')
    
    # Creates a 6 by 5 inch enpty plot
    fig = plt.figure(figsize = (6, 5))
    
    # Creates lists containing the players and their ratings from the inputted
    # dictionary
    players = list(dictionary.keys())
    ratings = list(dictionary.values())
    
    # Labeling and sizing the y-axis
    plt.ylabel('Rating', fontsize = 24)
    plt.ylim(1300, 1700)
    
    # Labeling and sizing the x-axis
    plt.xlabel('Players', fontsize = 24)
    plt.xticks(fontsize = 24)
    plt.yticks([i * 50 + 1300 for i in range(9)], fontsize = 24)
    
    # Draws bar graph in empty 6 x 5 inch empty space created above
    plt.bar(players, ratings)
    
    # Places axes and labels within the plot area
    plt.tight_layout()
    
    # Saves the plot to an external file named projections.pdf
    plt.savefig('projections.pdf')
    
    # Displays the plot on the console
    plt.show()
    
    return
  


def project_win_probs(dictionary):
    """
    

    Parameters
    ----------
    dictionary : Dictionary
        Dictionary containing the players of the game and their ratings.

    Returns
    -------
    probability_dict : Dictionary
        Dictionary containing the players and the probability that they win
        the entire tournament.

    """
    # Ensuring that the user inputs a dictionary value as the argument
    assert (isinstance(dictionary, dict)), "Enter valid dictionary"
    
    
    # creating a numpy array containing the players of the game
    players = np.array(list(dictionary.keys()))
    
    # creating a numpy array conatining the number of times that each
    # player won over the n trials
    wins_array = np.zeros(8, dtype = np.int32)
    
    # creating a list containing the players still in contention
    in_contention = list(players)
    
    

    # Setting the number of times that the simulation should run the tournament
    times_run = 100
    
    # Setting up the simulation to run n = 100 times
    for n in range(times_run):
        
        # Creating variable to hold individual tournament winner
        tournament_winner = None
    
        # Create a list to contain the matchups within the current stage of 
        # the tournament
        current_bracket = create_bracket(in_contention, dictionary)
        
        # Determine how many matches are left in the tournament
        matches_remaining = len(current_bracket)
 
        # Repeat narrowing of tournament bracket until no other matches remain
        while matches_remaining > 0:
            
            # Iterate through each match in the current bracket
            for match in current_bracket:
                # Use helper function to randomly determine the loser of a match
                match_loser = find_loser(match)
                # Remove the loser from the list of players still in contention
                in_contention.remove(match_loser)
            
            # Create a new bracket out of the players still in contention
            current_bracket = create_bracket(in_contention, dictionary)
            
            # Update matches_remaining variable based on how many matchups there
            # are in the new bracket
            matches_remaining = len(current_bracket)
                
            # If no matches remain, name the last standing player the winner 
            if matches_remaining == 0:
                tournament_winner = in_contention[0]
        
        wins_array[int(tournament_winner)] += 1
        
        # creating a list containing the players of the game
        in_contention = list(players)
        # Creating the randomizing lineup for the next tournament's intial matchups
        rand.shuffle(in_contention)

    

    # Creating the ditionary containing each player's probability of winning
    # (to be returned)
    probability_dict = {}
    
    # Performing operation on numpy array to determine probabilities of winning 
    # for each player
    probabilities = wins_array / times_run
    
    # Placing the probabilities for each player into a dictionary
    for a, b in zip(players, probabilities):
        probability_dict[a] = b
        

    # Returning dictionary containing players of game and their likelihood of winning
    return probability_dict


def display_probs(prob_dictionary):
    """
    

    Parameters
    ----------
    prob_dictionary : Dictionary
        Dictionary containing the players and their probabilities of winning 
        the entire tournament.

    Returns
    -------
    None.

    """
    
    # Ensuring that the user inputs a dictionary value as the argument
    assert (isinstance(prob_dictionary, dict)), "Enter valid dictionary"
    
    
    # create a sorted dictionary sorted by win probability
    sorted_dict = {}
    
    # Create a list of the win probabilities
    probabilities_list = list(prob_dictionary.values())
    
    # Sort the above list from greatest probability to smallest
    sorted_probabilities_list = sorted(probabilities_list, reverse = True)
    
    # Iterate through elements in sorted list
    for prob in sorted_probabilities_list:
        
        # Find the location of the player in the dicitionary with 
        # the matching probability  
        player_location = list(prob_dictionary.values()).index(prob)
        # Finding the actual player's name
        player_name = list(prob_dictionary.keys())[player_location]
        # Adding this player's name and win probability to the sorted dictionary
        sorted_dict[player_name] = prob_dictionary[player_name]

    
    # Creating dictionary that will be turned into csv using pandas
    csv_dict = {}
    csv_dict['Player Name'] = []
    csv_dict['Win Probability'] = []
    
    # Iterate through each key-value pair in the sorted dictionary
    for key, value in sorted_dict.items():
        # Adding to the csv dictionary each key-value pair
        csv_dict['Player Name'].append(key)
        csv_dict['Win Probability'].append(value)
        
    # Create a data fram to hold the dictionary that is going to be written to
    # the fiile probs.csv
    data_frame = pd.DataFrame(csv_dict)
    data_frame.to_csv('probs.csv', index = False)
    
    # Create a figure for the plot to be 6 x 5 inches
    fig = plt.figure(figsize = (6, 5))
    
    # use the matplotlib pie function to draw pie chart with the player's 
    # win probabilities
    plt.pie(list(sorted_dict.values()), labels = list(sorted_dict.keys()), \
            radius = 1.4, autopct = '%1.1f%%', textprops = {'fontsize': 14})
    
    # save the pie chart to a file named projections_pie.pdf
    plt.savefig('projections_pie.pdf')
    
    # diplay the pie chart to the console
    plt.show()
    
    return 
          


def create_bracket(player_list, dictionary):
    """
    

    Parameters
    ----------
    player_list : list
        List containing the players in the next round of the tournament.
    ratings_dictionary : dictionary
        Dictionary containing all of the player's ratings.

    Returns
    -------
    bracket : List
        List containing the matchups in the bracket with players and their
        associated rating.

    """
    # Create list containing the matchup that will take place during the
    # tournament round
    bracket = []
    
    # Create a dictionary containing matchup players names and ratings to be
    # added to the bracket list 
    matchup = {}
    
    # Assigning the matchups for the first round of the tournament
    for i in range(len(player_list) // 2):
        # Assigning the two players next to each other in the list to play
        # against each other
        player_A = player_list[i * 2]
        player_B = player_list[i * 2 + 1]
        # Matching each player with their rating from the inputted dictionary
        matchup[player_A] = dictionary[player_A]
        matchup[player_B] = dictionary[player_B]
        
        # adding the matchups to the dictionary representing the current bracket
        # that is to be returned
        bracket.append(matchup)
        
        # Reset matchup dict for next matchup
        matchup = {}
    
    return bracket


       
def find_loser(dictionary):
    """
    

    Parameters
    ----------
    dictionary : Dictionary
        Dictionary conatining the current players and their rating in a matchup.

    Returns
    -------
    String
        The name of the player won the match.

    """
    # Ensuring that the user inputs a dictionary value as the argument
    assert (isinstance(dictionary, dict)), "Enter valid dictionary"
    
    # Generate random number to help determine winner
    rand_num = rand.random()
    
    # Getting the player names from the inputted dictionary
    player_A = list(dictionary.keys())[0]
    player_B = list(dictionary.keys())[1]
    c = 100
    
    # calculating the difference in skill level between the two players
    # who are competing based on their ratings
    delta = (dictionary[player_A] - dictionary[player_B]) / c
    # calculating the probability that player A wins the game
    probability_A = np.exp(delta) / (1 + np.exp(delta))

    # determining who loses the game based on the probability of player
    # A winning and the random number that was generated
    if rand_num < probability_A:
        return player_B
    else:
        return player_A
    