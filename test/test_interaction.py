import unittest
import json
from unittest.mock import patch, MagicMock, Mock


import interaction
import main

class TestInteraction(unittest.TestCase):

    def setUp(self) -> None:
        self.students = '../resources/Students-ESCO-demo.json'
        self.projects = '../resources/Projects-ESCO-demo2.json'
        self.preferences = '../resources/Preferences-ESCO-demo.json'
        self.response_path = '../resources/team_response.json'

    def test_basic_feedback(self):
        data = json.loads(main.generate_data(self.students, self.projects, self.preferences, 'Precalc-ESCO-demo'))
        assignment = main.call_uploading_data_paths(self.students, self.projects, self.preferences)
        feedback = '{"accepted": ["Ludovica", "Martha", "Marco"]}'
        remaining_assignements = interaction.simple_interaction(assignment, feedback)
        pref_remove = set() # Used to store what preferences have to be removed
        for id_proj in {k: v for k, v in assignment.items() if k not in remaining_assignements}:
            # We have to remove this project since all asignees have accepted
            # We have to remove the assigned students since their assignment has been solved
            del data['Projects'][id_proj]
            for id_student in assignment[id_proj]:
                del data['Students'][id_student]
                for id_pref, value in data['Preferences'].items():
                    if id_student in value['sid'] or id_proj in value['pid']: pref_remove.add(id_pref)

        # We have to remove from Preferences any presence from removed project and assignees to avoid
        # index out of range error from Docker container
        for id_pref in pref_remove: data['Preferences'].pop(id_pref)

        new_assignment = main.call_uploading_data(json.dumps(data))

        print(assignment) # Original assignment
        print(remaining_assignements) # After processing interaction (acceptance for Buitoni)
        print(new_assignment) # The assignments have changed after accepted assignment has been processed


if __name__ == '__main__':
    unittest.main()