import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() # load all environment variables from .env
import os
import ast

genai.configure(api_key=os.environ['GEMINI_API_KEY'])



#### Get Info using GenAI ####

def get_gemini_reponse(file, info_prompt, output):
    input_prompt = f'''
    You are an expert in understanding football match report. 
    You will receive input pdf as football match report and you will answer question
    based on the input pdf file.
    You should return {output}
    '''
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(file)
    response = model.generate_content([input_prompt, sample_pdf, info_prompt])
    return response.text


def get_info_games(file):
    game_info_input = 'match game information'
    game_output = '''Get all match game information in JSON format. 

    Use this JSON schema:
    Game = {'championship': str, 
            'round': int, 
            'date': get date with order year-month-day like '2024-08-23',  # Date in YYYY-MM-DD format
            'time': 'HH:MM:SS',    # Time in HH:MM:SS format
            'stadium': str, 
            'home_team': str, 
            'away_team': str, 
            'referee'; str, 
            'assistant_referee1': str, 
            'assistant_referee2'; str, 
            'fourth_official': str, 
            'result_1sthalf'; str, 
            'result_final': str}
    without newline
    '''

    game_response = get_gemini_reponse(file, game_info_input, game_output)
    game = ast.literal_eval(game_response)
    return game


def get_info_teams(file):
    team_info_input = 'team information'
    team_output = '''Get all team information in JSON format. 

    Use this JSON schema:
    [{'team': str, 
            'type': either home/away}]
    without newline
    ''' 

    team_response = get_gemini_reponse(file, team_info_input, team_output)
    teams = ast.literal_eval(team_response)
    return teams
    
    
def get_info_players(file):
    player_info_input = 'player information'
    player_output = '''Get all player information for each team in JSON format. 

    Use this JSON schema:
    [ {
        "team_name": "string",
        "players": [
            {
            'name': str either home/away, 
            'number': int,
            'registration': str,
            'position': either Starter or Reserve,
            'type': either Professional or Amateur,
            }
        ]
    } ]
    without newline
    '''

    player_response = get_gemini_reponse(file, player_info_input, player_output)
    players = ast.literal_eval(player_response)
    return players

    
def get_info_staffs(file):
    staff_info_input = 'staff information'
    staff_output = '''Get all staff information for each team in JSON format. 

    Use this JSON schema:
    [ {
        "team_name": "string",
        "staffs": [
            {
            'name': str, 
            'role': str
            }
        ]
    } ]
    without newline
    '''


    staff_response = get_gemini_reponse(file, staff_info_input, staff_output)
    staffs = ast.literal_eval(staff_response)
    return staffs
    

def get_info_substitutions(file):
    substitution_info_input = 'substitution information'
    substitution_output = '''Get all substitution information for each team in JSON format. 

    Use this JSON schema:
    [  {
        "team_name": "string",
        "substitutions": [
            {
            'player_out': int no of player, 
            'player_in': int no of player,
            'time': str,
            'half': str
    '        }
        ]
    }]
    without newline
    '''


    substitution_response = get_gemini_reponse(file, substitution_info_input, substitution_output)
    substitutions = ast.literal_eval(substitution_response)
    return substitutions

    
def get_info_goals(file):
    goal_info_input = 'goal information'
    goal_output = '''Get all goal information for each team in JSON format. 

    Use this JSON schema:
    [  {
        "team_name": "string",
        "goals": [
            {
            'player_num': int no of player, 
            'time': str,
            'type':  "Penalty" (use full type names like "Normal", "Penalty", "Against", or "Foul")
    '        }
        ]
    }]

    without newline
    '''

    goal_response = get_gemini_reponse(file, goal_info_input, goal_output)
    goals = ast.literal_eval(goal_response)
    return goals

    
def get_info_cards(file):
    card_info_input = 'card information'
    card_output = '''Get all card information for each team in JSON format. 

    Use this JSON schema:
    [  {
        "team_name": "string",
        "cards": [
            {
            'player_num': int no of player, 
            'time': str,
            'reason':  str,
            'half: str
    '        }
        ]
    }]
    without newline
    '''

    card_response = get_gemini_reponse(file, card_info_input, card_output)
    cards = ast.literal_eval(card_response)
    return cards

    
# get info foortball per pdf file
def get_info_football(dir_path):
    
    game = get_info_games(dir_path)
    teams = get_info_teams(dir_path)
    players = get_info_players(dir_path)
    staffs = get_info_staffs(dir_path)
    substitutions =  get_info_substitutions(dir_path)
    goals = get_info_goals(dir_path)
    cards = get_info_cards(dir_path)
    
    return game, teams, players, staffs, substitutions, goals, cards

