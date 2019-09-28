from django.core.management.base import BaseCommand
from graphqlclient import GraphQLClient
from api.matches.models import Match
from api.teams.models import Team
import json

event_types = [
    dict(code='score_change', model='statScoreChange'),
    dict(code='red_card', model='statRedCard'),
    dict(code='corner_kick', model='statCornerKick'),
    dict(code='penalty_awarded', model='statPenaltyAwarded'),
]

match_ids = ['16514885']

base_query = '''
        {
          stat_match(id: "%s") {
            id
            currentMinute
            status
            scheduledAt
            venue { city }
            home {
              score
              team { id name logo { url: resize(width:"255", height: "255") }}
            }
            away {
              score
              team { id name logo { url: resize(width:"255", height: "255") }}
            }
    
            events(radarType: ["%s"])
            {
              id
              time
              value {
                ... on %s {
                  time
                  matchTime
                  team
                }
                ... on statRedCard { player {name }}
                ... on statPenaltyAwarded { player {name }, team }
              }
            }
          }
        }
'''




class Command(BaseCommand):
    def handle(self, *args, **options):

        client = GraphQLClient('https://vk-hackathon-gateway.trbna.com/ru/graphql/')

        for match_id in match_ids:
            query = base_query % (match_ids[0], 'red_card', 'statRedCard')
            response = client.execute(query)
            response = json.loads(response)
            match_data = response.get('data', {}).get('stat_match')
            home_team_data = match_data.get('home')
            away_team_data = match_data.get('away')

            start_time = match_data.get('scheduledAt')
            status = match_data.get('status')
            minute = match_data.get('currentMinute')

            home_team, created = Team.objects.update_or_create(
                global_id=home_team_data.get('team', {}).get('id'),
                defaults=dict(
                    name=home_team_data.get('team', {}).get('name'),
                    logo = home_team_data.get('team', {}).get('logo').get('url'),
                )
            )
            away_team, created = Team.objects.update_or_create(
                global_id=away_team_data.get('team', {}).get('id'),
                defaults=dict(
                    name=away_team_data.get('team', {}).get('name'),
                    logo = away_team_data.get('team', {}).get('logo').get('url'),
                )
            )
            print(home_team)
            match, created = Match.objects.update_or_create(
                global_id=match_id,
                defaults=dict(
                    start_datetime=start_time, status=status, minute=minute,
                    home_team_score = home_team_data.get('score'),
                    away_team_score = away_team_data.get('score'),
                    home_team_id=home_team,
                    away_team_id=away_team
                )
            )

            for event_type in event_types:
                query = base_query % (match_ids[0], event_type['code'], event_type['model'])
                result = client.execute(query)
                data = json.loads(result)

                events = data.get('data', {}).get('stat_match').get('events', [])
                for event in events:
                    print(type)
                    print(event)







