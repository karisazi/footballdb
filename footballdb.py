import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() # load all environment variables from .env
import os

import mysql.connector


genai.configure(api_key=os.environ['GEMINI_API_KEY'])


# import modules football_info_function
from footballai import get_info_football


def extract_football_to_db(path, db_user='root', db_password='root'):
    #initialize cursor 
    db = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_password
    )
    
    cursor = db.cursor()
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    cursor.execute('CREATE DATABASE IF NOT EXISTS football;')
    cursor.execute('USE football;')
        
    
    ## create all tables
    # Create Table Game
    cursor.execute('''CREATE TABLE IF NOT EXISTS GameS (
        game_id INT PRIMARY KEY AUTO_INCREMENT,
        championship VARCHAR(100),
        round smallint,
        date DATE,
        time TIME,
        stadium VARCHAR(150),
        home_team VARCHAR(50)  NOT NULL,
        away_team VARCHAR(50) NOT NULL,
        referee VARCHAR(50),
        assistant_referee1 VARCHAR(50),
        assistant_referee2 VARCHAR(50),
        fourth_official VARCHAR(50),
        result_1sthalf VARCHAR(10),
        result_final VARCHAR(10)
    );''')
    cursor.execute('ALTER TABLE gameS AUTO_INCREMENT=1000')

    # Create Table Team
    cursor.execute('''CREATE TABLE IF NOT EXISTS Teams (
        team_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        type VARCHAR(10),
        game_id INT,
        FOREIGN KEY(game_id) REFERENCES Games(game_id)
    );''')
    cursor.execute('ALTER TABLE Teams AUTO_INCREMENT=2000')
    
    # Create Table Player
    cursor.execute('''CREATE TABLE IF NOT EXISTS Players (
        player_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        number smallint,
        registration VARCHAR(15),
        position VARCHAR(10),
        type VARCHAR(15),
        team_id INT,
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    );''')
    cursor.execute('ALTER TABLE Players AUTO_INCREMENT=3000')
    
    # Create Table Staff
    cursor.execute('''CREATE TABLE IF NOT EXISTS StaffS (
        staff_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        role VARCHAR(20),
        team_id INT,
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    );''')
    cursor.execute('ALTER TABLE StaffS AUTO_INCREMENT=4000')

    # Create Table Substitutions
    cursor.execute('''CREATE TABLE IF NOT EXISTS Substitutions (
        substitution_id INT PRIMARY KEY AUTO_INCREMENT,
        player_out INT,
        player_in INT,
        time VARCHAR(6),
        team_id INT,
        half varchar(5),
        FOREIGN KEY(player_out) REFERENCES Players(player_id),
        FOREIGN KEY(player_in) REFERENCES Players(player_id),
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    );''')
    cursor.execute('ALTER TABLE Substitutions AUTO_INCREMENT=5000')

    # Create Table Goals
    cursor.execute('''CREATE TABLE IF NOT EXISTS Goals (
        goal_id INT PRIMARY KEY AUTO_INCREMENT,
        player_id INT,
        time VARCHAR(5),
        team_id INT,
        type VARCHAR(10),
        FOREIGN KEY(player_id) REFERENCES Players(player_id),
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    );''')
    cursor.execute('ALTER TABLE Goals AUTO_INCREMENT=6000')
    
    # Create Table Card
    cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (
        card_id INT PRIMARY KEY AUTO_INCREMENT,
        player_id INT,
        time VARCHAR(5),
        reason VARCHAR(35),
        team_id INT,
        half VARCHAR(10),
        FOREIGN KEY(player_id) REFERENCES Players(player_id),
        FOREIGN KEY(team_id) REFERENCES Teams(team_id)
    );''')
    cursor.execute('ALTER TABLE Cards AUTO_INCREMENT=7000')


    ## Add football info to Database
    # get and insert info football to database
    for filename in os.listdir(path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(path, filename)
        game, teams, players, staffs, substitutions, goals, cards = get_info_football(file_path)
    
    try:
        # Add Game Match
        cursor.execute('''
            INSERT INTO Games (
                championship, round, date, time, stadium, home_team, away_team, referee,
                assistant_referee1, assistant_referee2, fourth_official, result_1sthalf, result_final
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (game['championship'], game['round'], game['date'], game['time'], game['stadium'], 
            game['home_team'], game['away_team'], game['referee'], game['assistant_referee1'], 
            game['assistant_referee2'], game['fourth_official'], game['result_1sthalf'], 
            game['result_final']))
        # db.commit()
        
        
        # Add Team
        cursor.execute('SELECT game_id FROM games WHERE championship = %s', (game['championship'],))
        game_id = cursor.fetchone()[0]  
        for team in teams:
            cursor.execute('''
                INSERT INTO Teams (
                    name, type, game_id
                ) 
                VALUES (%s, %s, %s)     ## must as String
            ''', (team['team'], team['type'], game_id))
        # db.commit()
        
        
        # Add player
        for team in players:
            cursor.execute('SELECT team_id FROM teams WHERE name = %s', (team['team_name'],))
            team_id = cursor.fetchone()[0]  
            for player in team['players']:
                cursor.execute('''
                    INSERT INTO players (
                        name, number, registration, position, type, team_id
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s)     ##  must as String
                ''', (player['name'], player['number'], player['registration'], player['position'], player['type'], team_id))
                # db.commit()
                
                
        # Add staff
        for team in staffs:
            cursor.execute('SELECT team_id FROM teams WHERE name = %s', (team['team_name'],))
            team_id = cursor.fetchone()[0]  
            for staff in team['staffs']:
                cursor.execute('''
                    INSERT INTO staffs (
                        name, role, team_id
                    ) 
                    VALUES (%s, %s, %s)     ##  must as String
                ''', (staff['name'], staff['role'], team_id))
                # db.commit()
                

        # Add substitution
        for team in substitutions:
            cursor.execute('SELECT team_id FROM teams WHERE name = %s', (team['team_name'],))
            team_id = cursor.fetchone()[0]  
            for substitution in team['substitutions']:
                cursor.execute('SELECT player_id FROM Players WHERE number = %s and team_id=%s', (substitution['player_out'], team_id))
                player_out_id = cursor.fetchone()[0]
                
                cursor.execute('SELECT player_id FROM Players WHERE number = %s and team_id=%s', (substitution['player_in'], team_id))
                player_in_id = cursor.fetchone()[0]  
                
                cursor.execute('''
                    INSERT INTO substitutions (
                        player_out, player_in, time, team_id, half
                    ) 
                    VALUES (%s, %s, %s, %s, %s)     ##  must as String
                ''', (player_out_id, player_in_id, substitution['time'], team_id, substitution['half']))
                # db.commit()
        
        
        # Add Goals
        for team in goals:
            cursor.execute('SELECT team_id FROM teams WHERE name = %s', (team['team_name'],))
            team_id = cursor.fetchone()[0]  
            for goal in team['goals']:
                cursor.execute('SELECT player_id FROM Players WHERE number = %s and team_id=%s', (goal['player_num'], team_id))
                player_id = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT INTO Goals (
                        player_id, time, team_id, type
                    ) 
                    VALUES (%s, %s, %s, %s)     ##  must as String
                ''', (player_id, goal['time'], team_id, goal['type']))
                # db.commit()
                
        
        # Add Cards
        for team in cards:
            cursor.execute('SELECT team_id FROM teams WHERE name = %s', (team['team_name'],))
            team_id = cursor.fetchone()[0]  
            for card in team['cards']:
                cursor.execute('SELECT player_id FROM Players WHERE number = %s and team_id=%s', (card['player_num'], team_id))
                player_id = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT INTO Cards (
                        player_id, time, reason, team_id, half
                    ) 
                    VALUES (%s, %s, %s, %s, %s)     ##  must as String
                ''', (player_id, card['time'], card['reason'], team_id, card['half']))
                # db.commit()

    finally:
        db.commit()
        # close database
        db.close()


# if __name__ == '__main__':
#     path = 'D:/signup/upwork/footbal/football_docs'
#     extract_football_to_db(path=path, db_user='root', db_password='root')