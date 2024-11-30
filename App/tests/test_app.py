import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from io import StringIO
import sys


from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):
    #User Unit Tests
    def test_new_user(self):
        user = User("ryan", "ryanpass", "ryan@email.com")
        assert user.username == "ryan"

    def test_hashed_password(self):
        password = "ryanpass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("ryan", password, "ryan@email.com")
        assert user.password != password

    def test_check_password(self):
        password = "ryanpass"
        user = User("ryan", password, "ryan@email.com")
        assert user.check_password(password)

    #Student Unit Tests
    def test_new_student(self):
      
      student = Student("james", "jamespass", "james@email.com")
      assert student.username == "james"

    def test_student_get_json(self):
      
      student = Student("james", "jamespass", "james@email.com")
      self.assertDictEqual(student.get_json(), {"id": None, "username": "james", "rating_score": 0, "comp_count": 0, "curr_rank": 0})

    #Moderator Unit Tests
    def test_new_moderator(self):
      
      mod = Moderator("robert", "robertpass", "robert@email.com")
      assert mod.username == "robert"

    def test_moderator_get_json(self):
      
      mod = Moderator("robert", "robertpass", "robert@email.com")
      self.assertDictEqual(mod.get_json(), {"id":None, "username": "robert", "competitions": []})
    
    #Team Unit Tests
    def test_new_team(self):
      
      team = Team("Scrum Lords")
      assert team.name == "Scrum Lords"
    
    def test_team_get_json(self):
      
      team = Team("Scrum Lords")
      self.assertDictEqual(team.get_json(), {"id":None, "name":"Scrum Lords", "students": []})
    
    #Competition Unit Tests
    def test_new_competition(self):
      
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
      
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      self.assertDictEqual(competition.get_json(), {"id": None, "name": "RunTime", "date": "09-02-2024", "location": "St. Augustine", "level": 1, "max_score": 25, "moderators": [], "teams": []})
    
    #Notification Unit Tests
    def test_new_notification(self):
      
      notification = Notification(1, "Ranking changed!")
      assert notification.student_id == 1 and notification.message == "Ranking changed!"

    def test_notification_get_json(self):
      
      notification = Notification(1, "Ranking changed!")
      self.assertDictEqual(notification.get_json(), {"id": None, "student_id": 1, "notification": "Ranking changed!"})
    
    #Ranking Unit Tests
    def test_new_ranking(self):
      
      ranking = Ranking(1, 1, "20-02-2024")
      assert ranking.student_id == 1 and ranking.rank == 1 and ranking.date == "20-02-2024"
  
    # def test_set_points(self):
    
    #   ranking = Ranking(1)
    #   ranking.set_points(15)
    #   assert ranking.total_points == 15

    # def test_update_ranking(self):
      
    #   ranking = Ranking(1)
    #   ranking.update_rankings(12)
    #   assert ranking.rank == 12

    # def test_previous_ranking(self):
    
    #   ranking = Ranking(1)
    #   ranking.set_previous_ranking(1)
    #   assert ranking.prev_ranking == 1

    # def test_ranking_get_json(self):
    
    #   ranking = Ranking(1)
    #   ranking.set_points(15)
    #   ranking.set_ranking(1)
    #   self.assertDictEqual(ranking.get_json(), {"rank":1, "total points": 15})
    
    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
      
      competition_team = CompetitionTeam(1, 1)
      assert competition_team.comp_id == 1 and competition_team.team_id == 1

    def test_competition_team_update_points(self):
      
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_points(15)
      assert competition_team.points_earned == 15

    def test_competition_team_update_rating(self):
      
      competition_team = CompetitionTeam(1, 1)
      competition_team.update_rating(12)
      assert competition_team.rating_score == 12

    def test_competition_team_get_json(self):
      
      competition_team = CompetitionTeam(4, 4)
      competition_team.update_points(15)
      competition_team.update_rating(12)
      self.assertDictEqual(competition_team.get_json(), {"id": 4, "team_id": 4, "competition_id": 4, "points_earned": 15, "rating_score": 12})

    def test_competition_team_attatch_manager(self):
      comp_team = CompetitionTeam(1, 1)
      student = Student("james", "jamespass", "james@email.com")
      student2 = Student("james2", "james2pass", "james2@email.com")
      comp_team.attach(student)
      comp_team.attach(student2)
      self.assertEqual(len(comp_team.managers),2)

    def test_competition_team_attatch_manager_dupe(self):
      comp_team = CompetitionTeam(1, 1)
      student = Student("james", "jamespass", "james@email.com")
      comp_team.attach(student)
      comp_team.attach(student)
      self.assertEqual(len(comp_team.managers),1)

    def test_competition_team_detach_manager(self):
      comp_team = CompetitionTeam(1, 1)
      student = Student("james", "jamespass", "james@email.com")
      comp_team.attach(student)
      comp_team.detach(student)
      self.assertEqual(len(comp_team.managers),0)



    #CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
      
      competition_moderator = CompetitionModerator(1, 1)
      assert competition_moderator.comp_id == 1 and competition_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
      
      competition_moderator = CompetitionModerator(1, 1)
      self.assertDictEqual(competition_moderator.get_json(), {"id": None, "competition_id": 1, "moderator_id": 1})

    #StudentTeam Unit Tests
    def test_new_student_team(self):
      
      student_team = StudentTeam(1, 1)
      assert student_team.student_id == 1 and student_team.team_id == 1
    
    def test_student_team_get_json(self):
     
      student_team = StudentTeam(1, 1)
      self.assertDictEqual(student_team.get_json(), {"id": None, "student_id": 1, "team_id": 1})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()



class IntegrationTests(unittest.TestCase):

    def setUp(self):
        # This method is called before each test
        db.drop_all()
        db.create_all()

    
    def test_create_student(self):
        newStudent = create_student("tyrell", "tyrellpass", "tyrell@email.com")
        student = get_student_by_username("tyrell")
        self.assertEqual(student.username, "tyrell")

    
    def test_create_moderator(self):
        newMod = create_moderator("debra", "debrapass", "debra@email.com")
        mod = get_moderator_by_username("debra")
        self.assertEqual(mod.username, "debra")


    def test_create_team(self):

        student1 = create_student("james", "jamespass", "james@email.com")
        student2 = create_student("steven", "stevenpass", "steven@email.com")
        student3 = create_student("emily", "emilypass", "emily@email.com")
        students = [student1.username, student2.username, student3.username]
        newteam = create_team("Runtime Errors", students)
        team = get_team_by_name("Runtime Errors")
        self.assertEqual(team.name, "Runtime Errors")
        
    
    #Feature 1 Integration Tests
    def test1_create_competition(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      
      newComp = get_competition_by_name("RunTime")
      self.assertEqual(newComp.name, "RunTime")

    def test_create_dupe_competition(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      
      assert comp2 == None

    # def test2_create_competition(self):
      
    #   mod = create_moderator("debra", "debrapass", "debra@email.com")
    #   comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   self.assertDictEqual(comp.get_json(), {"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": []})
      
    #Feature 2 Integration Tests


    def test_competition_team_notify_manager(self):

      


      comp_team = CompetitionTeam(1, 1)
      student = create_student("james", "jamespass", "james@email.com")
      comp_team.attach(student)

      captured_output = StringIO()
      sys.stdout = captured_output


      comp_team.notify()

      sys.stdout = sys.__stdout__


      output = captured_output.getvalue().strip()
      expected_output = ("Notifying 1 managers.\nNotifying manager 1: james\nUpdating manager: james")
      self.assertEqual(len(comp_team.managers),1)
      self.assertEqual(output, expected_output)

    def test_add_results(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      assert comp_team.points_earned == 15

    def test_display_competition_results(self):

      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      student7 = create_student("isabella", "isabellapass", "isabella@email.com")
      student8 = create_student("richard", "richardpass", "richard@email.com")
      student9 = create_student("jessica", "jessicapass", "jessica@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 12)
      students3 = [student7.username, student8.username, student9.username]
      team3 = add_team(mod.username, comp.name, "Beyond Infinity", students3)
      comp_team = add_results(mod.username, comp.name, "Beyond Infinity", 10)
      self.assertListEqual(display_competition_results(comp.name), [{"placement": 1 , "team": "Runtime Terrors", "members" : ['james', 'steven', 'emily'], "score": 15.0}, {"placement": 2 , "team": "Scrum Lords", "members" : ['mark', 'eric', 'ryan'], "score": 12.0}, {"placement": 3 , "team": "Beyond Infinity", "members" : ['isabella', 'richard', 'jessica'], "score": 10.0}, ])

    def test1_add_team(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      students = [student1.username, student2.username, student3.username]
      newteam = create_team("Runtime Terrors", students)
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      self.assertIn("Runtime Terrors", [t.name for t in comp.teams])
    
    def test2_add_team(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      students = [student1.username, student2.username, student3.username]
      add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students = [student1.username, student4.username, student5.username]
      team = add_team(mod.username, comp.name, "Scrum Lords", students)
      assert team == None
    
    def test3_add_team(self):
      
      mod1 = create_moderator("debra", "debrapass", "debra@email.com")
      mod2 = create_moderator("robert", "robertpass", "robert@email.com")
      comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod2.username, comp.name, "Runtime Terrors", students)
      assert team == None

    #Feature 3 Integration Tests
    def test_display_student_info(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      students = [student1.username, student2.username, student3.username]
      team = add_team(mod.username, comp.name, "Runtime Terrors", students)
      comp_team = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertDictEqual(display_student_info("james"), {"profile": {'id': 1, 'username': 'james', 'rating_score': 120, 'comp_count': 1, 'curr_rank': 1}, "competitions": [{'name': 'RunTime', 'points_earned': 15, 'rating_score': 120, 'team': 'Runtime Terrors'}]})

      


    def test_get_historical_rank(self):
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)

      
      self.assertListEqual(get_rank_history_json("steven"), [{'date': datetime(2024, 2, 23, 0, 0), 'rank': 4, 'student_id': 2},{'date': datetime(2024, 3, 29, 0, 0), 'rank': 1, 'student_id': 2}])


    #Feature 4 Integration Tests
    def test_display_competition(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      student7 = create_student("isabella", "isabellapass", "isabella@email.com")
      student8 = create_student("richard", "richardpass", "richard@email.com")
      student9 = create_student("jessica", "jessicapass", "jessica@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      #comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      #comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 12)
      students3 = [student7.username, student8.username, student9.username]
      team3 = add_team(mod.username, comp.name, "Beyond Infinity", students3)
      #comp_team = add_results(mod.username, comp.name, "Beyond Infinity", 10)
      # update_ratings(mod.username, comp.name)
      # update_rankings()
      self.assertDictEqual(comp.get_json(), {'id': 1, 'name': 'RunTime', 'date': '29-03-2024', 'location': 'St. Augustine', 'level': 2, 'max_score': 25, 'moderators': ['debra'], 'teams': ['Runtime Terrors', 'Scrum Lords', 'Beyond Infinity']})

    #Feature 5 Integration Tests
    def test_display_rankings(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertListEqual(display_rankings(), [{"placement": 1, "student": "james", "rating score": 120}, {"placement": 1, "student": "steven", "rating score": 120}, {"placement": 1, "student": "emily", "rating score": 120}, {"placement": 4, "student": "mark", "rating score": 80}, {"placement": 4, "student": "eric", "rating score": 80}, {"placement": 4, "student": "ryan", "rating score": 80}])

    #Feature 6 Integration Tests
    def test1_display_notification(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp.name, "Runtime Terrors", students1)
      comp_team1 = add_results(mod.username, comp.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp.name, "Scrum Lords", students2)
      comp_team2 = add_results(mod.username, comp.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp.name)
      update_rankings(comp.name)
      self.assertDictEqual(display_notifications("james"), {"notifications": [{"ID": 1, "Notification": "RANK : 1. Congratulations on your first rank!"}]})

    def test2_display_notification_rank_retained(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 30)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 15)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      self.assertDictEqual(display_notifications("james"), {"notifications": [{"ID": 1, "Notification": "RANK : 1. Congratulations on your first rank!"}, {"ID": 7, "Notification": "RANK : 1. Well done! You retained your rank."}]})

    def test3_display_notification_rank_down(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      self.assertDictEqual(display_notifications("steven"), {"notifications": [{"ID": 2, "Notification": "RANK : 1. Congratulations on your first rank!"}, {"ID": 10, "Notification": "RANK : 4. Oh no! Your rank has went down."}]})

    def test4_display_notification_rank_up(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      self.assertDictEqual(display_notifications("mark"), {"notifications": [{"ID": 4, "Notification": "RANK : 4. Congratulations on your first rank!"}, {"ID": 8, "Notification": "RANK : 2. Congratulations! Your rank has went up."}]})

    #Additional Integration Tests
    # def test1_add_mod(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod1 = create_moderator("debra", "debrapass", "debra@email.com")
    #   mod2 = create_moderator("robert", "robertpass", "robert@email.com")
    #   comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   assert add_mod(mod1.username, comp.name, mod2.username) != None
       
    # def test2_add_mod(self):
    #   db.drop_all()
    #   db.create_all()
    #   mod1 = create_moderator("debra", "debrapass", "debra@email.com")
    #   mod2 = create_moderator("robert", "robertpass", "robert@email.com")
    #   mod3 = create_moderator("raymond", "raymondpass", "raymond@email.com")
    #   comp = create_competition(mod1.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
    #   assert add_mod(mod2.username, comp.name, mod3.username) == None
    
    def test_student_list(self):
      
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      comp1_team1 = add_results(mod.username, comp1.name, "Runtime Terrors", 15)
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      comp1_team2 = add_results(mod.username, comp1.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp1.name)
      update_rankings(comp1.name)
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      comp_team3 = add_results(mod.username, comp2.name, "Runtime Terrors", 20)
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      comp_team4 = add_results(mod.username, comp2.name, "Scrum Lords", 10)
      update_ratings(mod.username, comp2.name)
      update_rankings(comp2.name)
      self.assertEqual(get_all_students_json(), [{'id': 1, 'username': 'james', 'rating_score': 220, 'comp_count': 2, 'curr_rank': 1}, {'id': 2, 'username': 'steven', 'rating_score': 170, 'comp_count': 2, 'curr_rank': 4}, {'id': 3, 'username': 'emily', 'rating_score': 170, 'comp_count': 2, 'curr_rank': 4}, {'id': 4, 'username': 'mark', 'rating_score': 180, 'comp_count': 2, 'curr_rank': 2}, {'id': 5, 'username': 'eric', 'rating_score': 180, 'comp_count': 2, 'curr_rank': 2}, {'id': 6, 'username': 'ryan', 'rating_score': 130, 'comp_count': 2, 'curr_rank': 6}])

    def test_comp_list(self):
     
      mod = create_moderator("debra", "debrapass", "debra@email.com")
      comp1 = create_competition(mod.username, "RunTime", "29-03-2024", "St. Augustine", 2, 25)
      comp2 = create_competition(mod.username, "Hacker Cup", "23-02-2024", "Macoya", 1, 20)
      student1 = create_student("james", "jamespass", "james@email.com")
      student2 = create_student("steven", "stevenpass", "steven@email.com")
      student3 = create_student("emily", "emilypass", "emily@email.com")
      student4 = create_student("mark", "markpass", "mark@email.com")
      student5 = create_student("eric", "ericpass", "eric@email.com")
      student6 = create_student("ryan", "ryanpass", "ryan@email.com")
      students1 = [student1.username, student2.username, student3.username]
      team1 = add_team(mod.username, comp1.name, "Runtime Terrors", students1)
      
      students2 = [student4.username, student5.username, student6.username]
      team2 = add_team(mod.username, comp1.name, "Scrum Lords", students2)
      
      students3 = [student1.username, student4.username, student5.username]
      team3 = add_team(mod.username, comp2.name, "Runtime Terrors", students3)
      
      students4 = [student2.username, student3.username, student6.username]
      team4 = add_team(mod.username, comp2.name, "Scrum Lords", students4)
      
      self.assertListEqual(get_all_competitions_json(), [{"id": 1, "name": "RunTime", "date": "29-03-2024", "location": "St. Augustine", "level": 2, "max_score": 25, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}, {"id": 2, "name": "Hacker Cup", "date": "23-02-2024", "location": "Macoya", "level": 1, "max_score": 20, "moderators": ["debra"], "teams": ["Runtime Terrors", "Scrum Lords"]}])