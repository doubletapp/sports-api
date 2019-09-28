from django.core.management.base import BaseCommand
from graphqlclient import GraphQLClient
from api.matches.models import Match
from api.teams.models import Team
from api.events.models import Event
import json

event_types = [
    dict(code='corner_kick', model='statCornerKick'),
    dict(code='free_kick', model='statFreeKick'),
    dict(code='goal_kick', model='statGoalKick'),
    dict(code='match_started', model='statMatchStarted'),
    dict(code='offside', model='statOffside'),
    dict(code='penalty_awarded', model='statPenaltyAwarded'),
    dict(code='possible_video_assistant_referee', model='statPossibleVideoAssistantReferee'),
    dict(code='red_card', model='statRedCard'),
    dict(code='score_change', model='statScoreChange'),
    dict(code='shot_off_target', model='statShotOffTarget'),
    dict(code='shot_on_target', model='statShotOnTarget'),
    dict(code='yellow_card', model='statYellowCard'),

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
              team
              value {
                ... on %s {
                  time
                }
                ... on statCornerKick { matchTime team }
                ... on statFreeKick { matchTime team }
                ... on statGoalKick { matchTime team }
                ... on statOffside { matchTime team }
                ... on statPenaltyAwarded { matchTime team }
                ... on statPossibleVideoAssistantReferee { matchTime }
                ... on statRedCard { matchTime }
                ... on statScoreChange { matchTime player:goalScorer { lastName avatar {main} } homeScore awayScore methodScore}
                ... on statShotOffTarget { matchTime }
                ... on statShotOnTarget { matchTime }
                ... on statYellowCard { matchTime player { lastName avatar { main } } }

                
              }
            }
          }
        }
'''




class Command(BaseCommand):
    def handle(self, *args, **options):
        # Event.objects.all().delete()
        # Match.objects.all().delete()
        # return

        client = GraphQLClient('https://vk-hackathon-gateway.trbna.com/ru/graphql/')

        for match_id in match_ids:
            query = base_query % (match_id, 'match_started', 'statMatchStarted')
            response = client.execute(query)
            print(response)
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

            match, created = Match.objects.update_or_create(
                global_id=match_id,
                defaults=dict(
                    start_datetime=start_time, status=status, minute=minute,
                    home_team_score = home_team_data.get('score'),
                    away_team_score = away_team_data.get('score'),
                    home_team=home_team,
                    away_team=away_team
                )
            )

            for event_type in event_types:
                query = base_query % (match_id, event_type['code'], event_type['model'])
                result = client.execute(query)
                print(result)
                data = json.loads(result)
                events = data.get('data', {}).get('stat_match').get('events', [])

                for event_data in events:
                    time = event_data.get('time')
                    code = event_type['code']
                    if code is 'match_started':
                        match.real_start_datetime = time
                        match.save()
                        continue

                    try:
                        event = Event.objects.get(global_id=event_data.get('id'))
                    except Event.DoesNotExist:
                        event = Event(global_id=event_data.get('id'))
                    event.type = code
                    event.time = time
                    event.team = event_data.get('team')
                    event.match = match
                    event.match_time = event_data.get('value', {}).get('matchTime')
                    event.player_name = event_data.get('value', {}).get('player', {}).get('lastName')
                    event.player_avatar = event_data.get('value', {}).get('player', {}).get('avatar', {}).get('main')
                    event.home_score = event_data.get('value', {}).get('homeScore')
                    event.away_score = event_data.get('value', {}).get('awayScore')
                    event.method_score = event_data.get('value', {}).get('methodScore')
                    event.save()




